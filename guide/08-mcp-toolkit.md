# Chapter 8. An address lookup from an MCP server: Orchestrate Toolkits

Level: intermediate. Time: about 75 minutes. Prerequisites: chapter 7 completed, or its Tool, Connection and Agent imported from the walkthrough folder as that chapter's Overview describes.

## Overview

You send a message to CivicPulse: "The rubbish was not collected today at 18 elm st, which days do they collect it?". The Agent of chapter 7 has a Tool that knows the collection days of Elm Street, but the Tool does not find the street, because "18 elm st" is not how the city spells it. An Address Registry solves this: it receives an address as a resident types it and returns the official street name, the house number, the district and the postcode. In this chapter, Bob writes that Address Registry as an MCP server, with the ten streets of the Collection Calendar, and the Agent uses it.

MCP, the Model Context Protocol, is a standard way for a program to offer tools to AI Agents. You have used it since chapter 2: Bob reaches your instance through one MCP server and the Orchestrate documentation through another. In this chapter Bob builds an MCP server of its own, with its built-in capability for creating MCP servers, and connects to it to try its tools. Then watsonx Orchestrate imports a copy of the MCP server as an Orchestrate Toolkit, and the Agent gets its tools.

The Orchestrate Toolkit is the component introduced in this chapter. Bob's capability is the creation of MCP servers.

Skip this chapter if you have already imported an MCP server into watsonx Orchestrate with Bob. To continue with chapter 9 without building it, send Bob these instructions in Agent mode: `Import the MCP server in walkthroughs/ch08/toolkits/address_registry into my instance as a toolkit named address_registry, with all its tools, then import walkthroughs/ch08/agents/civic_info_agent.yaml.`

## 8.1 Before you start

- The setup from chapter 2, complete.
- The Agent `civic_info_agent` from chapter 7 on your instance, in Draft, with its four Tools and the Connection `utopia_311`. If you skipped chapter 7, import them as described in that chapter's Overview.
- In Bob's settings, MCP tab, the setting Enable MCP Server Creation switched on. It is on by default; when it is off, Bob does not know how to write an MCP server.
- A new conversation in Bob for this chapter.

Check that the Agent is there: in Ask mode, ask `Which tools does civic_info_agent have?` and confirm the four names, `get_permit_status`, `get_request_status`, `get_collection_days` and `report_issue`.

The list comes from the Agent in Draft. Bob's Orchestrate server reads and changes the Draft environment of the active instance only; the Agent deployed in Live in chapter 7 is not touched until section 8.9.

## 8.2 What an MCP server is, and what an Orchestrate Toolkit is

An MCP server is a program that offers tools over a standard protocol. Any client that speaks the protocol can list the tools, read their descriptions and call them.

Companies meet MCP servers from two sides. Vendors publish MCP servers for their products, so that an Agent can search a ticketing system, read a document store or query a database without anyone writing code for it. And teams write MCP servers for their own systems, so that the same address registry, the same product catalogue, serves every Agent in the company. The ADK documentation lists MCP servers of both kinds that watsonx Orchestrate can import.

An Orchestrate Toolkit is a group of Tools that you import together as one asset. In this chapter the group is the MCP server: when watsonx Orchestrate imports it, the Toolkit is created and each tool of the MCP server becomes a Tool of the Toolkit. At import, you choose all the tools of the MCP server or some of them; the Agent sees each one under the name of the Toolkit, `address_registry:lookup_address`, and uses it like any other Tool, from its description and its parameters.

**Where the MCP server runs**

An MCP server can run inside watsonx Orchestrate or outside it. Inside, the platform receives the code of the MCP server at import, a folder with the program and its dependencies in Python or Node.js, and starts it when an Agent calls one of its tools. Outside, the MCP server runs on your own infrastructure or on a vendor's, and the platform reaches it over HTTP. This guide calls the first a local Toolkit and the second a remote Toolkit.

In this chapter, Bob writes an MCP server for watsonx Orchestrate.

**What changes compared with a Tool**

| | Orchestrate Tool (chapter 6) | Orchestrate Toolkit (this chapter) |
|---|---|---|
| What you import | One function | One MCP server with all its tools |
| Who else can use it | watsonx Orchestrate | Any MCP client, including Bob |
| Name in the Agent | `get_collection_days` | `address_registry:lookup_address` |
| Updating it | Import the Tool again | Remove the Toolkit, import it again, then import the Agents that use it again and deploy those that are in Live |
| Credentials | A Connection named at import | A Connection named at import, whose values reach the MCP server as environment variables |

