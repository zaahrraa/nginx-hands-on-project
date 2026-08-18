# Task 15: Rate Limiting, Connection Limits, and Buffering

## What is this?
Configured Nginx with rate limiting, connection limits, and buffering to protect the server from abuse and handle traffic efficiently.

## Why does it matter?
- **Protect your server** from DDoS attacks and brute force attempts
- **Prevent resource exhaustion** from too many connections
- **Improve performance** for legitimate users
- **Handle slow clients** without tying up server resources
- **Essential for production** environments to stay stable under load

## Configuration

### Step 1: Added to `http {}` block in `/etc/nginx/nginx.conf`

```nginx
http {
    # Rate limiting zone - 5 requests per second
    limit_req_zone $binary_remote_addr zone=mylimit:10m rate=5r/s;
    
    # Connection limit zone - max 5 connections per IP
    limit_conn_zone $binary_remote_addr zone=addr:10m;

    # ... rest of the config ...
}
```

### Step 2: Server Block Configuration

See `conf/rate-limit.conf`

```nginx
server {
    listen 8081;
    server_name localhost;

    # Rate limiting
    limit_req zone=mylimit burst=10 nodelay;
    
    # Connection limiting
    limit_conn addr 5;

    # Buffering settings
    proxy_buffering on;
    proxy_buffers 8 16k;
    proxy_buffer_size 32k;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Configuration Breakdown

| Directive | What it does |
|-----------|--------------|
| `limit_req_zone $binary_remote_addr zone=mylimit:10m rate=5r/s;` | Creates a zone tracking 5 requests per second per IP |
| `limit_conn_zone $binary_remote_addr zone=addr:10m;` | Creates a zone tracking max connections per IP |
| `limit_req zone=mylimit burst=10 nodelay;` | Allows 5r/s + burst of 10 requests |
| `limit_conn addr 5;` | Maximum 5 concurrent connections per IP |
| `proxy_buffering on;` | Enables buffering for proxied responses |
| `proxy_buffers 8 16k;` | 8 buffers of 16KB each for buffering |
| `proxy_buffer_size 32k;` | Buffer size for response headers |

## What I Actually Did

### Step 1: Added Rate Limiting to `nginx.conf`
```bash
sudo nano /etc/nginx/nginx.conf
```

Added these lines inside the `http {}` block:
```nginx
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=5r/s;
limit_conn_zone $binary_remote_addr zone=addr:10m;
```

### Step 2: Created Rate Limiting Config
Created `/etc/nginx/sites-available/rate-limit.conf` with the above configuration.

### Step 3: Enabled Rate Limiting Config
```bash
# Remove old configs
sudo rm /etc/nginx/sites-enabled/*

# Enable rate limit config
sudo ln -s /etc/nginx/sites-available/rate-limit.conf /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### Step 4: Started Backend Server
```bash
cd ~/backend-demo
python3 -m http.server 5000 &
```

## How I Tested It

### Test 1: Normal Request (Should work)
```bash
curl -I http://localhost:8081
```

**Output:**
```
HTTP/1.1 200 OK
```
✅ Normal request works!

### Test 2: Rapid Requests (Rate Limiting Applied)
```bash
for i in {1..20}; do curl -o /dev/null -s -w "%{http_code}\n" http://localhost:8081; done
```

**Output:**
```
200
200
200
200
200
503
503
503
503
503
200
200
200
200
200
503
503
503
503
503
```

✅ Some requests got `503 Service Temporarily Unavailable` (rate limited!)
✅ First 5 requests succeeded (within rate limit)
✅ Next 5 got 503 (burst limit exceeded)
✅ Pattern repeats every 5 requests

## How It Works

### Rate Limiting Flow:
```
User sends 20 rapid requests
    ↓
Nginx checks: How many requests in last second?
    ↓
First 5 requests: Under limit → 200 OK ✅
    ↓
Requests 6-10: Exceed limit → 503 Unavailable ❌
    ↓
Wait for 1 second
    ↓
Next 5 requests: Under limit again → 200 OK ✅
```

### Connection Limiting Flow:
```
User opens multiple connections
    ↓
Nginx checks: How many connections from this IP?
    ↓
Up to 5 connections: Allowed ✅
    ↓
6th connection: Rejected (503) ❌
```

### Buffering Flow:
```
Nginx receives response from backend
    ↓
Buffering ON: Stores response in buffers (8 x 16KB)
    ↓
Sends to slow client gradually
    ↓
Backend connection freed quickly! ✅
```

## Issues I Encountered

**Issue:** Port 5000 already in use.
- **Symptom:** `OSError: [Errno 98] Address already in use`
- **Cause:** Python backend was already running
- **Fix:** 
  ```bash
  sudo lsof -i :5000  # Find process
  sudo kill -9 PID    # Kill it
  # OR
  sudo fuser -k 5000/tcp
  ```

## Result
✅ Rate limiting working (503 responses on rapid requests)
✅ Connection limits configured (max 5 per IP)
✅ Buffering enabled for slow clients
✅ Server protected from abuse

## Commands Reference

```bash
# Test rate limiting
for i in {1..20}; do curl -o /dev/null -s -w "%{http_code}\n" http://localhost:8081; done

# Test normal request
curl -I http://localhost:8081

# Check if backend is running
ps aux | grep python
sudo netstat -tulpn | grep 5000

# Kill process on port 5000
sudo fuser -k 5000/tcp

# Start backend
cd ~/backend-demo
python3 -m http.server 5000 &

# Check rate limit zones in nginx.conf
sudo cat /etc/nginx/nginx.conf | grep limit

# Check Nginx logs for rate limiting
sudo tail -20 /var/log/nginx/error.log
```

## Files Created/Modified
| File | Purpose |
|------|---------|
| `/etc/nginx/nginx.conf` | Added `limit_req_zone` and `limit_conn_zone` |
| `/etc/nginx/sites-available/rate-limit.conf` | Nginx config for rate limiting |
| `/etc/nginx/sites-enabled/rate-limit.conf` | Symlink to active config |

## Summary

| Feature | What it does |
|---------|--------------|
| **Rate Limiting** | 5 requests per second per IP |
| **Burst** | Allows up to 10 extra requests |
| **Connection Limit** | Max 5 concurrent connections per IP |
| **Buffering** | Handles slow clients efficiently |