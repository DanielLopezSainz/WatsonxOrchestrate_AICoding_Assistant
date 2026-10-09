# Chapter 8. An address lookup from an MCP server: Orchestrate Toolkits

Level: intermediate. Time: about 75 minutes. Prerequisites: chapter 7 completed, or its Tool, Connection and Agent imported from the walkthrough folder as that chapter's Overview describes.

## Overview

You send a message to CivicPulse: "The rubbish was not collected today at 18 elm st, which days do they collect it?". The Agent of chapter 7 has a Tool that knows the collection days of Elm Street, but the Tool does not find the street, because "18 elm st" is not how the city spells it. An Address Registry solves this: it receives an address as a resident types it and returns the official street name, the house number, the district and the postcode. In this chapter, Bob writes that Address Registry as an MCP server, with the ten streets of the Collection Calendar, and the Agent uses it.

MCP, the Model Context Protocol, is a standard way for a program to offer tools to AI Agents. You have used it since chapter 2: Bob reaches your instance through one MCP server and the Orchestrate documentation through another. Now Bob builds an MCP server of its own, with its built-in capability for creating MCP servers, and connects to it to try its tools. Then watsonx Orchestrate imports a copy of the MCP server as an Orchestrate Toolkit, and the Agent gets its tools.

The Orchestrate Toolkit is the component introduced in this chapter.

Skip this chapter if you have already imported an MCP server into watsonx Orchestrate with Bob. To continue with chapter 9 without building it, send Bob these instructions in Agent mode: `Import the MCP server in walkthroughs/ch08/toolkits/address_registry into my instance as a toolkit named address_registry, with all its tools, then import walkthroughs/ch08/agents/civic_info_agent.yaml.` The skip path gives the instance the Toolkit and the Agent; Bob's own connection to the MCP server, which 8.6 sets up, is not needed by the later chapters.

## 8.1 Before you start

- The setup from chapter 2, complete.
- The Agent `civic_info_agent` from chapter 7 on your instance, in Draft, with its four Tools and the Connection `utopia_311`. If you skipped chapter 7, import them as described in that chapter's Overview.
- In Bob's settings, MCP tab, the setting Enable MCP Server Creation switched on. It is on by default; when it is off, Bob has no instructions for writing one.
- A new conversation in Bob for this chapter.

Check that the Agent is there: in Ask mode, ask `Which tools does civic_info_agent have?` and confirm the four names, `get_permit_status`, `get_request_status`, `get_collection_days` and `report_issue`.

The list comes from the Agent in Draft. Bob's Orchestrate server reads and changes only the Draft environment of the active instance. The Agent deployed in Live in chapter 7 is not touched until section 8.9.

## 8.2 What an MCP server is, and what an Orchestrate Toolkit is

An MCP server is a program that offers tools over a standard protocol. Any client that speaks the protocol can list the tools, read their descriptions and call them.

Vendors publish MCP servers for their products, so that an Agent can search a ticketing system, read a document store or query a database without anyone writing code for it. Teams write MCP servers for their own systems, and the same address registry or product catalogue then serves every Agent in the company. The ADK documentation lists MCP servers of both kinds that watsonx Orchestrate can import.

An Orchestrate Toolkit is a group of Tools that you import together as one asset. For the Address Registry, the group is the MCP server: when watsonx Orchestrate imports it, the Toolkit is created and each tool of the MCP server becomes a Tool of the Toolkit. At import, you choose all the tools of the MCP server or some of them; the Agent sees each one under the name of the Toolkit, `address_registry:lookup_address`, and uses it like any other Tool, from its description and its parameters.

**Where the MCP server runs**

An MCP server can run inside watsonx Orchestrate or outside it. Inside, the platform receives the code of the MCP server at import, a folder with the program and the file that lists its dependencies, in Python or Node.js, and starts it when an Agent calls one of its tools. Outside, the MCP server runs on your own infrastructure or on a vendor's, and the platform reaches it over HTTP. This guide calls the first a local Toolkit and the second a remote Toolkit. In this chapter, Bob writes an MCP server for watsonx Orchestrate.

**What changes compared with a Tool**

| | Orchestrate Tool (chapter 6) | Orchestrate Toolkit (this chapter) |
|---|---|---|
| What you import | One function | One MCP server with all its tools |
| Who else can use it | watsonx Orchestrate | Any MCP client, including Bob |
| Name in the Agent | `get_collection_days` | `address_registry:lookup_address` |
| Updating it | Import the Tool again | Remove the Toolkit, import it again, then import the Agents that use it again and deploy those that are in Live |
| Credentials | A Connection named at import | A Connection named at import, whose values reach the MCP server as environment variables |

