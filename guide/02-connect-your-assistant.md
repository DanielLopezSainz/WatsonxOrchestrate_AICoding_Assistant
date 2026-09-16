# Chapter 2. Connect Bob to watsonx Orchestrate

Level: beginner. Time: about 30 minutes. Prerequisites: an Orchestrate instance you can log in to, and IBM Bob installed.

This chapter takes you from "I have Bob and an Orchestrate instance" to "Bob just listed the agents on my instance", with the project folder prepared for every chapter that follows.

The setup relies on the watsonx Orchestrate ADK extension, which IBM provides for Bob: one button installs the toolkit, connects Bob to your instance, and lays out the project folder. The same extension exists for Cursor and VS Code, and other assistants can connect to the same server by other means; 2.5 says where that is documented, but this guide walks through Bob only.

One detail decides whether the rest of the guide works, so it is stated here and repeated later: the folder you open in Bob, the folder the extension initialises, and the folder Bob is allowed to work in must be the same folder.

## 2.1 What you need before starting

- An Orchestrate instance. Either a SaaS tenant (IBM Cloud or AWS) on which you can generate an API key, or the Developer Edition running on your machine. The guide is written for a tenant; a box in 2.3 covers the Developer Edition. Note that the Developer Edition itself needs credentials from a SaaS tenant, or from another model provider, to start.
- Your service instance URL and an API key for the tenant. Both come from the Orchestrate interface: your user icon, Settings, API details, where the key can be generated. The key is shown once. Keep both in a file named `.env` in the project folder, made by copying `.env.example`; git is told to ignore that file, so it never leaves your machine. Never paste the key into a chat with the assistant, and never write it into any other file.
- IBM Bob 2.1 or later.
- Git installed on your machine. Bob uses it to clone repositories from its own interface, so you will not type git commands, but the program has to be there.
- Nothing from IBM installed in advance. The ADK and the MCP server are not prerequisites: the extension installs both inside the project folder.

## 2.2 The two pieces that make it work

Two IBM packages do the work behind the scenes, and it helps to know their names because you will see them in messages.

The watsonx Orchestrate Agent Development Kit, the ADK, is IBM's toolkit for defining agents, tools and everything around them as files, and for pushing those files to an instance. It also provides the `orchestrate` command used for the few operations that stay on the command line.

The watsonx Orchestrate MCP server is a small program that exposes the ADK's operations to coding assistants, so that your assistant can list, import, test and export things on your instance by itself. MCP is the standard protocol coding assistants use to talk to programs like this one; nothing more about it is needed for this guide. The server works inside one folder only, the one named in its settings as its working directory, and refuses to read or write anything outside it. That folder is your project folder.

IBM also runs a second, remote MCP server that gives assistants a search over the Orchestrate documentation. The extension connects it too, so that Bob can look things up instead of guessing.

## 2.3 Point the ADK at your instance

The ADK keeps a list of named environments, one per Orchestrate instance, and one of them is active; every operation, whether typed on the command line or performed by Bob, goes to the active one. Nothing in this section needs to be typed. The extension installs the ADK inside the project folder and registers the environment for you, asking once for your API key. Afterwards, the Environment Manager section of its side panel lists your environments and switches between them.

Two facts about environments matter for the whole guide. First, the token obtained when an environment is activated expires after two hours. When it does, every operation your assistant attempts fails with an authentication error until the environment is activated again from the Environment Manager. If an assistant suddenly cannot do anything it could do an hour ago, this is the first thing to check. Second, the active environment is one setting on your machine, shared by every assistant and every copy of the MCP server. Activating another environment switches all of them at once. Only chapter 11 switches environments, and it does so on purpose.

Developer Edition instead of a tenant: it registers itself as an environment named `local`, needs no key, and the extension can start and stop it from the Environment Manager. It has only a draft environment, so nothing can be deployed on it, and it does not process uploaded documents unless started with the document-processing option. Everything else in this guide works on it.

