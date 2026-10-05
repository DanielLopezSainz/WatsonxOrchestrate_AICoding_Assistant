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

An Orchestrate Connection is defined in a file, like an Orchestrate Agent or an Orchestrate Tool, and the file contains no secret: the name, the kind, the address. That file is the developer's; it goes into git and Bob imports it. The credential is set separately, on the instance, by the person who holds it. In a company, that is the team that owns the service or the operations team, and the developer never sees the production key. In this guide you play both roles: Bob imports the Connection, and you set the credential yourself in watsonx Orchestrate.

**One credential per environment**

The credential is stored per environment: the Connection has one value for Draft and one for Live. You test in Draft with a test key; operations sets the production key in Live when the Agent is deployed. Deploying the Agent does not copy the credential; section 7.9 sets the Live value before the deployment.

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

- The credential. Nobody mentioned one, and Bob raises it: the service desk will require an API key, the key must not be written in the code or the prompts, and an Orchestrate Connection is where the key is kept and handed to the Tool when it runs. Section 7.2 explains why. If your Bob does not raise it, the answer below does.
- What it found on the instance: the Agent, the Knowledge Base, the three Tools, and no Connection.
- Its questions: the name, kind and scope of the Connection and the header for the key; the Tool's parameters; whether to generate a request number, since the test service returns none; what the Agent must collect before reporting and what it says on success and on failure.

The second prompt answers them. It names the Connection and the header, so that the chapter and the walkthrough files agree.

```
These are my answers. The connection is named utopia_service_desk, shared by
the whole team, with the key sent in the header x-api-key. One tool,
report_issue, which receives the street and a description of the problem,
sends them to the service desk with the key from the connection, and returns a
request number in the format RQ-2026-NNNN that the Tool generates, since the
test service returns none. The Tool treats a report as accepted only if the
service echoes the key header back; otherwise it reports a failure, and the
Agent says that the report could not be sent and gives the contact of Roads
and Infrastructure.

The agent uses the tool when a resident asks to report a road problem. Before
calling it, the agent makes sure it has the street and a description; it asks
for whatever is missing. After a successful report, the agent gives the
resident the request number and says that the status can be checked with it.
The facts, the knowledge base and the three lookup tools stay as they are.
```

Bob confirms the answers and lays out the implementation in the chat, as in chapter 6: the Connection file, the Tool, the change to the Agent. Do not switch to Agent mode yet.

## 7.4 Plan mode: write the design

Mode: Plan, in the same conversation.

```
Write the design for this change into design/report-issue-design.md.
```

Bob writes the file after your approval and summarises it. Open it and check the following:

| Content | What to check |
|---|---|
| The Connection | Its name, `utopia_service_desk`; the kind, an API key sent in the header `x-api-key`; the address of the service; shared by the team; defined for Draft and for Live |
| The credential | The design says that the credential is set by you in watsonx Orchestrate, after the import, and that no file and no prompt contains it |
| The Tool | `report_issue`, its two parameters, the Connection it uses, the check on the echoed header, the request number it returns |
| The change to the Agent | The Tool attached; the instructions say when to use it, what to ask for first, what to answer on success and on failure; everything else unchanged |
| The build order | Connection, Tool packaged with its folder, Agent; then the credential, set by you; then the tests |
| The tests | The pothole report of the Overview at least, with what the Agent must answer |

## 7.5 Approve the design

Mode: Plan, same conversation.

Read the design against the table in 7.4 and ask Bob to change what is missing. Check one point in particular: the design must not contain a key value, not even an example. If it does, send `Remove every credential value from the design. The credential is set in watsonx Orchestrate, not in a file.` When the design is correct, it is approved.

## 7.6 Agent mode: build, set the credential, test

Mode: Agent, in a new conversation.

```
The design in @design/report-issue-design.md is approved. Build it. Stop
before the tests and tell me when the connection is ready for its credential.
```

The second sentence is new: Bob builds everything except the credential, which it must not have. Bob:

1. Writes the Connection file in the `connections` folder and imports it, for Draft and for Live.
2. Writes the Tool in the `tools` folder and imports it, packaged with its folder.
3. Updates the Agent: the Tool is attached, the instructions are extended, and the Agent is imported again, replacing the Agent in Draft.
4. Stops and tells you that the Connection `utopia_service_desk` is waiting for its credential.

