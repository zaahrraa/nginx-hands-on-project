# Task 13: Understand and Modify `nginx.conf` using `include`

## What is this?
Examined the main Nginx configuration file (`/etc/nginx/nginx.conf`) to understand how it uses the `include` directive to pull in other configuration files. This is why we have `sites-available/` and `sites-enabled/` as separate files per site.

## Why does it matter?
- **Modular configuration:** Instead of one giant file, config is split into manageable pieces
- **Easy management:** Enable/disable sites by simply adding/removing symlinks
- **Clean organization:** Each site has its own config file
- **Best practice:** This is how real-world Nginx setups are organized

## The Key Line in `nginx.conf`

```nginx
include /etc/nginx/sites-enabled/*;
```

### What This Does
This line tells Nginx: **"Include (read) all files in the `/etc/nginx/sites-enabled/` directory as part of the configuration."**

## How the Structure Works

```
/etc/nginx/
├── nginx.conf              # Main config file
├── sites-available/        # ALL configs (enabled or disabled)
│   ├── site1.conf
│   ├── site2.conf
│   └── default
├── sites-enabled/          # ONLY active configs (symlinks)
│   ├── site1.conf -> ../sites-available/site1.conf
│   └── site2.conf -> ../sites-available/site2.conf
└── conf.d/                 # Additional config snippets
```

### Two Key Folders

| Folder | Purpose | Contains |
|--------|---------|----------|
| **`sites-available/`** | Storage for ALL site configs | Actual config files for every site |
| **`sites-enabled/`** | ONLY ACTIVE sites | Symlinks to configs in `sites-available/` |

## How to Enable/Disable a Site

### Enable a Site (Create Symlink)
```bash
sudo ln -s /etc/nginx/sites-available/site1.conf /etc/nginx/sites-enabled/
```

### Disable a Site (Remove Symlink)
```bash
sudo rm /etc/nginx/sites-enabled/site1.conf
```

### Check Active Sites
```bash
ls -la /etc/nginx/sites-enabled/
```

## What I Actually Did

### Step 1: Viewed the Main Config File
```bash
sudo cat /etc/nginx/nginx.conf
```

### Step 2: Found the Key `include` Lines
Looked for these lines in `nginx.conf`:
```nginx
include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;
```

### Step 3: Checked Active Sites
```bash
ls -la /etc/nginx/sites-enabled/
```

**Output:**
```
lrwxrwxrwx 1 root root 34 site1.conf -> ../sites-available/site1.conf
lrwxrwxrwx 1 root root 34 site2.conf -> ../sites-available/site2.conf
```

### Step 4: Disabled a Site
```bash
sudo rm /etc/nginx/sites-enabled/site1.conf
sudo nginx -t
sudo systemctl reload nginx
```

### Step 5: Re-enabled a Site
```bash
sudo ln -s /etc/nginx/sites-available/site1.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## How the Flow Works

### Nginx Starts Up:
```
Nginx starts
    ↓
Reads /etc/nginx/nginx.conf
    ↓
Sees: include /etc/nginx/sites-enabled/*;
    ↓
Loads ALL configs in sites-enabled/
    ↓
Nginx is ready to serve requests!
```

### Enabling a Site:
```
Config exists in sites-available/site1.conf
    ↓
Create symlink in sites-enabled/
    ↓
Nginx reload: include loads the new config
    ↓
Site is now ACTIVE! ✅
```

### Disabling a Site:
```
Remove symlink from sites-enabled/
    ↓
Nginx reload: include no longer loads the config
    ↓
Site is now INACTIVE! ❌
    ↓
Config still exists in sites-available/ (safe)
```

## Key Benefits of This Structure

| Benefit | Why |
|---------|-----|
| **Safety** | Disabling a site doesn't delete the config (just removes symlink) |
| **Organization** | Each site has its own config file |
| **Modularity** | Add/remove sites without touching main config |
| **Testing** | Test configs before enabling |
| **Version Control** | Track changes per site |

## Real-World Example

### Before (All in one file):
```nginx
server {
    listen 80;
    server_name site1.test;
    root /var/www/site1;
}

server {
    listen 80;
    server_name site2.test;
    root /var/www/site2;
}
```
❌ Giant file, hard to manage

### After (Modular):
```
/etc/nginx/sites-available/site1.conf
/etc/nginx/sites-available/site2.conf
```
✅ Each site has its own file, easy to manage

## Files Structure

```
/etc/nginx/
├── nginx.conf              # Main config with "include sites-enabled/*"
├── sites-available/        # All configs (enabled or not)
│   ├── site1.conf
│   ├── site2.conf
│   └── site3.conf (disabled)
└── sites-enabled/          # Only active sites (symlinks)
    ├── site1.conf -> ../sites-available/site1.conf
    └── site2.conf -> ../sites-available/site2.conf
    # site3.conf is DISABLED (no symlink)
```

## Commands Reference

```bash
# View main config
sudo cat /etc/nginx/nginx.conf

# Find include lines
sudo cat /etc/nginx/nginx.conf | grep include

# List available sites
ls -la /etc/nginx/sites-available/

# List enabled sites
ls -la /etc/nginx/sites-enabled/

# Enable a site
sudo ln -s /etc/nginx/sites-available/site1.conf /etc/nginx/sites-enabled/

# Disable a site
sudo rm /etc/nginx/sites-enabled/site1.conf

# Test config after changes
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx

# Show full config (all includes combined)
sudo nginx -T
```

## What I Learned

- **`include`** is the key that makes modular configuration possible
- **`sites-available/`** stores all configs (like a library)
- **`sites-enabled/`** only has symlinks to active sites
- **Disabling** = remove symlink (config stays safe)
- **Enabling** = create symlink (config becomes active)
- This is the **standard Nginx pattern** used in production

## Summary

| Component | Purpose |
|-----------|---------|
| `nginx.conf` | Main config with `include` directive |
| `include /etc/nginx/sites-enabled/*;` | Loads all active site configs |
| `sites-available/` | ALL site configs (storage) |
| `sites-enabled/` | ONLY active site configs (symlinks) |
| Symlink | Connect `sites-available` to `sites-enabled` |