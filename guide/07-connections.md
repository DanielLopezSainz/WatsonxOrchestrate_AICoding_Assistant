# Chapter 7. Reporting an issue: Orchestrate Connections

Level: beginner. Time: about 60 minutes. Prerequisites: chapter 6 completed, or its Tools and Agent imported from the walkthrough folder as that chapter's Overview describes.

## Overview

A pothole outside 18 Elm Street has been there for a month, and you are the resident who hits it every morning. You ask CivicPulse: "There is a pothole outside 18 Elm Street. Can you report it?" The Agent of chapter 6 can tell you the status of a report that exists. It cannot create one.

In this chapter, Bob creates an Orchestrate Tool that sends reports to the city's service desk. The Orchestrate Agent sends the resident's data to an external system, a database or an application, using an Orchestrate Tool (you built one in chapter 6). The address of that external system and the credentials that it requires are not written in the Tool: watsonx Orchestrate stores them in a separate asset, the Orchestrate Connection, and gives them to the Tool when the Agent calls it.

The Orchestrate Connection is the component introduced in this chapter. Bob creates both the Orchestrate Connection and the Orchestrate Tool. With Orchestrate Tools and Orchestrate Connections, the Agent can update external systems, not only read them.

Skip this chapter if you have already given a Tool a credential through a Connection with Bob. To continue with chapter 8 without building it, send Bob these instructions in Agent mode: `Import walkthroughs/ch07/connections/utopia_service_desk.yaml into my instance, import the tool in walkthroughs/ch07/tools packaged with its folder, then import walkthroughs/ch07/agents/civic_info_agent.yaml.` Then set the credential of the Connection as section 7.6 describes.

## 7.1 Before you start

- The setup from chapter 2, complete.
- The Agent `civic_info_agent` from chapter 6 on your instance, in Draft, with its three Tools. If you skipped chapter 6, import them as described in that chapter's Overview.
- A new conversation in Bob for this chapter.

Check that the Tools are there: in Ask mode, ask `Which tools exist on my instance?` and confirm that `get_permit_status`, `get_request_status` and `get_collection_days` are listed.

## 7.2 What an Orchestrate Connection is

A Tool that calls a service needs two things: the address of the service and a credential that the service accepts. The address can be written in the Tool. A key written in the code would be copied into git, into every copy of the project and into every chat that shows the file, so the credential is kept elsewhere.

An Orchestrate Connection is where watsonx Orchestrate keeps the credential instead. It has a name, the kind of credential (an API key, a user and password, a token, an OAuth login), the address of the service, and the credential itself. A Tool names the Connection it needs. When the Agent calls the Tool, the platform hands the Tool the credential; the Tool uses it and never stores it.

**The definition and the credential**

An Orchestrate Connection is defined in a file, like an Orchestrate Agent or an Orchestrate Tool, and the file contains no secret: the name, the kind, the address. That file is the developer's; it goes into git and Bob imports it. The credential is set separately, on the instance, by the person who holds it. In a company, that is the team that owns the service or the operations team, and the developer never sees the production key. In this guide you play both roles: Bob imports the Connection, and the key comes from your `.env` file, the file that chapter 2 created for secrets and that git ignores.

**One credential per environment**

The credential is stored per environment: the Connection has one value for Draft and one for Live. You test in Draft with a test key; operations sets the production key in Live when the Agent is deployed. Deploying the Agent does not copy the credential. In this chapter, the Connection is defined for Draft first; section 7.10 adds the Live environment and its key before the deployment.

**Shared or personal**

A Connection is either shared by everyone, `team`, with one credential that an administrator sets, or personal, `member`, where each user is asked for their own credential in the chat the first time. The city's service desk account is shared, so the Connection of this chapter is a team Connection.

**The service desk of this chapter**

The City of Utopia has no service desk, so this chapter uses a public test service, Postman Echo, which answers every request by sending back what it received, including the headers. The mechanism is the same as with a real service desk: the Tool sends the report with the key in a header, and it treats the report as accepted only if the service echoes that header back. The key is a value you invent. A real service desk would also return a request number; the test service does not, so the Tool creates one in the format of chapter 6.

## 7.3 Ask mode: describe the report

Mode: Ask, in a new conversation.

The prompt describes what residents need and which system is involved, and says nothing about how that system is reached or secured. As before, Bob must understand the request before anything is written, and this time the question of credentials is Bob's to raise.

