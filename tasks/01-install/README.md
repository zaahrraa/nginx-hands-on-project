# Task 1: Install Nginx

## What is this?
Installing Nginx — a lightweight, high-performance web server and reverse proxy — on Ubuntu (running via WSL2 on Windows), and confirming it starts correctly and stays running.

## Why does it matter?
Every other task in this project builds on top of a working Nginx installation. Before Nginx can serve pages, proxy requests, or load-balance traffic, it needs to be installed, running, and set to auto-start on boot so it survives reboots without manual intervention.

## Commands used
```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx    # auto-start on boot
sudo systemctl status nginx    # confirm it's active
```

## How I tested it
- `curl -I localhost:8081` → confirmed `Server: nginx/1.18.0` in the response headers
- `sudo systemctl status nginx` → confirmed `active (running)`
- Visited `http://localhost:8081` in the browser to visually confirm the welcome page

## Result
Nginx installed successfully and running on port 8081. Verified both via terminal (`curl`, `systemctl`) and browser.

## What I learned / Issues I hit
Ran into a confusing bug where `curl` confirmed Nginx was running and responding correctly, but my browser kept showing an **Apache2 Default Page** instead of Nginx's welcome page — on the exact same port.

**Diagnosis process:**
1. First suspected a WSL2 networking/port-forwarding conflict (Windows intercepting the port before it reached WSL) — ruled out by checking `netstat -ano | findstr :8081` on the Windows side, which showed nothing listening there.
2. Then suspected Apache running *inside* WSL alongside Nginx, both fighting over the port — ruled out, since `systemctl status nginx` showed a single clean process with no conflicts.
3. Root cause: inspecting `/var/www/html/` (Nginx's document root) showed **two files** — an old `index.html` (dated back to a prior Apache install in June) and Nginx's own untouched `index.nginx-debian.html` (freshly created on install day). Nginx doesn't delete files it doesn't own, so it was simply serving the pre-existing `index.html` it found — which happened to be Apache's leftover default page, not a real port conflict at all.

**Fix:**
```bash
sudo rm /var/www/html/index.html
sudo mv /var/www/html/index.nginx-debian.html /var/www/html/index.html
sudo systemctl reload nginx
```

**Final twist:** even after the fix, my regular Chrome window kept showing the old Apache page — this turned out to be simple browser caching, not a real issue. Opening an incognito window (no cache) confirmed the fix had worked immediately. Lesson learned: verify server-side with `curl` before trusting what the browser shows, since the browser can lie via caching even when the server is already fixed.