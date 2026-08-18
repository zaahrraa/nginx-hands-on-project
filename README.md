# Nginx Hands-On Project

## Complete Beginner-to-Portfolio Nginx Guide

This is a comprehensive hands-on project where I installed, configured, and mastered Nginx from scratch on Ubuntu (WSL). I documented everything with screenshots, configs, and troubleshooting steps — making this a complete portfolio-ready project.

---

## Project Overview

I built this project to learn Nginx by actually **doing** it — not just watching videos. I completed 17 hands-on tasks covering everything from basic installation to advanced monitoring and troubleshooting.

**What I built:**
- A fully functional Nginx web server on Ubuntu 22.04 (WSL)
- 17 different Nginx configurations with real testing
- Complete documentation with screenshots and READMEs
- A GitHub-ready portfolio project

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Nginx** | Web server and reverse proxy |
| **Ubuntu 22.04** | Operating system (WSL) |
| **PHP-FPM** | PHP processing |
| **Python** | Backend servers for testing |
| **OpenSSL** | SSL/TLS certificates |
| **Bash** | Scripting and automation |
| **Git** | Version control |

---

##  Project Structure

```
nginx-hands-on-project/
├── README.md                          # Main project overview
├── LICENSE
├── docs/
│   └── portfolio-writeup.md           # Detailed portfolio write-up
├── screenshots/                       # All task screenshots
│   └── tasks/
│       ├── 01-install/
│       ├── 02-static-content/
│       ├── 03-reverse-proxy/
│       ├── 04-load-balancing/
│       ├── 05-ssl-tls/
│       ├── 06-caching/
│       ├── 07-websocket/
│       ├── 08-php-fpm/
│       ├── 09-rewrites-redirects/
│       ├── 10-security-headers-auth/
│       ├── 11-custom-error-pages/
│       ├── 12-multiple-sites/
│       ├── 13-nginx-conf-includes/
│       ├── 14-nginx-variables/
│       ├── 15-rate-limiting/
│       ├── 16-logging/
│       └── 17-monitoring-troubleshooting/
└── tasks/                            # Config files and READMEs
    ├── 01-install/
    ├── 02-static-content/
    ├── 03-reverse-proxy/
    ├── 04-load-balancing/
    ├── 05-ssl-tls/
    ├── 06-caching/
    ├── 07-websocket/
    ├── 08-php-fpm/
    ├── 09-rewrites-redirects/
    ├── 10-security-headers-auth/
    ├── 11-custom-error-pages/
    ├── 12-multiple-sites/
    ├── 13-nginx-conf-includes/
    ├── 14-nginx-variables/
    ├── 15-rate-limiting/
    ├── 16-logging/
    └── 17-monitoring-troubleshooting/
```

---

##  Complete Task List

### 01. Install Nginx 
Installed Nginx on Ubuntu 22.04 and verified it was running.

