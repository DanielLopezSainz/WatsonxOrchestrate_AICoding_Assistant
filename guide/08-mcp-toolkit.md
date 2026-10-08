# Chapter 8. An address lookup from an MCP server: Orchestrate Toolkits

Level: intermediate. Time: about 75 minutes. Prerequisites: chapter 7 completed, or its Tool, Connection and Agent imported from the walkthrough folder as that chapter's Overview describes.

## Overview

You live at 18 Elm Street and you write to CivicPulse the way people write on their phones: "bins not collected at 18 elm st, which day is it?". The Agent of chapter 7 has a Tool that knows the collection days of Elm Street, but the Tool wants the street as the city spells it, and "18 elm st" is not that. What CivicPulse needs is an address registry: give it an address as a resident types it, and it answers with the official street name, the house number, the district and the postcode. In a city, such a registry is a service that other systems use too, and a service of that kind is offered to assistants and agents as an MCP server. The City of Utopia has none, so Bob writes one for this guide with the ten streets of the collection calendar, as Postman Echo stood in for the 311 Call Center in chapter 7.

MCP, the Model Context Protocol, is a standard way for a program to offer tools to AI assistants. You have used it since chapter 2: Bob reaches your instance through one MCP server and the Orchestrate documentation through another. In this chapter the roles turn around. Bob builds an MCP server, the address registry of Utopia, with its built-in capability for creating MCP servers, and connects to it to try its tools. Then watsonx Orchestrate receives a copy of the same server, imports it as an Orchestrate Toolkit, and the Agent gets its tools. The same program serves two clients: the assistant that builds and the platform that serves residents, each running its own copy.

Bob also writes the registry's data, as it wrote the records of chapter 6: the ten streets of Utopia that the collection calendar already knows, each with its district and postcode.

The Orchestrate Toolkit is the component introduced in this chapter. Bob's capability is the creation of MCP servers, which is part of Bob itself.

Skip this chapter if you have already imported an MCP server into watsonx Orchestrate with Bob. To continue with chapter 9 without building it, send Bob these instructions in Agent mode: `Import the MCP server in walkthroughs/ch08/mcp/utopia_addresses into my instance as a toolkit named utopia_addresses, with all its tools, then import walkthroughs/ch08/agents/civic_info_agent.yaml.`

## 8.1 Before you start

- The setup from chapter 2, complete.
- The Agent `civic_info_agent` from chapter 7 on your instance, in Draft, with its four Tools and the Connection `utopia_311`. If you skipped chapter 7, import them as described in that chapter's Overview.
- In Bob's settings, MCP tab, the setting Enable MCP Server Creation switched on. It is on by default; when it is off, Bob does not know how to write a server.
- A new conversation in Bob for this chapter.

Check that the Agent is there: in Ask mode, ask `Which tools does civic_info_agent have?` and confirm the four names, `get_permit_status`, `get_request_status`, `get_collection_days` and `report_issue`.

## 8.2 What an MCP server is, and what an Orchestrate Toolkit is

An MCP server is a program that offers tools over a standard protocol. Any client that speaks the protocol can list the tools, read their descriptions and call them: Bob, other coding assistants, and watsonx Orchestrate. The tools of chapter 6 were written for watsonx Orchestrate alone; the tools of an MCP server are written once and used by whichever client connects.

Companies meet MCP servers from two sides. Vendors publish servers for their products, so that an assistant can search a ticketing system, read a document store or query a database without anyone writing code for it. And teams write servers for their own systems, so that the same address registry, the same product catalogue, serves every assistant and every agent in the company. The ADK documentation lists servers of both kinds that watsonx Orchestrate can import.

An Orchestrate Toolkit is one asset that holds several tools, imported and removed in one operation. It has two kinds: an MCP toolkit, which is an MCP server registered on the instance, and a Python toolkit, which is a set of Python Tools that run in one process. This chapter builds an MCP toolkit. At import, you choose all the tools of the server or some of them; the Agent sees each one under the name of the toolkit, `utopia_addresses:lookup_address`, and uses it like any other Tool, from its description and its parameters.