The Address Registry of this chapter needs no key, so the last row does not apply to it.

**The MCP server of this chapter: Address Registry**

The MCP server that Bob writes is a small Python program with two tools. `lookup_address` receives an address as a resident types it and returns the official street name, the house number, the district and the postcode. `list_streets` receives a district and returns its streets. The data behind both is a list of the ten streets of the Collection Calendar of chapter 6, each with its district and postcode.

**Why this is one of the most important chapters of this guide**

The Agents that you build after this guide will often use an MCP server. You and your team will write MCP servers to reach a database, an internal API, a product catalogue or any other system of the company, and through them your Agents reach systems inside and outside the company. This chapter covers what applies to all of them. You learn how to describe an MCP server to Bob so that the design names the component and ends with the build steps, and how to try the MCP server from Bob before the platform receives a copy. You also learn where the MCP server runs, inside the platform or on a server of your own; how a Toolkit gets its credentials through a Connection, as the Tool of chapter 7 did; and how a Toolkit is updated when its MCP server changes. Section 8.10 collects these practices in one list, with the reason for each.

This chapter explains how watsonx Orchestrate runs an MCP server, how Bob connects to it and what the design and the prompts must specify. These details are explained once and are not repeated in later chapters. The practices in 8.10 address these problems, but your Toolkits may still need corrections after one build.

## 8.3 Ask mode: describe the Address Registry

Mode: Ask, in a new conversation.

In the previous chapters, the prompts did not name the Orchestrate asset to create; Bob chose it based on your prompt. This time the prompt asks for an MCP server by name. You know by now which components exist and what each one is for, so you can state what you need, and Bob no longer has to guess your intention. It also names Python instead of leaving the language to Bob, for two reasons: Bob may write the MCP server in TypeScript, which brings Node.js and its own dependencies into the project; and Python is the language of the Tools of chapter 6, the one that most readers know, with fewer dependencies. The prompt also says where the MCP server runs and asks Bob to try it before the import, two decisions that Bob would otherwise ask about.

```
The city of Utopia needs an address registry that resolves any address a
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
- What exists: the Agent with its four Tools and its Knowledge Base, the Collection Calendar with the ten streets, the two servers in Bob's MCP configuration, and no Toolkit.
- The questions: Bob asks between two and five. Expect one about the districts and postcodes; the others may be what the tool returns for an unknown address, how far the matching of a typed address should go, which Python library to use, whether to install it in the project's environment or in one of its own, what to test from Bob, and whether the Agent must look up every address or only the informal ones. Each one is a decision for you, and none has a single right answer. The second prompt takes the simplest option every time, so that your Address Registry and every other reader's give the same answers. Bob may end by asking you to switch to Agent mode; stay in Ask mode.

Send the prompt below whole, still in Ask mode and in the same conversation; it covers what Bob asked and the points it did not raise. If Bob asked something that it does not cover, add one line with your answer at the end.

```
These are my answers.

