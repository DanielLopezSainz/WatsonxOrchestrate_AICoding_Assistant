# Chapter 2. Connect Bob to watsonx Orchestrate

Level: beginner. Time: about 30 minutes. Prerequisites: IBM Bob installed, and a watsonx Orchestrate instance you can log in to.

## Overview

Before Bob can create anything in watsonx Orchestrate, it must be connected to your instance. IBM provides an extension for Bob that does most of this work: it installs the toolkit that Bob uses, connects Bob to the instance, and prepares the project folder. This chapter takes you through the installation click by click, without typing a command.

At the end of the chapter:

- The guide's repository is open in Bob as your project folder.
- Bob is connected to your watsonx Orchestrate instance and can list what exists on it.
- Bob reads from the instance without asking, and asks for your approval before any change.

The installation is section 2.2. The sections after it explain what you installed and the views of Bob that the guide uses.

Skip this chapter if every line of the checklist in section 2.7 is already true for the folder that you have open in Bob.

## 2.1 Before you start

You need the following.

| You need | Where it comes from |
|---|---|
| IBM Bob 2.1 or later | Installed and open |
| Git | Installed on your machine; Bob uses it to clone. You will not type git commands |
| An Orchestrate instance | A SaaS tenant on IBM Cloud or AWS, or the Developer Edition running on your machine |
| For a tenant: its URL and an API key | In the Orchestrate interface: your user icon, Settings, API details. The key is displayed only once. After cloning the repository (2.2, step 1), copy the URL and the key into a file named `.env` in the project folder, using `.env.example` as the model. Git ignores this file |

Nothing from IBM needs to be installed in advance. The extension installs what it needs inside the project folder.

Do not paste the API key into a chat with Bob, and do not write it into any other file.

## 2.2 Installation, step by step

Perform the steps in this order. Each step states what you should see before you continue.

Step 1. Clone the repository.

1. In Bob, click the files icon at the top left. With no folder open, the panel shows two buttons: Open Folder and Clone Repository.
2. Click Clone Repository and paste `https://github.com/DanielLopezSainz/WatsonxOrchestrate_AICoding_Assistant.git`.
3. Choose where to save it. Bob creates a folder named `WatsonxOrchestrate_AICoding_Assistant` there.
4. When Bob offers to open the cloned repository, click Open.

You should see: the folder name at the top of the panel. If Bob's chat is in front, click the files icon to see the files: `README.md`, the `guide` folder with the chapters, and the `walkthroughs` folder.

Step 2. Install the extension.

1. Open the Extensions view: `Cmd Shift X` on a Mac, `Ctrl Shift X` elsewhere.
2. Search for `watsonx Orchestrate ADK`, publisher watson-devex, and click Install.

You should see: a watsonx Orchestrate icon in the left bar. If the bar is full, the icon is under the three dots at its bottom.

Step 3. Initialise the workspace.

1. Click the watsonx Orchestrate icon. A panel headed "Watsonx Orchestrate: Explorer" opens with the message "No workspace found. Please initialise a workspace to begin building" and a button, Initialise Workspace.
2. If the panel says instead that the extension loaded in restricted mode, click its link to trust the folder, confirm, and reload the window when asked. Bob asks this once per folder.
3. Click Initialise Workspace. A dialog asks "Initialize watsonx Orchestrate workspace in the current folder?" and shows the folder's path. Click Continue with Current Folder.
4. If Bob asks permission to install `uv`, accept. The extension needs `uv` to create the Python environment. If `uv` cannot be installed, for example on a machine where installations are restricted, the extension displays the address of the manual installation instructions; install `uv` and click Initialise Workspace again.
5. Wait. A progress message counts through the steps; the extension installs a Python environment and the ADK inside the folder, which takes a minute or two.

You should see: the panel now has two sections. Explorer lists Agents, Tools, Connections, Knowledge Bases and Toolkits. Environment Manager shows an Environment dropdown and an Add button.

Step 4. Send Bob its starting message.

When the initialisation ends, the extension places a message in the chat input box of Bob and does not send it. No notification is displayed, so the message is easy to overlook. Check the chat input box before you continue.

