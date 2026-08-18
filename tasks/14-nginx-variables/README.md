# Task 14: Using Variables (`$host`, `$remote_addr`, `$request_uri`)

## What is this?
Configured Nginx to capture and display live information about each request using built-in variables. The server shows the hostname, visitor's IP address, and full request URI in the response.

## Why does it matter?
- **Dynamic responses:** Show different content based on request details
- **Debugging:** See exactly what Nginx receives from clients
- **Logging:** Customize log formats with request data
- **Security:** Track visitor IP addresses
- **Real-world use:** Many applications need this info (analytics, geo-location, personalization)

## Configuration
See `conf/variables-demo.conf`

```nginx
server {
    listen 8081;
    server_name localhost;

    root /var/www/static-site;
    index index.html;

    location / {
        add_header X-Debug-Host $host;
        add_header X-Debug-IP $remote_addr;
        add_header X-Debug-URI $request_uri;
        return 200 "Host: $host | IP: $remote_addr | URI: $request_uri\n";
    }
}
```

### Configuration Breakdown

| Directive | What it does |
|-----------|--------------|
| `add_header X-Debug-Host $host;` | Adds header showing the requested domain |
| `add_header X-Debug-IP $remote_addr;` | Adds header showing visitor's IP address |
| `add_header X-Debug-URI $request_uri;` | Adds header showing the full request URL |
| `return 200 "Host: $host...";` | Returns a response with the variable values |

### Variables Used

| Variable | What it contains | Example |
|----------|------------------|---------|
| `$host` | Domain name requested | `localhost` |
| `$remote_addr` | Visitor's IP address | `127.0.0.1` |
| `$request_uri` | Full URL path + query string | `/test?x=1` |

## What I Actually Did

### Step 1: Created Variables Config
Created `/etc/nginx/sites-available/variables.conf` with the above configuration.

### Step 2: Enabled Variables Config
```bash
# Remove old configs
sudo rm /etc/nginx/sites-enabled/*

# Enable variables config
sudo ln -s /etc/nginx/sites-available/variables.conf /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### Step 3: Tested Variables

## How I Tested It

### Test 1: Simple Request
```bash
curl http://localhost:8081
```

**Output:**
```
Host: localhost | IP: 127.0.0.1 | URI: /
```
✅ Variables captured correctly!

### Test 2: With Query String
```bash
curl http://localhost:8081/test?x=1
```

**Output:**
```
Host: localhost | IP: 127.0.0.1 | URI: /test?x=1
```
✅ Query string captured in `$request_uri`!

### Test 3: Different Path
```bash
curl http://localhost:8081/about?page=2&sort=asc
```

**Output:**
```
Host: localhost | IP: 127.0.0.1 | URI: /about?page=2&sort=asc
```
✅ Full URI captured correctly!

### Test 4: Check Headers
```bash
curl -I http://localhost:8081/test?x=1
```

**Output:**
```
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
X-Debug-Host: localhost
X-Debug-IP: 127.0.0.1
X-Debug-URI: /test?x=1
```
✅ Custom headers added correctly!

### Test 5: Browser Test
Opened browser and went to `http://localhost:8081/test?x=1`

**Result:**
```
Host: localhost | IP: 127.0.0.1 | URI: /test?x=1
```
✅ Variables work in browser too!

## How Variables Work

### When a request comes in:
```
User types: http://localhost:8081/test?x=1
    ↓
Nginx receives the request
    ↓
Nginx captures variables:
    $host = "localhost"
    $remote_addr = "127.0.0.1"
    $request_uri = "/test?x=1"
    ↓
Nginx adds headers:
    X-Debug-Host: localhost
    X-Debug-IP: 127.0.0.1
    X-Debug-URI: /test?x=1
    ↓
Nginx returns response:
    "Host: localhost | IP: 127.0.0.1 | URI: /test?x=1"
```

## Common Nginx Variables

| Variable | What it contains |
|----------|------------------|
| `$host` | Domain name from the request |
| `$remote_addr` | Visitor's IP address |
| `$request_uri` | Full URL with query string |
| `$uri` | URL path without query string |
| `$args` | Query string parameters |
| `$scheme` | `http` or `https` |
| `$http_user_agent` | Visitor's browser info |
| `$request_method` | `GET`, `POST`, etc. |
| `$status` | Response status code |
| `$body_bytes_sent` | Size of response body |

## Result
✅ Variables captured correctly in both curl and browser
✅ `$host` shows the domain name
✅ `$remote_addr` shows the visitor's IP
✅ `$request_uri` shows the full URL with query string
✅ Custom headers added to responses

## Commands Reference

```bash
# Simple request
curl http://localhost:8081

# With query string
curl http://localhost:8081/test?x=1

# Different path and query
curl http://localhost:8081/about?page=2&sort=asc

# Check headers
curl -I http://localhost:8081/test?x=1
```

## Files Created/Modified
| File | Purpose |
|------|---------|
| `/etc/nginx/sites-available/variables.conf` | Nginx config showing variables |
| `/etc/nginx/sites-enabled/variables.conf` | Symlink to active config |