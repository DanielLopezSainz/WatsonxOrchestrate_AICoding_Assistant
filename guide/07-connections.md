# Chapter 7. Reporting an issue: connections

Level: beginner. Time: about 60 minutes. Prerequisites: chapter 6 completed, or its tools and agent imported from the walkthrough folder as that chapter's Overview describes.

## Overview

A pothole outside 18 Elm Street has been there for a month, and you are the resident who hits it every morning. You ask CivicPulse: "There is a pothole outside 18 Elm Street. Can you report it?" The agent of chapter 6 can tell you the status of a report that exists. It cannot create one. Reporting a pothole means writing a record into the city's service desk, and the service desk, like every real system, asks who is calling: it wants an API key with every request.

That key is the subject of this chapter. The agent needs it to report the pothole; nobody else should ever see it. Not the resident, not the chat, not the project folder in git, not the code of the tool, and not Bob. In watsonx Orchestrate, a credential like this lives in a connection: a named place on the instance where the key is stored, and from which a tool receives it at the moment it calls the service.

In this chapter, Bob writes a tool that reports an issue to the service desk and a connection that holds the service desk's key. Bob never sees the key: you set it yourself, in watsonx Orchestrate, the way an operations team sets production credentials. Then the agent reports the pothole and gives the resident a request number.

The component introduced in this chapter is the connection. The tool is of the kind you know from chapter 6, with one difference: it acts instead of reading.

Skip this chapter if you have already given a tool a credential through a connection with Bob. To continue with chapter 8 without building it, send Bob these instructions in Agent mode: `Import walkthroughs/ch07/connections/utopia_service_desk.yaml into my instance, import the tool in walkthroughs/ch07/tools packaged with its folder, then import walkthroughs/ch07/agents/civic_info_agent.yaml.` Then set the credential of the connection as section 7.6 describes.

## 7.1 Before you start

- The setup from chapter 2, complete.
- The agent `civic_info_agent` from chapter 6 on your instance, in Draft, with its three tools. If you skipped chapter 6, import them as described in that chapter's Overview.
- A new conversation in Bob for this chapter.

Check that the tools are there: in Ask mode, ask `Which tools exist on my instance?` and confirm that `get_permit_status`, `get_request_status` and `get_collection_days` are listed.

## 7.2 What a connection is

A tool that calls a service needs two things: the address of the service and a credential that the service accepts. The address can be written in the tool. The credential cannot: a key in the code is a key in git, in every copy of the project, and in every chat where the file is shown.

A connection is where watsonx Orchestrate keeps the credential instead. It has a name, the kind of credential (an API key, a user and password, a token, an OAuth login), the address of the service, and the credential itself. A tool names the connection it needs. When the agent calls the tool, the platform hands the tool the credential; the tool uses it and never stores it.

**Two parts, two owners**

A connection is defined in a file, like an agent or a tool, and the file contains no secret: the name, the kind, the address. That file is the developer's; it goes into git and Bob imports it. The credential is set separately, on the instance, by the person who holds it. In a company, that is the team that owns the service or the operations team, and the developer never sees the production key. In this guide you play both roles: Bob imports the connection, and you set the credential yourself in watsonx Orchestrate.

**One credential per environment**

The credential is stored per environment: the connection has one value for Draft and one for Live. You test in Draft with a test key; operations sets the production key in Live when the agent is deployed. Deploying the agent does not copy the credential; section 7.9 sets the Live value before the deployment.

**Shared or personal**

A connection is either shared by everyone, `team`, with one credential that an administrator sets, or personal, `member`, where each user is asked for their own credential in the chat the first time. The city's service desk account is shared, so the connection of this chapter is a team connection.

**The service desk of this chapter**

The City of Utopia has no service desk, so this chapter uses a public test service, Postman Echo, which answers every request by sending back what it received, including the headers. That is enough for the mechanism to be real: the tool sends the report with the key in a header, and it treats the report as accepted only if the service echoes that header back. The key is a value you invent. A real service desk would also return a request number; the test service does not, so the tool creates one in the format of chapter 6, and the chapter says so where it matters.

## 7.3 Ask mode: describe the report

