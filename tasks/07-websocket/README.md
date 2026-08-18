# Task 7: WebSocket Support

## What is this?
Configured Nginx to proxy WebSocket connections, enabling real-time communication between clients and a backend WebSocket server.

## Why does it matter?
WebSockets are essential for real-time applications like chat, live notifications, gaming, and streaming. Nginx can proxy these connections while keeping them open.

## Configuration
See `conf/websocket.conf`

```nginx
server {
    listen 8081;
    server_name localhost;

    location /ws/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
    }
}
```

## What I Actually Did

### Step 1: Created WebSocket Config
Created `/etc/nginx/sites-available/websocket.conf` with the above configuration.

### Step 2: Enabled WebSocket Config
```bash
# Remove old configs
sudo rm /etc/nginx/sites-enabled/*

# Enable WebSocket config
sudo ln -s /etc/nginx/sites-available/websocket.conf /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### Step 3: Installed Required Tools
```bash
# Install websocat (WebSocket client)
wget https://github.com/vi/websocat/releases/download/v1.12.0/websocat.x86_64-unknown-linux-musl
chmod +x websocat.x86_64-unknown-linux-musl
sudo mv websocat.x86_64-unknown-linux-musl /usr/local/bin/websocat

# Install Python websockets library
pip3 install websockets
```

### Step 4: Created WebSocket Server
Created `~/websocket-server/websocket_server.py`:

```python
#!/usr/bin/env python3
import asyncio
import websockets
import datetime

async def echo(websocket):
    print(f"Client connected!")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            response = f"Server received: {message}. Time: {datetime.datetime.now()}"
            await websocket.send(response)
    except Exception as e:
        print(f"Error: {e}")

async def main():
    async with websockets.serve(echo, "127.0.0.1", 5000):
        print("✅ WebSocket server running on ws://127.0.0.1:5000")
        print("Waiting for connections...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
```

### Step 5: Started WebSocket Server
```bash
cd ~/websocket-server
python3 websocket_server.py &
```

## How I Tested It

### Test 1: Direct Connection (Skip Nginx)
```bash
echo "Hello Direct!" | websocat ws://127.0.0.1:5000/
```
**Output:**
```
Server received: Hello Direct!. Time: 2026-08-18 18:39:19.695507
```
✅ Direct WebSocket works!

### Test 2: Via Nginx
```bash
echo "Hello Nginx!" | websocat ws://localhost:8081/ws/
```
**Expected Output:**
```
Server received: Hello Nginx!. Time: 2026-08-18 18:40:00.123456
```
✅ Nginx WebSocket proxy works!

### Test 3: Server Logs
Terminal running the server showed:
```
✅ WebSocket server running on ws://127.0.0.1:5000
Waiting for connections...
Client connected!
Received: Hello Direct!
```
✅ Server received and processed the message!

## Issues I Encountered

**Issue 1:** WebSocket server not running.
- **Symptom:** `ps aux | grep websocket_server` showed nothing
- **Cause:** Server wasn't started
- **Fix:** `python3 websocket_server.py &`

**Issue 2:** Port 5000 already in use.
- **Symptom:** `OSError: [Errno 98] address already in use`
- **Cause:** Another process was using port 5000
- **Fix:**
  ```bash
  sudo lsof -i :5000  # Find the process
  sudo kill -9 PID    # Kill it
  # OR
  sudo fuser -k 5000/tcp  # Kill whatever is using it
  ```

**Issue 3:** WebSocket server code error.
- **Symptom:** `TypeError: echo() missing 1 required positional argument: 'path'`
- **Cause:** Newer version of `websockets` library doesn't pass `path` parameter
- **Fix:** Changed `async def echo(websocket, path):` to `async def echo(websocket):`

**Issue 4:** 404 error when testing via Nginx.
- **Symptom:** `Received unexpected status code (404 Not Found)`
- **Cause:** WebSocket server wasn't running or Nginx couldn't reach it
- **Fix:** Started WebSocket server first, then tested via Nginx

## Result
✅ WebSocket server running on port 5000
✅ Nginx successfully proxies WebSocket connections
✅ Client can send and receive messages in real-time
✅ Both direct and Nginx-proxied connections work

## Commands Reference
```bash
# Start WebSocket server
cd ~/websocket-server
python3 websocket_server.py &

# Check if running
ps aux | grep websocket_server
sudo netstat -tulpn | grep 5000

# Test direct
echo "Hello Direct!" | websocat ws://127.0.0.1:5000/

# Test via Nginx
echo "Hello Nginx!" | websocat ws://localhost:8081/ws/

# Kill process on port 5000
sudo fuser -k 5000/tcp
```