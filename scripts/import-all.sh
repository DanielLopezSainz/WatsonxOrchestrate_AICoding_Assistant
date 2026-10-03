#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

source venv/bin/activate

echo "==> Importing knowledge base city_regulations..."
(cd knowledge-bases && orchestrate knowledge-bases import -f city_regulations.yaml)

echo "==> Waiting for city_regulations to be ready..."
for i in $(seq 1 20); do
  STATUS=$(orchestrate knowledge-bases status -n city_regulations 2>/dev/null | grep -E "ready" | head -1 || true)
  if echo "$STATUS" | grep -q "True.*ready"; then
    echo "    city_regulations is ready."
    break
  fi
  if [ "$i" -eq 20 ]; then
    echo "ERROR: city_regulations did not reach ready status after 10 minutes." >&2
    exit 1
  fi
  echo "    Still indexing... (attempt $i/20, waiting 30s)"
  sleep 30
done

echo "==> Importing civic_info_agent..."
orchestrate agents import -f agents/civic_info_agent.yaml

echo "==> Done."