1. Find the text headed "SYSTEM PROMPT - IBM watsonx Orchestrate" in the chat input box.
2. Press Enter to send it as it is.

The message tells Bob to switch to Agent mode, to load the Orchestrate skills, and to use the Orchestrate server for all agent, tool and environment operations and the documentation server for reference. The box can be empty, for example if the text was deleted or a new conversation was started before it was sent. An empty box does not indicate an error. In that case, paste the following text and send it:

```
# SYSTEM PROMPT - IBM watsonx Orchestrate
## Instructions
1. Switch to **Agent mode** if not already active.
2. Use the `fetch_all_skills` tool on the `watsonx-orchestrate-adk` MCP server to load available skills.
3. Use the fetched skills and `watsonx-orchestrate-adk` MCP for all agent, tool, and environment operations. Consult `watsonx-orchestrate-adk-docs` MCP for API reference and documentation guidance.
```

You should see: Bob answering that the skills are loaded, with a table of the skills, and that it is in Agent mode. The number of skills depends on the version of the ADK; version 2.17 provides eight. The skills are stored in `.bob/skills` in the project folder. Chapter 12 uses them.

Step 5. Connect to your instance.

Your instance is the watsonx Orchestrate service where your agents run: a SaaS tenant in IBM Cloud or AWS, or the Developer Edition running on your machine. The ADK calls a connection to an instance an environment. The Environment Manager section of the panel shows the environments that exist, and its dropdown shows which one is active; Bob works against the active one.

- Developer Edition running on your machine: nothing to do. The dropdown already reads `local (active)`, and below it "Local server: Started".
- SaaS tenant: the dropdown is empty. Click Add and answer four questions in turn: a name for the environment, for example `mytenant`; the instance URL from 2.1; the SSL setting, where you select the first option, Verify SSL (Recommended); and your API key, typed into a masked box. When asked whether to activate the environment now, confirm.

You should see: in Environment Manager, the dropdown reading your environment's name followed by "(active)". In Explorer, expand Agents: the list is read from the instance, so it shows the agents that exist there. A new tenant has one, `AskOrchestrate`. A new Developer Edition has two, shown as "Try Document Processing Agent (DocProcessing)" and "AskOrchestrate".

Step 6. Check that Bob reaches the two servers.

The extension gave Bob two connections: the Orchestrate server, through which Bob acts on your instance, and the documentation server, through which it looks up IBM's documentation. Both must be connected for the later chapters to work.

1. Open Bob's settings with the settings icon in the Bob panel, then the MCP tab.
2. Find the two entries `watsonx-orchestrate-adk` and `watsonx-orchestrate-adk-docs`.

You should see: both marked as connected, and about sixty operations listed under the first one when you expand it.

Step 7. Set the approvals.

By default, Bob asks for approval before every action, including each file that it reads and each query to your instance. This produces dozens of approval requests per chapter. With every action approved automatically, Bob could write files, run commands and remove agents without asking. The following settings are a balance: Bob reads files and queries the instance without asking, and asks for approval before any action that changes a file or the instance. Section 2.5 describes the two settings in more detail.

1. Click the Permissions button, next to the mode dropdown at the bottom of the chat input. A list of nine categories opens: Read, Edit, Execute, MCP, Skill, Todo, Subtask, Subagent, Mode. Switch on Read and MCP. Leave Edit and Execute off. The same list is in Bob's settings under Auto-Approve.
2. Open Bob's settings, MCP tab, expand `watsonx-orchestrate-adk`, and switch on Always allow for these operations only: `check_version`, `list_agents`, `list_tools`, `list_toolkits`, `list_knowledge_bases`, `list_connections`, `list_models`, `export_agent`, `export_tool`, `export_toolkit`, `chat_with_agent`.

You should see: no change yet. The effect is visible in the next step, where Bob lists the agents without requesting approval.

Step 8. Test the connection. Start a new conversation, select Ask mode in the mode dropdown, and send:

```
Which agents exist on my instance? List their names and one line each.
```

