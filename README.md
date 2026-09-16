# Building watsonx Orchestrate agents with an AI coding assistant

A training guide for people who want to create agents on IBM watsonx Orchestrate by working with an AI coding assistant rather than by hand. The guide is written for IBM Bob, and every step works with any assistant that can connect to the watsonx Orchestrate ADK MCP server: Cursor, VS Code with Copilot, Claude Code or Claude Desktop.

The chapters follow one fictional company, Lumen Logistics, from a first question-answering agent to a multi-agent solution, one working session at a time. Each chapter states its level, its prerequisites and a checkpoint, so that readers with experience can start at the chapter they need.

## How this repository is organised

This repository is also the project folder you work in. Clone it, open it in your assistant, and follow chapter 2 to connect it to your Orchestrate instance.

- `guide/` the chapters, in reading order.
- `walkthroughs/` the files each chapter produces, and the starting state for chapters that build on earlier ones.
- `AGENTS.md` the instructions the assistant follows in this project, and `.bob/`, `.cursor/`, `.github/`, `CLAUDE.md` the same rules for each assistant. Chapter 2 explains them; nothing in them needs editing.
- `agents/`, `tools/`, `knowledge-bases/`, `connections/`, `toolkits/`, `models/`, `design/`, `exports/` the working folders, empty until you build something.
- `setup.sh` a script chapter 2 runs once to complete the connection settings.

## Where to start

Read chapter 2 first if you want to see the assistant talk to your instance within half an hour. Read chapter 3 before building anything; it explains how the assistant is briefed in three phases, and it is the part most people get wrong at first.

Chapters available so far:

- `guide/02-connect-your-assistant.md`
- `guide/03-how-to-brief-your-assistant.md`
- `guide/04-your-first-agent.md`

The guide was written and tested against watsonx Orchestrate ADK 2.16.1 and IBM Bob 2.1.

Daniel Lopez Sainz, IBM
