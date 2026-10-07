# Design: Report Road Problem Tool (`report_issue`)

## 1. Overview

This document describes the design for adding an action tool, `report_issue`, to `civic_info_agent`. The tool enables residents to report road infrastructure problems (such as potholes, street lights out, and damaged signs) directly to the City of Utopia 311 Call Center.

Because the City of Utopia 311 backend is not yet accessible, the public echo endpoint `https://postman-echo.com/post` stands in for the external 311 service. The tool authenticates using an API key managed through a dedicated watsonx Orchestrate connection (`utopia_311`). When the real 311 service becomes available, only the connection endpoint and credentials will need to change.

---

## 2. Scope of Change

| Asset | Change |
|---|---|
| `connections/utopia_311.yaml` / Platform Connection | New — Connection object named `utopia_311` (kind: `api_key`, team-shared) |
| `tools/report_issue.py` | New — Python action tool sending HTTP POST with API key header and returning generated request ID |
| `agents/civic_info_agent.yaml` | Updated — add `report_issue` to `tools` list, update instructions to describe reporting flow and remove restriction on creating requests |
| `scripts/import-all.sh` | Updated — add connection setup and `report_issue` tool import steps |
| `scripts/delete-all.sh` | Updated — add `report_issue` tool removal and connection removal steps |
| `design/report-issue-design.md` | New — this design specification |

The existing lookup tools (`get_permit_status`, `get_request_status`, `get_collection_days`), the `city_regulations` knowledge base, and department facts remain unchanged.

---

## 3. Connection Specification (`utopia_311`)

| Property | Value |
|---|---|
| Connection Name / App ID | `utopia_311` |
| Sharing / Scope | Team-shared (`type: team`) |
| Authentication Kind | `api_key` |
| Header Name | `x-api-key` |
| Target Endpoint (Test) | `https://postman-echo.com/post` |
| Credential Source | `.env` variable `UTOPIA_311_API_KEY` |
| Security Policy | The API key value must never appear in chat messages, project files, commit history, or tool source code. It is configured securely via CLI or environment variable binding. |

---

## 4. Tool Specification (`report_issue`)

### 4.1 Metadata & Signature

- **File**: `tools/report_issue.py`
- **Tool Name**: `report_issue`
- **Description**: Report a road problem (such as a pothole, street light outage, or damaged sign) to the 311 Call Center. Requires the street location and a description of the issue.
- **Connection**: `app_id: "utopia_311"`

### 4.2 Inputs

| Parameter | Type | Required | Description |
|---|---|---|---|
| `street` | `str` | Yes | The street name or location where the road issue is located (e.g., "18 Elm Street", "Elm Street") |
| `description` | `str` | Yes | A free-text description of the problem (e.g., "pothole outside house", "street light out") |

### 4.3 Output Structure

```python
class ReportIssueResult(BaseModel):
    status: str  # "SUCCESS" or "FAILED"
    request_number: str = ""  # Format: "RQ-2026-NNNN" (on success)
    message: str = ""  # Status explanation or error details
```

### 4.4 Execution Logic

1. **HTTP Request**:
   - Method: `POST`
   - URL: `https://postman-echo.com/post`
   - Headers: `{"x-api-key": <api_key_from_connection>, "Content-Type": "application/json"}`
   - Body JSON: `{"street": street, "description": description}`
2. **Echo Verification**:
   - The tool inspects the JSON response from `postman-echo.com`.
   - The report is considered **accepted** if and only if the response echoes back the `x-api-key` header (under `headers["x-api-key"]` or equivalent).
   - If the header is missing, wrong, or the HTTP call fails (e.g., non-200 status code, network error), the tool marks the result as `status = "FAILED"`.
3. **Request Number Generation**:
   - Since the test echo service does not generate internal ticket IDs, the tool generates a synthetic identifier in the format `RQ-2026-NNNN` (e.g. `RQ-2026-` followed by 4 random or sequence digits) and returns it with `status = "SUCCESS"`.

---

