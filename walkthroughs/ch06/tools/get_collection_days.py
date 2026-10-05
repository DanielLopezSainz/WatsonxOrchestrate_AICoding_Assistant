import csv
from pathlib import Path

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import BaseModel


class CollectionDays(BaseModel):
    street: str
    grey: str
    green: str
    blue: str
    yellow: str


_CSV_PATH = Path(__file__).parent / "collection_calendar.csv"


def _load_calendar() -> dict[str, CollectionDays]:
    records: dict[str, CollectionDays] = {}
    with open(_CSV_PATH, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            key = row["street"].strip().lower()
            records[key] = CollectionDays(
                street=row["street"].strip(),
                grey=row["grey"].strip(),
                green=row["green"].strip(),
                blue=row["blue"].strip(),
                yellow=row["yellow"].strip(),
            )
    return records


@tool(permission=ToolPermission.READ_ONLY)
def get_collection_days(street_name: str) -> CollectionDays:
    """Look up the weekly bin collection days for a street.

    Args:
        street_name (str): The name of the street, e.g. Elm Street.
    Returns:
        CollectionDays: Collection days for grey, green, blue, and yellow bins, or NOT_FOUND in all day fields if the street is not found.
    """
    key = street_name.strip().lower()
    records = _load_calendar()
    if key in records:
        return records[key]
    return CollectionDays(
        street=street_name,
        grey="NOT_FOUND",
        green="NOT_FOUND",
        blue="NOT_FOUND",
        yellow="NOT_FOUND",
    )
