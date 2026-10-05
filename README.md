# Building watsonx Orchestrate Agents with IBM Bob

A training guide for people who want to create Agents on IBM watsonx Orchestrate with IBM Bob, using Bob and the watsonx Orchestrate ADK extension as shipped. Other assistants that connect to the watsonx Orchestrate ADK MCP server can follow the same steps; chapter 2 points to their setup instructions.

The guide builds CivicPulse, a citizen services platform for the fictional City of Utopia, starting with a single question-answering Agent and ending with several Agents working together. Each chapter lists its level, its prerequisites and a checkpoint. Follow the chapters in sequence, or begin at any chapter whose prerequisites you meet.

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
- [Chapter 4. Your first Orchestrate Agent](guide/04-your-first-Agent.md)
- [Chapter 5. Adding an Orchestrate Knowledge Base (RAG)](guide/05-knowledge-base.md)
- [Chapter 6. Adding Orchestrate Tools](guide/06-Tools.md)

The guide was written and tested against watsonx Orchestrate ADK 2.16.1 and IBM Bob 2.1.

Daniel Lopez Sainz, IBM