Open your watsonx Orchestrate instance in the browser, go to the Connections page, find `utopia_service_desk`, and enter the key for the Draft environment: any value you invent, for example a word and a number. Save it. The value never passes through Bob.

Tell Bob to continue:

```
The Draft credential is set. Run the tests.
```

Bob asks the Agent to report the pothole of the Overview and reports the answer.

If the test fails with an authentication error, the credential was saved under the wrong environment or the wrong Connection; check the page and run the test again. If it fails because the Tool could not read the Connection, the Tool's code names a different Connection than the one you set; Bob reads the error and corrects it.

## 7.7 What Bob built

Open the `connections` folder in the File Explorer and the file `utopia_service_desk.yaml`. It is a few lines: the name, and for each environment, Draft and Live, the kind of credential, `api_key`, the header name, `x-api-key`, the address of the service, and the type, `team`. It contains no key, so it can be shared and committed.

Open `tools/report_issue.py`. Two things are new compared with the Tools of chapter 6. The `@tool` line names the Connection the Tool expects, `utopia_service_desk`. And near the top of the function, one line asks the platform for the credential, and the key arrives in a variable that the function uses in the request header and nowhere else. The function then sends the report, checks that the echo contains the header, builds the request number, and returns it.

Open `agents/civic_info_agent.yaml`. Under `tools`, a fourth name, `report_issue`. The instructions have a new paragraph: when a resident asks to report a road problem, get the street and the description, call the Tool, and answer with the request number, or with the Roads and Infrastructure contact if the report could not be sent.

Save your work: `Commit everything I changed with a short message saying what was built, and push.`

## 7.8 Try it

Ask the Agent, through Bob with `Ask civic_info_agent:` in front, or in the preview panel of watsonx Orchestrate:

```
There is a pothole outside 18 Elm Street. Can you report it?
```

The Agent reports it and answers with a request number in the RQ-2026 format, and says that the status can be checked with that number. Then try three more:

- Without a street: "I want to report a broken street light." The Agent asks where.
- With everything in one sentence: "Report a damaged road sign at the corner of Mill Road and Station Road, it has been down since Monday." The Agent makes one report and returns one number.
- A check on the number you were given: "Has my report RQ-2026-NNNN been scheduled?", with the number from the first answer. The Agent looks it up with the chapter 6 Tool and finds no record, because the test service keeps nothing; a real service desk would have it. The Agent answers that it has no record under that number and gives the contact.

Ask the first question again with reasoning. The steps show the call to `report_issue` with the street and the description, and the Tool's result with the request number. The key is not in the steps: the Tool received it from the Connection and did not return it.

## 7.9 Deploy the change in Live

Mode: Agent, same conversation.

The Agent that reports issues exists in Draft, and the Connection has a credential for Draft only. The Agent deployed in Live would fail at the first report. In a company, operations sets the Live credential before the deployment; here you do it yourself.

In the Connections page of watsonx Orchestrate, enter the key for the Live environment of `utopia_service_desk` and save it. Then:

```
Deploy civic_info_agent from draft to live.
```

When Bob reports the deployment, go to the watsonx Orchestrate chat and report the pothole: the resident of the Overview gets a request number. On the Developer Edition, skip this step.

## 7.10 Summary

The Agent can now act on a resident's behalf: it reports a pothole to the city's service desk and gives the resident a request number. You set the credential in watsonx Orchestrate, in Draft and in Live; it is the one thing in this chapter that is not a file in your project, and Bob never saw it.

- An Orchestrate Connection is where watsonx Orchestrate keeps a credential for a service. A Tool names the Connection it needs and receives the credential at run time; the credential is in no file, no prompt and no chat.
- The Connection is defined by the developer and imported with the project. The credential is set on the instance by the person who holds it, once per environment, Draft and Live.
- A Connection is shared by the team, one credential for all users, or personal, one credential per user, asked for in the chat.
- An Orchestrate Tool that acts is built like one that reads: a function, a description, parameters, a result. The Agent decides when to call it from the description and the question.

The Agent now looks up records and creates them, with three Python Tools that Bob wrote and that the city maintains. Many services come with their Tools ready: an MCP server offers a set of Tools that any Agent can use, and watsonx Orchestrate can import the whole set at once as an Orchestrate Toolkit. In chapter 8, Bob builds one, with a skill made for that, and the Agent gets an address lookup from it.
