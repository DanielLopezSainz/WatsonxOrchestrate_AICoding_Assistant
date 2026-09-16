# Chapter 2. Connect your assistant to watsonx Orchestrate

Level: beginner. Time: about 30 minutes. Prerequisites: an Orchestrate instance you can log in to, and one of the supported coding assistants installed.

This chapter takes you from "I have an assistant and an Orchestrate instance" to "my assistant just listed the agents on my instance", with the project folder prepared for every chapter that follows. It is the only chapter where the steps depend on which assistant you use.

There are two routes. The first uses the watsonx Orchestrate ADK extension, which IBM provides for Bob, Cursor and VS Code; one button installs the toolkit, connects the assistant to your instance, and lays out the project folder. This is the route the guide recommends, and the one Bob users should take. The second route is manual, for Claude Code and Claude Desktop, which have no extension, and for anyone who prefers to see each step. Both end at the same place, and the check at the end of the chapter is the same for both.

Whichever route you take, one detail decides whether the rest of the guide works, so it is stated here and repeated later: the folder you open in your assistant, the folder the extension initialises, and the folder the assistant is allowed to work in must be the same folder.

## 2.1 What you need before starting

- An Orchestrate instance. Either a SaaS tenant (IBM Cloud or AWS) on which you can generate an API key, or the Developer Edition running on your machine. The guide is written for a tenant; a box in 2.3 covers the Developer Edition. Note that the Developer Edition itself needs credentials from a SaaS tenant, or from another model provider, to start.
- Your service instance URL and an API key for the tenant. Both come from the Orchestrate interface: your user icon, Settings, API details, where the key can be generated. The key is shown once. Keep both in a file named `.env` in the project folder, made by copying `.env.example`; git is told to ignore that file, so it never leaves your machine. Never paste the key into a chat with the assistant, and never write it into any other file.
- One of the supported coding assistants: IBM Bob 2.1 or later, Cursor, VS Code with GitHub Copilot, Claude Code, or Claude Desktop.
- Git installed on your machine. Bob, Cursor and VS Code use it to clone repositories from their own interface, so you will not type git commands on the extension route, but the program has to be there. Python 3.11 or later is needed only on the manual route.

## 2.2 The two pieces that make it work

Two IBM packages do the work behind the scenes, and it helps to know their names because you will see them in messages.

The watsonx Orchestrate Agent Development Kit, the ADK, is IBM's toolkit for defining agents, tools and everything around them as files, and for pushing those files to an instance. It also provides the `orchestrate` command used for the few operations that stay on the command line.

The watsonx Orchestrate MCP server is a small program that exposes the ADK's operations to coding assistants, so that your assistant can list, import, test and export things on your instance by itself. MCP is the standard protocol coding assistants use to talk to programs like this one; nothing more about it is needed for this guide. The server works inside one folder only, the one named in its settings as its working directory, and refuses to read or write anything outside it. That folder is your project folder.

IBM also runs a second, remote MCP server that gives assistants a search over the Orchestrate documentation. Both routes below connect it too, so that the assistant can look things up instead of guessing.

## 2.3 Point the ADK at your instance

The extension route does this for you in 2.4, with a single prompt for the API key. Read this section anyway, because two facts in it matter for the whole guide, and the manual route needs the commands.

The ADK keeps a list of named environments and one of them is active; every operation, whether typed on the command line or performed by your assistant, goes to the active one. To register and activate a tenant by hand:

```bash
orchestrate env add -n mytenant -u https://api.<region>.watson-orchestrate.cloud.ibm.com/instances/<instance-id> --activate
orchestrate env activate mytenant --api-key <your-api-key>
```

The output ends with `Environment 'mytenant' is now active`. A warning about the authentication type being inferred from the URL may appear; it is harmless when the URL comes from the Settings page.

The two facts. First, the token obtained by activation expires after two hours. When it does, every operation your assistant attempts fails with an authentication error until the environment is activated again, from the command line or, with the extension, from the environment switcher. If an assistant suddenly cannot do anything it could do an hour ago, this is the first thing to check. Second, the active environment is one setting on your machine, shared by every assistant and every copy of the MCP server. Activating another environment switches all of them at once. Only chapter 11 switches environments, and it does so on purpose.

