# Task 2: Serve Static Content (root and index directives)

## What is this?
Configuring Nginx to serve plain HTML files directly from a folder on disk, using the `root` directive to point to that folder and `index` to define the default file to hand out.

## Why does it matter?
This is Nginx's most basic job — handing out files without any backend processing. Understanding `root` and `index` is foundational, since almost every later task (reverse proxy, PHP, multi-site hosting) still relies on these same two directives underneath.

## Configuration
See `conf/static-site.conf`:
```nginx
server {
    listen 8081;
    server_name static.example.com;

    root /var/www/static-site;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## Commands used
```bash
sudo mkdir -p /var/www/static-site
echo "<h1>Hello from my static site!</h1>" | sudo tee /var/www/static-site/index.html

sudo ln -s /etc/nginx/sites-available/static-site.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## How I tested it
```bash
curl http://localhost:8081
```
Expected and got back the custom HTML (`Hello from my static site!`) instead of Nginx's default welcome page.

## Result
Nginx now serves my own static HTML file instead of the default one — confirmed via both `curl` and browser.

## What I learned / Issues I hit
`try_files $uri $uri/ =404;` is what makes Nginx check: does this exact file exist? Does it exist as a folder (fall back to its index)? If neither, return a proper 404 instead of a confusing error. Without it, requesting a non-existent file gives a less clean failure.