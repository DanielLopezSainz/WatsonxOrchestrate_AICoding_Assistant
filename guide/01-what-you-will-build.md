# Chapter 1. What you will build

Level: beginner. Time: about 5 minutes of reading. Prerequisites: none.

## Overview

Creating an Agent in watsonx Orchestrate the traditional way means writing definition files, Python functions and commands by hand. With IBM Bob, you describe what the Agent must do in natural language. Bob performs the development for you, sends the code to your Orchestrate instance, and tests the result to confirm that the AI Agent works as expected.

In this guide you build the agentic application CivicPulse for the City of Utopia. Residents ask CivicPulse questions such as:

- Which department handles a dark street light?
- Do I need a permit for a garden shed?
- When is the green bin collected on my street?
- What is the status of my permit application?

A resident asks, CivicPulse answers, and when something has to be done, such as reporting a pothole, it does it. You start in chapter 4 with one Agent that knows three phone numbers. Chapter by chapter you make it grow:

- The city's regulations, to search and quote.
- Tools that look up records: a permit application, a road repair, the collection days of a street.
- A Connection to the city's 311 Call Center, to report problems.
- An address registry, so that "18 elm st" is understood.
- A team of specialised Agents, one per department.
- A WhatsApp number.

At the end of chapter 10, you have built:

- A front desk Agent and three department Agents that work together.
- An Orchestrate Knowledge Base of city guides and regulations that the Agents search.
- Orchestrate Tools that read the status of requests and permits, and report new issues to an external system, through an Orchestrate Connection.
- An Orchestrate Channel: a WhatsApp number for CivicPulse.

If you already know watsonx Orchestrate and Bob, go to section 1.3 for the scenario and section 1.4 for the list of chapters.

## 1.1 The 2 main characters

This guide uses IBM Bob and IBM watsonx Orchestrate.

| Product | What it is | Its job in this guide |
|---|---|---|
| IBM watsonx Orchestrate | A platform that runs AI agents. An Orchestrate Agent answers questions and performs tasks for its users, using instructions, documents, and Connections to other systems | The Agents that you create run here. Your copy of the platform is called an instance: a SaaS tenant, or the Developer Edition on your own machine |
| IBM Bob | An AI coding assistant that works inside a development environment. You describe what you want in a chat; Bob writes the files, runs the operations, and reports the result | You create the Agents here. You do not write the Agent, Tool or Knowledge Base files by hand |

Chapter 2 installs the watsonx Orchestrate ADK extension for Bob. That extension connects the two products, so Bob can list what exists on your instance, send new Agents to it, and test them.

## 1.2 What an Orchestrate Agent is made of

An Orchestrate Agent is built from a small set of components. Several of them are Orchestrate assets with a type of their own, named with a capital in this guide.

| Component | What it is |
|---|---|
| Instructions | The text that defines the Agent: its role, the facts it knows, how it answers, and what it must not do |
| Model | The language model that the Agent runs on. The guide uses the default model of the instance. Each Agent can use a different model |
| Orchestrate Knowledge Base | A set of documents that the Agent searches when a question needs more information than its instructions hold |
| Orchestrate Tools | Functions that the Agent calls to look up data or to perform an action |
| Orchestrate Connections | The addresses and credentials of the external systems that Tools use |
| Orchestrate Toolkits | Groups of Tools provided by an external server and attached to the Agent as a set |
| Collaborator Agents | Other Orchestrate Agents that an Agent delegates to, so that each Agent has a clear purpose |
| Orchestrate Flows | Sequences of steps defined in advance, with branches where needed, instead of decided by the model at each question |
| Orchestrate Channels | The interfaces through which users reach an Agent, such as WhatsApp or a chat window on a web page |

An Agent that you create stays in the Draft environment of the instance, where only builders can use it, until you deploy it to Live, where its users reach it.

## 1.3 The scenario

CivicPulse, the citizen services platform of the City of Utopia, is the one system that the guide builds from start to finish. Each component of an Orchestrate Agent has a job in that scenario: regulations to search, a permit status to look up, a 311 Call Center to report to, departments to route questions between.

The city, its departments, its residents and all its data are fictional. The guide uses these departments:

| Department | What it handles |
|---|---|
| Permits and Planning | Building permits and planning applications |
| Roads and Infrastructure | Potholes, street lights, damaged signs, urgent hazards on public roads |
| Waste and Recycling | Collection days, bulky item collection, recycling rules |

## 1.4 The chapters

| Chapter | What you do | Orchestrate component | Bob capability |
|---|---|---|---|
| 2 | Connect Bob to your watsonx Orchestrate instance | The instance and its environments | The extension, the views, the approvals |
| 3 | Learn the working method | None | The Ask, Plan and Agent modes; prompts; git |
| 4 | Create an Orchestrate Agent that tells residents which department to contact, and deploy it in Live | Instructions and model; the Draft and Live environments | The three modes in sequence |
| 5 | Give the Agent the city's guides and regulations | Orchestrate Knowledge Base | Bob writes the documents |
| 6 | Let the Agent look up the status of a request or a permit | Orchestrate Tools | Bob writes the Tools; reading the Agent's reasoning |
| 7 | Let the Agent report a new issue to the city's 311 Call Center | Orchestrate Connections | Credentials kept out of the chat |
| 8 | Add an address lookup provided by an MCP server | Orchestrate Toolkit | Bob builds the MCP server and tests it before the platform does |
| 9 | Split the work between a front desk Agent and one Agent per department | Collaborator Agents | Plan mode for a design with several Agents |
| 10 | Give CivicPulse a WhatsApp number | Orchestrate Channel | A structured prompt for a task in Agent mode, without a design |

From chapter 4 onwards, each chapter has an overview with a skip note, prerequisites, steps, tests and a summary, and chapters 4 to 9 end with a deployment. The files that each chapter produces are in the `walkthroughs` folder of the repository, so that you can start at any chapter.
