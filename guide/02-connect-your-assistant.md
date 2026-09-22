# Chapter 2. Connect Bob to watsonx Orchestrate

Level: beginner. Time: about 30 minutes. Prerequisites: IBM Bob installed, and a watsonx Orchestrate instance you can log in to.

## What this chapter is about

At the end of this chapter Bob is connected to your Orchestrate instance and works inside one project folder, the one you clone from this guide's repository. Bob can list what is on your instance, and every later chapter starts from here.

What you will be able to do afterwards:

- Clone the guide's repository from inside Bob and connect it to your instance with the watsonx Orchestrate ADK extension, without typing a command.
- Decide which operations Bob may run without asking you.
- Keep your work in git through Bob.
- Recognise the common setup failures and fix them.

Skip this chapter if the checklist in 2.7 answers yes on every line for the folder you have open in Bob.

## 2.1 Before you start

Have these at hand.

| You need | Where it comes from |
|---|---|
| IBM Bob 2.1 or later | Installed and open |
| Git | Installed on your machine; Bob uses it to clone. You will not type git commands |
| An Orchestrate instance | A SaaS tenant on IBM Cloud or AWS, or the Developer Edition running on your machine |
| For a tenant: its URL and an API key | In the Orchestrate interface: your user icon, Settings, API details. The key is shown once; copy it into a file named `.env` in the project folder once you have cloned it (2.2, step 1), using `.env.example` as the model. Git ignores that file |

Nothing from IBM needs to be installed in advance. The extension installs what it needs inside the project folder.

Never paste the API key into a chat with Bob, and never write it into any other file.

## 2.2 Installation, step by step

Do the steps in this order. Each one says what you should see before going to the next.

Step 1. Clone the repository.

1. In Bob, click the files icon at the top left. With no folder open, the panel shows two buttons: Open Folder and Clone Repository.
2. Click Clone Repository and paste `https://github.com/DanielLopezSainz/WatsonxOrchestrate_AICoding_Assistant.git`.
3. Choose where to save it. Bob creates a folder named `WatsonxOrchestrate_AICoding_Assistant` there.
4. When Bob offers to open the cloned repository, click Open.

You should see: the folder name at the top of the panel. If Bob's chat is in front, click the files icon to see the files, among them `AGENTS.md`, `guide` and empty folders such as `agents` and `tools`.

Step 2. Install the extension.

1. Open the Extensions view: `Cmd Shift X` on a Mac, `Ctrl Shift X` elsewhere.
2. Search for `watsonx Orchestrate ADK`, publisher watson-devex, and click Install.

You should see: a watsonx Orchestrate icon in the left bar. If the bar is full, the icon is under the three dots at its bottom.

Step 3. Initialise the workspace.

1. Click the watsonx Orchestrate icon. Its panel has two sections, Explorer and Environment Manager.
2. If the panel says the extension loaded in restricted mode, click its link to trust the folder, confirm, and reload the window when asked. Bob asks this question once per folder.
3. In Explorer, click the link Initialise Workspace.
4. If Bob asks permission to install `uv`, accept.
5. If you use a tenant, a box asks for your API key: paste it. If the Developer Edition is running on your machine, nothing is asked.
6. Wait. The extension installs a Python environment and the ADK inside the folder; this takes a minute or two.
7. When the chat shows a ready-made message headed "SYSTEM PROMPT - IBM watsonx Orchestrate", send it. Bob answers that the session is ready.

You should see: the Explorer section listing the agents on your instance. A new tenant shows `AskOrchestrate`; a new Developer Edition also shows `DocProcessing`.

Step 4. Check the two servers.

1. Open Bob's settings with the settings icon in the Bob panel, then the MCP tab.
2. Find the two entries `watsonx-orchestrate-adk` and `watsonx-orchestrate-adk-docs`.

You should see: both marked as connected, and about sixty operations listed under the first one when you expand it.

Step 5. Set the approvals.

1. In the auto-approve toolbar above the chat, switch on Read and MCP. Leave Edit and Execute off.
2. In the MCP tab, expand `watsonx-orchestrate-adk` and switch on Always allow for these operations only: `check_version`, `list_agents`, `list_tools`, `list_toolkits`, `list_knowledge_bases`, `list_connections`, `list_models`, `export_agent`, `export_tool`, `export_toolkit`, `chat_with_agent`.

You should see: nothing yet. The effect shows in the next step, where Bob lists agents without asking you first.

Step 6. Prove the connection. Start a new chat, choose Ask mode in the dropdown at the bottom of the chat, and send:

```
Which agents exist on my instance? List their names and one line each.
```

You should see: Bob calling the server, visible above its answer, and the same agents the Explorer showed. If Bob asks for approval first, step 5 was skipped. If the answer mentions a working directory, a forbidden path or an authentication problem, go to 2.8.

The setup is complete. What each step installed is explained next; the chapters that build things start at chapter 3.

## 2.3 What was installed, and the three things to remember

Two IBM packages now sit inside your project folder.

| Package | What it is |
|---|---|
| The watsonx Orchestrate Agent Development Kit, the ADK | IBM's toolkit for defining agents, tools and everything around them as files, and for pushing those files to an instance. It also provides the `orchestrate` command, which this guide never asks you to type |
| The watsonx Orchestrate MCP server | A small program that lets Bob use the ADK: list, import, test and export things on your instance. Bob starts it when needed. MCP is the standard by which coding assistants talk to programs like this one; nothing more about it is needed |

A third piece is remote: IBM's documentation server, which gives Bob a search over the Orchestrate documentation. The extension connected it too, so that Bob looks things up instead of guessing.

