# Task 9: URL Rewriting and Redirects

## What is this?
Configured Nginx to handle URL rewriting and redirects. `return 301` sends a redirect to the browser (user sees URL change), while `rewrite` internally changes the URL without the user knowing.

## Why does it matter?
- **SEO:** Redirect old pages to new ones so search engines update their indexes
- **Clean URLs:** Turn ugly URLs like `/product.php?id=123` into pretty ones like `/product/123`
- **User experience:** Visitors see clean, memorable URLs
- **Link sharing:** Clean URLs are easier to share and look more professional

## Configuration
See `conf/rewrites.conf`

```nginx
server {
    listen 8081;
    server_name localhost;

    root /var/www/static-site;
    index index.html;

    # Redirect old page to new page (browser sees the change)
    location /old-page {
        return 301 /new-page.html;
    }

    # Rewrite a pretty URL internally to a real file (browser sees no change)
    rewrite ^/product/(\d+)$ /product.php?id=$1 last;

    # PHP handler - required for .php files to execute
    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Configuration Breakdown

| Directive | What it does |
|-----------|--------------|
| `listen 8081;` | Nginx listens on port 8081 |
| `location /old-page` | Matches requests to `/old-page` |
| `return 301 /new-page.html;` | Redirects browser to `/new-page.html` (user sees URL change) |
| `rewrite ^/product/(\d+)$ /product.php?id=$1 last;` | Internally changes `/product/123` to `/product.php?id=123` (user doesn't see change) |
| `location ~ \.php$` | Handles all `.php` files and sends them to PHP-FPM |
| `fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;` | Sends PHP requests to PHP-FPM |

## What I Actually Did

### Step 1: Created Rewrite Config
Created `/etc/nginx/sites-available/rewrites.conf` with the above configuration.

### Step 2: Created Test Files
```bash
# Create new page for redirect test
echo '<h1>This is the NEW page!</h1>' | sudo tee /var/www/static-site/new-page.html

# Create PHP file for rewrite test
echo '<?php echo "Product ID: " . $_GET["id"]; ?>' | sudo tee /var/www/static-site/product.php
```

### Step 3: Enabled Rewrite Config
```bash
# Remove old configs
sudo rm /etc/nginx/sites-enabled/*

# Enable rewrite config
sudo ln -s /etc/nginx/sites-available/rewrites.conf /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

## How I Tested It

### Test 1: Redirect (`return 301`)

**Check redirect headers:**
```bash
curl -I http://localhost:8081/old-page
```

**Output:**
```
HTTP/1.1 301 Moved Permanently
Location: http://localhost:8081/new-page.html
```
✅ Browser gets redirected to the new page!

**Follow the redirect:**
```bash
curl -L http://localhost:8081/old-page
```

**Output:**
```
<h1>This is the NEW page!</h1>
```
✅ Redirect works! User automatically goes to the new page.

### Test 2: Rewrite (Internal URL Change)

```bash
curl http://localhost:8081/product/123
```

**Output:**
```
Product ID: 123
```

```bash
curl http://localhost:8081/product/456
```

**Output:**
```
Product ID: 456
```

✅ Rewrite works! User sees `/product/123` but Nginx serves `/product.php?id=123`

## Issues I Encountered

**Issue 1:** Initial 404 error when testing redirect.
- **Symptom:** `curl -L http://localhost:8081/old-page` returned 404
- **Cause:** The target file `/var/www/static-site/new-page.html` didn't exist
- **Fix:** Created the file: `echo '<h1>This is the NEW page!</h1>' | sudo tee /var/www/static-site/new-page.html`

**Issue 2:** PHP code showing as text instead of executing.
- **Symptom:** `curl http://localhost:8081/product/123` showed `<?php echo "Product ID: " . $_GET["id"]; ?>`
- **Cause:** No PHP handler in the config
- **Fix:** Added `location ~ \.php$` block with `fastcgi_pass`

**Issue 3:** Redirect target mismatch.
- **Symptom:** Redirect went to `/new-page` but file was `/new-page.html`
- **Cause:** Missing `.html` extension in redirect
- **Fix:** Changed `return 301 /new-page;` to `return 301 /new-page.html;`

## How the Flow Works

### Redirect Flow (`return 301`):
```
User types: /old-page
    ↓
Nginx: "That page moved! Go to /new-page.html"
    ↓
Browser: "OK, I'll go to /new-page.html"
    ↓
User sees: http://localhost:8081/new-page.html (URL CHANGES!)
```

### Rewrite Flow (Internal):
```
User types: /product/123
    ↓
Nginx: "I'll internally change this to /product.php?id=123"
    ↓
Nginx: Serves /product.php?id=123
    ↓
User still sees: http://localhost:8081/product/123 (URL STAYS THE SAME!)
```

## Result
✅ Redirect works - `/old-page` goes to `/new-page.html` with 301 status
✅ Rewrite works - `/product/123` serves `/product.php?id=123` internally
✅ URL stays clean - User sees `/product/123`, not `/product.php?id=123`
✅ PHP executes correctly - Shows dynamic product ID

## Commands Reference
```bash
# Test redirect headers
curl -I http://localhost:8081/old-page

# Follow redirect
curl -L http://localhost:8081/old-page

# Test rewrite with different product IDs
curl http://localhost:8081/product/123
curl http://localhost:8081/product/456
curl http://localhost:8081/product/789
```

## Key Learning Points
- `return 301` = Redirect (user sees URL change)
- `rewrite` = Internal change (user doesn't see URL change)
- PHP files need a `location ~ \.php$` block to execute
- Always test with `nginx -t` before reloading