Mode: Ask, in a new conversation.

The purpose of this prompt is the same as in the earlier chapters: before anything is written, Bob must understand what you want and tell you what it needs to know. The request has a new element, a service that needs a key, and the prompt says what the key must never touch.

```
I want civic_info_agent to report a road problem to the city's service desk
when a resident asks it to, for example "There is a pothole outside 18 Elm
Street. Can you report it?". The service desk is reached over an API that needs
an API key with every request, and the key must never appear in the chat, in
the project files or in the tool's code. The City of Utopia has no service desk:
use the public test service at https://postman-echo.com/post, which returns
what it receives, and treat a report as accepted when the service echoes the
key header back.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Read Bob's answer for three things:

- How Bob keeps the key out of everything: it proposes a connection on the instance, with the tool reading the key from it at run time. That is the right choice, and 7.2 says why.
- What it found on the instance: the agent, the knowledge base, the three tools, and no connection.
- Its questions: what the report contains, how the request number is made, what the agent says back, and whether the connection is shared or personal.

The second prompt answers them. It also names the connection, so that the chapter and the walkthrough files agree.

```
These are my answers. The connection is named utopia_service_desk, shared by
the whole team, with the key sent in the header x-api-key. One tool,
report_issue, which receives the street and a description of the problem,
sends them to the service desk with the key from the connection, and returns a
request number in the format RQ-2026-NNNN that the tool generates, since the
test service returns none. If the service does not echo the key header back,
the tool reports a failure and the agent says that the report could not be
sent and gives the contact of Roads and Infrastructure.