**Key Commands:**
```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

---

### 02. Serve Static Content 
Created a custom static website with `root` and `index` directives.

**Config:**
```nginx
server {
    listen 8081;
    server_name localhost;
    root /var/www/static-site;
    index index.html;
}
```

---

### 03. Reverse Proxy 
Configured Nginx to proxy requests to a Python backend server.

**Key Learning:** `proxy_pass` forwards requests to backend servers with custom headers.

---

### 04. Load Balancing 
Implemented round-robin, least_conn, and ip_hash load balancing algorithms.

**Key Learning:** `upstream` blocks define backend pools for distributing traffic.

---

### 05. SSL/TLS with Self-Signed Certificate 
Generated a self-signed SSL certificate and configured HTTPS on port 443.

**Key Learning:** SSL/TLS encrypts traffic; self-signed certs are great for learning.

---

### 06. Caching with `proxy_cache` 
Configured caching to serve repeated requests faster from cache.

**Key Learning:** `X-Cache-Status: HIT` vs `MISS` shows if cache is working.

---

### 07. WebSocket Support 
Configured Nginx to proxy WebSocket connections for real-time apps.

**Key Learning:** WebSockets need special headers (`Upgrade`, `Connection`).

---

### 08. PHP Integration via PHP-FPM 
Configured Nginx to execute PHP code using PHP-FPM.

**Key Learning:** Nginx can't run PHP directly — uses `fastcgi_pass` to PHP-FPM.

---

### 09. URL Rewriting and Redirects 
Implemented `return 301` redirects and internal `rewrite` rules.

**Key Learning:** `rewrite` changes URL internally; `return` redirects the browser.

---

### 10. Security Headers and Basic Authentication 
Added security headers and password-protected the `/admin` area.

**Key Headers:** `X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`, `Referrer-Policy`

---

### 11. Custom Error Pages (404, 403) 
Created custom user-friendly error pages for 404 and 403 errors.

**Key Learning:** `error_page` directive with `internal` location blocks.

---

### 12. Multiple Sites with Subdomains 
Hosted multiple sites on one server using separate server blocks.

**Key Learning:** `server_name` tells Nginx which site to serve.

---

### 13. Understand `nginx.conf` using `include` 
Explored how `include` loads configs from `sites-enabled/`.

**Key Learning:** `sites-available` stores configs; `sites-enabled` contains symlinks to active configs.

---

### 14. Using Variables (`$host`, `$remote_addr`, `$request_uri`) 
Used Nginx variables to capture and display request information.

**Key Learning:** Variables like `$host`, `$remote_addr`, `$request_uri` contain live request data.

---

### 15. Rate Limiting, Connection Limits, Buffering 
Protected the server from abuse with rate limiting and connection limits.

**Key Learning:** `limit_req` and `limit_conn` protect against DDoS attacks.

---

### 16. Customize Access and Error Logs 
Created custom log formats and separate access/error logs.

**Key Learning:** `log_format` defines custom log structures; `tail -f` watches logs live.

---

### 17. Monitor and Troubleshoot Using Logs 
Learned to monitor logs, validate configs, and troubleshoot by breaking and fixing.

**Key Learning:** The "break, diagnose, fix" process is essential for DevOps.

---

##  Skills Demonstrated

| Skill | Details |
|-------|---------|
| **Nginx Installation** | Installed and managed Nginx on Ubuntu |
| **Static Content** | Served HTML, CSS, and images |
| **Reverse Proxy** | Proxied requests to backend servers |
| **Load Balancing** | Round-robin, least_conn, ip_hash |
| **SSL/TLS** | Self-signed certificates and HTTPS |
| **Caching** | `proxy_cache` for faster responses |
| **WebSockets** | Real-time communication |
| **PHP-FPM** | PHP integration with FastCGI |
| **URL Rewriting** | Clean URLs and redirects |
| **Security** | Headers and basic authentication |
| **Error Pages** | Custom 404/403 pages |
| **Multiple Sites** | Subdomains and server blocks |
| **Variables** | Dynamic request handling |
| **Rate Limiting** | DDoS protection |
| **Logging** | Custom formats and monitoring |
| **Troubleshooting** | Log analysis and debugging |

---

## How to Run This Project

### Prerequisites
- Ubuntu 22.04 (or WSL on Windows)
- Nginx installed
- Basic terminal knowledge

### Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/nginx-hands-on-project.git

# Navigate to project
cd nginx-hands-on-project

# Install Nginx
sudo apt update
sudo apt install nginx -y

# Copy configs (adjust paths as needed)
sudo cp tasks/02-static-content/conf/static-site.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/static-site.conf /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```


---

##  Screenshots

All screenshots are organized by task in the `screenshots/tasks/` folder. Each task has its own directory with terminal and browser screenshots showing the working configuration.

---


### DocumentTION
- **Document everything** - screenshots and READMEs
- **Test everything** - always run `nginx -t`
- **Break and fix** - learn from mistakes
- **Portfolio ready** - GitHub + LinkedIn

---