Developer Edition instead of a tenant: it registers itself as an environment named `local`, needs no key, and the extension can start and stop it from its side panel. It has only a draft environment, so nothing can be deployed on it, and it does not process uploaded documents unless started with the document-processing option. Everything else in this guide works on it.

## 2.4 Route 1: the watsonx Orchestrate ADK extension (Bob, Cursor, VS Code)

The extension is published by IBM under the name "watsonx Orchestrate ADK" and is in public preview. It installs from the Extensions view of Bob, Cursor or VS Code.

Step 1. Get the guide's repository onto your machine and open it. The repository is the project folder: besides the chapters and the walkthrough files, it holds the instructions the assistant follows in this project and the empty folders your agents will go into. From Bob this needs no command. Click the files icon at the top left of the Bob panel; with no folder open, the Explorer shows two buttons, Open Folder and Clone Repository. Click Clone Repository, paste `https://github.com/DanielLopezSainz/WatsonxOrchestrate_AICoding_Assistant.git`, and choose where to save it when Bob asks. Bob creates a folder named after the repository in that location, then offers to open it: click Open, and answer Yes, I trust the authors to the question that follows. The repository is public, so no credentials are asked for.

Do this before installing or initialising anything. The extension in step 3 records the folder that is open as the working directory of the MCP server, permanently; initialising one folder and then working in another is the most common way to end up with the "outside the working directory" error described in 2.10. If you would rather the folder had another name, such as `lumen-agents`, rename it now and open it again before going on.

If you want your work to end up in a repository of your own on GitHub, fork the guide's repository first (the Fork button on its page) and clone the address of the fork instead; 2.8 explains why.

Step 2. Open the Extensions view (`Ctrl Shift X`, or `Cmd Shift X` on a Mac), search for "watsonx Orchestrate ADK", and install it. A watsonx Orchestrate icon appears in the left sidebar.

Note: if you started from the Orchestrate interface with Create agent and Launch Bob, Bob opens with a prompt to install this extension; accept it, then clone and open the repository as in step 1.