The agent uses the tool when a resident asks to report a road problem. Before
calling it, the agent makes sure it has the street and a description; it asks
for whatever is missing. After a successful report, the agent gives the
resident the request number and says that the status can be checked with it.
The facts, the knowledge base and the three lookup tools stay as they are.
```

Bob confirms the answers and lays out the implementation in the chat, as in chapter 6: the connection file, the tool, the change to the agent. Do not switch to Agent mode yet.

## 7.4 Plan mode: write the design

Mode: Plan, in the same conversation.

```
Write the design for this change into design/report-issue-design.md.
```

Bob asks for approval to write the file, writes it, and shows a summary. Open the file and check that it contains the following:

| Content | What to check |
|---|---|
| The connection | Its name, `utopia_service_desk`; the kind, an API key sent in the header `x-api-key`; the address of the service; shared by the team; defined for Draft and for Live |
| The credential | The design says that the credential is set by you in watsonx Orchestrate, after the import, and that no file and no prompt contains it |
| The tool | `report_issue`, its two parameters, the connection it uses, the check on the echoed header, the request number it returns |
| The change to the agent | The tool attached; the instructions say when to use it, what to ask for first, what to answer on success and on failure; everything else unchanged |
| The build order | Connection, tool packaged with its folder, agent; then the credential, set by you; then the tests |
| The tests | The pothole report of the Overview at least, with what the agent must answer |

## 7.5 Approve the design

Mode: Plan, same conversation.

Read the design once. If something is missing or wrong, ask Bob to change it, as in chapter 4. Check one point in particular: the design must not contain a key value, not even an example. If it does, send `Remove every credential value from the design. The credential is set in watsonx Orchestrate, not in a file.` When the design says what you mean, it is approved.

## 7.6 Agent mode: build, set the credential, test

Mode: Agent, in a new conversation.

```
The design in @design/report-issue-design.md is approved. Build it. Stop
before the tests and tell me when the connection is ready for its credential.
```

The second sentence is new. Bob can build everything, but it cannot set the credential, because it must not have it. Bob:

1. Writes the connection file in the `connections` folder and imports it, for Draft and for Live.
2. Writes the tool in the `tools` folder and imports it, packaged with its folder.
3. Updates the agent: the tool is attached, the instructions are extended, and the agent is imported again, replacing the agent in Draft.
4. Stops and tells you that the connection `utopia_service_desk` is waiting for its credential.

Now set it. Open your watsonx Orchestrate instance in the browser, go to the Connections page, and find `utopia_service_desk`. Enter the key for the Draft environment: any value you invent, for example a word and a number. Save it. Nothing in Bob's conversation has seen it.

Tell Bob to continue:

```
The Draft credential is set. Run the tests.
```

Bob asks the agent to report the pothole of the Overview and reports the answer.

If the test fails with an authentication error, the credential was saved under the wrong environment or the wrong connection; check the page and run the test again. If it fails because the tool could not read the connection, the tool's code names a different connection than the one you set; Bob reads the error and corrects it.

## 7.7 What Bob built

Open the `connections` folder in the File Explorer and the file `utopia_service_desk.yaml`. It is a few lines: the name, and for each environment, Draft and Live, the kind of credential, `api_key`, the header name, `x-api-key`, the address of the service, and the type, `team`. Read it twice: there is no key in it. This file can be shared with anyone.

Open `tools/report_issue.py`. Two things are new compared with the tools of chapter 6. The `@tool` line names the connection the tool expects, `utopia_service_desk`. And near the top of the function, one line asks the platform for the credential, and the key arrives in a variable that the function uses in the request header and nowhere else. The function then sends the report, checks that the echo contains the header, builds the request number, and returns it.

Open `agents/civic_info_agent.yaml`. Under `tools`, a fourth name, `report_issue`. The instructions have a new paragraph: when a resident asks to report a road problem, get the street and the description, call the tool, and answer with the request number, or with the Roads and Infrastructure contact if the report could not be sent.

Save your work: `Commit everything I changed with a short message saying what was built, and push.`

## 7.8 Try it

Ask the agent, through Bob with `Ask civic_info_agent:` in front, or in the preview panel of watsonx Orchestrate:

```
There is a pothole outside 18 Elm Street. Can you report it?
```

The agent reports it and answers with a request number in the RQ-2026 format, and says that the status can be checked with that number. Then ask as residents do:

- Without a street: "I want to report a broken street light." The agent asks where.
- With everything in one sentence: "Report a damaged road sign at the corner of Mill Road and Station Road, it has been down since Monday." One report, one number.
- A check on the number you were given: "Has my report RQ-2026-NNNN been scheduled?", with the number from the first answer. The agent looks it up with the chapter 6 tool and finds no record, because the test service keeps nothing. A real service desk would have the record, and the chapter 6 tool would find it. The agent says that it has no record under that number and gives the contact, which is the right answer for a number that is not in its records.

Ask the first question again with reasoning. The steps show the call to `report_issue` with the street and the description, and the tool's result with the request number. The key is not in the steps: the tool received it from the connection and did not return it.

## 7.9 Deploy the change in Live

Mode: Agent, same conversation.

The agent that reports issues exists in Draft, and the connection has a credential for Draft only. The agent deployed in Live would fail at the first report. In a company, operations sets the Live credential before the deployment; here you do it yourself.

In the Connections page of watsonx Orchestrate, enter the key for the Live environment of `utopia_service_desk` and save it. Then:

```
Deploy civic_info_agent from draft to live.
```

Bob reports that the agent is deployed. Go to the watsonx Orchestrate chat and report the pothole: the resident of the Overview gets a request number. On the Developer Edition, skip this step.

## 7.10 Summary

The agent can now act on a resident's behalf: it reports a pothole to the city's service desk and gives the resident a request number. Bob wrote the tool, the connection and the change to the agent; you set the credential, in Draft and in Live, and Bob never saw it.

- A connection is where watsonx Orchestrate keeps a credential for a service. A tool names the connection it needs and receives the credential at run time; the credential is in no file, no prompt and no chat.
- The connection is defined by the developer and imported with the project. The credential is set on the instance by the person who holds it, once per environment, Draft and Live.
- A connection is shared by the team, one credential for all users, or personal, one credential per user, asked for in the chat.
- A tool that acts is built like a tool that reads: a function, a description, parameters, a result. The agent decides when to call it from the description and the question.

The agent now looks up records and creates them, with three Python tools that Bob wrote and that the city maintains. Many services come with their tools ready: an MCP server offers a set of tools that any agent can use, and watsonx Orchestrate can import the whole set at once as a toolkit. In chapter 8, Bob builds one, with a skill made for that, and the agent gets an address lookup from it.
