# Chapter 7 files

Files produced by chapter 7, as built with Bob on a watsonx Orchestrate tenant:

- `design/report-issue-design.md`: the design that Bob wrote in Plan mode.
- `tools/report_issue.py`: the Python Tool that reports a road problem to the 311 Call Center and reads the API key from the Connection `utopia_311` at run time.
- `agents/civic_info_agent.yaml`: the Agent with the four Tools attached and the extended instructions.

The Connection has no file: Bob created it on the instance with two commands, and the credential comes from the `UTOPIA_311_API_KEY` variable of your `.env` file (section 7.6).

To start the guide at chapter 8 without building this chapter, add the `UTOPIA_311_API_KEY` line to your `.env` file as section 7.6 describes, then send Bob these instructions in Agent mode: `Create the connection utopia_311 on my instance, kind API key sent in the header x-api-key, type team, for the Draft environment, and set its Draft credential from the variable UTOPIA_311_API_KEY in my .env file without displaying its value. Then import the tool walkthroughs/ch07/tools/report_issue.py with that connection, and import walkthroughs/ch07/agents/civic_info_agent.yaml.`