## 2.4 Setting up Bob with the watsonx Orchestrate ADK extension

The extension is published by IBM under the name "watsonx Orchestrate ADK" and is in public preview. It installs from the Extensions view of Bob.

Step 1. Get the guide's repository onto your machine and open it. The repository is the project folder: besides the chapters and the walkthrough files, it holds the instructions the assistant follows in this project and the empty folders your agents will go into. From Bob this needs no command. Click the files icon at the top left of the Bob panel; with no folder open, the Explorer shows two buttons, Open Folder and Clone Repository. Click Clone Repository, paste `https://github.com/DanielLopezSainz/WatsonxOrchestrate_AICoding_Assistant.git`, and choose where to save it when Bob asks. Bob creates a folder named after the repository in that location, then offers to open it: click Open, and answer Yes, I trust the authors to the question that follows. The repository is public, so no credentials are asked for.

Do this before installing or initialising anything. The extension in step 3 records the folder that is open as the working directory of the MCP server, permanently; initialising one folder and then working in another is the most common way to end up with the "outside the working directory" error described in 2.10. If you would rather the folder had another name, such as `lumen-agents`, rename it now and open it again before going on.

If you want your work to end up in a repository of your own on GitHub, fork the guide's repository first (the Fork button on its page) and clone the address of the fork instead; 2.8 explains why.

Step 2. Open the Extensions view (`Ctrl Shift X`, or `Cmd Shift X` on a Mac), search for "watsonx Orchestrate ADK", and install it. A watsonx Orchestrate icon appears in the left sidebar.

Note: if you started from the Orchestrate interface with Create agent and Launch Bob, Bob opens with a prompt to install this extension; accept it, then clone and open the repository as in step 1.

