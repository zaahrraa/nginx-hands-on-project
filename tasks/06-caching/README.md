# Task 6: Caching with `proxy_cache`

## What is this?
Configured Nginx to cache responses from a backend server. When multiple users request the same page, Nginx serves it from cache instead of asking the backend again — making it faster and reducing load on the backend.

## Why does it matter?
Caching dramatically improves performance and reduces server load. If 100 users request the same page, only the first request hits the backend — the other 99 get served instantly from Nginx's cache.

## Configuration

### Step 1: Add cache path to main nginx.conf
Added this line inside the `http {}` block in `/etc/nginx/nginx.conf`:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=100m inactive=60m;
```
This tells Nginx:
- Store cache in `/var/cache/nginx`
- Use 10MB of memory for cache keys
- Maximum 100MB disk space
- Remove files not accessed in 60 minutes

### Step 2: Create cache config
Created `/etc/nginx/sites-available/cache.conf`:
```nginx
server {
    listen 8081;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_cache my_cache;
        proxy_cache_valid 200 10m;
        add_header X-Cache-Status $upstream_cache_status;
    }
}
```

### Step 3: Start backend server
Started a Python HTTP server on port 5000 (the "backend"):
```bash
cd ~/backend-demo
python3 -m http.server 5000 &
```

### Step 4: Enable cache config
```bash
# Remove old configs
sudo rm /etc/nginx/sites-enabled/*

# Enable cache config
sudo ln -s /etc/nginx/sites-available/cache.conf /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

## How I tested it

### First request (CACHE MISS):
```bash
curl -I http://localhost:8081
```
**Output:**
```
HTTP/1.1 200 OK
Server: nginx/1.18.0
X-Cache-Status: MISS
```

### Second request (CACHE HIT):
```bash
curl -I http://localhost:8081
```
**Output:**
```
HTTP/1.1 200 OK
Server: nginx/1.18.0
X-Cache-Status: HIT
```

✅ First request shows `MISS` (cached first time)
✅ Second request shows `HIT` (served from cache!)

## Issues I encountered

**Issue 1:** Old SSL config was still enabled, causing redirects.
- **Symptom:** `curl -I http://localhost:8081` returned `301 Moved Permanently` to HTTPS
- **Cause:** `ssl-site.conf` was still active in `sites-enabled/`
- **Fix:** `sudo rm /etc/nginx/sites-enabled/*` then enabled only cache config

**Issue 2:** No response from backend.
- **Symptom:** `curl` gave `Connection refused` or `502 Bad Gateway`
- **Cause:** The Python backend on port 5000 wasn't running
- **Fix:** Started backend with `python3 -m http.server 5000 &`

## Result
✅ Cache is working!
✅ First request shows `X-Cache-Status: MISS`
✅ Second request shows `X-Cache-Status: HIT`
✅ Backend only handles the first request — all subsequent requests are served from cache

## Commands Reference
```bash
# Start backend
cd ~/backend-demo && python3 -m http.server 5000 &

# Enable cache config
sudo rm /etc/nginx/sites-enabled/*
sudo ln -s /etc/nginx/sites-available/cache.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Test cache
curl -I http://localhost:8081
curl -I http://localhost:8081
```