```
I want civic_info_agent to report a road problem to the city's service desk
when a resident asks it to, for example "There is a pothole outside 18 Elm
Street. Can you report it?". The service desk is an external system, and the
city has not given us access yet, so for now the public test service at
https://postman-echo.com/post, which returns what it receives, stands in for
it.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Three things to find in Bob's answer:

- The Connection. Nobody mentioned credentials, and Bob raises them: the test service needs none, but the real service desk will need an address and an API key, so Bob asks whether to create a Connection now, so that the Tool is wired correctly when the city gives access. Section 7.2 explains what a Connection is. If your Bob does not raise it, the answer below does.
- What it found on the instance: the Agent, the Knowledge Base, the three Tools, an empty `connections` folder, and the line in the Agent's instructions from chapter 4 that forbids creating requests, which Bob says must change.
- Its questions, which vary from one run to another: what the report contains, as free text or from a fixed list of problem types, and whether residents identify themselves; what the Agent says back, and what reference number it gives, since the test service returns none; whether the Agent confirms the details before sending; and how the real service desk authenticates.

These are the questions that an integration engineer asks before connecting anything to an external system: how the system authenticates, what a request carries, and what happens when it fails. Bob asked them without being told that the service desk needs a key. The second prompt answers them, and names the Connection and the header, so that the chapter and the walkthrough files agree.

```
These are my answers. Create the connection now: the real service desk will
require an API key with every request, and the tool must send it from the
start, so that only the address and the key change when the city gives
access. The connection is named utopia_service_desk, shared by the whole team,
with the key sent in the header x-api-key. For now the key is a test value
that I invent, since the test service accepts anything, but it is stored and
used exactly as the real key will be. The key must never appear in the chat,
in the project files or in the tool's code. It is in my .env file, as the
variable SERVICE_DESK_API_KEY, and the credential is set from that variable
without displaying its value.

One tool, report_issue, which receives the street and a free-text description
of the problem, with no category and no resident details, since reports are
anonymous. It sends them to the service desk with the key from the connection
and returns a request number in the format RQ-2026-NNNN that the tool
generates, since the test service returns none. The tool treats a report as
accepted only if the service echoes the key header back; otherwise it reports
a failure, and the agent says that the report could not be sent and gives the
contact of Roads and Infrastructure.

