import csv
from pathlib import Path

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import BaseModel


class RequestRecord(BaseModel):
    request_number: str
    street: str
    problem_type: str
    status: str
    scheduled_date: str


_CSV_PATH = Path(__file__).parent / "requests.csv"


def _load_requests() -> dict[str, RequestRecord]:
    records: dict[str, RequestRecord] = {}
    with open(_CSV_PATH, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            key = row["request_number"].strip().upper()
            records[key] = RequestRecord(
                request_number=row["request_number"].strip(),
                street=row["street"].strip(),
                problem_type=row["problem_type"].strip(),
                status=row["status"].strip(),
                scheduled_date=row["scheduled_date"].strip(),
            )
    return records


@tool(permission=ToolPermission.READ_ONLY)
def get_request_status(request_number: str) -> RequestRecord:
    """Look up the status of a road problem report by request number.

    Args:
        request_number (str): The road problem request number, e.g. RQ-2026-1187.
    Returns:
        RequestRecord: The request record, or a record with status NOT_FOUND if not found.
    """
    key = request_number.strip().upper()
    records = _load_requests()
    if key in records:
        return records[key]
    return RequestRecord(
        request_number=request_number,
        street="",
        problem_type="",
        status="NOT_FOUND",
        scheduled_date="",
    )
