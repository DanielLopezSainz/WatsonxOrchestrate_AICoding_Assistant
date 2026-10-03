#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

source venv/bin/activate

echo "==> Removing civic_info_agent..."
orchestrate agents remove -n civic_info_agent --kind native || true

echo "==> Removing knowledge base city_regulations..."
orchestrate knowledge-bases remove -n city_regulations || true

echo "==> Done."
