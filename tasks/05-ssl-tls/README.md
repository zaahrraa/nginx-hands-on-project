# Task 5: SSL/TLS with a Self-Signed Certificate

## What is this?
Encrypting traffic to Nginx using HTTPS via a self-signed SSL/TLS certificate — one generated locally rather than issued by a trusted certificate authority.

## Why does it matter?
HTTPS encrypts data between the browser and server, preventing anyone snooping on the network from reading it. A self-signed certificate works technically identically to a real one for encryption purposes, but browsers show a warning since no trusted authority has verified it — this is expected and standard for local/learning environments. (Production sites use a trusted CA like Let's Encrypt instead.)

## Configuration
See `conf/ssl-site.conf`:
```nginx
server {
    listen 443 ssl;
    server_name localhost;

    ssl_certificate     /etc/nginx/ssl/selfsigned.crt;
    ssl_certificate_key /etc/nginx/ssl/selfsigned.key;

    root /var/www/static-site;
    index index.html;
}

server {
    listen 8081;
    server_name localhost;
    return 301 https://$host$request_uri;
}
```

## Commands used

### 1. Create SSL directory and certificate
```bash
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/selfsigned.key \
  -out /etc/nginx/ssl/selfsigned.crt \
  -subj "/C=PK/ST=Punjab/L=Lahore/O=Zahra/CN=localhost"
```

### 2. Enable SSL site (remove old configs)
```bash
# Remove old configs
sudo rm /etc/nginx/sites-enabled/*

# Enable SSL config
sudo ln -s /etc/nginx/sites-available/ssl-site.conf /etc/nginx/sites-enabled/

# Verify
ls -la /etc/nginx/sites-enabled/
```

### 3. Test and reload Nginx
```bash
sudo nginx -t
sudo systemctl reload nginx
```

## How I tested it

### Test 1: HTTPS with curl
```bash
curl -k https://localhost
```
**Output:**
```html
<h1>Hello from my static site!</h1>
```
✅ HTTPS works!

### Test 2: HTTP redirect to HTTPS
```bash
curl -I http://localhost:8081
```
**Output:**
```
HTTP/1.1 301 Moved Permanently
Location: https://localhost/
```
✅ HTTP automatically redirects to HTTPS!

### Test 3: Browser Test
Visited `https://localhost` in the browser:
1. Got the expected **"Not Secure"** warning (self-signed certificate)
2. Clicked **"Advanced"** → **"Proceed to localhost (unsafe)"**
3. Confirmed the site loaded correctly over HTTPS
4. Clicked the padlock icon to view certificate details (issued to `localhost`)

## Issues I encountered

**Issue 1:** Nginx wasn't listening on port 443.
- **Symptom:** `curl -k https://localhost` gave "Connection refused"
- **Cause:** SSL config wasn't enabled in `sites-enabled/`
- **Fix:** Enabled SSL config with `sudo ln -s /etc/nginx/sites-available/ssl-site.conf /etc/nginx/sites-enabled/`

**Issue 2:** `https://localhost:8081` gave SSL error.
- **Symptom:** "SSL received a record that exceeded the maximum permissible length"
- **Cause:** HTTPS uses port 443 by default, not 8081
- **Fix:** Use `https://localhost` (no port number)

**Issue 3:** Old configs (`default`, `static-site.conf`) were still active.
- **Cause:** They were taking priority and blocking SSL
- **Fix:** `sudo rm /etc/nginx/sites-enabled/*` then enabled only SSL config

## Result
✅ Site now serves over HTTPS on port 443 with a self-signed certificate
✅ Plain HTTP requests on port 8081 are automatically redirected to HTTPS
✅ Certificate details show it's issued to `localhost`