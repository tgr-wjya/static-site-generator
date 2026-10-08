python3 src/main.py
if command -v fuser >/dev/null 2>&1; then
  fuser -k 8888/tcp >/dev/null 2>&1 || true
fi
cd public && python3 -m http.server 8888