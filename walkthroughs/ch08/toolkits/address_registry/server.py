"""Address Registry MCP server for the City of Utopia.

Provides two tools:
  - lookup_address: resolve a raw address string to a canonical street record
  - list_streets: return all canonical streets for a given district
"""

import re
import json
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("address_registry")

# ---------------------------------------------------------------------------
# Canonical data
# ---------------------------------------------------------------------------

REGISTRY = [
    {"street": "Elm Street",    "district": "North",    "postcode": "UT1 1AA"},
    {"street": "Oak Avenue",    "district": "North",    "postcode": "UT1 1AB"},
    {"street": "Harbour Lane",  "district": "Harbour",  "postcode": "UT2 2AA"},
    {"street": "River Close",   "district": "Harbour",  "postcode": "UT2 2AB"},
    {"street": "Mill Road",     "district": "Old Town", "postcode": "UT3 3AA"},
    {"street": "High Street",   "district": "Old Town", "postcode": "UT3 3AB"},
    {"street": "Station Road",  "district": "Old Town", "postcode": "UT3 3AC"},
    {"street": "Cedar Way",     "district": "West",     "postcode": "UT4 4AA"},
    {"street": "Maple Drive",   "district": "West",     "postcode": "UT4 4AB"},
    {"street": "Birch Lane",    "district": "West",     "postcode": "UT4 4AC"},
]

# Abbreviation expansion table
ABBREVS = {
    "st":  "street",
    "rd":  "road",
    "ln":  "lane",
    "ave": "avenue",
    "dr":  "drive",
    "cl":  "close",
}

# Pre-build a lookup: normalised-canonical-name -> record
def _normalise_street(name: str) -> str:
    """Lowercase, strip punctuation, expand abbreviations, return token-joined string."""
    name = name.lower()
    name = re.sub(r"[,.\-#]", " ", name)
    tokens = name.split()
    tokens = [ABBREVS.get(t, t) for t in tokens]
    return " ".join(tokens)

CANONICAL_MAP = {
    _normalise_street(rec["street"]): rec
    for rec in REGISTRY
}

# Pre-build district -> list of street names
DISTRICT_MAP: dict[str, list[str]] = {}
for rec in REGISTRY:
    DISTRICT_MAP.setdefault(rec["district"], []).append(rec["street"])


# ---------------------------------------------------------------------------
# Normalisation helpers
# ---------------------------------------------------------------------------

def _extract_house_number(tokens: list[str]) -> tuple[str | None, list[str]]:
    """Separate a leading (or trailing) house-number token from the street tokens.

    A house-number token is one that starts with a digit.
    """
    if tokens and tokens[0][0].isdigit():
        return tokens[0], tokens[1:]
    if tokens and tokens[-1][0].isdigit():
        return tokens[-1], tokens[:-1]
    return None, tokens


def _normalise_input(address: str) -> tuple[str | None, str]:
    """Return (house_number_or_None, normalised_street_string)."""
    address = address.lower()
    address = re.sub(r"[,.\-#]", " ", address)
    tokens = address.split()
    tokens = [ABBREVS.get(t, t) for t in tokens]
    house_number, street_tokens = _extract_house_number(tokens)
    return house_number, " ".join(street_tokens)


# ---------------------------------------------------------------------------
# MCP tools
# ---------------------------------------------------------------------------

@mcp.tool()
def lookup_address(address: str) -> str:
    """Resolve a raw resident address to the official canonical record.

    Args:
        address: The raw address text as typed by the resident (e.g. "18 elm st").

    Returns:
        JSON string with found/not-found result including street, house_number,
        district, and postcode when matched.
    """
    house_number, normalised = _normalise_input(address)

    record = CANONICAL_MAP.get(normalised)
    if record is None:
        return json.dumps({
            "found": False,
            "message": "Address not found in the official registry.",
        })

    return json.dumps({
        "found": True,
        "street": record["street"],
        "house_number": house_number,
        "district": record["district"],
        "postcode": record["postcode"],
    })


@mcp.tool()
def list_streets(district: str) -> str:
    """Return all canonical streets in a given City of Utopia district.

    Args:
        district: The name of the district (e.g. "Old Town", "North").

    Returns:
        JSON string with district name and list of official street names.
    """
    # Case-insensitive district match
    matched_key = next(
        (k for k in DISTRICT_MAP if k.lower() == district.strip().lower()),
        None,
    )

    if matched_key is None:
        return json.dumps({
            "district": "Unknown",
            "streets": [],
            "message": "District not found.",
        })

    return json.dumps({
        "district": matched_key,
        "streets": DISTRICT_MAP[matched_key],
    })


if __name__ == "__main__":
    mcp.run()
