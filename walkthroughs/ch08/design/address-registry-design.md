# Design: Address Registry MCP Toolkit (`address_registry`)

## 1. Overview

This document describes the design for adding a local MCP toolkit, `address_registry`, to `civic_info_agent`. The toolkit acts as Utopia's official address registry, resolving messy or abbreviated resident address inputs into canonical street names, house numbers, districts, and postcodes, and allowing street lookups by district.

The agent uses `lookup_address` as a prerequisite step before querying collection schedules (`get_collection_days`) or reporting road infrastructure problems (`report_issue`).

The existing department facts, `city_regulations` knowledge base, four standalone tools (`get_permit_status`, `get_request_status`, `get_collection_days`, `report_issue`), and the `utopia_311` connection remain in place.

---

## 2. Scope of Change

| Asset | Change |
|---|---|
| `toolkits/address_registry/server.py` | New — Single-file Python MCP server implementing `lookup_address` and `list_streets` using official `mcp` SDK |
| `toolkits/address_registry/requirements.txt` | New — Dependency specification (`mcp>=1.0.0`) |
| `.bob/mcp.json` | Updated — Register `address_registry` using the virtual environment's Python interpreter for local testing from Bob |
| `agents/civic_info_agent.yaml` | Updated — Add `lookup_address` and `list_streets` to agent tools, add resolution instructions |
| `scripts/import-all.sh` | Updated — Add toolkit import step for `address_registry` before agent import |
| `scripts/delete-all.sh` | Updated — Add toolkit removal step for `address_registry` |
| `design/address-registry-design.md` | New — This design specification |

---

## 3. Data Specification

The City of Utopia contains four official districts covering 10 canonical streets:

| District | Official Street Name | Postcode | Abbreviations / Aliases |
|---|---|---|---|
| **North** | Elm Street | `UT1 1AA` | `st` → `street` |
| **North** | Oak Avenue | `UT1 1AB` | `ave` → `avenue` |
| **Harbour** | Harbour Lane | `UT2 2AA` | `ln` → `lane` |
| **Harbour** | River Close | `UT2 2AB` | `cl` → `close` |
| **Old Town** | Mill Road | `UT3 3AA` | `rd` → `road` |
| **Old Town** | High Street | `UT3 3AB` | `st` → `street` |
| **Old Town** | Station Road | `UT3 3AC` | `rd` → `road` |
| **West** | Cedar Way | `UT4 4AA` | — |
| **West** | Maple Drive | `UT4 4AB` | `dr` → `drive` |
| **West** | Birch Lane | `UT4 4AC` | `ln` → `lane` |

### House Number Rules
- The house number is whatever the resident typed (e.g. `"18"` in `"18 elm st"` or `"7"` in `"7 Harbour Ln"`).
- The address registry extracts and returns the house number as given, without checking or validating it against building records.
- If no house number is present in the input, `house_number` is returned as empty or `None`.

---

## 4. Normalization & Matching Logic

The MCP server implements deterministic normalization in Python without external NLP or fuzzy matching libraries:

1. **Lowercase & Strip Punctuation**: Convert input string to lowercase and remove punctuation marks (`,`, `.`, `-`, `#`, etc.).
2. **Tokenize & Extract House Number**: Identify leading, trailing, or isolated numeric/alphanumeric house number tokens.
3. **Abbreviation Expansion**: Map individual words:
   - `st` → `street`
   - `rd` → `road`
   - `ln` → `lane`
   - `ave` → `avenue`
   - `dr` → `drive`
   - `cl` → `close`
4. **Exact Canonical Matching**: Compare normalized street tokens against the 10 known official street names. If matched, return the corresponding record; otherwise, return not found.

---

## 5. Tool Specifications

### 5.1 `lookup_address`

- **Purpose**: Receives an address as typed and resolves it to official street name, house number (if present), district, and postcode.
- **Input Parameters**:
  - `address` (`str`): The raw address text as typed by the resident (e.g., `"18 elm st"`, `"7 Harbour Ln"`).
- **Return Value (Matched)**:
  ```json
  {
    "found": true,
    "street": "Elm Street",
    "house_number": "18",
    "district": "North",
    "postcode": "UT1 1AA"
  }
  ```
- **Return Value (Not Matched)**:
  When an address matches no street, `lookup_address` explicitly states so and returns nothing else:
  ```json
  {
    "found": false,
    "message": "Address not found in the official registry."
  }
  ```

### 5.2 `list_streets`

- **Purpose**: Receives a district name and returns all canonical streets located in that district.
- **Input Parameters**:
  - `district` (`str`): The name of the district (e.g., `"Old Town"`, `"North"`).
- **Return Value (Matched)**:
  ```json
  {
    "district": "Old Town",
    "streets": [
      "Mill Road",
      "High Street",
      "Station Road"
    ]
  }
  ```
- **Return Value (Not Matched)**:
  ```json
  {
    "district": "Unknown",
    "streets": [],
    "message": "District not found."
  }
  ```

---

## 6. Agent Behaviour Rules

### 6.1 Address Resolution Requirement
- Whenever a resident provides an address or asks about collection days or reports a road issue on a street, `civic_info_agent` **always calls `lookup_address` first** before calling any tool that takes a street name.

### 6.2 Forwarding Canonical Data
- **Collection Calendar**: Pass the resolved official `street` name to `get_collection_days(street_name=...)`.
- **Road Problem Reports**:
  - Pass the resolved official `street` name to `report_issue(street=...)`.
  - Include the extracted `house_number` in the `description` parameter (e.g. `"Pothole outside house number 18"`).

### 6.3 Unresolved Address Handling
- When `lookup_address` returns `found = false`:
  - The Agent replies asking the resident to check the address.
  - The Agent **calls no other tool**.

---

## 7. Build Steps

Execute the following build steps in exact order:

1. **Write the MCP Server and Requirements File**:
   - Create `toolkits/address_registry/requirements.txt` with `mcp>=1.0.0`.
   - Create `toolkits/address_registry/server.py` using the official Python MCP SDK with `lookup_address` and `list_streets`.
2. **Install Requirements into Project Python Environment**:
   - Run `pip install -r toolkits/address_registry/requirements.txt` using `venv/bin/pip`.
3. **Register MCP Server in Bob MCP Configuration & Test Tools**:
   - Register `address_registry` in `.bob/mcp.json` using the project's Python interpreter and the server file, both with absolute paths.
   - From Bob, call the two tools:
     - `lookup_address` with `"18 elm st"`
     - `list_streets` with `"Old Town"`
4. **Import Toolkit into watsonx Orchestrate**:
   - Import the toolkit from `toolkits/address_registry` with all its tools:
     ```bash
orchestrate toolkits add -k mcp -n address_registry \
  --description "Official City of Utopia address registry. Resolves raw resident addresses to canonical street names, districts, and postcodes." \
  --package-root toolkits/address_registry --language python \
  --command '["python", "server.py"]' --tools "*"
```
5. **Import the Agent**:
   - Update `agents/civic_info_agent.yaml` to include `lookup_address` and `list_streets` and the resolution instructions.
   - Import the updated agent:
     ```bash
     orchestrate agents import -f agents/civic_info_agent.yaml
     ```
6. **Run Test Scenarios**:
   - Test address resolution chained with bin collection (`"When is bin day for 18 elm st?"`).
   - Test address resolution chained with reporting road problems (`"Report a pothole outside 7 Harbour Ln"`).
   - Test unrecognized address flow (`"When is collection on 99 Atlantis Way?"`).
