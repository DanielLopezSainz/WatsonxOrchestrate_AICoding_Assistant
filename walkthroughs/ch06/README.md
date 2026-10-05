# Chapter 6 files

Files produced by chapter 6, as built with Bob on a watsonx Orchestrate tenant:

- `design/city-services-tools-design.md`: the design that Bob wrote in Plan mode, including the packaging of the record files that section 6.5 asks for.
- `tools/get_permit_status.py`, `get_request_status.py`, `get_collection_days.py`: the three Python Tools.
- `tools/permits.csv`, `requests.csv`, `collection_calendar.csv`: the records that the Tools read, with the three records of section 6.3 and seven that Bob added to each file.
- `agents/civic_info_agent.yaml`: the Agent with the three Tools attached and the extended instructions.

To start the guide at chapter 7 without building this chapter, first make sure that the Knowledge Base of chapter 5 exists on your instance, then send Bob these instructions in Agent mode: `Import the three Python tools in walkthroughs/ch06/tools into my instance, each one packaged with its record file, then import walkthroughs/ch06/agents/civic_info_agent.yaml.`