**Where the server runs**

watsonx Orchestrate runs an MCP server in two ways. A local toolkit is a server whose code the platform receives at import, a folder with the program and its dependencies, and runs itself when an Agent calls a tool, in Python or Node.js. A remote toolkit is a server that runs elsewhere, on your infrastructure or a vendor's, and that the platform reaches over HTTP. A local server talks to its client through its standard input and output, called stdio: the client starts the program, writes the call to it and reads the answer back. Bob does the same when it connects to the server on your machine. This chapter builds a local toolkit: a copy of the folder that Bob writes is uploaded to the instance, the way the Tools of chapter 6 were, and the platform starts the server when needed. A change to the folder on your machine reaches the instance only through a new import.

**What changes compared with a Tool**

| | Orchestrate Tool (chapter 6) | Orchestrate Toolkit (this chapter) |
|---|---|---|
| What you import | One function | One server with all its tools |
| Who else can use it | watsonx Orchestrate | Any MCP client, including Bob |
| Name in the Agent | `get_collection_days` | `utopia_addresses:lookup_address` |
| Updating it | Import the Tool again | Remove the toolkit, import it again, then import the Agents that use it again and deploy those that are in Live |
| Credentials | A Connection named at import | A Connection named at import, whose values reach the server as environment variables |

The last row matters when a server needs a key. The registry of this chapter needs none.

**The registry of this chapter**

The registry of this chapter is a small MCP server in Python with two tools, written by Bob. `lookup_address` receives an address as a resident types it and returns the official street name, the house number, the district and the postcode. `list_streets` receives a district and returns its streets. The data is a table of ten streets, the ones of the collection calendar of chapter 6, that Bob writes into the server's folder.

## 8.3 Ask mode: describe the registry

Mode: Ask, in a new conversation.

The prompt describes the service, what residents type, and what the Agent must do with the answer. It names MCP and Python, and it says that the registry is not a customer care server: one of the Orchestrate skills loaded in chapter 2 builds MCP servers for customer care, with a welcome tool and a login, and Bob must not use it here.

```
The city of Utopia has an address registry that resolves any address a
resident types, such as "18 elm st" or "7 Harbour Ln", into the official
street name, the house number, the district and the postcode. The registry is
offered as an MCP server. I want civic_info_agent to use it so that, when a
resident gives an address, the Agent finds the official street before it looks
up collection days or reports a road problem. The city has no registry yet:
build the MCP server yourself, in Python, with the data for the ten streets of
the collection calendar. It is a plain lookup service, not a customer care
server, so do not use the customer care MCP builder skill.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Look for these points in Bob's answer:

- Bob proposes to write the server, to register it in its own MCP configuration so that it can try the tools itself, and then to import it into watsonx Orchestrate as a toolkit. The server must work for one client before a copy is given to the second.
- On the instance, Bob finds the Agent, its four Tools, the Connection and the Knowledge Base, and no toolkit.
- The questions vary from one run to another: which tools the server offers and what they return, the districts and postcodes to use, what the Agent does when an address is not in the registry, and whether the Agent should look up every address or only ambiguous ones.

The second prompt answers them. It fixes the data, so that your registry and every other reader's registry give the same answers.

```
These are my answers. Two tools: lookup_address, which receives an address as
typed and returns the official street name, the house number if there is one,
the district and the postcode; and list_streets, which receives a district and
returns its streets. The registry has four districts. North: Elm Street
(UT1 1AA) and Oak Avenue (UT1 1AB). Harbour: Harbour Lane (UT2 2AA) and River
Close (UT2 2AB). Old Town: Mill Road (UT3 3AA), High Street (UT3 3AB) and
Station Road (UT3 3AC). West: Cedar Way (UT4 4AA), Maple Drive (UT4 4AB) and
Birch Lane (UT4 4AC). The lookup accepts abbreviations such as st, rd, ln,
ave, and any capitalisation. When an address matches no street, the tool says
so and returns nothing else.

