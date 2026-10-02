# Chapter 1. What you will build

Level: beginner. Time: about 10 minutes of reading. Prerequisites: none.

## Overview

Creating an agent in watsonx Orchestrate usually means writing definition files, Python functions and commands by hand. With IBM Bob, you describe what the agent must do, and Bob writes the files, sends them to your instance, and tests the result. This guide teaches that way of working, from a first agent to a complete system.

The system is CivicPulse, the citizen services platform of the fictional City of Utopia. Residents ask it which department handles their question, check the status of a permit, report a pothole, and apply for a building permit. You start with one agent that answers from a short list of facts. Chapter by chapter, you give it the city's regulations to search, tools to look up data, a connection to the city's service desk, a team of specialised agents and a permit workflow. In the last step, you put it on the city's website.

At the end of the guide, you have built:

- A front desk agent and three department agents that work together.
- A knowledge base of city guides and regulations that the agents search.
- Tools that read the status of requests and permits, and report new issues to an external system.
- A permit application that follows fixed steps, with an approval by a city clerk.
- A chat window that residents use on a web page.

You write prompts. Bob writes the code.

This chapter introduces the two products, the scenario and the chapters. If you already know watsonx Orchestrate and Bob, go to section 1.3 for the scenario and section 1.4 for the list of chapters.

## 1.1 The two products

The guide uses two IBM products. Each one has a different job.

| Product | What it is | Its job in this guide |
|---|---|---|
| IBM watsonx Orchestrate | A platform that runs AI agents. An agent answers questions and performs tasks for its users, using instructions, documents, and connections to other systems | The agents that you create run here. Your copy of the platform is called an instance: a SaaS tenant, or the Developer Edition on your own machine |
| IBM Bob | An AI coding assistant that works inside a development environment. You describe what you want in a chat; Bob writes the files, runs the operations, and reports the result | You create the agents here. You do not write code or configuration files by hand |

The two products are connected by the watsonx Orchestrate ADK extension for Bob, which chapter 2 installs. With the extension, Bob can list what exists on your instance, send new agents to it, and test them.

## 1.2 What an agent is made of

An agent in watsonx Orchestrate is defined by a small set of components. The guide starts with the first two and adds one component per chapter.

| Component | What it is |
|---|---|
| Instructions | Text that tells the agent what it does, how it answers, and what it must not do |
| Model | The language model that the agent runs on. The guide uses the default model of the instance. Each agent can use a different model |
| Knowledge base | A set of documents that the agent searches when a question needs more information than its instructions hold |
| Tools | Functions that the agent calls to look up data or to perform an action |
| Connections | The addresses and credentials of the external systems that tools use |
| MCP toolkits | Groups of tools provided by an external server and attached to the agent as a set |
| Collaborator agents | Other agents that an agent delegates to, so that each agent has a clear purpose |
| Flows | Fixed sequences of steps that run the same way every time |

Everything that you create is stored first in the draft environment of the instance, where only you can use it. Deployment makes an agent available to its users. A channel, such as a chat window on a web page, is how users reach a deployed agent.

## 1.3 The scenario

The guide builds one system from start to finish: CivicPulse, the citizen services platform of the City of Utopia. Residents use CivicPulse to find out which city department handles their question, to check the status of a request or a permit, to report a problem, and to apply for a permit.

The city, its departments, its residents and all its data are fictional. Three departments are used throughout the guide:

| Department | What it handles |
|---|---|
| Permits and Planning | Building permits and planning applications |
| Roads and Infrastructure | Potholes, street lights, damaged signs, urgent hazards on public roads |
| Waste and Recycling | Collection days, bulky item collection, recycling rules |

The scenario was chosen because it needs no explanation, and because each component of an agent has an obvious use in it.

## 1.4 The chapters

Chapters 2 and 3 prepare the work. Chapters 4 to 11 each add one component to CivicPulse. Chapter 12 is an exercise that uses all of them.

| Chapter | What you do | Orchestrate component | Bob capability |
|---|---|---|---|
| 2 | Connect Bob to your watsonx Orchestrate instance | The instance and its environments | The extension, the views, the approvals |
| 3 | Learn the working method | None | The Ask, Plan and Agent modes; prompts; git |
| 4 | Create an agent that tells residents which department to contact | Instructions and model | The three modes in sequence |
| 5 | Give the agent the city's guides and regulations | Knowledge base | Bob writes the documents |
| 6 | Let the agent look up the status of a request or a permit | Tools | Bob writes the tools; reading the agent's reasoning |
| 7 | Let the agent report a new issue to the city service desk | Connections | Credentials kept out of the chat |
| 8 | Add an address lookup provided by an external server | MCP toolkit | Bob's skill for building an MCP server |
| 9 | Split the work between a front desk agent and one agent per department | Collaborator agents | Plan mode for a design with several agents |
| 10 | Add a permit application that follows fixed steps | Flow | Agent mode on a build with several steps |
| 11 | Make CivicPulse available to residents on the city's website | Deployment and the web chat channel | The deployment approval |
| 12 | Add a new department, Parks and Events, without step-by-step help | All of the above | The Orchestrate skills |

Each chapter from 4 onwards has the same structure: an overview that says what is built and who can skip the chapter, the prerequisites, the steps, and a set of questions to check the result. The files that each chapter produces are in the `walkthroughs` folder of the repository, so that you can start at any chapter.
