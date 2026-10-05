import csv
from pathlib import Path

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import BaseModel


class PermitRecord(BaseModel):
    permit_number: str
    address: str
    work_type: str
    status: str
    submitted: str
    decision_date: str
    notes: str


_CSV_PATH = Path(__file__).parent / "permits.csv"


def _load_permits() -> dict[str, PermitRecord]:
    records: dict[str, PermitRecord] = {}
    with open(_CSV_PATH, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            key = row["permit_number"].strip().upper()
            records[key] = PermitRecord(
                permit_number=row["permit_number"].strip(),
                address=row["address"].strip(),
                work_type=row["work_type"].strip(),
                status=row["status"].strip(),
                submitted=row["submitted"].strip(),
                decision_date=row["decision_date"].strip(),
                notes=row["notes"].strip(),
            )
    return records


@tool(permission=ToolPermission.READ_ONLY)
def get_permit_status(permit_number: str) -> PermitRecord:
    """Look up the status of a building permit application by permit number.

    Args:
        permit_number (str): The permit application number, e.g. PP-2026-0412.
    Returns:
        PermitRecord: The permit record, or a record with status NOT_FOUND if not found.
    """
    key = permit_number.strip().upper()
    records = _load_permits()
    if key in records:
        return records[key]
    return PermitRecord(
        permit_number=permit_number,
        address="",
        work_type="",
        status="NOT_FOUND",
        submitted="",
        decision_date="",
        notes="",
    )