The Agent looks up every address that a resident gives, and uses the official
street name for the collection calendar and for problem reports, keeping the
house number in the description of a report. When the registry does not know
the address, the Agent asks the resident to check it and calls no other Tool.
The Agent can also answer which district a street is in and which streets a
district has. The facts, the Knowledge Base, the four Tools and the Connection
stay as they are.
```

Bob confirms the answers and lays out the server in the chat: its two tools, the data, the files it will create, and the import into watsonx Orchestrate. Do not switch to Agent mode yet.

## 8.4 Plan mode: write the design

Mode: Plan, in the same conversation.

```
Write the design for this change into design/address-registry-design.md.
```

Bob writes the file after your approval and summarises it. Open `design/address-registry-design.md` and check it against this table:

| Content | What to check |
|---|---|
| The server | Its folder in the project, in Python, with the two tools, their descriptions and parameters, the data of the ten streets, and a requirements file |
| Bob's own connection to it | The server registered in Bob's MCP configuration, so that Bob can call the tools before the import |
| The toolkit | Its name, `utopia_addresses`; the import from the server's folder with the command that starts the server; both tools imported |
| The change to the Agent | The two tools of the toolkit attached; the instructions say to look up every address first and what to do when the registry does not know it; everything else unchanged |
| The build order | Server, Bob's connection and a test through Bob, toolkit, Agent, then the test through the Agent |

## 8.5 Approve the design

Mode: Plan, same conversation.

There is no prompt to send in this section unless the design needs a change. Read the design against the table in 8.4. The most common gap is the second row: a design that goes from the server straight to the import, without Bob connecting to the server itself. If that is the case, send `Add a step after the server is written: register it in your MCP configuration and call lookup_address with "18 elm st" before importing anything into watsonx Orchestrate.` Bob may also ask you about details that the design does not fix; answer `Decide these yourself and proceed.` When the design is correct, go to 8.6: its first prompt is the approval.

## 8.6 Agent mode: build, try, import, test

Mode: Agent, in a new conversation.

The build starts in a new conversation, as in every chapter: the planning discussion is out of Bob's context, and Bob reads the design and the project files that the design names.

```
The design in @design/address-registry-design.md is approved. Build it.
```

Bob:

1. Writes the server: a folder with the Python program, the data file and the requirements file.
2. Registers the server in its MCP configuration and calls `lookup_address` with a test address. This is Bob using the server as a client, the way it uses the Orchestrate server. The tools appear in Bob's MCP tab, next to the two servers of chapter 2.
3. Imports a copy of the server into watsonx Orchestrate as the toolkit `utopia_addresses`, from the folder and with the command that starts the server.
4. Updates the Agent: the two tools are attached, the instructions are extended, and the Agent is imported again, replacing the Agent in Draft.
5. Tests the Agent with an address and reports.

Approve each request as it comes. The import of the toolkit is the step that can fail: the platform installs the server's dependencies and starts it to read the list of tools. The usual causes of an error at that point are a missing dependency, a wrong start command and a toolkit of the same name already on the instance; Bob reads the error and corrects what it names.

## 8.7 What Bob built

Open the server's folder in the File Explorer; Bob names it after the registry, for example `mcp/utopia_addresses`. It has at least three files: the program, a data file with the ten streets, and `requirements.txt`, which names the MCP library the program uses. Bob may add a README or a test file.

Open the program. It is longer than a Tool of chapter 6, and most of it is the same idea: each tool is a function with a description and typed parameters, and a line above it registers the function with the server. The difference is at the end of the file, where the server starts and waits for a client. When watsonx Orchestrate calls a tool, it starts this program, sends the call through its standard input, reads the answer from its standard output, and stops it.

Open Bob's MCP tab (chapter 2, section 2.3). The registry is listed as a server, connected, with its two tools, next to `watsonx-orchestrate-adk` and `watsonx-orchestrate-adk-docs`. Bob's configuration for it is in `.bob/mcp.json`, which git ignores: it points at the folder on your machine, and every reader's Bob writes its own.

Open `agents/civic_info_agent.yaml`. The two tools are listed under `tools` as `utopia_addresses:lookup_address` and `utopia_addresses:list_streets`, or the toolkit under `toolkits` as `utopia_addresses`; the ADK accepts both. The instructions have a new paragraph: look up every address that a resident gives, use the official street name for the other Tools, and ask the resident to check an address that the registry does not know.

Save your work: `Commit everything I changed with a short message saying what was built.`

## 8.8 Try it

Ask the Agent, through Bob with `Ask civic_info_agent:` in front, or in the preview panel of watsonx Orchestrate:

```
bins not collected at 18 elm st, which day is it?
```

The Agent resolves the address to Elm Street, looks up the collection days, and answers with the days of the four bins and the Waste and Recycling contact. Then try these:

- The registry alone, through Bob, in Agent mode: `Call lookup_address on the utopia_addresses server with "7 harbour ln" and show me the result.` Harbour Lane, house number 7, Harbour district, UT2 2AA. This is Bob calling the server on your machine; the Agent calls the copy on the instance.
- An address with another abbreviation: "Report a pothole at 7 harbour ln." The report goes to the stand-in of the 311 Call Center from chapter 7, with the street Harbour Lane and the house number in the description, and the Agent gives a request number.
- A question about districts: "Which streets are in the Old Town district?" Mill Road, High Street and Station Road.
- An address the registry does not know: "Which day is the grey bin collected at 3 Castle Street?" The Agent says that it does not know that address and asks you to check it. With reasoning, the steps show the lookup and no call to `get_collection_days`.

Ask the first question again with reasoning. The steps show two tool calls in order: `utopia_addresses:lookup_address` with the address as typed, returning Elm Street, then `get_collection_days` with Elm Street. The toolkit's tool carries the toolkit's name in front, and the chapter 6 Tool does not.

## 8.9 Deploy the change in Live

Mode: Agent, same conversation.

A toolkit belongs to the instance, like a Tool, so Live needs only the Agent. On the Developer Edition, skip this section. If you skipped chapter 7, the Connection `utopia_311` exists for Draft only; send the first prompt of section 7.10 before the deployment, or the Agent in Live fails at its first report.

```
Deploy civic_info_agent from draft to live.
```

When Bob reports the deployment, go to the watsonx Orchestrate chat and ask the question of the Overview: a resident who writes "18 elm st" gets the collection days of Elm Street.

## 8.10 Summary

The Agent now understands addresses the way residents write them, through a service of the kind that a city offers to every system, and the same program answered Bob's test calls before it answered residents. Bob wrote the server, tried it as a client, imported it as an Orchestrate Toolkit, and changed the Agent; you described the registry, fixed its data, and approved the design.

- An MCP server is a program that offers tools over a standard protocol to any client: Bob, other assistants, watsonx Orchestrate.
- An Orchestrate Toolkit holds several tools as one asset; the MCP kind is an MCP server registered on the instance. The Agent sees each tool as `toolkit:tool` and uses it like any other Tool.
- A local toolkit is a folder that the platform runs; a remote toolkit is a server reached over HTTP. A toolkit is updated by removing it and importing it again; the Agents that use it are then imported again, and deployed again where they are in Live.
- Bob creates MCP servers itself, and uses them as a client before the platform does.

The Agent of CivicPulse now knows the departments, searches the regulations, looks up records, reports problems and resolves addresses, all from one set of instructions that has grown with every chapter. In chapter 9, that one Agent becomes several: a front desk Agent that talks to residents, and one Agent per department behind it, each with the Tools and the knowledge of its own domain.
