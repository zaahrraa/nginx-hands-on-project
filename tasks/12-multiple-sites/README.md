# Task 12: Multiple Sites with Subdomains / Separate Server Blocks

## What is this?
Configured Nginx to host multiple websites on a single server using separate server blocks. Each site has its own domain/subdomain (`site1.test` and `site2.test`) with its own root directory and configuration.

## Why does it matter?
- **Host multiple websites** on a single server (cost-effective)
- **Different subdomains** for different services (blog.example.com, shop.example.com, api.example.com)
- **Isolation** between sites (each site has its own config and files)
- **Common practice** in web hosting and DevOps

## Configuration

### Site 1 Config: `conf/site1.conf`
```nginx
server {
    listen 8081;
    server_name site1.test;

    root /var/www/site1;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Site 2 Config: `conf/site2.conf`
```nginx
server {
    listen 8081;
    server_name site2.test;

    root /var/www/site2;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Configuration Breakdown

| Directive | What it does |
|-----------|--------------|
| `listen 8081;` | Both sites listen on port 8081 |
| `server_name site1.test;` | Matches requests for `site1.test` |
| `server_name site2.test;` | Matches requests for `site2.test` |
| `root /var/www/site1;` | Serves files from `/var/www/site1` for Site 1 |
| `root /var/www/site2;` | Serves files from `/var/www/site2` for Site 2 |
| `index index.html;` | Serves `index.html` by default |

## What I Actually Did

### Step 1: Created Site Directories and Content
```bash
# Create directories
sudo mkdir -p /var/www/site1
sudo mkdir -p /var/www/site2

# Create index pages
echo '<h1>Welcome to SITE 1!</h1>' | sudo tee /var/www/site1/index.html
echo '<h1>Welcome to SITE 2!</h1>' | sudo tee /var/www/site2/index.html
```

### Step 2: Created Site Configs
Created `/etc/nginx/sites-available/site1.conf` and `/etc/nginx/sites-available/site2.conf` with the above configurations.

### Step 3: Enabled Both Sites
```bash
# Remove old configs
sudo rm /etc/nginx/sites-enabled/*

# Enable both sites
sudo ln -s /etc/nginx/sites-available/site1.conf /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/site2.conf /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### Step 4: Edited Hosts File (For Testing Subdomains)
Since we don't have real domains, we simulated them by editing the Windows hosts file.

**Added to `C:\Windows\System32\drivers\etc\hosts`:**
```
127.0.0.1 site1.test
127.0.0.1 site2.test
```

**Or in WSL `/etc/hosts`:**
```
127.0.0.1 site1.test site2.test
```

## How I Tested It

### Test 1: Site 1 with curl
```bash
curl http://site1.test:8081
```

**Output:**
```
<h1>Welcome to SITE 1!</h1>
```
✅ Site 1 is working!

### Test 2: Site 2 with curl
```bash
curl http://site2.test:8081
```

**Output:**
```
<h1>Welcome to SITE 2!</h1>
```
✅ Site 2 is working!

### Test 3: Browser Test

**Site 1:**
```
http://site1.test:8081
```
**Result:** Shows "Welcome to SITE 1!" ✅

**Site 2:**
```
http://site2.test:8081
```
**Result:** Shows "Welcome to SITE 2!" ✅

## How the Flow Works

### When User Visits Site 1:
```
User types: http://site1.test:8081
    ↓
Nginx checks: Which server_name matches?
    ↓
Matches: server_name site1.test;
    ↓
Nginx serves: /var/www/site1/index.html
    ↓
User sees: "Welcome to SITE 1!" ✅
```

### When User Visits Site 2:
```
User types: http://site2.test:8081
    ↓
Nginx checks: Which server_name matches?
    ↓
Matches: server_name site2.test;
    ↓
Nginx serves: /var/www/site2/index.html
    ↓
User sees: "Welcome to SITE 2!" ✅
```

### Nginx Decision Flow:
```
Request: site1.test:8081
    ↓
Check server blocks:
    ├── site1.test → Match! → Serve site1
    └── site2.test → No match

Request: site2.test:8081
    ↓
Check server blocks:
    ├── site1.test → No match
    └── site2.test → Match! → Serve site2
```

## Issues I Encountered

**Issue:** Trying to open URL in terminal instead of browser.
- **Symptom:** `bash: http://site1.test:8081: No such file or directory`
- **Cause:** Typed URL directly in terminal without `curl`
- **Fix:** Used `curl http://site1.test:8081` or opened in browser

## Result
✅ Site 1 accessible at `http://site1.test:8081`
✅ Site 2 accessible at `http://site2.test:8081`
✅ Both sites show their respective content
✅ Nginx correctly routes requests based on `server_name`
✅ Hosts file configured for local subdomain testing

## Commands Reference
```bash
# Test Site 1
curl http://site1.test:8081

# Test Site 2
curl http://site2.test:8081

# Open in browser (Windows)
start http://site1.test:8081
start http://site2.test:8081

# Check enabled sites
ls -la /etc/nginx/sites-enabled/

# Check configs
sudo nginx -T | grep -A 10 "server_name site1"
sudo nginx -T | grep -A 10 "server_name site2"

# Reload Nginx
sudo nginx -t
sudo systemctl reload nginx
```

## Files Created/Modified
| File | Purpose |
|------|---------|
| `/var/www/site1/index.html` | Site 1 content |
| `/var/www/site2/index.html` | Site 2 content |
| `/etc/nginx/sites-available/site1.conf` | Site 1 Nginx config |
| `/etc/nginx/sites-available/site2.conf` | Site 2 Nginx config |
| `/etc/nginx/sites-enabled/site1.conf` | Symlink to active Site 1 config |
| `/etc/nginx/sites-enabled/site2.conf` | Symlink to active Site 2 config |
| `C:\Windows\System32\drivers\etc\hosts` | DNS simulation for testing |