## 5. Agent Behaviour Rules

### 5.1 Trigger & Flow

- **Trigger**: When a resident asks to report a road problem (such as a pothole, broken street light, damaged sign, or road damage).
- **Immediate Submission**: As soon as the agent has both the **street location** and a **description** of the problem, it calls `report_issue` immediately without asking for extra confirmation.
- **Missing Information**: If either the street or the description is missing, the agent asks for the missing detail before calling the tool.
- **Anonymous Reporting**: Reports are anonymous; the agent does not ask for resident names, contact info, or categorize into strict types.

### 5.2 Success Handling

When `report_issue` returns `status = "SUCCESS"`:
- The agent provides the resident with the generated `request_number` (e.g., `RQ-2026-5821`).
- The agent informs the resident that they can check the status of their report in the future using this request number (via `get_request_status`).
- Concludes with Roads and Infrastructure contact details.

### 5.3 Failure Handling

When `report_issue` returns `status = "FAILED"`:
- The agent states that the report could not be submitted to the 311 Call Center at this time.
- Directs the resident to contact Roads and Infrastructure directly (Phone: `555 0120`, Email: `roads@utopia.example`).

### 5.4 Instruction Revisions in `agents/civic_info_agent.yaml`

1. **Update `tools` list**:
   ```yaml
   tools:
     - get_permit_status
     - get_request_status
     - get_collection_days
     - report_issue
   ```
2. **Update Boundaries**:
   - Replace: `"Do not create requests or tickets and do not access any systems other than the tools provided."`
   - With: `"Do not access any systems other than the tools provided. For road issues, use report_issue to submit reports."`
3. **New Section in Instructions (`### Tools: Action - Report Road Issue`)**:
   - Define exact parameters required (`street`, `description`).
   - Define missing detail prompts.
   - Define success and failure message patterns.

---

## 6. Security & Credential Management

1. **Zero Secret Leakage**:
   - `UTOPIA_311_API_KEY` is loaded strictly from `.env` in shell execution during credential setting.
   - The key is passed directly to the Orchestrate connection credentials store.
   - Tool code reads credentials securely via the Orchestrate SDK context / connection binding (`app_id="utopia_311"`).
2. **TLS / Network**:
   - All outgoing calls use HTTPS (`https://postman-echo.com/post`).
   - Standard TLS verification is enforced.

---

## 7. Import & Deployment Steps

1. **Create and Configure Connection**:
   ```bash
   orchestrate connections configure --app-id utopia_311 --kind api_key --type team --environment draft
   # Set credentials using environment variable from .env without echoing:
   orchestrate connections set-credentials --app-id utopia_311 --environment draft --api-key "$UTOPIA_311_API_KEY"
   ```
2. **Import Tool**:
   ```bash
   orchestrate tools import -k python \
     --file tools/report_issue.py \
     --app-id utopia_311
   ```
3. **Update Agent**:
   ```bash
   orchestrate agents import --file agents/civic_info_agent.yaml
   ```

---

## 8. Test Scenarios

| # | User Prompt | Expected Action | Expected Outcome |
|---|---|---|---|
| 1 | "There is a pothole outside 18 Elm Street. Can you report it?" | Calls `report_issue(street="18 Elm Street", description="pothole outside")` | Returns success with request number (e.g. `RQ-2026-XXXX`). Agent informs resident of the number and explains they can check status later. |
| 2 | "A street light is out on Harbour Lane. Please submit a report." | Calls `report_issue(street="Harbour Lane", description="street light out")` | Returns success with request number. |
| 3 | "Can you report a pothole for me?" | None (asks for street) | Agent asks resident for the street location where the pothole is located. |
| 4 | "Can you report a problem on High Street?" | None (asks for description) | Agent asks resident what kind of problem is present on High Street. |
| 5 | Connection/Network failure simulation | Calls `report_issue`, receives `FAILED` | Agent explains that the report could not be submitted and provides Roads & Infrastructure contact (555 0120 / roads@utopia.example). |
