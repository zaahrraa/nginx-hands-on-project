# Task 4: Load Balancing (round robin, least_conn, ip_hash)

## What is this?
Configuring Nginx to distribute incoming requests across multiple backend servers instead of sending everything to just one, using an `upstream` block to define the pool of backends and a chosen algorithm to decide how traffic gets split between them.

## Why does it matter?
In real production systems, a single backend server can only handle so much traffic before it slows down or crashes. Load balancing spreads requests across several identical backend instances, improving both performance and reliability — if one backend goes down, the others can still serve traffic. Understanding the different algorithms matters because each suits a different scenario (evenly distributed traffic vs. long-running connections vs. session consistency).

## Configuration
See `conf/load-balancer.conf`. Tested all three algorithms by swapping the `upstream` block:

**Round robin (default — no keyword needed):**
```nginx
upstream backend_pool {
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    listen 8081;
    server_name localhost;

    location / {
        proxy_pass http://backend_pool;
    }
}
```

**Least connections:**
```nginx
upstream backend_pool {
    least_conn;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}
```

**IP hash (same client always routed to the same backend):**
```nginx
upstream backend_pool {
    ip_hash;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}
```

## Commands used
```bash
# Two demo backends
mkdir ~/backend1 && echo "Response from Server 1" > ~/backend1/index.html
mkdir ~/backend2 && echo "Response from Server 2" > ~/backend2/index.html
cd ~/backend1 && python3 -m http.server 5001 &
cd ~/backend2 && python3 -m http.server 5002 &

sudo nginx -t
sudo systemctl reload nginx
```

## How I tested it
```bash
for i in {1..6}; do curl -s http://localhost:8081; done
```
- **Round robin:** responses alternated evenly between "Server 1" and "Server 2".
- **Least connections:** with both backends idle and equally fast, behaved like round robin in this simple test — the difference only becomes visible when one backend is deliberately slowed down or under heavier load.
- **IP hash:** since all test requests came from the same machine (same IP), every request landed on the same backend consistently — proving IP hash correctly "sticks" a client to one server.

## Result
Verified all three load balancing algorithms with real traffic, confirming each behaves according to its documented logic.

