# Chapter 1. What you will build

Level: beginner. Time: about 5 minutes of reading. Prerequisites: none.

## Overview

Creating an Agent in watsonx Orchestrate usually means writing definition files, Python functions and commands by hand. With IBM Bob, you describe what the Agent must do. Bob writes the files, sends them to your instance, and tests the result.

The system is CivicPulse, the citizen services platform of the fictional City of Utopia. Residents ask it which department handles their question, check the status of a permit, report a broken street light, and apply for a building permit. You start with one Orchestrate Agent that answers from a short list of facts. Chapter by chapter, you give it the city's regulations to search, Tools to look up data, a Connection to the city's 311 Call Center, a team of specialised Agents and a permit workflow. Chapter 11 puts it on the city's website.

At the end of the guide, you have built:

- A front desk Agent and three department Agents that work together.
- An Orchestrate Knowledge Base of city guides and regulations that the Agents search.
- Orchestrate Tools that read the status of requests and permits, and report new issues to an external system, through an Orchestrate Connection.
- An Orchestrate Flow for the permit application, with fixed steps and an approval by a city clerk.
- An Orchestrate Channel: a chat window that residents use on a web page.

If you already know watsonx Orchestrate and Bob, go to section 1.3 for the scenario and section 1.4 for the list of chapters.

## 1.1 The 2 main characters

IBM Bob and IBM watsonx Orchestrate are the two products of this guide, each with a different job.

| Product | What it is | Its job in this guide |
|---|---|---|
| IBM watsonx Orchestrate | A platform that runs AI agents. An Orchestrate Agent answers questions and performs tasks for its users, using instructions, documents, and Connections to other systems | The Agents that you create run here. Your copy of the platform is called an instance: a SaaS tenant, or the Developer Edition on your own machine |
| IBM Bob | An AI coding assistant that works inside a development environment. You describe what you want in a chat; Bob writes the files, runs the operations, and reports the result | You create the Agents here. You do not write code or configuration files by hand |

Chapter 2 installs the watsonx Orchestrate ADK extension for Bob. That extension connects the two products, so Bob can list what exists on your instance, send new Agents to it, and test them.

## 1.2 What an Orchestrate Agent is made of

An Orchestrate Agent is built from a small set of components. Each component is an Orchestrate asset with its own type, named with a capital in this guide.

| Component | What it is |
|---|---|
| Instructions | The text that defines the Agent: its role, the facts it knows, how it answers, and what it must not do |
| Model | The language model that the Agent runs on. The guide uses the default model of the instance. Each Agent can use a different model |
| Orchestrate Knowledge Base | A set of documents that the Agent searches when a question needs more information than its instructions hold |
| Orchestrate Tools | Functions that the Agent calls to look up data or to perform an action |
| Orchestrate Connections | The addresses and credentials of the external systems that Tools use |
| Orchestrate Toolkits | Groups of Tools provided by an external server and attached to the Agent as a set |
| Collaborator Agents | Other Orchestrate Agents that an Agent delegates to, so that each Agent has a clear purpose |
| Orchestrate Flows | Fixed sequences of steps that run the same way every time |
| Orchestrate Channels | The interfaces through which users reach an Agent, such as a chat window on a web page |

Everything that you create stays in the Draft environment of the instance, where only you can use it, until you deploy it to Live, where its users reach it.

## 1.3 The scenario

CivicPulse, the citizen services platform of the City of Utopia, is the one system that the guide builds from start to finish. Each component of an Orchestrate Agent gets a use in that scenario: regulations to search, a permit status to look up, a 311 Call Center to report to, departments to route between.

The city, its departments, its residents and all its data are fictional; three departments are used throughout the guide:

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
| 8 | Add an address lookup provided by an external server | Orchestrate Toolkit | Bob's skill for building an MCP server |
| 9 | Split the work between a front desk Agent and one Agent per department | Collaborator Agents | Plan mode for a design with several Agents |
| 10 | Add a permit application that follows fixed steps | Orchestrate Flow | Agent mode on a build with several steps |
| 11 | Make CivicPulse available to residents on the city's website | Re-deployment after changes, and the Orchestrate Channel for web chat | The deployment approval |
| 12 | Add a new department, Parks and Events, without step-by-step help | All of the above | The Orchestrate skills |

From chapter 4 onwards, each chapter opens with an overview that says what is built and whether you can skip it, states its prerequisites, lists its steps, and ends with questions to check the result. The files that each chapter produces are in the `walkthroughs` folder of the repository, so that you can start at any chapter.
