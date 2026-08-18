# Task 10: Security Headers and Basic Authentication

## What is this?
Configured Nginx with security headers to protect against common web attacks and set up basic authentication (username/password) to restrict access to the `/admin` area.

## Why does it matter?
- **Security Headers:** Protect against clickjacking, MIME sniffing, XSS attacks, and referrer leaks
- **Basic Authentication:** Adds a simple but effective password wall to sensitive areas like admin panels
- **Industry Best Practices:** Security headers are recommended by OWASP and security standards

## Configuration
See `conf/security.conf`

```nginx
server {
    listen 8081;
    server_name localhost;

    root /var/www/static-site;
    index index.html;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Protected admin area with basic auth
    location /admin {
        auth_basic "Restricted Area";
        auth_basic_user_file /etc/nginx/.htpasswd;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Security Headers Breakdown

| Header | Value | What it does |
|--------|-------|--------------|
| `X-Frame-Options` | `SAMEORIGIN` | Prevents your site from being embedded in iframes on other sites (stops clickjacking) |
| `X-Content-Type-Options` | `nosniff` | Prevents browsers from MIME-sniffing files (stops XSS attacks) |
| `X-XSS-Protection` | `1; mode=block` | Enables browser's XSS filter and blocks suspicious pages |
| `Referrer-Policy` | `no-referrer-when-downgrade` | Controls how much referrer info is sent (privacy protection) |

### Basic Auth Breakdown

| Directive | Value | What it does |
|-----------|-------|--------------|
| `auth_basic` | `"Restricted Area"` | Enables basic authentication with a custom realm message |
| `auth_basic_user_file` | `/etc/nginx/.htpasswd` | Points to the file containing usernames and encrypted passwords |

## What I Actually Did

### Step 1: Installed Apache Utils (for htpasswd)
```bash
sudo apt install apache2-utils -y
```

### Step 2: Created Password File
```bash
sudo htpasswd -c /etc/nginx/.htpasswd admin
```
**Entered password when prompted.**

### Step 3: Created Admin Directory and Index File
```bash
sudo mkdir -p /var/www/static-site/admin
echo '<h1>Welcome to the Admin Area!</h1>' | sudo tee /var/www/static-site/admin/index.html
```

### Step 4: Created Security Config
Created `/etc/nginx/sites-available/security.conf` with the above configuration.

### Step 5: Enabled Security Config
```bash
# Remove old configs
sudo rm /etc/nginx/sites-enabled/*

# Enable security config
sudo ln -s /etc/nginx/sites-available/security.conf /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### Step 6: Tested Security Headers
```bash
curl -I http://localhost:8081
```

**Output:**
```
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: no-referrer-when-downgrade
```
✅ All 4 security headers are present!

### Step 7: Tested Basic Auth
```bash
curl -I http://localhost:8081/admin
```

**Output:**
```
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Restricted Area"
```
✅ Admin area is password protected!

## How I Tested It

### Test 1: Security Headers
```bash
curl -I http://localhost:8081
```

**Output:**
```
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: no-referrer-when-downgrade
```
✅ All security headers are working!

### Test 2: Unauthorized Access (No Credentials)
```bash
curl -I http://localhost:8081/admin
```

**Output:**
```
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Restricted Area"
```
✅ Admin area is protected!

### Test 3: Browser Test (Login Popup)
Opened browser and went to `http://localhost:8081/admin`

**Result:**
1. Browser showed username/password popup ✅
2. Entered credentials (`admin` + password)
3. Saw "Welcome to the Admin Area!" ✅

### Test 4: Access with Correct Credentials
```bash
curl -u admin:YOUR_PASSWORD http://localhost:8081/admin
```

**Output:**
```
<h1>Welcome to the Admin Area!</h1>
```
✅ Login works!

## Issues I Encountered

**Issue 1:** File name was `security.con` instead of `security.conf`.
- **Symptom:** Nginx config test failed with "No such file or directory"
- **Cause:** Typo in file name
- **Fix:** `sudo mv /etc/nginx/sites-available/security.con /etc/nginx/sites-available/security.conf`

**Issue 2:** 404 error after login.
- **Symptom:** After entering credentials, got 404 Not Found
- **Cause:** No `index.html` in `/var/www/static-site/admin/`
- **Fix:** `sudo mkdir -p /var/www/static-site/admin && echo '<h1>Welcome to the Admin Area!</h1>' | sudo tee /var/www/static-site/admin/index.html`

## How the Flow Works

### Security Headers Flow:
```
Browser requests page from Nginx
    ↓
Nginx adds security headers to response
    ↓
Browser receives: Page + Security Headers
    ↓
Browser enforces security rules
    ↓
User is protected from attacks! ✅
```

### Basic Auth Flow:
```
User visits: /admin
    ↓
Nginx: "This area is protected!"
    ↓
Nginx sends: 401 Unauthorized + WWW-Authenticate
    ↓
Browser shows: Login popup
    ↓
User enters: username + password
    ↓
Nginx checks: /etc/nginx/.htpasswd
    ↓
Credentials correct? → Show page ✅
Credentials wrong? → Show popup again ❌
```

## Result
✅ Security headers added to all responses
✅ Admin area protected with basic auth
✅ Login popup appears when accessing `/admin`
✅ Correct credentials grant access
✅ All 4 security headers are present and working

## Commands Reference
```bash
# Install apache2-utils
sudo apt install apache2-utils -y

# Create password file
sudo htpasswd -c /etc/nginx/.htpasswd admin

# Create admin folder
sudo mkdir -p /var/www/static-site/admin
echo '<h1>Welcome to the Admin Area!</h1>' | sudo tee /var/www/static-site/admin/index.html

# Enable config
sudo rm /etc/nginx/sites-enabled/*
sudo ln -s /etc/nginx/sites-available/security.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Test headers
curl -I http://localhost:8081

# Test admin (should show 401)
curl -I http://localhost:8081/admin

# Test login (replace YOUR_PASSWORD)
curl -u admin:YOUR_PASSWORD http://localhost:8081/admin

# Add another user
sudo htpasswd /etc/nginx/.htpasswd anotheruser

# Reset password
sudo htpasswd /etc/nginx/.htpasswd admin
```

## Files Created/Modified
| File | Purpose |
|------|---------|
| `/etc/nginx/.htpasswd` | Password file for basic auth |
| `/var/www/static-site/admin/index.html` | Admin area page |
| `/etc/nginx/sites-available/security.conf` | Nginx config for security headers and auth |
| `/etc/nginx/sites-enabled/security.conf` | Symlink to active config |