The last row matters when an MCP server needs a key. The Address Registry of this chapter needs none.

**The MCP server of this chapter: Address Registry**

The MCP server that Bob writes is a small Python program with two tools. `lookup_address` receives an address as a resident types it and returns the official street name, the house number, the district and the postcode. `list_streets` receives a district and returns its streets. The data behind both is a list of the ten streets of the Collection Calendar of chapter 6, each with its district and postcode.

**Why this is one of the most important chapters of this guide**

Most Agents that you build after this guide will use an MCP server at some point. You and your team will write MCP servers to reach a database, an internal API, a product catalogue or any other system of the company. Through them, your Agents gain access to systems inside and outside the company. This chapter teaches what applies to all of them: how to describe an MCP server to Bob so that the design names the component and ends with the build steps; how to try the MCP server from Bob before the platform receives a copy; where it runs, inside the platform or on a server of your own; how a Toolkit gets its credentials through a Connection, as the Tool of chapter 7 did; and how a Toolkit is updated when its MCP server changes.

## 8.3 Ask mode: describe the Address Registry

Mode: Ask, in a new conversation.

In the previous chapters, the prompts did not name the Orchestrate asset to create; Bob chose it based on your prompt. This time the prompt asks for an MCP server by name. You know by now which components exist and what each one is for, so you can state what you need, and Bob no longer has to work out your intention. It also names Python instead of leaving the language to Bob, for two reasons: Bob may write the MCP server in TypeScript, which brings Node.js and its own dependencies into the project; and Python is the language of the Tools of chapter 6, the one that most readers know, with fewer dependencies. The prompt also says where the MCP server runs and asks Bob to try it before the import, two decisions that Bob would otherwise ask about.

```
The city of Utopia has an address registry that resolves any address a
resident types, such as "18 elm st" or "7 Harbour Ln", into the official
street name, the house number, the district and the postcode. The address
registry will be an MCP server, running inside watsonx Orchestrate as a local
toolkit. I want civic_info_agent to use it so that, when a resident gives an
address, the Agent finds the official street before it looks up collection
days or reports a road problem. The city has no address registry yet: build
the MCP server in Python, with the data for the ten streets of the collection
calendar, and connect to it from Bob to try its tools before importing it
into watsonx Orchestrate.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Look for these points in Bob's answer:

- What Bob understood: a Python MCP server with the ten streets of the Collection Calendar as its data, running inside watsonx Orchestrate as a local Toolkit, called by the Agent before any Tool that takes a street, and tried from Bob before the import.
- What exists on the instance: the Agent, its four Tools, the Connection and the Knowledge Base, and no Toolkit. Bob also lists the project files it will change: the Agent definition, its own MCP configuration in `.bob/mcp.json`, and the import script if your project has one.
- The questions. In the run there were five: which districts and postcodes to use; how far the matching of a typed address should go; which Python library to build the MCP server with; what to test from Bob; and whether the Agent must look up every address or only the informal ones. Yours may differ in number and wording. Each one is a decision for you, and none has a single right answer; the second prompt takes the simplest option every time, so that your Address Registry and every other reader's give the same answers.

The second prompt answers the questions in Bob's order, still in Ask mode and in the same conversation. If Bob asked something that the prompt does not cover, add one line with your answer at the end.

```
These are my answers.

1. Do not invent the data. The address registry has four districts. North:
Elm Street (UT1 1AA) and Oak Avenue (UT1 1AB). Harbour: Harbour Lane
(UT2 2AA) and River Close (UT2 2AB). Old Town: Mill Road (UT3 3AA), High
Street (UT3 3AB) and Station Road (UT3 3AC). West: Cedar Way (UT4 4AA), Maple
Drive (UT4 4AB) and Birch Lane (UT4 4AC). The house number is whatever the
resident typed; the address registry returns it as given and does not check it.

2. Normalise only: lowercase, remove punctuation, expand the abbreviations st,
rd, ln, ave, dr, cl. No fuzzy matching and no extra library for it.

3. The official mcp Python SDK, one file, started with "python server.py", with
a requirements.txt next to it.

4. From Bob, call the two tools only: lookup_address with "18 elm st" and
list_streets with "Old Town". The chain through the Agent is tested after the
import.

