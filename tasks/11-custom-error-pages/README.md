# Task 11: Custom Error Pages (404, 403)

## What is this?
Configured Nginx to serve custom error pages instead of the default plain, ugly error pages. When a user visits a page that doesn't exist (404) or doesn't have permission (403), they see a branded, user-friendly page.

## Why does it matter?
- **Better user experience:** Users see friendly messages instead of scary default errors
- **Branding consistency:** Error pages match your site's design and feel
- **Keeps users engaged:** Can include helpful links (home page, search, contact)
- **Looks professional:** Custom error pages make your site look polished and well-maintained

## Configuration
See `conf/error-pages.conf`

```nginx
server {
    listen 8081;
    server_name localhost;

    root /var/www/static-site;
    index index.html;

    # Custom error pages
    error_page 404 /404.html;
    error_page 403 /403.html;

    # Serve custom error pages from /var/www/errors
    location = /404.html {
        root /var/www/errors;
        internal;
    }

    location = /403.html {
        root /var/www/errors;
        internal;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Configuration Breakdown

| Directive | What it does |
|-----------|--------------|
| `error_page 404 /404.html;` | Tells Nginx to use `/404.html` for 404 errors |
| `error_page 403 /403.html;` | Tells Nginx to use `/403.html` for 403 errors |
| `location = /404.html` | Matches the exact URL `/404.html` |
| `root /var/www/errors;` | Serves error pages from `/var/www/errors` folder |
| `internal;` | Prevents direct access to error pages (only Nginx can serve them) |

## What I Actually Did

### Step 1: Created Custom Error Pages
```bash
sudo mkdir -p /var/www/errors
echo '<h1>404 - Page not found, but you are in the right place :)</h1>' | sudo tee /var/www/errors/404.html
echo '<h1>403 - Forbidden</h1>' | sudo tee /var/www/errors/403.html
```

### Step 2: Created Error Pages Config
Created `/etc/nginx/sites-available/error-pages.conf` with the above configuration.

### Step 3: Enabled Error Pages Config
```bash
# Remove old configs
sudo rm /etc/nginx/sites-enabled/*

# Enable error pages config
sudo ln -s /etc/nginx/sites-available/error-pages.conf /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### Step 4: Tested 404 Error
```bash
curl http://localhost:8081/nonsense123
```

**Output:**
```html
<h1>404 - Page not found, but you are in the right place :)</h1>
```

## How I Tested It

### Test 1: Non-Existent Page (404)
```bash
curl http://localhost:8081/nonsense123
```

**Output:**
```html
<h1>404 - Page not found, but you are in the right place :)</h1>
```
✅ Custom 404 page shows instead of default Nginx error!

### Test 2: Another Non-Existent Page
```bash
curl http://localhost:8081/xyzabc
```

**Output:**
```html
<h1>404 - Page not found, but you are in the right place :)</h1>
```
✅ Same custom 404 page for ALL non-existent pages!

### Test 3: Browser Test
Opened browser and went to `http://localhost:8081/nonsense123`

**Result:** Saw the custom 404 page with the friendly message ✅

## Issues I Encountered

**Issue:** Error page not showing.
- **Symptom:** Default Nginx 404 page appeared instead of custom
- **Cause:** Config wasn't enabled or error files didn't exist
- **Fix:** 
  ```bash
  # Check files exist
  ls -la /var/www/errors/
  
  # Check config is enabled
  ls -la /etc/nginx/sites-enabled/
  
  # Test config
  sudo nginx -t
  sudo systemctl reload nginx
  ```

## How the Flow Works

### Without Custom Error Page:
```
User visits: /nonsense123
    ↓
Nginx: "File not found!"
    ↓
User sees: Default ugly 404 page ❌
```

### With Custom Error Page:
```
User visits: /nonsense123
    ↓
Nginx: "File not found! Use custom 404 page"
    ↓
Nginx serves: /var/www/errors/404.html
    ↓
User sees: "404 - Page not found, but you're in the right place :)" ✅
```

## Result
✅ Custom 404 page shows for non-existent pages
✅ Error pages are stored in `/var/www/errors/`
✅ Error pages are `internal` (users can't access them directly)
✅ Clean, user-friendly error experience

## Commands Reference
```bash
# Create error pages
sudo mkdir -p /var/www/errors
echo '<h1>404 - Page not found, but you are in the right place :)</h1>' | sudo tee /var/www/errors/404.html
echo '<h1>403 - Forbidden</h1>' | sudo tee /var/www/errors/403.html

# Enable config
sudo rm /etc/nginx/sites-enabled/*
sudo ln -s /etc/nginx/sites-available/error-pages.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Test 404
curl http://localhost:8081/nonsense123

# Check error files
ls -la /var/www/errors/
```

## Error Pages Used

### 404.html
```html
<h1>404 - Page not found, but you're in the right place :)</h1>
```

### 403.html
```html
<h1>403 - Forbidden</h1>
```

