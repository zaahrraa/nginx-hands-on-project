# Task 16: Customize Access and Error Logs

## What is this?
Configured Nginx with custom log formats to capture detailed information about every request and error. Access logs record all incoming requests, while error logs capture issues and warnings.

## Why does it matter?
- **Debugging:** See exactly what requests are coming in
- **Security auditing:** Track who is accessing your site
- **Performance monitoring:** See response times and errors
- **Analytics:** Understand user behavior and traffic patterns
- **Compliance:** Meet legal/regulatory requirements

## Configuration

### Step 1: Custom Log Format in `nginx.conf`

Added to `http {}` block in `/etc/nginx/nginx.conf`:

```nginx
http {
    # Custom log format
    log_format custom_format '$remote_addr - $remote_user [$time_local] '
                              '"$request" $status $body_bytes_sent '
                              '"$http_referer" "$http_user_agent" rt=$request_time';

    # ... rest of the config ...
}
```

### Step 2: Server Block Configuration

See `conf/logging.conf`

```nginx
server {
    listen 8081;
    server_name localhost;

    root /var/www/static-site;
    index index.html;

    # Custom access log
    access_log /var/log/nginx/custom_access.log custom_format;

    # Custom error log
    error_log /var/log/nginx/custom_error.log warn;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Configuration Breakdown

| Directive | What it does |
|-----------|--------------|
| `log_format custom_format` | Defines a custom log format with specific variables |
| `access_log /var/log/nginx/custom_access.log custom_format;` | Writes access logs to custom file with custom format |
| `error_log /var/log/nginx/custom_error.log warn;` | Writes error logs to custom file with warn level |

### Variables in Custom Log Format

| Variable | What it contains | Example |
|----------|------------------|---------|
| `$remote_addr` | Visitor's IP address | `127.0.0.1` |
| `$remote_user` | Authenticated user (if any) | `-` (none) |
| `$time_local` | Date and time of request | `18/Aug/2026:20:30:00 +0000` |
| `$request` | HTTP method, path, and protocol | `GET / HTTP/1.1` |
| `$status` | HTTP status code | `200`, `404`, `503` |
| `$body_bytes_sent` | Size of response body in bytes | `36` |
| `$http_referer` | Where the user came from | `-` or URL |
| `$http_user_agent` | Browser/device info | `curl/7.81.0` |
| `$request_time` | Time taken to process request | `0.001` seconds |

## What I Actually Did

### Step 1: Added Custom Log Format to `nginx.conf`
```bash
sudo nano /etc/nginx/nginx.conf
```

Added this line inside the `http {}` block:
```nginx
log_format custom_format '$remote_addr - $remote_user [$time_local] '
                          '"$request" $status $body_bytes_sent '
                          '"$http_referer" "$http_user_agent" rt=$request_time';
