# Docker Search (One Button, No Drama)

This is the advanced, optional path for open-source search.

# Docker Search (One Button, No Drama)

This is the “I want web search, but I don’t want to hand my queries to a third party” path. You run a local search service in Docker, the repo points to it, and you get a more private and controllable setup. It’s optional, it’s powerful, and yes, it occasionally behaves like Docker.

This doc exists so you can get the benefit without the usual container spelunking. The goal is: start it, verify it, run a query, and know exactly what to do when port 8080 is taken or Docker Desktop decides it’s on a lunch break.

## Overview

Docker search is a local web-search backend. It only matters if you’ve enabled web search and you want the provider to be Docker instead of an API.

The “happy path” looks like this:
- start Docker Desktop
- run the one-button script
- set your web provider to docker
- query again and check results

When it works, it feels boring. That’s the point.

When it doesn’t work, it’s usually one of three things:
- Docker isn’t running
- the port is already in use
- the container is in a weird state and needs a reset

This doc shows you how to diagnose which one you hit and get back to boring.

---

## Steps

### Step 1: Install Docker Desktop
- Download Docker Desktop (macOS or Windows)
- Install it (Mac: drag to Applications; Windows: run installer)
- Open Docker Desktop once and wait for it to finish starting

Verify:
```
open -a Docker  # macOS only
docker --version
docker ps
```

### Step 2: Run the one-button script
From the repo root:
```
chmod +x scripts/docker_search.sh
./scripts/docker_search.sh "why safe sucks"
```

The script creates a runtime config at `logs/searxng.settings.yml` with a
generated secret key.

### If port 8080 is in use
```
SEARXNG_PORT=8081 ./scripts/docker_search.sh "why safe sucks"
```

### Warnings and fixes
- If the container is stuck restarting:
  ```
  docker rm -f searxng
  ```
- If you see "Connection refused": wait a few seconds and rerun the script.
- If Docker feels like too much, use API search instead.
