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

1. Click the watsonx Orchestrate icon. A panel headed "Watsonx Orchestrate: Explorer" opens with the message "No workspace found. Please initialise a workspace to begin building" and a button, Initialise Workspace.
2. If the panel says instead that the extension loaded in restricted mode, click its link to trust the folder, confirm, and reload the window when asked. Bob asks this once per folder.
3. Click Initialise Workspace. A dialog asks "Initialize watsonx Orchestrate workspace in the current folder?" and shows the folder's path. Click Continue with Current Folder.
4. If Bob asks permission to install `uv`, accept.
5. Wait. A progress message counts through the steps; the extension installs a Python environment and the ADK inside the folder, which takes a minute or two.

You should see: the panel now has two sections. Explorer lists Agents, Tools, Connections, Knowledge Bases and Toolkits. Environment Manager shows an Environment dropdown and an Add button.

Step 4. Send Bob its starting message.

When initialisation ends, the extension quietly types a message into the box at the bottom of Bob's chat, where you normally write, and does not send it. It is easy to miss: no notification announces it, and the box looks as if you had typed something yourself. Look at the box before doing anything else.

1. Find the text headed "SYSTEM PROMPT - IBM watsonx Orchestrate" in the chat input box.
2. Press Enter to send it as it is.

Its three lines tell Bob to switch to Agent mode, to load IBM's Orchestrate skills, and to use the Orchestrate server for all agent, tool and environment operations and the documentation server for reference. If the box is empty because the text was cleared, paste this and send it:

```
# SYSTEM PROMPT - IBM watsonx Orchestrate
## Instructions
1. Switch to **Agent mode** if not already active.
2. Use the `fetch_all_skills` tool on the `watsonx-orchestrate-adk` MCP server to load available skills.
3. Use the fetched skills and `watsonx-orchestrate-adk` MCP for all agent, tool, and environment operations. Consult `watsonx-orchestrate-adk-docs` MCP for API reference and documentation guidance.
```

You should see: Bob answering that the skills are loaded, with a table of eight of them, and that it is in Agent mode. The skills now sit in `.bob/skills` in the folder; nothing before chapter 12 uses them. Bob may also ask how you want to proceed with the guide's example agent: it read that name from the walkthrough files in the repository, and no agent exists yet.

Step 5. Connect to your instance.

Your instance is the watsonx Orchestrate service where your agents will live: a SaaS tenant in IBM Cloud or AWS, or the Developer Edition running on your machine. The ADK calls a connection to an instance an environment. The Environment Manager section of the panel shows the environments that exist, and its dropdown shows which one is active; Bob works against the active one.

- Developer Edition running on your machine: nothing to do. The dropdown already reads `local (active)`, and below it "Local server: Started".
- SaaS tenant: the dropdown is empty. Click Add and answer four questions in turn: a name for the environment, for example `mytenant`; the instance URL from 2.1; Verify SSL (Recommended); and your API key, typed into a masked box. When asked whether to activate the environment now, say yes.

You should see: in Environment Manager, the dropdown reading your environment's name followed by "(active)". In Explorer, expand Agents: the list is read from the instance, so it shows the agents that exist there. A new tenant has one, `AskOrchestrate`. A new Developer Edition has two, shown as "Try Document Processing Agent (DocProcessing)" and "AskOrchestrate".

Step 6. Check that Bob reaches the two servers.

The extension gave Bob two connections: the Orchestrate server, through which Bob acts on your instance, and the documentation server, through which it looks up IBM's documentation. If either is down, nothing in the later chapters works.

1. Open Bob's settings with the settings icon in the Bob panel, then the MCP tab.
2. Find the two entries `watsonx-orchestrate-adk` and `watsonx-orchestrate-adk-docs`.

You should see: both marked as connected, and about sixty operations listed under the first one when you expand it.

Step 7. Set the approvals.

Bob asks your permission before every action unless you tell it otherwise. Left as it is, that means a click for each file Bob reads and each time it looks at your instance, dozens per chapter, and readers stop reading what they approve. Switched on entirely, Bob could write files, run commands and remove agents without a word. The settings below sit in between: Bob reads and looks without asking, and asks before anything that changes a file or the instance. Section 2.4 explains the two settings in more detail.