Step 3. Click the watsonx Orchestrate icon in the left bar (if it is not visible, the bar's overflow menu at its bottom lists it). The side panel has two sections, Explorer and Environment Manager. Explorer shows the message "No workspace found. Please initialise a workspace to begin building" with a link, Initialise Workspace; click it. If the panel says instead that the extension loaded in restricted mode, the folder is not trusted yet: use Manage Workspace Trust from the command palette, trust the folder, and reload. If it says there is no open folder although one is open, reload the window (command palette, Developer: Reload Window); the extension checked before the folder was opened. What happens next, in order:

- The extension checks for an existing setup and, if none, asks for permission to install `uv`, a Python package manager. Accept. It creates a `venv` folder in your project with Python 3.12 and the latest ADK inside it, which may be newer than the version this guide was written with; that is fine. Nothing is installed system-wide.
- It makes sure the standard folders exist: `agents`, `tools`, `connections`, `knowledge-bases`, `toolkits`, `models`. The repository already has them, empty, so nothing changes there. It adds a small file, `workspace_config.yaml`, that records that layout.
- It writes the connection settings for your assistant. In Bob that is the file `.bob/mcp.json` in your project, with two entries: `watsonx-orchestrate-adk`, the MCP server, launched through `uvx` with your project folder as its working directory, and `watsonx-orchestrate-adk-docs`, the documentation server. Cursor and VS Code get the equivalent files.
- It activates an environment. With a Developer Edition present it activates `local`; otherwise it asks once for your API key and connects to the tenant.
- In Bob only, it places a ready-made message in the chat, headed "SYSTEM PROMPT - IBM watsonx Orchestrate", and asks you to press Enter to send it. The message tells Bob to switch to Agent mode, load IBM's Orchestrate skills through the server, and use the two servers for all Orchestrate work. Send it. Bob asks for approval to run the operation that fetches the skills; approve it, and the seven skills land in `.bob/skills`. They are procedures the assistant follows for larger pieces of work, and chapter 12 uses them. Bob may mention using one of its own built-in skills while doing this; that is normal.

When the extension reports success, the Explorer view shows your instance: its agents, tools, connections, knowledge bases and toolkits. On a new tenant the Agents list holds `AskOrchestrate`; on a new Developer Edition it also holds `DocProcessing`. That list is the first proof that the connection works.

What the repository provides for the assistant, and what each piece is for:

- `AGENTS.md`, two pages that tell the assistant how to work in this project: where files go, how to work with your instance, what to verify, what never to do without asking. Bob reads it at the start of every conversation. You may read it; you will not need to edit it.
- `.bob/rules-ask/`, `.bob/rules-plan/` and `.bob/rules-code/`, one short file each, with the rules for the Discover, Design and Build phases of chapter 3. In Bob they load with the Ask, Plan and Agent modes. Cursor and VS Code read them through `.cursor/rules/orchestrate.mdc` and `.github/copilot-instructions.md`, also provided.
- `design/` and `exports/`, two folders the assistant uses for design documents and for files exported from the instance.
- `guide/` and `walkthroughs/`, the chapters you are reading and the files each chapter produces. The assistant knows they are reading material, not build output.

Step 4. Check the two servers. Open Bob's settings (the settings icon in the Bob panel) and its MCP tab. Both entries the extension wrote, `watsonx-orchestrate-adk` and `watsonx-orchestrate-adk-docs`, should show as connected, and expanding the first one lists its operations, about sixty of them with names such as `list_agents` and `import_agent`. If an entry shows an error, use its restart control once; if it still fails, 2.10 has the usual causes.

Step 5. Decide how often Bob asks for approval. Out of the box Bob asks before every one of those operations, including the ones that only read, and that gets tiresome quickly. The right balance is to pre-approve reading and keep asking for anything that creates, changes or removes something on your instance. In the MCP tab, each operation under `watsonx-orchestrate-adk` has an Always allow switch. Turn it on for these, which only read:

- `check_version`, `list_agents`, `list_tools`, `list_toolkits`, `list_knowledge_bases`, `list_connections`, `list_models`
- `export_agent`, `export_tool`, `export_toolkit`
- `chat_with_agent`, which sends a test message to an agent

Leave every other switch off. The switches only take effect if the MCP category is enabled in Bob's auto-approve toolbar, above the chat input; enable MCP and Read there, and leave Edit and Execute off while learning, so that Bob asks before writing a file or running a command. Do not switch on every operation to save clicks: an assistant that can remove agents and set credentials without a prompt is not something to run against an instance you care about.

One last Bob point. Do not run Bob's `/init` command in this folder. It generates an `AGENTS.md` by scanning the project and would offer to overwrite the one from the repository.

Cursor and VS Code follow the same five steps; the extension writes their settings files, the repository provides their rule files, and the pre-approval is the per-tool setting in each product's MCP panel.

## 2.5 Route 2: manual setup (Claude Code, Claude Desktop)

Step 1. Install the two packages at the same version, preferably in a virtual environment:

```bash
pip install --upgrade ibm-watsonx-orchestrate ibm-watsonx-orchestrate-mcp-server
orchestrate --version
```

The first line printed is the ADK version, for example `ADK Version: 2.16.1`, the version this guide was written with. The command `ibm-watsonx-orchestrate-mcp-server` must also be on your path; typing it starts the server and waits, which is normal, and `Ctrl C` stops it.

Note: some IBM examples for connecting assistants pin the ADK to an old version such as `1.13.0`. Do not copy that; the server and the ADK must be the same version, and the current one.

Step 2. Register and activate your environment with the two commands from 2.3.

Step 3. Get the repository onto your machine, with your git client or with Download ZIP from its GitHub page, and note the absolute path of the folder. Then create a file named `.mcp.json` at the top of that folder with this content, replacing the path with yours:

```json
{
  "mcpServers": {
    "watsonx-orchestrate-adk": {
      "command": "ibm-watsonx-orchestrate-mcp-server",
      "env": {
        "WXO_MCP_WORKING_DIRECTORY": "/absolute/path/to/WatsonxOrchestrate_AICoding_Assistant"
      }
    },
    "watsonx-orchestrate-adk-docs": {
      "type": "http",
      "url": "https://developer.watson-orchestrate.ibm.com/mcp"
    }
  }
}
```

The first entry starts the MCP server and tells it which folder it may work in; the second connects the documentation server. The file is ignored by git because it contains a path specific to your machine. The folder already contains the `AGENTS.md`, phase rules and working folders described in 2.4, and `CLAUDE.md`, which makes Claude Code read them. If you move or rename the folder later, update the path in the file.

Step 4, Claude Code. Open a terminal in the folder and start Claude Code there. It finds `.mcp.json`, asks once whether to use the two project servers, and reads `CLAUDE.md`. There are no modes; start each prompt with the phase name, as chapter 3 explains.

Step 4, Claude Desktop. Its settings are global, in `claude_desktop_config.json`, reached through Settings, Developer, Edit Config. Copy the `watsonx-orchestrate-adk` block above into that file's `mcpServers` section, with your absolute path, and restart Claude Desktop. Remote servers such as the documentation server are only available on some plans; skip that entry if yours does not support them. Since Claude Desktop does not read files from a folder automatically, attach `AGENTS.md` at the start of each conversation.


## 2.6 Prove the connection

Two prompts, in a new chat, in Ask mode for Bob (or with "Discover phase:" in front for the others).

```
Which version of the Orchestrate MCP server are you connected to?
```

The assistant answers with something like `ibm-watsonx-orchestrate-mcp-server v2.16.1`. It got that by calling the server, and in Bob you can see the call listed above the answer.

```
Which agents exist on my instance? List their names and one line each.
```

On a new tenant there is one agent, `AskOrchestrate`; on a new Developer Edition there are two, with `DocProcessing`. If the instance has been used before you will see more. Any answer that mentions a working directory, a forbidden path, or an authentication problem means one of the steps above is not right; 2.10 says which.

If both prompts work, the setup is complete. Chapters 3 and 4 take it from here.

## 2.7 What the extension gives you beyond setup

Route 1 readers have a few more things in the side panel that this guide uses or refers to.

- The Explorer lists what is on your instance and refreshes on demand. Chapter 4 uses it to look at the draft agent without leaving the assistant.
- The environment switcher adds, activates and changes environments without commands. Remember that switching affects every assistant on the machine.
- Chat with agent opens a chat with any agent on the instance, and right-clicking an agent file offers to import it and open the chat. The guide has the assistant do these things through prompts, so that you see the operations; the panel is a convenient second view.
- The status bar shows the ADK version and offers updates. Update the ADK and the MCP server together.

None of these change how the assistant works. The Orchestrate documentation says so explicitly: the extension streamlines setup, and coding agents operate independently of it.

## 2.8 Keeping your project in git, from Bob

Your project folder is worth keeping under version control from the first chapter: the definition files the assistant writes are the real product of this guide, and being able to go back to yesterday's version is the safety net that lets you let the assistant work. Because the folder is a clone, it is already a git repository. Bob can do the rest through prompts, without you typing a git command; each prompt produces an approval request showing the exact command before it runs.

One thing to settle first: where your commits go. The clone points at the guide's repository, which you cannot push to, and where your project does not belong. Two ways to fix that:

- Fork before cloning, as suggested in 2.4. The clone then points at your fork, pushes work as soon as you sign in, and the Sync fork button on GitHub brings in guide updates later. This is the cleanest option.
- If you already cloned the original, create an empty repository in your GitHub account (any name, private is fine), then send in Agent mode:

```
Change the remote named origin to https://github.com/<your-account>/<your-repo>.git
and push the current branch to it.
```

The first push asks for your GitHub credentials the way any git client does: a personal access token over HTTPS, or an SSH key if you have one configured.

After each chapter, or whenever the assistant has built something you want to keep:

```
Stage all my changes, show me the list of files, and commit them with a short
message that summarises what was built. Then push.
```

Bob composes the message and asks you to approve the `git add`, `git commit` and `git push` commands: Approve for task on the first, and on the commit a warning to acknowledge with I understand the risks, then Approve. If you would rather point and click, the Source Control icon in the left bar (the third one down, a branch symbol) opens the standard view where changed files are listed, staged with the plus sign, and committed with a message typed in the box; the prompts do the same thing through the assistant. Before committing, `/review` in the chat runs Bob's code review over your uncommitted changes, and `@git-changes` in a prompt gives the assistant your current diff to reason about, for instance "explain what changed in agents/ since the last commit". Bob's `/create-pr` command opens a pull request from a branch, authenticating with GitHub in a browser window the first time; it is not needed for a personal project but is there when you work in a team.

Two cautions. The connection settings written by the extension and the script contain the absolute path of your folder and nothing secret, and the repository's `.gitignore` keeps them, the `venv` folder and the copied skills out of commits, so a clone on another machine has to run Initialise Workspace again. And never ask the assistant to commit a file that contains an API key; the rules in `AGENTS.md` forbid writing credentials into files precisely so that this does not happen.

## 2.9 Setup checklist

Answer every line with yes before moving on.

1. The folder open in the assistant is the cloned repository, and it is the one that was initialised (route 1) or the one named in `.mcp.json` (route 2).
2. `AGENTS.md` is visible at the top level of that folder, next to the `.bob` folder.
3. The settings file for your assistant names two servers, `watsonx-orchestrate-adk` and `watsonx-orchestrate-adk-docs`, and the working directory in the first one is this folder.
4. In Bob, Always allow is on for the reading operations of step 5, and MCP and Read are enabled in the auto-approve toolbar.
5. Both servers show as connected.
6. An environment is active (`orchestrate env list` marks it, or the extension's switcher shows it).
7. The version prompt returns a version.
8. The agent list prompt returns the agents you expect.
9. You have not run `/init`, and `AGENTS.md` is the one from the repository.

## 2.10 When setup goes wrong

Five failures, each seen while preparing this guide, with the exact message and the fix.

The assistant reports `Attempting to access resources outside the working directory is forbidden.` The working directory in the settings is not the folder open in the assistant, or the assistant is pointing at a file elsewhere on your disk. During the tests, an assistant whose settings pointed at another folder had to copy every file across before it could use it, and reported that as a limitation of the server; it was a setup error. Route 1: check that you initialised the folder you are working in; if not, run Update MCP Servers from the command palette with the right folder open, or edit the path in the settings. Route 2: correct the path in `.mcp.json`.

Every operation fails with an authentication or authorization error after working earlier. The two-hour token has expired. Activate the environment again, from the switcher or with `orchestrate env activate <name> --api-key <key>`; the next call works without restarting anything.

The assistant says an artifact was imported, but listing the instance does not show it. Some Orchestrate operations report success even when the platform logged an error; the knowledge base import with an unsupported document type does this, answering `Knowledge base imported successfully.` and creating nothing. The real message appears when the same operation is run from the command line. This is why the rules make the assistant verify after every change.

A Python tool import fails with `No module named '<tool>'` even though the file exists. The assistant tried to import from that folder before the folder existed, and the server remembers the failure for as long as it runs. Restart the MCP server (in Bob, the restart control in the MCP tab) and import again. The rules tell the assistant to create files before importing precisely to avoid this.

The assistant reports that the server command was not found. On route 2 the assistant is not using the Python environment where the packages were installed; start it from a terminal where that environment is active, or replace the command in the settings with `uvx` and the arguments with `["ibm-watsonx-orchestrate-mcp-server"]`, which is what the extension does. On route 1, run Initialise Workspace again; it repairs a damaged environment.

One more that is not a failure but looks like one: after the assistant chats with an agent that has no tools, it reports that the reasoning came back empty. That is expected; chapter 4 explains it.
