# Introduction

Building watsonx Orchestrate Agents with IBM Bob. IBM CSM Team, France. Written and tested in September and October 2026 with IBM Bob 2.1, the watsonx Orchestrate ADK 2.18.0 and a watsonx Orchestrate instance on IBM Cloud, on macOS.

## Who this guide is for

For anyone who has to build an Agent on watsonx Orchestrate: a consultant, an architect, a developer, or a business analyst who has never written a line of code. Bob writes the files; you describe, read, decide and approve. A reader with coding experience reads the same files and understands the platform faster; a reader without it follows the chapters as they are.

At the end, you have built a working city service with every component the platform offers to an Agent, and you know how to brief Bob for the next one.

## What you need

| | Why |
|---|---|
| IBM Bob 2.1 or later, installed | The assistant that writes and runs everything |
| A watsonx Orchestrate instance, or the Developer Edition on your machine | Where the Agents live. Chapter 2 connects Bob to it |
| Git, installed | Bob uses it to clone the repository and to save your work; you type no git command |
| A phone with WhatsApp | Chapter 10 only |
| About eight hours | The ten chapters, at their stated times; each one fits in a working session |

Chapter 10 and the deployments at the end of chapters 4 to 9 need an instance; on the Developer Edition, the chapters say what to skip.

## How to read it

The chapters build on each other, in order: chapter 2 connects Bob to your instance, chapter 3 gives the way of working, and chapters 4 to 10 add one component each to the same Agent. Every chapter from chapter 4 opens with a skip note: the files of the previous chapters are in the `walkthroughs` folder of the repository, with one instruction to Bob that imports them, so that you can start at the chapter you need. Chapter 3 has a reading table for those who know the platform or Bob already.

Each chapter states its level, its time and its prerequisites in its first line, and ends with a summary of what was built and what to keep in mind.

## Conventions

- A prompt for Bob is in a code block. Send it whole, as it is; the chapter says in which mode and whether in a new conversation.
- "Mode: Ask, in a new conversation." before a prompt says the mode and the conversation.
- "Look for these points in Bob's answer:" lists what the answer must contain; "You should see:" describes the screen after a step.
- "Approve each request as it comes." means that Bob asks for approval before writing a file or running a command, and that you approve each one.
- "Save your work:" gives the instruction that commits the chapter's files.
- A paragraph that starts with IMPORTANT is a rule that holds for the rest of the guide.
- The types of Orchestrate assets are capitalised in the text (an Agent, a Tool, a Knowledge Base, a Connection, a Toolkit, a Channel); in prompts and files they are written as Bob and the platform write them, in lowercase.
- `Ask civic_info_agent:` in front of a question sends it to the Agent through Bob.

## The repository

The guide is this repository: the chapters in `guide`, the files of each chapter in `walkthroughs`, the README with the chapter list. It is also the project folder you work in with Bob, as chapter 2 explains. The `.env.example` file lists the values that stay on your machine, never in the repository or in a chat.

## Reporting a problem

The platform and Bob change with their versions, and a step that worked when the guide was written may read differently on yours. Open an issue in the repository with the chapter, the section, what you sent and what you got; the guide is corrected from those reports.