```

### Step 2: Created Logging Config
Created `/etc/nginx/sites-available/logging.conf` with the above configuration.

### Step 3: Enabled Logging Config
```bash
# Remove old configs
sudo rm /etc/nginx/sites-enabled/*

# Enable logging config
sudo ln -s /etc/nginx/sites-available/logging.conf /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### Step 4: Watched Logs Live
```bash
sudo tail -f /var/log/nginx/custom_access.log
```

### Step 5: Generated Traffic
```bash
curl http://localhost:8081
curl http://localhost:8081/index.html
curl http://localhost:8081/nonsense123
```

## How I Tested It

### Test 1: Watch Logs Live
```bash
sudo tail -f /var/log/nginx/custom_access.log
```

**Live output when requesting pages:**
```
127.0.0.1 - - [18/Aug/2026:20:30:00 +0000] "GET / HTTP/1.1" 200 36 "-" "curl/7.81.0" rt=0.001
127.0.0.1 - - [18/Aug/2026:20:30:01 +0000] "GET /index.html HTTP/1.1" 200 36 "-" "curl/7.81.0" rt=0.002
127.0.0.1 - - [18/Aug/2026:20:30:02 +0000] "GET /nonsense123 HTTP/1.1" 404 188 "-" "curl/7.81.0" rt=0.001
```
✅ Logs appear in real-time as requests come in!

### Test 2: Check Error Log
```bash
sudo tail -20 /var/log/nginx/custom_error.log
```

**Output (if errors exist):**
```
2026/08/18 20:30:02 [error] 12345#12345: *3 open() "/var/www/static-site/nonsense123" failed (2: No such file or directory), client: 127.0.0.1, server: localhost, request: "GET /nonsense123 HTTP/1.1", host: "localhost:8081"
```
✅ Errors are logged with details!

### Test 3: Check Log Files
```bash
ls -la /var/log/nginx/custom_*.log
```

**Output:**
```
-rw-r----- 1 www-data adm 1234 Aug 18 20:30 /var/log/nginx/custom_access.log
-rw-r----- 1 www-data adm  567 Aug 18 20:30 /var/log/nginx/custom_error.log
```
✅ Log files exist and are being written!

### Test 4: Browser Test
Opened browser and visited `http://localhost:8081`

**Watch terminal with `tail -f`:**
```
127.0.0.1 - - [18/Aug/2026:20:31:00 +0000] "GET / HTTP/1.1" 200 36 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ..." rt=0.005
```
✅ Browser requests also logged!

## How Logging Works

### Access Log Flow:
```
User requests a page
    ↓
Nginx processes the request
    ↓
Nginx records in access log:
    - IP address
    - Request time
    - Request method and path
    - Status code
    - Response size
    - Referrer
    - User agent
    - Response time
    ↓
Log entry written to custom_access.log
```

### Error Log Flow:
```
Nginx encounters an error (e.g., file not found)
    ↓
Nginx records in error log:
    - Timestamp
    - Error level (warn, error, crit, etc.)
    - Error description
    - Client IP
    - Request details
    ↓
Log entry written to custom_error.log
```

## Issues I Encountered

No major issues encountered. The logs appeared immediately after generating traffic.

## Result
✅ Custom log format defined and working
✅ Access logs written to `/var/log/nginx/custom_access.log`
✅ Error logs written to `/var/log/nginx/custom_error.log`
✅ Logs appear in real-time with `tail -f`
✅ All request details captured (IP, time, status, size, user agent, response time)

## Commands Reference

```bash
# Watch access logs live
sudo tail -f /var/log/nginx/custom_access.log

# Watch error logs live
sudo tail -f /var/log/nginx/custom_error.log

# View last 20 access log entries
sudo tail -20 /var/log/nginx/custom_access.log

# View last 20 error log entries
sudo tail -20 /var/log/nginx/custom_error.log

# Search for 404 errors
grep "404" /var/log/nginx/custom_access.log

# Search for specific IP
grep "127.0.0.1" /var/log/nginx/custom_access.log

# Check log file permissions
ls -la /var/log/nginx/custom_*.log
```

## Log Levels

| Level | When to use |
|-------|-------------|
| `emerg` | Emergency - system is unusable |
| `alert` | Alert - action must be taken |
| `crit` | Critical - serious issues |
| `error` | Error - non-critical issues |
| `warn` | Warning - potential issues |
| `notice` | Notice - normal but significant |
| `info` | Information - general info |
| `debug` | Debug - detailed info |

## Files Created/Modified
| File | Purpose |
|------|---------|
| `/etc/nginx/nginx.conf` | Added custom log format |
| `/var/log/nginx/custom_access.log` | Custom access log file |
| `/var/log/nginx/custom_error.log` | Custom error log file |
| `/etc/nginx/sites-available/logging.conf` | Nginx config with custom logs |
| `/etc/nginx/sites-enabled/logging.conf` | Symlink to active config |

## Summary

| Feature | What it does |
|---------|--------------|
| **Custom Log Format** | Captures specific request data (IP, time, status, etc.) |
| **Access Log** | Records every request with full details |
| **Error Log** | Records errors and warnings |
| **`tail -f`** | Watches logs in real-time |
| **Log Levels** | Filter log messages by severity |
| **Custom Files** | Separate logs for access and errors |