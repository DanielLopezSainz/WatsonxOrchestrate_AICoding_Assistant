# Chapter 8 files

Files produced by chapter 8, as built with Bob on a watsonx Orchestrate tenant:

- `design/address-registry-design.md`: the design that Bob wrote in Plan mode, with the build steps at the end. Two lines of its build steps are as Bob corrected them during the build (section 8.6): the absolute paths of the entry in Bob's configuration, and the import command.
- `toolkits/address_registry/server.py`: the MCP server of the Address Registry, in Python, with its two tools, `lookup_address` and `list_streets`, and the ten streets inside it.
- `toolkits/address_registry/requirements.txt`: the MCP library the server uses. The version is pinned to the one Bob tested, as section 8.10 advises; the run had `mcp>=1.0.0`, which installs whatever version is current.
- `agents/civic_info_agent.yaml`: the Agent with the two tools of the Toolkit listed under `tools` as `address_registry:lookup_address` and `address_registry:list_streets`, and the extended instructions.

Bob's own entry for the server, in `.bob/mcp.json`, is not here: it holds absolute paths of one machine, and every reader's Bob writes its own.

To start the guide at chapter 9 without building this chapter, send Bob these instructions in Agent mode: `Import the MCP server in walkthroughs/ch08/toolkits/address_registry into my instance as a toolkit named address_registry, with all its tools, then import walkthroughs/ch08/agents/civic_info_agent.yaml.`