1. The address registry covers the ten streets of tools/collection_calendar.csv
and nothing else. It has four districts: North, with Elm Street (UT1 1AA);
Harbour, with Harbour Lane (UT2 2AA); Old Town, with Mill Road (UT3 3AA); and
West. Put the other seven streets of the calendar into these four districts,
two or three per district, with postcodes that continue the pattern (UT1 1AB,
UT2 2AB, UT4 4AA and so on). The house number is whatever the resident typed;
the address registry returns it as given and does not check it.

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
else. Name the toolkit and its folder address_registry, and attach both tools
to the agent, listed under tools as toolkit:tool. The facts, the Knowledge
Base, the four tools and the Connection stay as they are.
```

Bob confirms the answers and lays out the build in the chat: the MCP server file and its data, its entry in Bob's MCP configuration, the two test calls, the changes to the Agent, and in some runs the import into watsonx Orchestrate. Bob may start as if it were going to write the files, and stop because Ask mode does not allow it. Do not switch to Agent mode: the design is written first, in Plan mode.

## 8.4 Plan mode: write the design

Mode: Plan, in the same conversation.

A design for an MCP server often describes files only: the program, Bob's configuration entry, a script with the import command. From such a design, Bob writes the files and stops; nothing is installed, tested or imported. The prompt below prevents that by asking for the build steps as a numbered list at the end of the design. It also names two details that Bob tends to get wrong: the Python that starts the MCP server, and the import from the MCP server's folder. Section 8.10 explains both.

```
Write the design for this change into design/address-registry-design.md. End
it with the build steps in order: write the MCP server and its requirements
file, install the requirements into the project's Python environment, register
the MCP server in your MCP configuration, started with the Python of the
project's environment, with absolute paths, and call its two tools through
that connection, import the toolkit into watsonx Orchestrate from its folder
with all its tools, import the agent, run the test scenarios through the chat
operation of the Orchestrate server.
```

Read Bob's answer. Sometimes, in its first lines, Bob says that it cannot write files and asks you to switch to Agent mode. If you get that answer and you have confirmed that you are in Plan mode, send the following prompt: `You are in Plan mode and can write files. Write the design to design/address-registry-design.md.` Approve the write; Bob then writes the file and summarises it.

Open `design/address-registry-design.md` and check it against this table:

| Content | What to check |
|---|---|
| The MCP server | Its folder in the project, `toolkits/address_registry`, in Python, with the two tools, their descriptions and parameters, the data of the ten streets, and a requirements file |
| Bob's own connection to it | The MCP server registered in Bob's MCP configuration, started with the Python of the project's environment, so that Bob can call the tools before the import |
| The Toolkit | Its name, `address_registry`; the import from the MCP server's folder with the command that starts the MCP server; both tools imported |
| The change to the Agent | The two tools listed under `tools` with the Toolkit's name in front, `address_registry:lookup_address` and `address_registry:list_streets`; the instructions say to look up every address first and what to do when the Address Registry does not know it; everything else unchanged |
| The build steps | A numbered list at the end, in the order of the prompt. Without it, the build ends after the files are written |

## 8.5 Approve the design

Mode: Plan, same conversation.

Read Bob's summary and the design file against the table in 8.4. If something is missing or wrong, request the change in the same conversation; Bob revises the file and waits again. When you agree with the design, go to 8.6: its first prompt is the approval.

## 8.6 Agent mode: build, try, import, test

Mode: Agent, in a new conversation.

Create a new conversation and switch to Agent mode to run the prompt:

```
The design in @design/address-registry-design.md is approved. Build it.
```

Bob follows the build steps of the design:

1. Writes the MCP server, `toolkits/address_registry/server.py` with the ten streets inside it, and `requirements.txt`.
2. Installs the library into the project's environment and checks that the program imports. The library may have changed its version since the design was written and renamed its server class; Bob reads the error and changes one line.
3. Registers the MCP server in its MCP configuration and tests `lookup_address` and `list_streets`. The design says to call them through that connection; Bob may run the two functions in Python instead and report their results, which is not the same test. The registry appears in Bob's MCP tab next to the two MCP servers of chapter 2, and the test in 8.8 makes Bob use the connection.
4. Imports a copy of the MCP server into watsonx Orchestrate as the Toolkit `address_registry`, from the folder and with the command that starts it. The design may have the wrong form of the command; Bob corrects it from the command's help. The platform may answer the first attempt with "We are configuring your tool in the background"; Bob waits a minute and tries again, and the second attempt succeeds.
5. Updates the Agent and imports it again, replacing the Agent in Draft. Bob may first put the Toolkit on the `toolkits` line: the import succeeds and the Agent ignores the tools, which Bob sees in its first test; it then lists them under `tools` as `address_registry:lookup_address` and `address_registry:list_streets`, and imports the Agent again.
6. Sends three test questions to the Agent and reports: an address with an abbreviation, a pothole report with a house number, and an address the registry does not know.

Approve each request as it comes. Bob corrects failures of this kind during the build and reports only the results; to see what it corrected, ask in the same conversation: `List every problem you met during the build and how you solved it.`

## 8.7 What Bob built

Open the MCP server's folder in the File Explorer, `toolkits/address_registry`. It has two files: `server.py`, the program with its data, and `requirements.txt`, which names the MCP library the program uses. The library is not part of what chapter 2 installed. Bob installed it in the project's environment during the build, for its own test, and watsonx Orchestrate installs it on the instance from this file when the Toolkit is imported. Bob may add a README or a test file.

The program is longer than a Tool of chapter 6, and most of it is the same idea: each tool is a function with a description and typed parameters, and a line above it registers the function with the MCP server, an object of the library's server class, `MCPServer` in version 2 of the library and `FastMCP` in version 1. The difference is at the end of the file, where the MCP server starts and waits for a client. When watsonx Orchestrate calls a tool, it starts this program, sends the call through its standard input, reads the answer from its standard output (the stdio transport, which every local Toolkit uses), and stops it.

Bob's MCP tab (chapter 2, section 2.3) lists the Address Registry as an MCP server, connected, with its two tools, next to `watsonx-orchestrate-adk` and `watsonx-orchestrate-adk-docs`. Bob's configuration for it is in `.bob/mcp.json`, which git ignores: it points at the folder on your machine, and every reader's Bob writes its own. If the entry shows as disconnected, in red, the usual cause is a relative path in it: Bob starts its MCP servers from a directory of its own, where `venv/bin/python` does not exist. Send, in Agent mode: `The address_registry server in your MCP tab is disconnected. Fix its entry in .bob/mcp.json with absolute paths for the Python interpreter and the program, and restart it.`

In `agents/civic_info_agent.yaml`, the `tools` list has, after the four Tools of chapter 7, the two tools of the Toolkit with its name in front: `address_registry:lookup_address` and `address_registry:list_streets`. The `toolkits` line stays empty. It is for another kind of Agent. The instructions have a new section: look up every address that a resident gives, use the official street name for the other Tools, and ask the resident to check an address that the Address Registry does not know.

Save your work: `Commit everything I changed with a short message saying what was built.`

## 8.8 Try it

Ask the Agent, through Bob with `Ask civic_info_agent:` in front, or in the preview panel of the Agent in the watsonx Orchestrate builder (Build, Agents, `civic_info_agent`). On a tenant, do not use the chat of the home page yet: it talks to the Agent deployed in Live, which is still the chapter 7 version and answers that it has no record for "18 elm st". The chat shows the change after 8.9. On the Developer Edition, the chat shows the Agent in Draft and answers correctly already.

```
The rubbish was not collected today at 18 elm st, which days do they collect it?
```

The Agent resolves the address to Elm Street, looks up the collection days, and answers with the days of the four bins and the Waste and Recycling contact. Then try these:

- The Address Registry alone, through Bob, in a new conversation in Ask mode: `Call lookup_address with "7 harbour ln" on the address_registry MCP server and show me the result.` Harbour Lane, house number 7, Harbour district, UT2 2AA. Then `Now call list_streets with "Old Town" on the same server.`: Mill Road and the other streets of that district. Ask mode leaves Bob no way to run the program itself, so the calls go through its MCP connection, and Bob shows the server and the tool above its answer. This is Bob calling the MCP server on your machine; the Agent calls the copy on the instance.
- An address with another abbreviation: "Report a pothole at 7 harbour ln." The report goes to the stand-in of the 311 Call Center from chapter 7, with the street Harbour Lane and the description "Pothole outside house number 7", and the Agent gives a request number.
- A question about districts: "Which streets are in the Old Town district?" Mill Road and the other streets that your registry puts there.
- An address the Address Registry does not know: "Which day is the grey bin collected at 3 Castle Street?" The Agent says that it does not know that address and asks you to check it. With reasoning, the steps show the lookup and no call to `get_collection_days`.

Ask the first question again with reasoning. The steps show two tool calls in order: `lookup_address` with the address as typed, returning Elm Street, house number 18, North and UT1 1AA, then `get_collection_days` with Elm Street. In the reasoning, the tool of the Toolkit appears under its own name, without the Toolkit's name in front; the prefix is for the Agent definition only.

## 8.9 Deploy the change in Live

Mode: Agent, same conversation.

The Agent changed in Draft and needs to be deployed to Live again. On the Developer Edition, skip this section.

```
Deploy civic_info_agent from draft to live.
```

When Bob reports the deployment, go to the watsonx Orchestrate chat and ask the question of the Overview: a resident who writes "18 elm st" gets the collection days of Elm Street.

## 8.10 Advice for building Orchestrate Toolkits with Bob

Every MCP server that you build with Bob for watsonx Orchestrate goes through the steps of this chapter: a description, a design, a build, an import and a test. Each practice below says what to put in your prompts or what to check in the design, and what happens without it.

1. Tell Bob in the first prompt that you want an MCP server. If the prompt describes only what the Agent must do, Bob proposes the simplest component that does it, usually a Python Tool, and no MCP server is built.
2. Tell Bob which language to use, Python in this guide. Bob's documentation says that it typically writes MCP servers in TypeScript, which adds Node.js and its dependencies to the project. Python is the language of the Tools and of the environment that chapter 2 installed.
3. Tell Bob where the MCP server runs. "Running inside watsonx Orchestrate as a local toolkit" is enough, because a local Toolkit always uses stdio. Without it, Bob asks about transports and may claim that a cloud instance needs HTTP, which is wrong.
4. Ask Bob to test the MCP server itself before importing it, and check that it did so through its MCP connection rather than by running the Python functions. Bob rarely proposes this test on its own. A failure found before the import is corrected in the file; the same failure after the import appears only when the Agent calls the tool.
5. Give the data in the prompt and keep the matching simple. Otherwise Bob invents the data. Every library that the MCP server imports has to be installed again on the instance, so keep the number of libraries small.
6. Name the tools, say what each returns, and say what happens when nothing matches. If the prompt omits them, Bob proposes one tool where two are needed and chooses their names. Say also what the Agent does with a not-found result; for the Address Registry, it asks the resident and calls no other Tool.
7. Use one name for the Toolkit and its folder, with underscores. Otherwise Bob may write a folder with a hyphen and give the Toolkit another name, and the Agent, the import command and your notes disagree.
8. Tell Bob that the tools go into the Agent's `tools` list with the Toolkit's name in front, as `toolkit:tool`. If Bob names the Toolkit on the `toolkits` line instead, the Agent imports without any error and ignores the tools, and only a test shows it.
9. Ask Bob to end the design with the build steps. Without them, "Build it" means "write the files": Bob writes them, checks their syntax and stops, with nothing installed, tested or imported. With the steps, the installation, the tests and the imports are part of the same build.
10. Ask Bob to start the MCP server with the Python of the project's environment and with absolute paths in its `.bob/mcp.json` entry. A bare `python` is usually not the environment where the library is installed, and a relative path is not found, because Bob starts its servers from a directory of its own. In both cases the entry shows red in the MCP tab.
11. For a local Toolkit, ask Bob to import it from its folder, with all its tools. The ADK command is `orchestrate toolkits add --kind mcp --name <name> --description "<text>" --package-root <folder> --command "python server.py" --tools "*"`. Without the folder, the platform receives no code, and the first call to a tool fails.
12. Keep to the three modes. Bob asks to switch to Agent mode after the first prompt, after the second, and sometimes instead of writing the design in Plan mode. Answer the questions in Ask mode, write the design in Plan mode, and build in a new conversation in Agent mode. If Bob shows the design in the chat instead of writing it, tell it that it is in Plan mode and can write the file.
13. In case of doubt, check what Bob says about the platform against the ADK documentation. Language models state a wrong claim with the same confidence as a right one. Bob can search the documentation server of section 2.4 itself; ask it to confirm a claim before you build on it.
14. Specify the version of the MCP library in `requirements.txt`, for example `mcp==2.3.0`. A range such as `mcp>=1.0.0` installs whatever version is current, and a new major version can rename the classes that the server uses. The instance installs the library from the same file, so name the version that Bob tested.
15. Tell Bob how to test the Agent: in the build steps of the design, with the words "run the test scenarios through the chat operation of the Orchestrate server", as the prompt of 8.4 does; for a test of your own, with `Ask civic_info_agent:` in front of the question. That operation sends a message to the Agent in Draft and returns its answer, as if you were talking to the Orchestrate Agent directly.

## 8.11 Summary

You have built an MCP server with Bob, tried it from Bob, imported it into watsonx Orchestrate as a Toolkit and given its tools to an Agent. The same steps apply to every system that your Agents will reach through an MCP server: a database, an internal API, a vendor's product. Before you build the next one, read section 8.10 again.

- An MCP server is a program that offers tools over a standard protocol to any client, Bob or watsonx Orchestrate among them.
- An Orchestrate Toolkit holds several tools as one asset; the MCP kind is an MCP server registered on the instance. The Agent sees each tool as `toolkit:tool` and uses it like any other Tool.
- A local Toolkit is a folder that the platform runs; a remote Toolkit is an MCP server reached over HTTP. A Toolkit is updated by removing it and importing it again; the Agents that use it are then imported again, and deployed again where they are in Live.
- Bob creates MCP servers itself, and uses them as a client before the platform does.
