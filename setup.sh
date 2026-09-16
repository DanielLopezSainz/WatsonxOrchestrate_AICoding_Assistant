#!/usr/bin/env bash
# Prepares this folder as a watsonx Orchestrate project for a coding assistant.
# Run it from inside the folder: bash setup.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

echo "Project folder: $HERE"

echo "1. Checking the ADK and the MCP server are installed..."
if ! command -v orchestrate >/dev/null 2>&1; then
  echo "   orchestrate not found. Install with: pip install --upgrade ibm-watsonx-orchestrate ibm-watsonx-orchestrate-mcp-server"; exit 1
fi
if ! command -v ibm-watsonx-orchestrate-mcp-server >/dev/null 2>&1; then
  echo "   ibm-watsonx-orchestrate-mcp-server not found. Install with: pip install --upgrade ibm-watsonx-orchestrate-mcp-server"; exit 1
fi
VERSION_LINE="$(orchestrate --version 2>/dev/null | grep -m1 "ADK Version" || true)"
echo "   ${VERSION_LINE:-ADK version could not be read}"

echo "2. Checking an Orchestrate environment is active..."
ACTIVE_LINE="$(orchestrate env list 2>/dev/null | grep -E '\(active\)' || true)"
if [ -n "$ACTIVE_LINE" ]; then echo "   $ACTIVE_LINE"; else echo "   No active environment. Run: orchestrate env activate <name> --api-key <key>"; fi

echo "3. Connection settings..."
write_if_missing() {
  local template="$1" target="$2" label="$3"
  if [ -f "$target" ]; then
    echo "   $target already exists ($label), left unchanged"
  else
    sed "s|__PROJECT_FOLDER__|$HERE|g" "$template" > "$target"
    echo "   $target written ($label)"
  fi
}
write_if_missing "$HERE/.bob/mcp.json.template"    "$HERE/.bob/mcp.json"    "IBM Bob"
write_if_missing "$HERE/.mcp.json.template"        "$HERE/.mcp.json"        "Claude Code"
write_if_missing "$HERE/.cursor/mcp.json.template" "$HERE/.cursor/mcp.json" "Cursor"
write_if_missing "$HERE/.vscode/mcp.json.template" "$HERE/.vscode/mcp.json" "VS Code Copilot"

echo "4. Adding the read-only pre-approval list to the Bob entry, if it is missing..."
python3 - "$HERE" <<'PY'
import json, sys, os
here = sys.argv[1]
path = os.path.join(here, ".bob", "mcp.json")
tpl = json.load(open(os.path.join(here, ".bob", "mcp.json.template")))
allow = tpl["mcpServers"]["watsonx-orchestrate-adk"]["alwaysAllow"]
cfg = json.load(open(path))
entry = cfg.get("mcpServers", {}).get("watsonx-orchestrate-adk")
if entry is None:
    print("   no watsonx-orchestrate-adk entry in .bob/mcp.json; nothing to do")
elif entry.get("alwaysAllow"):
    print("   alwaysAllow already present, left unchanged")
else:
    entry["alwaysAllow"] = allow
    json.dump(cfg, open(path, "w"), indent=2)
    print("   alwaysAllow added with", len(allow), "read-only tools")
wd = (entry or {}).get("env", {}).get("WXO_MCP_WORKING_DIRECTORY")
if wd and os.path.realpath(wd) != os.path.realpath(here):
    print("   WARNING: the Bob entry's working directory is", wd)
    print("            but this folder is", here, "; file operations will be refused until they match")
PY

echo "Done. Open this folder as the workspace in your assistant and restart its MCP servers."
