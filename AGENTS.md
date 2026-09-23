# Working on this project

Owner: Daniel Lopez Sainz, IBM. Last reviewed: 2026-09-17.

This folder is a watsonx Orchestrate project. The assistant reading this file builds, tests and maintains Orchestrate agents for the person working here, through the Orchestrate tools that are connected to it. Read this file first in every conversation; the phase files under `.bob/` add the rules for the current phase.

## What is in this folder

- `agents/` agent definitions (YAML), one file per agent, file name equals the agent name.
- `tools/` Python tools (one tool per file, file name equals the tool name) and OpenAPI documents. A tool that needs more than one file lives in its own subfolder.
- `knowledge-bases/` knowledge base definitions and the documents they index.
- `models/` model and model policy definitions, rarely needed.
- `connections/` connection definitions (never credentials).
- `toolkits/` MCP server folders for toolkits.
- `design/` design documents written in Plan mode, one per agent project.
- `exports/` files exported from the instance for comparison or backup.
- `guide/` and `walkthroughs/` belong to the training guide this project comes from: the chapters, and the starting-state and finished files for each chapter. Read them when the user refers to a chapter; copy files from `walkthroughs/` into the working folders only when a chapter or the user says so; never write build output into them.
- `workspace_config.yaml`, `venv/` and `.bob/skills/` are created by the watsonx Orchestrate ADK extension when it initialises the workspace; leave them alone.

## How to work with the Orchestrate instance

Use the connected Orchestrate tools for every operation on the instance: listing, importing, exporting, chatting with agents, creating connections, adding toolkits, importing knowledge bases. Do not use the `orchestrate` command line for these unless the rules below say so.

Four operations are only available from the command line and always need the user's explicit go: deploying or undeploying an agent, adding or activating an environment, importing agent skills, running evaluations. Ask before each of them, show the exact command, and run it only after the user says yes.

Everything imported lands in the draft environment. Importing an artifact with an existing name replaces the draft in place with no warning: say "this will replace the existing X" and wait before doing it.

## Rules that apply in every mode

1. Verify after every change. After any import, creation or removal, run the matching list or status call and report what it shows. A success message alone does not count.
2. When testing an agent, always request the reasoning and read it. Report tool calls and tool results verbatim. Empty reasoning means no tool was called.
3. If an operation fails twice on something that should work, ask the user to restart the Orchestrate MCP server, then retry. Only after that fall back to the equivalent `orchestrate` command, and say which command you ran.
4. Never invent a tool name, a parameter or a command. If unsure of syntax or of a field, look it up in the Orchestrate documentation server first, then ask the user.
5. Never write a credential into a file or into a definition. For connections, create and configure the connection, then ask the user whether to set the values through you or from their own terminal.
6. Never remove anything without asking. Removing a toolkit strips its tools from every agent that used them.
7. Create files before importing them. Importing from a folder that does not exist yet fails and keeps failing until the server is restarted.

## Naming and defaults

- Names are lower case with underscores: `lumen_helpdesk_agent`, `get_order_status`. No spaces, no camel case, no generic words like "helper" or "assistant".
- Default model: `groq/openai/gpt-oss-120b`. Default style: `react_core`.
- An agent has at most ten tools and collaborators combined. Split into collaborators beyond that.
- Python tools: Google-style docstring with an `Args:` line per parameter and a typed `Returns:` line, full type hints, one file self-contained; sibling modules in a package are imported with absolute imports, never relative ones.
- Knowledge base documents: txt, pdf, docx, pptx, xlsx, csv or html. Not Markdown.

## Reporting

End every task with a short report: what was done, what was verified and how, what did not work and what you propose. Quote error messages exactly.