The agent uses the tool when a resident asks to report a road problem. It
sends the report as soon as it has the street and a description, without a
confirmation step, and asks for whatever is missing. After a successful
report, the agent gives the resident the request number and says that the
status can be checked with it. The line that forbids creating requests is
replaced by this tool. The facts, the knowledge base and the three lookup
tools stay as they are.
```

Bob confirms the answers and lays out the implementation in the chat, as in chapter 6. Three things to check in it:

- The Connection file has no key in it: a name, the kind of credential, the type `team`, the address of the service.
- In the Tool, one line asks the platform for the key at run time, and the key goes into the request header and nowhere else.
- Bob sets the key from the variable in `.env`, with a command whose output does not show the value, and never asks you to paste it in the chat.

Do not switch to Agent mode yet.

## 7.4 Plan mode: write the design

Mode: Plan, in the same conversation.

```
Write the design for this change into design/report-issue-design.md.
```

Bob writes the file after your approval and summarises it. Open it and check the following:

| Content | What to check |
|---|---|
| The Connection | Its name, `utopia_service_desk`; the kind, an API key sent in the header `x-api-key`; the address of the service; shared by the team; defined for Draft. Live is added in 7.10 |
| The credential | The design says that the credential is set from the variable `SERVICE_DESK_API_KEY` in `.env`, after the import, without displaying it, and that no other file and no prompt contains it |
| The Tool | `report_issue`, its two parameters, the Connection it uses, the check on the echoed header, the request number it returns |
| The change to the Agent | The Tool attached; the instructions say when to use it, what to ask for first, what to answer on success and on failure; everything else unchanged |
| The build order | Connection, Tool packaged with its folder, Agent, the credential from `.env`, then the test |

## 7.5 Approve the design

Mode: Plan, same conversation.

There is no prompt to send in this section unless the design needs a change. Read the design against the table in 7.4, and check one point in particular: it must not contain a key value, not even an example. If it does, send `Remove every credential value from the design. The credential is set on the instance, not in a file.` If something else is missing, ask Bob to add it. When the design is correct, go to 7.7: its first prompt is the approval.

## 7.6 Where the key comes from

The Connection that Bob imports has a name and a kind but no key. The key is yours to provide, and it must not pass through the chat. The guide keeps it where chapter 2 keeps the other secret of the project: the `.env` file in your project folder, which git ignores. Open `.env` and add one line, with a value you invent:

```
SERVICE_DESK_API_KEY=<a word and a number>
```

Bob sets the credential from that variable: it runs the ADK command that stores the key on the instance for one environment, and the shell fills in the value, so that the key appears neither in the conversation nor in any file of the project other than `.env`. In a company, the value comes from a vault instead of a `.env` file, and the command is the same one that a deployment pipeline runs.

## 7.7 Agent mode: build and test

Mode: Agent, in a new conversation.

```
The design in @design/report-issue-design.md is approved. Build it. Set the
Draft credential of the connection from the variable SERVICE_DESK_API_KEY in
my .env file, without displaying its value, then test the agent with the
pothole report of the Overview.
```

The second sentence is new: it tells Bob where the key is and that the value must not be shown. Bob:

1. Writes the Connection file in the `connections` folder and imports it.
2. Writes the Tool in the `tools` folder and imports it, packaged with its folder.
3. Updates the Agent: the Tool is attached, the instructions are extended, and the Agent is imported again, replacing the Agent in Draft.
4. Sets the Draft credential from `.env` and tests the Agent with the pothole report.

Approve each request as it comes. Read the command that sets the credential when Bob asks for approval: it names the variable, not the value.

If the test fails with an authentication error, the credential was saved under the wrong environment or the wrong Connection. If it fails because the Tool could not read the Connection, the Tool's code names a different Connection than the one that was imported. In both cases Bob reads the error and corrects it.

## 7.8 What Bob built

Open the `connections` folder in the File Explorer and the file `utopia_service_desk.yaml`. It is a few lines: the name, and for the Draft environment, the kind of credential, an API key, the address of the service, and the type, `team`. It contains no key, so it can be shared and committed.

Open `tools/report_issue.py`. Two things are new compared with the Tools of chapter 6. The `@tool` line names the Connection the Tool expects, `utopia_service_desk`. And near the top of the function, one line asks the platform for the credential, and the key arrives in a variable that the function uses in the request header and nowhere else. The function then sends the report, checks that the echo contains the header, builds the request number, and returns it.

Open `agents/civic_info_agent.yaml`. Under `tools`, a fourth name, `report_issue`. The instructions have a new paragraph: when a resident asks to report a road problem, get the street and the description, call the Tool, and answer with the request number, or with the Roads and Infrastructure contact if the report could not be sent.

Save your work: `Commit everything I changed with a short message saying what was built, and push.`

## 7.9 Try it

Ask the Agent, through Bob with `Ask civic_info_agent:` in front, or in the preview panel of watsonx Orchestrate:

```
There is a pothole outside 18 Elm Street. Can you report it?
```

The Agent reports it and answers with a request number in the RQ-2026 format, and says that the status can be checked with that number. Then try three more:

- Without a street: "I want to report a broken street light." The Agent asks where.
- With everything in one sentence: "Report a damaged road sign at the corner of Mill Road and Station Road, it has been down since Monday." The Agent makes one report and returns one number.
- A check on the number you were given: "Has my report RQ-2026-NNNN been scheduled?", with the number from the first answer. The Agent looks it up with the chapter 6 Tool and finds no record, because the test service keeps nothing; a real service desk would have it. The Agent answers that it has no record under that number and gives the contact.

Ask the first question again with reasoning. The steps show the call to `report_issue` with the street and the description, and the Tool's result with the request number. The key is not in the steps: the Tool received it from the Connection and did not return it.

## 7.10 Deploy the change in Live

Mode: Agent, same conversation.

The Agent that reports issues exists in Draft, and the Connection exists for Draft only: deployed as it is, the Agent would fail at the first report. Going live takes two steps, in this order. In a company, the first is done by operations, with the production key; here it is Bob with your test key.

First, the Connection gets its Live environment and its Live key:

```
Define the connection utopia_service_desk for the Live environment as well,
with the same kind and type, import it again, and set its Live credential
from the variable SERVICE_DESK_API_KEY in my .env file, without displaying
its value.
```

Second, deploy:

```
Deploy civic_info_agent from draft to live.
```

When Bob reports the deployment, go to the watsonx Orchestrate chat and report the pothole: the resident of the Overview gets a request number. On the Developer Edition, skip this step.

## 7.11 Summary

The Agent can now act on a resident's behalf: it reports a pothole to the city's service desk and gives the resident a request number. The key lived in your `.env` file and on the instance, and nowhere else: not in the chat, not in git, not in the code.

- An Orchestrate Connection is where watsonx Orchestrate keeps a credential for a service. A Tool names the Connection it needs and receives the credential at run time; the credential is in no file, no prompt and no chat.
- The Connection is defined by the developer and imported with the project. The credential is set on the instance separately, once per environment, Draft and Live, from a place that git does not see.
- A Connection is shared by the team, one credential for all users, or personal, one credential per user, asked for in the chat.
- An Orchestrate Tool that acts is built like one that reads: a function, a description, parameters, a result. The Agent decides when to call it from the description and the question.

The Agent now looks up records and creates them, with four Python Tools that Bob wrote and that the city maintains. Many services come with their Tools ready: an MCP server offers a set of Tools that any Agent can use, and watsonx Orchestrate can import the whole set at once as an Orchestrate Toolkit. In chapter 8, Bob builds one, with a skill made for that, and the Agent gets an address lookup from it.