You should see: Bob calling the Orchestrate server, shown above its answer, and the same agents that the Explorer lists. If Bob requests approval first, the settings of step 7 are not in place. If the answer mentions a working directory, a forbidden path or an authentication problem, see section 2.8.

The setup is complete. The following sections describe the views of Bob and what was installed.

## 2.3 The Bob views used in this guide

Bob shows different views depending on the icon selected in the left bar. This guide uses five of them. Each later chapter refers to them by the names given here.

### File Explorer

Open it with the files icon at the top of the left bar. It shows the project folder on your disk: the `guide` and `walkthroughs` folders from the repository, the folders that the extension created (`agents`, `tools`, `connections`, `knowledge-bases`, `toolkits`, `models`), and every file that Bob writes. Click a file to open it in the editor.

Use the File Explorer to read a design or an agent definition that Bob has written, and to open the chapters of this guide.

[Screenshot: the File Explorer with the project folder open]

### watsonx Orchestrate panel

Open it with the watsonx Orchestrate icon in the left bar. It has two sections.

- Explorer lists what exists on your instance: Agents, Tools, Connections, Knowledge Bases and Toolkits. The lists are read from the instance, not from the files in the project folder.
- Environment Manager shows the environments in a dropdown, with the active one marked "(active)", an Add button to register another instance, and, for the Developer Edition, the status of the local server with a button to start or stop it.

Use the Explorer to confirm that an import took place: an agent that appears under Agents exists on the instance. Use the Environment Manager to activate an environment again when its token has expired, or to switch to another instance.

[Screenshot: the watsonx Orchestrate panel after initialisation, with Explorer and Environment Manager]

### Source Control

Open it with the branch icon in the left bar. It lists the files that changed since the last commit. From this view you can stage files, type a commit message, commit, and synchronise with the remote repository, by clicking.

Use Source Control to see what Bob changed in the project folder and to keep your work in git. Chapter 3, section 3.6, describes how to do the same operations by asking Bob.

[Screenshot: the Source Control view with changed files]

### Bob chat panel

Open it with the Bob icon. It is where you write prompts and read Bob's answers. Five controls in this panel are used throughout the guide.

| Control | Location | Purpose |
|---|---|---|
| Mode dropdown | At the bottom of the chat input | Selects Ask, Plan or Agent mode |
| Permissions button | Next to the mode dropdown, at the bottom of the chat input | Opens the list of actions that Bob can perform without asking: Read, Edit, Execute, MCP and others |
| New conversation | The plus sign at the top of the panel | Starts a conversation with an empty context |
| @ mention | Typed in the chat input | References a file or folder, so that Bob reads it |
| Approve and reject buttons | Above the chat input, when Bob requests an action | Allow or refuse the action that Bob proposes |

[Screenshot: the Bob chat panel with the mode dropdown and the Permissions button]

### Bob settings, MCP tab

Open Bob's settings with the settings icon in the Bob chat panel, then select the MCP tab. It lists the servers that Bob is connected to, with their status. Expanding a server shows its operations, each with an Always allow switch, and a control to restart the server.

Use the MCP tab to check that the two Orchestrate servers are connected, to set the Always allow switches, and to restart a server when an operation fails for no apparent reason.

[Screenshot: the MCP tab with the two Orchestrate servers and the Always allow switches]

### How the views relate

An agent definition is a file in the File Explorer until Bob imports it. After the import, the agent appears in the Explorer section of the watsonx Orchestrate panel. If the two differ, the watsonx Orchestrate panel shows what is on the instance, and the file shows what you decided. Source Control shows which files changed since the last commit.

## 2.4 What was installed

Three components operate whenever Bob acts on the instance or searches the documentation. You do not run them yourself, but their names appear in Bob's messages and in the MCP tab.