The extension also created, inside the folder: `venv`, the Python environment with the ADK; `workspace_config.yaml`, which records where agents, tools and the rest live; and `.bob/mcp.json`, the settings that tell Bob how to start the two servers. None of them needs editing.

Three things to remember for the whole guide.

1. One folder. Bob works inside the cloned repository and nowhere else. The server refuses to read or write outside it, and the extension recorded that folder when you initialised it. Always open this folder in Bob; do not initialise another one and then work here.
2. The token lasts two hours. The API key you gave produced a token that expires after two hours. When it does, everything Bob tries fails with an authentication error until you activate the environment again from the Environment Manager. If Bob suddenly cannot do what it did an hour ago, this is the first thing to check.
3. The active environment is shared. The ADK keeps one active environment per machine, and every assistant on the machine uses it. Switching it in the Environment Manager switches it for all of them. Only chapter 11 switches environments, on purpose.

Developer Edition instead of a tenant: it registers itself as an environment named `local`, needs no key, and the Environment Manager starts and stops it. It has only a draft environment, so nothing can be deployed on it, and it does not process uploaded documents unless started with the document-processing option. Everything else in this guide works on it.

## 2.4 The approvals, explained

Bob asks your permission before it acts, and two settings decide how often.

- The auto-approve toolbar above the chat has one switch per category. Read lets Bob read files without asking. MCP lets it run Orchestrate operations without asking, but only the ones you mark individually. Edit and Execute cover writing files and running commands; leave them off while learning, so that Bob asks before either.
- The Always allow switch on each operation in the MCP tab marks that operation as safe. Step 5 marked the eleven that only read from the instance or send a test message. Every other operation, importing, creating, removing, setting credentials, still asks.

That is the intended balance: reading is free, changing asks. Do not mark every operation to save clicks. An assistant that can remove agents and set credentials without a prompt is not something to run against an instance you care about.

One more Bob setting. Do not run Bob's `/init` command in this folder. It generates an `AGENTS.md` by scanning the project and would offer to overwrite the one that came with the repository. Chapter 3 explains what that file does.

## 2.5 Other AI coding assistants

The instructions and rules in the repository work for any assistant, and the server is the same. Cursor and VS Code with Copilot have the same extension and the same steps; their rule files are in the repository. Claude Code and Claude Desktop connect through a settings file that names the server and the folder; `CLAUDE.md` in the repository makes Claude Code read the same instructions. IBM documents the installation for each at https://developer.watson-orchestrate.ibm.com/mcp_server/wxOmcp_installation. This guide follows Bob only.

## 2.6 Keeping your project in git, from Bob

The definition files Bob writes are the real product of this guide, and being able to go back to yesterday's version is what lets you let Bob work. The folder is a clone, so it is already a git repository. Bob does the rest through prompts in Agent mode; before each git command it shows the command and asks.

First, where your commits go. The clone points at the guide's repository, which you cannot push to. Two ways to fix that:

- Fork before cloning: on the repository's GitHub page, click Fork, then clone the fork's address in step 1 instead. Pushes work, and GitHub's Sync fork button brings in guide updates later.
- Or create an empty repository in your GitHub account and send:

```
Change the remote named origin to https://github.com/<your-account>/<your-repo>.git
and push the current branch to it.
```

The first push asks for your GitHub credentials, as any git client does.

Then, after each chapter:

```
Stage all my changes, show me the list of files, commit them with a short
message that summarises what was built, and push.
```

Bob composes the message and asks you to approve `git add`, `git commit` and `git push`. The Source Control icon in the left bar, the branch symbol, does the same by clicking. `/review` in the chat reviews your uncommitted changes, and `/create-pr` opens a pull request, signing in to GitHub in a browser the first time.

Two cautions. The settings files and the `venv` folder are ignored by git, so a clone on another machine needs Initialise Workspace again. And never ask Bob to commit a file with an API key in it; `.env` is ignored for that reason.

## 2.7 Checklist

Answer every line with yes before moving on.

1. The folder open in Bob is the cloned repository, and it is the one you initialised.
2. `AGENTS.md` is visible at the top level of that folder, next to the `.bob` folder.
3. The MCP tab shows `watsonx-orchestrate-adk` and `watsonx-orchestrate-adk-docs`, both connected.
4. Read and MCP are on in the toolbar, Edit and Execute are off, and Always allow is on for the eleven reading operations.
5. The Environment Manager shows an active environment.
6. The agent list prompt returns the agents you expect, without an approval request.
7. You have not run `/init`.

## 2.8 When something goes wrong

Five failures, each seen while preparing this guide, with the message and the fix.

| Bob reports | Cause | Fix |
|---|---|---|
| `Attempting to access resources outside the working directory is forbidden.` | The folder open in Bob is not the one that was initialised, or Bob is pointing at a file elsewhere on your disk | Open the initialised folder. If you must change folders, run Update MCP Servers from the command palette with the right folder open |
| Every operation fails with an authentication or authorization error after working earlier | The two-hour token expired | Activate the environment again in the Environment Manager; the next call works without a restart |
| An artifact was imported, but the list of the instance does not show it | Some operations report success even when the platform logged an error; the knowledge base import with an unsupported document type does this | Trust the list, not the message. The rules make Bob check after every change for this reason |
| A Python tool import fails with `No module named '<tool>'` although the file exists | Bob tried to import from that folder before it existed, and the server remembers the failure while it runs | Restart the server with the restart control in the MCP tab, then import again |
| The server command is not found, or the entry will not start | The environment the extension created is damaged or was moved | Run Initialise Workspace again; it repairs it |

One more that is not a failure: after Bob chats with an agent that has no tools, it reports that the reasoning came back empty. That is expected; chapter 4 explains it.
