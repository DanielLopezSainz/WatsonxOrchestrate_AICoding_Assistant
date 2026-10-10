# Building watsonx Orchestrate Agents with IBM Bob

A hands-on guide to creating AI agents on IBM watsonx Orchestrate with IBM Bob, IBM's AI coding assistant. You describe what the Agent must do; Bob writes the definitions, the Tools and the tests, sends them to your instance, and reports what happened. You read, decide and approve.

Across twelve chapters you build CivicPulse, the citizen services platform of the fictional City of Utopia. The first Agent tells residents which department to call about a dark street light. By the last chapter, a team of Agents searches the city's regulations, looks up permit applications, reports potholes to the 311 Call Center, takes a permit application through its steps, and answers residents from a chat window on the city's website. Each chapter adds one component of watsonx Orchestrate. Every chapter was run, as written, with Bob on a real instance.

The guide is for people who build Orchestrate Agents, with or without coding experience, and for anyone who wants to see how an AI coding assistant changes that work. Each chapter states its level and its prerequisites, so that you can follow the chapters in order or start at the one you need. The guide uses Bob and the watsonx Orchestrate ADK extension as shipped; other assistants that connect to the watsonx Orchestrate ADK MCP server can follow the same steps, and chapter 2 points to their setup instructions.

## How this repository is organised

To use this guide, clone this repository, which is also the project folder you work in, open it in IBM Bob, and complete the setup steps in chapter 2.

- `guide/` contains the chapters, in reading order.
- `walkthroughs/` contains the files that each chapter produces, and the starting state for the chapters that build on earlier ones.
- `agents/`, `tools/`, `connections/`, `knowledge-bases/`, `toolkits/` and `models/` are working folders, created by the watsonx Orchestrate ADK extension when you initialise the project in chapter 2.
- `design/` is a working folder, created by Bob when it writes the first design.
- `.env.example` is the model for the local `.env` file that chapter 2 asks you to create; git ignores `.env`.

## Where to start

To connect your assistant to watsonx Orchestrate, start with chapter 2. Read chapter 3 before creating Agents or Tools; it defines the three-phase workflow that every later chapter follows.

## Chapters

- [Chapter 1. What you will build](guide/01-what-you-will-build.md)
- [Chapter 2. Connect Bob to watsonx Orchestrate](guide/02-connect-your-assistant.md)
- [Chapter 3. How to work with Bob](guide/03-how-to-brief-your-assistant.md)
- [Chapter 4. Your first Orchestrate Agent](guide/04-your-first-agent.md)
- [Chapter 5. Adding an Orchestrate Knowledge Base (RAG)](guide/05-knowledge-base.md)
- [Chapter 6. Adding Orchestrate Tools](guide/06-tools.md)
- [Chapter 7. Reporting an issue: Orchestrate Connections](guide/07-connections.md)
- [Chapter 8. An address lookup from an MCP server: Orchestrate Toolkits](guide/08-mcp-toolkit.md)
- [Chapter 9. One Agent per department: Collaborator Agents](guide/09-collaborators.md)

The guide was written and tested against watsonx Orchestrate ADK 2.16.1 and IBM Bob 2.1.

IBM CSM Team, France