Step 3. Click the watsonx Orchestrate icon in the left bar (if it is not visible, the bar's overflow menu at its bottom lists it). The side panel has two sections, Explorer and Environment Manager. Explorer shows the message "No workspace found. Please initialise a workspace to begin building" with a link, Initialise Workspace; click it. If the panel says instead that the extension loaded in restricted mode, the folder is not trusted yet: use Manage Workspace Trust from the command palette, trust the folder, and reload. If it says there is no open folder although one is open, reload the window (command palette, Developer: Reload Window); the extension checked before the folder was opened. What happens next, in order:

- The extension checks for an existing setup and, if none, asks for permission to install `uv`, a Python package manager. Accept. It creates a `venv` folder in your project with Python 3.12 and the latest ADK inside it, which may be newer than the version this guide was written with; that is fine. Nothing is installed system-wide.
- It makes sure the standard folders exist: `agents`, `tools`, `connections`, `knowledge-bases`, `toolkits`, `models`. The repository already has them, empty, so nothing changes there. It adds a small file, `workspace_config.yaml`, that records that layout.
- It writes the connection settings for Bob: the file `.bob/mcp.json` in your project, with two entries: `watsonx-orchestrate-adk`, the MCP server, launched through `uvx` with your project folder as its working directory, and `watsonx-orchestrate-adk-docs`, the documentation server. Cursor and VS Code get the equivalent files.
- It activates an environment. With a Developer Edition present it activates `local`; otherwise it asks once for your API key and connects to the tenant.
- In Bob only, it places a ready-made message in the chat, headed "SYSTEM PROMPT - IBM watsonx Orchestrate", and asks you to press Enter to send it. The message tells Bob to switch to Agent mode, load IBM's Orchestrate skills through the server, and use the two servers for all Orchestrate work. Send it. The skills are procedures the assistant follows for larger pieces of work; chapter 12 uses them, and nothing before that needs them.

What Bob answers to that message varies, and it is worth knowing how to read it. On the run used for this guide, Bob first noted that the message came from the extension and said it would load the skills, then answered that the session was ready, that the Orchestrate server was connected, and listed what it could do: agent operations, tool operations, environment operations, knowledge base operations, toolkit operations. Bob may also mention using one of its own built-in skills on the way; that is normal.

Two remarks on that answer. First, Bob did not actually fetch the skills on that run, and no `.bob/skills` folder appeared; it may on yours. Either way is fine. Second, Bob's list included "deploy" and "activate environments" as things it could do through the server. It cannot; those two stay on the command line, and the instructions file in the folder says so. Bob was summarising from its general knowledge of Orchestrate rather than from the operations it had in front of it, which is the habit chapter 3 teaches you to watch for. When an assistant lists its abilities, treat the list as a guess until it has done the thing.

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

## 2.5 Other AI coding assistants

The instructions and rules in the repository are written for any assistant, and the server Bob talks to is the same one other assistants can use. Cursor and VS Code with Copilot have the same extension, with the same steps as 2.4; their settings files are written by the extension and their rule files, `.cursor/rules/orchestrate.mdc` and `.github/copilot-instructions.md`, are in the repository. Claude Code and Claude Desktop have no extension and connect through a settings file that names the server and the working directory; `CLAUDE.md` in the repository makes Claude Code read the same instructions. IBM documents the installation for each of these at https://developer.watson-orchestrate.ibm.com/mcp_server/wxOmcp_installation. None of it is covered further in this guide, which follows Bob from here on.

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

The side panel has a few more things that this guide uses or refers to.

- The Explorer lists what is on your instance and refreshes on demand. Chapter 4 uses it to look at the draft agent without leaving the assistant.
- The Environment Manager adds, activates and changes environments without commands. Remember that switching affects every assistant on the machine.
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

1. The folder open in Bob is the cloned repository, and it is the one that was initialised.
2. `AGENTS.md` is visible at the top level of that folder, next to the `.bob` folder.
3. The settings file for your assistant names two servers, `watsonx-orchestrate-adk` and `watsonx-orchestrate-adk-docs`, and the working directory in the first one is this folder.
4. In Bob, Always allow is on for the reading operations of step 5, and MCP and Read are enabled in the auto-approve toolbar.
5. Both servers show as connected.
6. An environment is active: the Environment Manager shows it.
7. The version prompt returns a version.
8. The agent list prompt returns the agents you expect.
9. You have not run `/init`, and `AGENTS.md` is the one from the repository.

## 2.10 When setup goes wrong

Five failures, each seen while preparing this guide, with the exact message and the fix.

The assistant reports `Attempting to access resources outside the working directory is forbidden.` The working directory in the settings is not the folder open in the assistant, or the assistant is pointing at a file elsewhere on your disk. During the tests, an assistant whose settings pointed at another folder had to copy every file across before it could use it, and reported that as a limitation of the server; it was a setup error. Check that you initialised the folder you are working in; if not, run Update MCP Servers from the command palette with the right folder open, or edit the path in the settings.

Every operation fails with an authentication or authorization error after working earlier. The two-hour token has expired. Activate the environment again from the Environment Manager; the next call works without restarting anything.

The assistant says an artifact was imported, but listing the instance does not show it. Some Orchestrate operations report success even when the platform logged an error; the knowledge base import with an unsupported document type does this, answering `Knowledge base imported successfully.` and creating nothing. The real message appears when the same operation is run from the command line. This is why the rules make the assistant verify after every change.

A Python tool import fails with `No module named '<tool>'` even though the file exists. The assistant tried to import from that folder before the folder existed, and the server remembers the failure for as long as it runs. Restart the MCP server (in Bob, the restart control in the MCP tab) and import again. The rules tell the assistant to create files before importing precisely to avoid this.

Bob reports that the server command was not found, or the entry in the MCP tab will not start. The environment the extension created is damaged or was moved. Run Initialise Workspace again; it repairs it.

One more that is not a failure but looks like one: after the assistant chats with an agent that has no tools, it reports that the reasoning came back empty. That is expected; chapter 4 explains it.
