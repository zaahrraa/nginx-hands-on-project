# Task 17: Monitor and Troubleshoot Using Logs

## What is this?
This ties everything together — being able to read logs to diagnose real problems is the actual day-to-day job of a DevOps engineer. Learned to monitor logs, validate configs, check service status, and troubleshoot issues by deliberately breaking and fixing a configuration.

## Why does it matter?
- **Real-world skill:** Troubleshooting is what DevOps engineers do daily
- **Problem-solving:** Finding and fixing issues quickly
- **Interview gold:** Showing you can break, diagnose, and fix demonstrates real engineering ability
- **Production readiness:** Being able to monitor and fix issues is essential for any live system

## What I Did

### Step 1: Created a Working Configuration
```bash
sudo tee /etc/nginx/sites-available/troubleshoot.conf << 'EOF'
server {
    listen 8081;
    server_name localhost;

    root /var/www/static-site;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
EOF

sudo rm /etc/nginx/sites-enabled/*
sudo ln -s /etc/nginx/sites-available/troubleshoot.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 2: Monitored Live Traffic
```bash
sudo tail -f /var/log/nginx/access.log
```

### Step 3: Validated Configuration
```bash
sudo nginx -t
```

**Output:**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### Step 4: Checked Nginx Status
```bash
sudo systemctl status nginx
```

**Output:**
```
● nginx.service - A high performance web server
     Active: active (running)
```

### Step 5: Checked System Logs
```bash
sudo journalctl -u nginx -n 50
```

### Step 6: Searched for 404 Errors
```bash
grep "404" /var/log/nginx/access.log | tail -10
```

## The "Break, Diagnose, Fix" Story

### 1. Break It ❌
Added a syntax error to the config (removed a semicolon):

```bash
sudo sed -i 's/try_files \$uri \$uri\/ =404;/try_files \$uri \$uri\/ =404/' /etc/nginx/sites-available/troubleshoot.conf
```

### 2. Diagnose It 🔍
Ran the config test:

```bash
sudo nginx -t
```

**Error Output:**
```
nginx: [emerg] invalid number of arguments in "try_files" directive in /etc/nginx/sites-available/troubleshoot.conf:8
nginx: configuration file /etc/nginx/nginx.conf test failed
```

### 3. Checked Error Log
```bash
sudo tail -20 /var/log/nginx/error.log
```

**Output:**
```
2026/08/18 20:30:00 [emerg] 12345#12345: invalid number of arguments in "try_files" directive in /etc/nginx/sites-available/troubleshoot.conf:8
```

### 4. Fixed It ✅
Fixed the syntax error (added back the semicolon):

```bash
sudo sed -i 's/try_files \$uri \$uri\/ =404/try_files \$uri \$uri\/ =404;/' /etc/nginx/sites-available/troubleshoot.conf
```

### 5. Verified Fix
```bash
sudo nginx -t
```

**Output:**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 6. Reloaded Nginx
```bash
sudo systemctl reload nginx
```

### 7. Tested It Works
```bash
curl http://localhost:8081
```

**Output:**
```
<h1>Hello from my static site!</h1>
```

## Commands Reference

| Command | What it does |
|---------|--------------|
| `sudo tail -f /var/log/nginx/access.log` | Watch live traffic in real-time |
| `sudo tail -f /var/log/nginx/error.log` | Watch live errors in real-time |
| `sudo nginx -t` | Validate Nginx config syntax |
| `sudo systemctl status nginx` | Check if Nginx is running |
| `sudo journalctl -u nginx -n 50` | Check system logs for Nginx |
| `grep "404" /var/log/nginx/access.log | tail` | Find recent 404 errors |
| `sudo systemctl reload nginx` | Reload Nginx after fixing config |

## What I Learned

### Common Nginx Errors

| Error | What it means | How to fix |
|-------|--------------|------------|
| `[emerg] invalid number of arguments` | Missing semicolon or extra arguments | Check syntax, add missing semicolon |
| `[emerg] open() "file" failed` | File doesn't exist | Create the file or fix the path |
| `[emerg] unknown directive` | Typo in directive name | Correct the spelling |
| `[emerg] duplicate server_name` | Same server_name used twice | Remove duplicate or use unique names |
| `[warn] conflicting server name` | Server name conflict | Fix duplicate server_name |

### Troubleshooting Flow

```
Issue Found
    ↓
Check Error Log: tail -f /var/log/nginx/error.log
    ↓
Run Config Test: sudo nginx -t
    ↓
Read Error Message: Tells you line number and issue
    ↓
Fix the Config: Edit the file
    ↓
Test Again: sudo nginx -t
    ↓
Passed! → Reload Nginx: sudo systemctl reload nginx
    ↓
Test: curl http://localhost:8081
```

## Result
✅ Access logs monitored in real-time with `tail -f`
✅ Error logs checked for issues
✅ Config validation working with `nginx -t`
✅ Nginx status checked with `systemctl status`
✅ System logs viewed with `journalctl`
✅ 404 errors searched in access logs
✅ Deliberately broke config and diagnosed the error
✅ Successfully fixed the config and verified it works

## Files Modified
| File | Purpose |
|------|---------|
| `/etc/nginx/sites-available/troubleshoot.conf` | Config used for troubleshooting |
| `/var/log/nginx/access.log` | Access log for monitoring traffic |
| `/var/log/nginx/error.log` | Error log for diagnosing issues |