# Task 3: Reverse Proxy (proxy_pass + custom headers)

## What is this?
Configuring Nginx to forward incoming requests to a separate backend application (running on a different port) instead of serving files itself, and passing along useful headers so the backend knows details about the original request.

## Why does it matter?
This is the core of what makes Nginx a "reverse proxy" rather than just a file server. In real production setups, Nginx typically sits in front of application servers (Node.js, Python, Java, etc.) — handling incoming traffic, then quietly forwarding it to the right backend and relaying the response back. Custom headers like `X-Real-IP` matter because, without them, the backend app would only ever see Nginx's own IP address instead of the real visitor's IP.

## Configuration
See `conf/reverse-proxy.conf`:
```nginx
server {
    listen 8081;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Commands used
```bash
# Set up a simple demo backend to proxy to
mkdir ~/backend-demo && cd ~/backend-demo
echo "Hello from backend on port 5000" > index.html
python3 -m http.server 5000 &

# Enable the Nginx config
sudo ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## How I tested it
```bash
curl http://localhost:8081
```
Expected and got: `Hello from backend on port 5000` — even though the request was made to Nginx's port (8081), not the backend's port (5000) directly. This confirms Nginx received the request and silently forwarded it to the backend, then relayed the backend's response back.

Also checked the headers arriving at the backend, to confirm `X-Real-IP` and friends were actually being passed through correctly.

## Result
Requests to Nginx on port 8081 are transparently forwarded to a Python backend on port 5000, with the backend correctly receiving custom headers about the original request.

