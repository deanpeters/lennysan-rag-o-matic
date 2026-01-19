#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: ./scripts/docker_search.sh \"your question here\""
  exit 1
fi

QUERY="$*"

echo "Starting Docker search for: $QUERY"

if [ ! -f "./explore.py" ]; then
  echo "Run this from the repo root (where explore.py lives)."
  exit 1
fi

if [ -x "./.venv/bin/python" ]; then
  PYTHON_BIN="./.venv/bin/python"
else
  PYTHON_BIN="python"
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed. Install Docker Desktop and start it once."
  exit 1
fi

if ! docker ps >/dev/null 2>&1; then
  echo "Docker is installed but not running."
  echo "Start Docker Desktop, then rerun this command."
  echo "  macOS: open -a Docker"
  echo "  Windows: open Docker Desktop"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SETTINGS_TEMPLATE="$SCRIPT_DIR/searxng/settings.yml"
RUNTIME_SETTINGS="./logs/searxng.settings.yml"
PORT="${SEARXNG_PORT:-8080}"
BASE_URL="http://localhost:${PORT}"

if [ ! -f "$RUNTIME_SETTINGS" ]; then
  mkdir -p ./logs
  cp "$SETTINGS_TEMPLATE" "$RUNTIME_SETTINGS"
  SECRET_KEY="$("$PYTHON_BIN" - <<'PY'
import secrets
print(secrets.token_hex(16))
PY
)"
  {
    echo ""
    echo "server:"
    echo "  limiter: false"
    echo "  secret_key: \"${SECRET_KEY}\""
  } >> "$RUNTIME_SETTINGS"
fi

if docker ps -a --format '{{.Names}}' | grep -q '^searxng$'; then
  EXISTING_PORT="$(docker inspect -f '{{(index (index .NetworkSettings.Ports "8080/tcp") 0).HostPort}}' searxng 2>/dev/null || true)"
  if [ -n "$EXISTING_PORT" ] && [ "$EXISTING_PORT" != "$PORT" ]; then
    echo "Existing searxng container uses port $EXISTING_PORT. Recreating on $PORT..."
    docker rm -f searxng >/dev/null
  else
    HAS_SETTINGS="$(docker inspect -f '{{range .Mounts}}{{.Source}} {{.Destination}}{{"\n"}}{{end}}' searxng 2>/dev/null | grep -q "$RUNTIME_SETTINGS /etc/searxng/settings.yml" && echo yes || echo no)"
    if [ "$HAS_SETTINGS" = "no" ]; then
      echo "Existing searxng container is missing the settings mount. Recreating..."
      docker rm -f searxng >/dev/null
    fi
  fi
fi

if ! docker ps --format '{{.Names}}' | grep -q '^searxng$'; then
  if docker ps -a --format '{{.Names}}' | grep -q '^searxng$'; then
    docker start searxng >/dev/null
  else
    echo "Starting searxng container..."
    docker run -d --name searxng -p "${PORT}:8080" --restart unless-stopped \
      -v "$RUNTIME_SETTINGS:/etc/searxng/settings.yml:rw" \
      searxng/searxng >/dev/null
  fi
fi

# Wait for SearXNG to respond with JSON (up to ~30s)
URL="${BASE_URL}/search?q=ping&format=json"
STATUS="000"
for _ in $(seq 1 30); do
  STATUS="$(curl -s -o /dev/null -w "%{http_code}" \
    -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
    -H "Accept: application/json,text/plain,*/*" \
    -H "Accept-Language: en-US,en;q=0.9" \
    -H "Referer: ${BASE_URL}/" \
    -H "X-Forwarded-For: 127.0.0.1" \
    -H "X-Real-IP: 127.0.0.1" \
    "$URL" || true)"
  if [ "$STATUS" = "200" ]; then
    break
  fi
  sleep 1
done

if [ "$STATUS" != "200" ]; then
  echo "SearXNG is not ready yet (HTTP $STATUS). Continuing anyway..."
  echo "If web search fails, try rerunning the script after it fully starts."
  echo "To reset the container:"
  echo "  docker rm -f searxng"
  echo "To inspect logs:"
  echo "  docker logs searxng | tail -n 40"
fi

echo "Running explore.py with Docker search..."
SEARXNG_ENDPOINT="$BASE_URL" "$PYTHON_BIN" explore.py --web-search always --web-provider docker "$QUERY"