5. The Agent always calls lookup_address before any tool that takes a street,
and uses the official street name for the collection calendar and for problem
reports, keeping the house number in the description of a report. When the
address registry does not know the address, the Agent asks the resident to
check it and calls no other tool.

Two tools: lookup_address, which receives an address as typed and returns the
official street name, the house number if there is one, the district and the
postcode; and list_streets, which receives a district and returns its streets.
When an address matches no street, lookup_address says so and returns nothing
else. The facts, the Knowledge Base, the four tools and the Connection stay as
they are.
```

Bob confirms the answers and lays out the whole build in the chat: the MCP server file and its data, its entry in Bob's MCP configuration, the two tools added to the Agent and the new instructions, and the import command. Bob may start as if it were going to write the files, and stop because Ask mode does not allow it; it then asks you to switch to Agent mode. Do not: the design comes first.

## 8.4 Plan mode: write the design

Mode: Plan, in the same conversation.

When the design is for an MCP server, Bob tends to write it as a description of files: the MCP server, its entry in Bob's configuration, the import command inside a script. Built from such a design, Bob writes the files and stops, with nothing installed, tested or imported. The prompt therefore asks for the build steps as a list at the end of the design. Make this a habit for every MCP server that you build with Bob: when the design ends with the steps, one approval builds everything.

```
Write the design for this change into design/address-registry-design.md. End
it with the build steps in order: write the MCP server and its requirements
file, install the requirements into the project's Python environment, register
the MCP server in your MCP configuration and call its two tools, import the
toolkit into watsonx Orchestrate, import the agent, run the test scenarios.
```

Bob writes the file after your approval and summarises it. Open `design/address-registry-design.md` and check it against this table:

| Content | What to check |
|---|---|
| The MCP server | Its folder in the project, `toolkits/address_registry`, in Python, with the two tools, their descriptions and parameters, the data of the ten streets, and a requirements file |
| Bob's own connection to it | The MCP server registered in Bob's MCP configuration, so that Bob can call the tools before the import |
| The Toolkit | Its name, `address_registry`; the import from the MCP server's folder with the command that starts the MCP server; both tools imported |
| The change to the Agent | The two tools listed under `tools` with the Toolkit's name in front, `address_registry:lookup_address` and `address_registry:list_streets`; the instructions say to look up every address first and what to do when the Address Registry does not know it; everything else unchanged |
| The build steps | A numbered list at the end, in the order of the prompt. Without it, Bob writes the files and stops |

## 8.5 Approve the design

Mode: Plan, same conversation.

Read Bob's summary and the design file against the table in 8.4. If something is missing or wrong, request the change in the same conversation; Bob revises the file and waits again. When you agree with the design, go to 8.6: its first prompt is the approval.

## 8.6 Agent mode: build, try, import, test

Mode: Agent, in a new conversation.

To build the design, open a new conversation in Bob. Bob then reads the final, approved design only, with a clean memory.

```
The design in @design/address-registry-design.md is approved. Build it.
```

Bob:

1. Writes the MCP server: a folder with the Python program, the data file and the requirements file.
2. Registers the MCP server in its MCP configuration and calls `lookup_address` with a test address. This is Bob using the MCP server as a client, the way it uses the Orchestrate server. The tools appear in Bob's MCP tab, next to the two MCP servers of chapter 2.
3. Imports a copy of the MCP server into watsonx Orchestrate as the Toolkit `address_registry`, from the folder and with the command that starts the MCP server.
4. Updates the Agent: the two tools are attached, the instructions are extended, and the Agent is imported again, replacing the Agent in Draft.
5. Tests the Agent with an address and reports.

Approve each request as it comes. The import of the Toolkit is the step that can fail: the platform installs the MCP server's dependencies and starts it to read the list of tools. The usual causes of an error at that point are a missing dependency, a wrong start command and a Toolkit of the same name already on the instance; Bob reads the error and corrects what it names.

## 8.7 What Bob built

Open the MCP server's folder in the File Explorer, `toolkits/address_registry`. It has two files: the program, `server.py`, with the ten streets inside it, and `requirements.txt`, which names the MCP library the program uses. The library is not part of the environment that chapter 2 installed: Bob installed it there during the build, for its own test, and watsonx Orchestrate installs it on the instance from this file when the Toolkit is imported. Bob may add a README or a test file.

Open the program. It is longer than a Tool of chapter 6, and most of it is the same idea: each tool is a function with a description and typed parameters, and a line above it registers the function with the MCP server. The difference is at the end of the file, where the MCP server starts and waits for a client. When watsonx Orchestrate calls a tool, it starts this program, sends the call through its standard input, reads the answer from its standard output, and stops it.

Open Bob's MCP tab (chapter 2, section 2.3). The Address Registry is listed as an MCP server, connected, with its two tools, next to `watsonx-orchestrate-adk` and `watsonx-orchestrate-adk-docs`. Bob's configuration for it is in `.bob/mcp.json`, which git ignores: it points at the folder on your machine, and every reader's Bob writes its own.

Open `agents/civic_info_agent.yaml`. Under `tools`, after the four Tools of chapter 7, the two tools of the Toolkit with its name in front: `address_registry:lookup_address` and `address_registry:list_streets`. The `toolkits` line stays empty; it is for another kind of Agent. The instructions have a new section: look up every address that a resident gives, use the official street name for the other Tools, and ask the resident to check an address that the Address Registry does not know.

Save your work: `Commit everything I changed with a short message saying what was built.`

## 8.8 Try it

Ask the Agent, through Bob with `Ask civic_info_agent:` in front, or in the preview panel of watsonx Orchestrate:

```
The rubbish was not collected today at 18 elm st, which days do they collect it?
```

The Agent resolves the address to Elm Street, looks up the collection days, and answers with the days of the four bins and the Waste and Recycling contact. Then try these:

- The Address Registry alone, through Bob, in Agent mode: `Call lookup_address on the address registry MCP server with "7 harbour ln" and show me the result.` Harbour Lane, house number 7, Harbour district, UT2 2AA. This is Bob calling the MCP server on your machine; the Agent calls the copy on the instance.
- An address with another abbreviation: "Report a pothole at 7 harbour ln." The report goes to the stand-in of the 311 Call Center from chapter 7, with the street Harbour Lane and the house number in the description, and the Agent gives a request number.
- A question about districts: "Which streets are in the Old Town district?" Mill Road, High Street and Station Road.
- An address the Address Registry does not know: "Which day is the grey bin collected at 3 Castle Street?" The Agent says that it does not know that address and asks you to check it. With reasoning, the steps show the lookup and no call to `get_collection_days`.

Ask the first question again with reasoning. The steps show two tool calls in order: `address_registry:lookup_address` with the address as typed, returning Elm Street, then `get_collection_days` with Elm Street. The Toolkit's tool carries the Toolkit's name in front, and the chapter 6 Tool does not.

## 8.9 Deploy the change in Live

Mode: Agent, same conversation.

A Toolkit belongs to the instance, like a Tool, so Live needs only the Agent. On the Developer Edition, skip this section. If you skipped chapter 7, the Connection `utopia_311` exists for Draft only; send the first prompt of section 7.10 before the deployment, or the Agent in Live fails at its first report.

```
Deploy civic_info_agent from draft to live.
```

When Bob reports the deployment, go to the watsonx Orchestrate chat and ask the question of the Overview: a resident who writes "18 elm st" gets the collection days of Elm Street.

## 8.10 Summary

The Agent now understands addresses the way residents write them, through a service of the kind that a city offers to every system, and the same program answered Bob's test calls before it answered residents. Bob wrote the MCP server, tried it as a client, imported it as an Orchestrate Toolkit, and changed the Agent; you described the Address Registry, fixed its data, and approved the design.

- An MCP server is a program that offers tools over a standard protocol to any client, Bob or watsonx Orchestrate among them.
- An Orchestrate Toolkit holds several tools as one asset; the MCP kind is an MCP server registered on the instance. The Agent sees each tool as `toolkit:tool` and uses it like any other Tool.
- A local Toolkit is a folder that the platform runs; a remote Toolkit is an MCP server reached over HTTP. A Toolkit is updated by removing it and importing it again; the Agents that use it are then imported again, and deployed again where they are in Live.
- Bob creates MCP servers itself, and uses them as a client before the platform does.

The Agent of CivicPulse now knows the departments, searches the regulations, looks up records, reports problems and resolves addresses, all from one set of instructions that has grown with every chapter. In chapter 9, that one Agent becomes several: a front desk Agent that talks to residents, and one Agent per department behind it, each with the Tools and the knowledge of its own domain.
