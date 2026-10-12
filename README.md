# Building watsonx Orchestrate Agents with IBM Bob

Ten chapters, one fictional city, and a working citizen service at the end, built on IBM watsonx Orchestrate without writing a file by hand. You brief IBM Bob; Bob writes the Agents, the Tools, the documents and the tests, runs them on your instance, and shows you the result.

CivicPulse starts as an Agent that knows three phone numbers. By chapter 10 it reads the city's regulations, looks up permit applications, reports potholes to the 311 Call Center, understands "18 elm st", works as a team of four Agents, and answers residents on WhatsApp. Every chapter adds one component of the platform and one way of working with Bob. Every chapter was run as written, and the text keeps what Bob got wrong and the line of a prompt that put it right.

## What you will have built

| By the end of | CivicPulse can |
|---|---|
| Chapter 4 | Tell a resident which department handles their question, with contact and hours |
| Chapter 5 | Answer from the city's regulations: permits, waste sorting, noise, with the document named |
| Chapter 6 | Look up a permit application, a road repair or the collection day of a street |
| Chapter 7 | Report a pothole to the city's 311 Call Center, with the key kept out of the chat |
| Chapter 8 | Understand "18 elm st" through an address registry that Bob wrote as an MCP server |
| Chapter 9 | Route each question to the right department, one Agent per department behind a front desk |
| Chapter 10 | Answer on WhatsApp |

One component of watsonx Orchestrate per chapter: Agent, Knowledge Base, Tools, Connection, Toolkit, Collaborator Agents, Channel. And one thing about working with Bob per chapter: the three modes, the design you approve before anything is built, the prompts that carry what the platform needs to know, the tests Bob runs, the reasoning you read.

## How it works

You write prompts; Bob writes everything else. Each chapter follows the same three steps: in Ask mode, Bob says what it understood and what exists on your instance; in Plan mode, it writes a design that you read and approve; in Agent mode, it builds, imports, tests and reports. You approve each file and each command as it comes, and you deploy when the tests pass. Chapter 3 explains the method in twenty minutes; the chapters after it practise it.

## Who it is for

Anyone who has to build an Agent on watsonx Orchestrate: consultants, architects, developers, business analysts. No code is written by hand, so no coding experience is needed; if you have some, you will read what Bob writes and learn the platform faster. The guide uses Bob and the watsonx Orchestrate ADK extension as they ship; other assistants that connect to the watsonx Orchestrate ADK MCP server can follow the same steps, and chapter 2 says where their setup is described.

## What you need

- IBM Bob, 2.1 or later.
- A watsonx Orchestrate instance, or the Developer Edition on your machine (chapter 10 and the deployments need an instance).
- Git, which Bob uses for you.
- A phone with WhatsApp, for chapter 10.
- About eight hours, one chapter per sitting.

## Start here

1. Clone this repository and open it in Bob. The repository is your project folder: Bob writes into it, and git keeps your work.
2. Do chapter 2: it installs the ADK, connects Bob to your instance, and prepares the folder. Thirty minutes.
3. Read chapter 3, then build your first Agent in chapter 4.

You can also start at any chapter from 5 on: the files of the earlier chapters are in `walkthroughs`, with one instruction to Bob that imports them.

## The chapters

- [Introduction](guide/00-introduction.md): who the guide is for, what you need, the conventions.
- [Chapter 1. What you will build](guide/01-what-you-will-build.md)
- [Chapter 2. Connect Bob to watsonx Orchestrate](guide/02-connect-your-assistant.md)
- [Chapter 3. How to work with Bob](guide/03-how-to-brief-your-assistant.md)
- [Chapter 4. Your first Orchestrate Agent](guide/04-your-first-agent.md)
- [Chapter 5. Adding an Orchestrate Knowledge Base (RAG)](guide/05-knowledge-base.md)
- [Chapter 6. Adding Orchestrate Tools](guide/06-tools.md)
- [Chapter 7. Reporting an issue: Orchestrate Connections](guide/07-connections.md)
- [Chapter 8. An address lookup from an MCP server: Orchestrate Toolkits](guide/08-mcp-toolkit.md)
- [Chapter 9. One Agent per department: Collaborator Agents](guide/09-collaborators.md)
- [Chapter 10. CivicPulse on WhatsApp: the Orchestrate Channel](guide/10-whatsapp-channel.md)

## What is in this repository

```
guide/            the chapters, in reading order
walkthroughs/     the files each chapter produces (ch04 to ch10), to start at any chapter
.env.example      the model for your local .env file: the instance URL, the API key, the test keys of chapters 7 and 10
.gitignore        keeps .env, Bob's settings and the Python environment out of git
```

When you work through the chapters, Bob and the ADK extension add their own folders next to these: `agents`, `tools`, `knowledge-bases`, `connections`, `toolkits`, `models`, `design`, `scripts`, `tests`, `exports`. They are yours; commit them as the chapters say.

## Versions

Written and tested with watsonx Orchestrate ADK 2.18.0 and IBM Bob 2.1, on an instance on IBM Cloud, in September and October 2026. The platform and Bob change with their versions; if a step reads differently on yours, open an issue with the chapter, the section, what you sent and what you got.

Daniel Lopez Sainz, IBM Customer Success, France
