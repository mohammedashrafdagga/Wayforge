#!/usr/bin/env bash
# scaffold_project.sh — Wayforge greenfield scaffolding.
#
# Usage:
#   scaffold_project.sh --root <path> --scope backend|frontend|both \
#       [--backend-framework fastapi] [--frontend-framework react-vite] [--project-name <name>]
#
# Only understands the default stack (FastAPI / React+Vite). If the user picked a
# non-default framework at `wayforge init`, the skill handles that override itself and
# should not call this script for the overridden side — it scaffolds the default
# side only and leaves the rest to the calling skill's own instructions.
#
# Exits non-zero and prints to stderr on any failure; never leaves a half-scaffolded
# side without saying so explicitly.

set -euo pipefail

ROOT=""
SCOPE=""
BACKEND_FRAMEWORK="fastapi"
FRONTEND_FRAMEWORK="react-vite"
PROJECT_NAME="app"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root) ROOT="$2"; shift 2 ;;
    --scope) SCOPE="$2"; shift 2 ;;
    --backend-framework) BACKEND_FRAMEWORK="$2"; shift 2 ;;
    --frontend-framework) FRONTEND_FRAMEWORK="$2"; shift 2 ;;
    --project-name) PROJECT_NAME="$2"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$ROOT" || -z "$SCOPE" ]]; then
  echo "usage: scaffold_project.sh --root <path> --scope backend|frontend|both [--project-name <name>]" >&2
  exit 1
fi

mkdir -p "$ROOT"

scaffold_backend() {
  if [[ "$BACKEND_FRAMEWORK" != "fastapi" ]]; then
    echo "scaffold_project.sh only scaffolds the default backend (fastapi); requested '$BACKEND_FRAMEWORK' — skipping, calling skill must scaffold this itself" >&2
    return 0
  fi

  local backend_dir="$ROOT/backend"
  mkdir -p "$backend_dir/src/shared" "$backend_dir/tests"
  cd "$backend_dir"

  if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 not found on PATH — cannot scaffold backend" >&2
    exit 1
  fi

  python3 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install --quiet --upgrade pip
  pip install --quiet fastapi "uvicorn[standard]" sqlalchemy pydantic-settings pytest httpx

  pip freeze > requirements.txt

  cat > src/main.py <<'PYEOF'
from fastapi import FastAPI

app = FastAPI(title="Wayforge app")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
PYEOF

  touch src/__init__.py

  deactivate
  echo "backend scaffolded at $backend_dir"
}

scaffold_frontend() {
  if [[ "$FRONTEND_FRAMEWORK" != "react-vite" ]]; then
    echo "scaffold_project.sh only scaffolds the default frontend (react-vite); requested '$FRONTEND_FRAMEWORK' — skipping, calling skill must scaffold this itself" >&2
    return 0
  fi

  if ! command -v npm >/dev/null 2>&1; then
    echo "npm not found on PATH — cannot scaffold frontend" >&2
    exit 1
  fi

  cd "$ROOT"
  npm create vite@latest frontend -- --template react-ts
  cd frontend
  npm install
  mkdir -p src/features src/shared src/app
  echo "frontend scaffolded at $ROOT/frontend"
}

case "$SCOPE" in
  backend) scaffold_backend ;;
  frontend) scaffold_frontend ;;
  both) scaffold_backend; scaffold_frontend ;;
  *) echo "invalid --scope: $SCOPE (expected backend|frontend|both)" >&2; exit 1 ;;
esac

echo "scaffold complete for scope=$SCOPE at $ROOT"