1. At the bottom of the chat input box, next to the dropdown where you choose the mode, click the Permissions button. A list of nine categories opens: Read, Edit, Execute, MCP, Skill, Todo, Subtask, Subagent, Mode. Switch on Read and MCP. Leave Edit and Execute off. The same list is in Bob's settings under Auto-Approve.
2. Open Bob's settings, MCP tab, expand `watsonx-orchestrate-adk`, and switch on Always allow for these operations only: `check_version`, `list_agents`, `list_tools`, `list_toolkits`, `list_knowledge_bases`, `list_connections`, `list_models`, `export_agent`, `export_tool`, `export_toolkit`, `chat_with_agent`.

You should see: nothing yet. The effect shows in the next step, where Bob lists agents without asking you first.

Step 8. Prove the connection. Start a new chat, choose Ask mode in the dropdown at the bottom of the chat, and send:

```
Which agents exist on my instance? List their names and one line each.
```

You should see: Bob calling the server, visible above its answer, and the same agents the Explorer showed. If Bob asks for approval first, step 7 was skipped. If the answer mentions a working directory, a forbidden path or an authentication problem, go to 2.8.

The setup is complete. What each step installed is explained next; the chapters that build things start at chapter 3.

## 2.3 The two views, and what was installed

Bob's left bar now has two icons that matter for this guide, and they show two different things.

| Icon | What it shows | Use it to |
|---|---|---|
| Files, at the top | The project folder on your disk: the repository's files, `AGENTS.md`, `guide`, `agents`, `tools` and the other folders, plus what the extension added | Read and edit the files Bob writes, definitions and designs, and keep them in git |
| watsonx Orchestrate | What is on your instance, read live from it: the Explorer lists its agents, tools, connections, knowledge bases and toolkits; the Environment Manager shows the environments and the local server | Check what really exists after Bob imports something, switch environment, start or stop the Developer Edition |

The two are connected by Bob's work: a definition is a file in the project folder until Bob imports it, and only then does it appear in the Orchestrate view. When the two disagree, the Orchestrate view is the truth about the instance and the file is the truth about what you decided. Chapter 4 uses both.

What connects Bob to the instance. Two IBM programs were installed in step 3 and do the work whenever Bob touches the instance; you never run them yourself, but their names appear in Bob's messages.

| Program | What it does |
|---|---|
| The watsonx Orchestrate Agent Development Kit, the ADK | Defines agents, tools and everything around them as files, and pushes those files to an instance |
| The watsonx Orchestrate MCP server | Lets Bob use the ADK: list, import, test and export things on your instance. Bob starts it when needed. MCP is the standard by which coding assistants talk to programs like this one; nothing more about it is needed |

A third connection, to IBM's documentation server on the internet, gives Bob a search over the Orchestrate documentation, so that it looks things up instead of guessing. That is the second entry you checked in step 6.

Three things to remember for the whole guide.

1. One folder. Bob works inside the cloned repository and nowhere else. The server refuses to read or write outside it, and the extension recorded that folder when you initialised it. Always open this folder in Bob; do not initialise another one and then work here.
2. The token lasts two hours. On a tenant, the API key you gave in step 5 produced a token that expires after two hours. When it does, everything Bob tries fails with an authentication error until you activate the environment again from the Environment Manager. If Bob suddenly cannot do what it did an hour ago, this is the first thing to check.
3. The active environment is shared. The ADK keeps one active environment per machine, and every assistant on the machine uses it. Switching it in the Environment Manager switches it for all of them. Only chapter 11 switches environments, on purpose.

## 2.4 The approvals, explained

Bob asks your permission before it acts, and two settings decide how often.

- The Permissions button below the chat input opens one switch per category. Read lets Bob read files without asking. MCP lets it run Orchestrate operations without asking, but only the ones you mark individually. Edit and Execute cover writing files and running commands; leave them off while learning, so that Bob asks before either.
- The Always allow switch on each operation in the MCP tab marks that operation as safe. Step 7 marked the eleven that only read from the instance or send a test message. Every other operation, importing, creating, removing, setting credentials, still asks.

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
4. Under the Permissions button, Read and MCP are on and Edit and Execute are off, and Always allow is on for the eleven reading operations.
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