| Component | What it does |
|---|---|
| The watsonx Orchestrate Agent Development Kit, the ADK | Defines agents, tools and everything around them as files, and pushes those files to an instance. Installed in step 3 |
| The watsonx Orchestrate MCP server, `watsonx-orchestrate-adk` in the MCP tab | Lets Bob use the ADK: list, import, test and export things on your instance. Bob starts it when needed. MCP is the standard protocol that coding assistants use to communicate with such programs |
| IBM's documentation server, `watsonx-orchestrate-adk-docs` in the MCP tab | Runs on the internet and gives Bob a search over the Orchestrate documentation, so that Bob consults the documentation instead of relying on its general knowledge |

Three facts apply to the whole guide.

1. One folder. Bob works inside the cloned repository only. The Orchestrate server does not read or write outside the folder that was open when you initialised the workspace. Always open this folder in Bob.
2. The token lasts two hours. On a tenant, the API key you gave in step 5 produced a token that expires after two hours. After that, every operation fails with an authentication error until you activate the environment again in the Environment Manager. If operations that worked earlier start to fail, check this first.
3. The active environment is shared. The ADK keeps one active environment per machine. Bob and any other coding assistant on the machine use it. Switching the environment in the Environment Manager switches it for all of them. Chapter 11 is the only chapter that switches environments.

## 2.5 The approvals, explained

Two settings determine when Bob asks for approval.

- The Permissions button, next to the mode dropdown at the bottom of the chat input, opens one switch per category. Read lets Bob read files without asking. MCP lets it run Orchestrate operations without asking, but only the ones you mark individually. Edit and Execute cover writing files and running commands. Leave them off, so that Bob asks before either.
- The Always allow switch on each operation in the MCP tab approves that operation permanently. Step 7 approved the eleven operations that only read from the instance or send a test message. Every other operation, such as importing, creating, removing or setting credentials, still requires approval.

With these settings, read operations are approved automatically and changes require approval. Do not switch on Always allow for every operation: Bob would then be able to remove agents and set credentials without asking.

## 2.6 Other AI coding assistants

The Orchestrate server is the same for every assistant. Cursor and VS Code with Copilot have the same extension and the same steps. Claude Code and Claude Desktop connect through a settings file that names the server and the folder. IBM documents the installation for each at https://developer.watson-orchestrate.ibm.com/mcp_server/wxOmcp_installation. If this address has changed, search the watsonx Orchestrate ADK documentation for the installation of the MCP server. This guide covers Bob only.

## 2.7 Checklist

Every line must be true before you continue.

1. The folder open in Bob is the cloned repository, and it is the one you initialised.
2. The `guide` folder is visible at the top level of that folder, next to the folders the extension created.
3. The MCP tab shows `watsonx-orchestrate-adk` and `watsonx-orchestrate-adk-docs`, both connected.
4. Under the Permissions button, Read and MCP are on and Edit and Execute are off, and Always allow is on for the eleven reading operations.
5. The Environment Manager shows an active environment.
6. The agent list prompt returns the agents you expect, without an approval request.

## 2.8 When something goes wrong

The following failures occurred while this guide was prepared.

| Bob reports | Cause | Fix |
|---|---|---|
| `Attempting to access resources outside the working directory is forbidden.` | The folder open in Bob is not the one that was initialised, or Bob is pointing at a file elsewhere on your disk | Open the initialised folder. If you must change folders, run Update MCP Servers from the command palette with the right folder open |
| Every operation fails with an authentication or authorization error after working earlier | The two-hour token expired | Activate the environment again in the Environment Manager; the next call works without a restart |
| An artifact was imported, but the list of the instance does not show it | Some operations report success even when the platform logged an error; the knowledge base import with an unsupported document type does this | Rely on the list, not on the message. After an import, ask Bob to list the artifacts of that kind and confirm the new one is there |
| A Python tool import fails with `No module named '<tool>'` although the file exists | Bob tried to import from that folder before it existed, and the server remembers the failure while it runs | Restart the server with the restart control in the MCP tab, then import again |
| The server command is not found, or the entry will not start | The environment the extension created is damaged or was moved | Run Initialise Workspace again; it repairs it |

The following is not a failure: when Bob tests an agent that has no tools, it reports that the reasoning is empty. This is expected, and chapter 4 explains it.
