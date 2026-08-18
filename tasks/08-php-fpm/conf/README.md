# Task 8: PHP Integration via PHP-FPM

## What is this?
Configured Nginx to execute PHP code by passing `.php` requests to PHP-FPM, a separate process manager that handles PHP processing. Nginx cannot run PHP itself, so it hands off PHP files to PHP-FPM via `fastcgi_pass`.

## Why does it matter?
PHP powers millions of websites including WordPress, Laravel, and Drupal. Nginx + PHP-FPM is a high-performance combination used extensively in production environments. Without PHP-FPM, Nginx would just display PHP code as plain text instead of executing it.

## Configuration
See `conf/php-site.conf`

```nginx
server {
    listen 8081;
    server_name localhost;

    root /var/www/php-site;
    index index.php index.html;

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    }
}
```

### Configuration Breakdown

| Directive | What it does |
|-----------|--------------|
| `listen 8081;` | Nginx listens for requests on port 8081 |
| `server_name localhost;` | This server block responds to `localhost` |
| `root /var/www/php-site;` | Website files are stored in `/var/www/php-site` |
| `index index.php index.html;` | If someone visits `/`, try `index.php` first, then `index.html` |
| `location ~ \.php$` | For any request ending in `.php`, send it to PHP-FPM |
| `include snippets/fastcgi-php.conf;` | Include default FastCGI settings for PHP |
| `fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;` | Send PHP requests to PHP-FPM via this socket |

## What I Actually Did

### Step 1: Checked PHP-FPM Status and Version
```bash
sudo systemctl status php8.1-fpm
php -v
ls /var/run/php/
```

**Output:**
```
● php8.1-fpm.service - The PHP 8.1 FastCGI Process Manager
     Loaded: loaded (/lib/systemd/system/php8.1-fpm.service; enabled)
     Active: active (running) since Tue 2026-08-18 18:58:00 PKT

PHP 8.1.2-1ubuntu2.25 (cli) (built: Jul 16 2026 18:32:33) (NTS)

php-fpm.sock  php8.1-fpm.pid  php8.1-fpm.sock
```
✅ PHP-FPM is installed and running!

### Step 2: Created PHP Site Directory and Test File
```bash
sudo mkdir -p /var/www/php-site
echo '<?php echo "Hello from PHP-FPM! Server time: " . date("Y-m-d H:i:s"); ?>' | sudo tee /var/www/php-site/index.php
```

### Step 3: Created PHP Nginx Config
```bash
sudo tee /etc/nginx/sites-available/php-site.conf << 'EOF'
server {
    listen 8081;
    server_name localhost;

    root /var/www/php-site;
    index index.php index.html;

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    }
}
EOF
```

### Step 4: Enabled PHP Site
```bash
# Remove old configs
sudo rm /etc/nginx/sites-enabled/*

# Enable PHP config
sudo ln -s /etc/nginx/sites-available/php-site.conf /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

**Output:**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```
✅ Nginx config is valid!

## How I Tested It

### Test 1: Curl Test
```bash
curl http://localhost:8081
```

**Output:**
```
Hello from PHP-FPM! Server time: 2026-08-18 19:02:44
```
✅ PHP is executing correctly!

### Test 2: Browser Test
Opened browser and went to `http://localhost:8081`

**Result:** The page shows dynamic PHP output with the current date and time. Refreshing the page updates the time, proving PHP is actually executing.

### Test 3: Verify PHP Info (Optional)
```bash
echo '<?php phpinfo(); ?>' | sudo tee /var/www/php-site/info.php
curl http://localhost:8081/info.php | head -20
```
✅ Shows detailed PHP configuration.

## Issues I Encountered

**Issue 1:** PHP-FPM service name was different.
- **Symptom:** `Unit php-fpm.service could not be found`
- **Cause:** The service name includes the PHP version number
- **Fix:** Used `php8.1-fpm` instead of `php-fpm`

**Issue 2:** Socket path needed correct version.
- **Symptom:** Possible 502 Bad Gateway if using wrong socket
- **Cause:** PHP version might be different
- **Fix:** Checked `ls /var/run/php/` and used `unix:/var/run/php/php8.1-fpm.sock`

**Issue 3:** Old configs were still enabled.
- **Symptom:** `curl` showed wrong page or redirects
- **Cause:** Previous task configs were still active
- **Fix:** `sudo rm /etc/nginx/sites-enabled/*` then enabled only PHP config

**Issue 4:** PHP code showing as text.
- **Symptom:** Saw `<?php echo "Hello..." ?>` instead of executed output
- **Cause:** Nginx didn't have the PHP location block
- **Fix:** Added `location ~ \.php$` block with `fastcgi_pass`

## How the PHP Execution Flow Works

```
Browser → Nginx (port 8081)
              ↓
      Request: GET /index.php
              ↓
      Does it end with .php?
              ↓
          YES!
              ↓
      location ~ \.php$ matches
              ↓
      Send to PHP-FPM via socket
      unix:/var/run/php/php8.1-fpm.sock
              ↓
      PHP-FPM executes PHP code
              ↓
      Returns HTML result
              ↓
      Nginx sends to browser
              ↓
      Browser shows: "Hello from PHP-FPM! Server time: 2026-08-18 19:02:44"
```

## Why the URL Works Without `.php`

When you visit `http://localhost:8081`, Nginx looks for:

| Step | What Nginx does |
|------|-----------------|
| 1 | User requests `/` |
| 2 | Nginx checks `index` directive: `index.php index.html` |
| 3 | Nginx looks for `/var/www/php-site/index.php` |
| 4 | Found! Sends to PHP-FPM for execution |
| 5 | Returns PHP output to browser |

So `http://localhost:8081` is really serving `/var/www/php-site/index.php`!

## Result
✅ PHP-FPM installed and running  
✅ Nginx successfully executes PHP files  
✅ Dynamic PHP output shows current date/time  
✅ Browser and curl tests pass  
✅ Both `http://localhost:8081` and `http://localhost:8081/index.php` work

## Commands Reference
```bash
# Check PHP-FPM status
sudo systemctl status php8.1-fpm

# Check PHP version
php -v

# Check socket path
ls /var/run/php/

# Create PHP site
sudo mkdir -p /var/www/php-site
echo '<?php echo "Hello from PHP-FPM! Server time: " . date("Y-m-d H:i:s"); ?>' | sudo tee /var/www/php-site/index.php

# Enable PHP config
sudo rm /etc/nginx/sites-enabled/*
sudo ln -s /etc/nginx/sites-available/php-site.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Test PHP
curl http://localhost:8081

# Create phpinfo page (for debugging)
echo '<?php phpinfo(); ?>' | sudo tee /var/www/php-site/info.php
curl http://localhost:8081/info.php | head -20
```

