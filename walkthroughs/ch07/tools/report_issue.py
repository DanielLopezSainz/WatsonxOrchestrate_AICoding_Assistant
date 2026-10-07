import os
import random
import requests
from pydantic import BaseModel

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate_core.types.connections.credentials import ExpectedCredentials
from ibm_watsonx_orchestrate_core.types.connections.configuration import ConnectionType


class ReportIssueResult(BaseModel):
    status: str  # "SUCCESS" or "FAILED"
    request_number: str = ""  # Format: "RQ-2026-NNNN" (on success)
    message: str = ""  # Status explanation or error details


@tool(
    name="report_issue",
    description="Report a road problem (such as a pothole, street light outage, or damaged sign) to the 311 Call Center. Requires the street location and a description of the issue.",
    permission=ToolPermission.ADMIN,
    expected_credentials=[
        ExpectedCredentials(app_id="utopia_311", type=ConnectionType.API_KEY_AUTH)
    ]
)
def report_issue(street: str, description: str) -> ReportIssueResult:
    """Report a road infrastructure problem to the City of Utopia 311 Call Center.

    Args:
        street (str): The street name or location where the road issue is located (e.g., "18 Elm Street", "Elm Street").
        description (str): A free-text description of the problem (e.g., "pothole outside house", "street light out").

    Returns:
        ReportIssueResult: The result of the report submission with status, request number, and message.
    """
    # Get the API key from the connection (injected as environment variable)
    api_key = os.environ.get("WXO_CONNECTION_utopia_311_api_key")
    if not api_key:
        return ReportIssueResult(
            status="FAILED",
            message="API key not configured for utopia_311 connection"
        )

    url = "https://postman-echo.com/post"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    body = {
        "street": street,
        "description": description
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)
        response.raise_for_status()
        response_data = response.json()

        # Verify the API key was echoed back in the headers
        echoed_headers = response_data.get("headers", {})
        echoed_api_key = echoed_headers.get("x-api-key") or echoed_headers.get("X-Api-Key")

        if echoed_api_key != api_key:
            return ReportIssueResult(
                status="FAILED",
                message=f"API key verification failed. Expected {api_key}, got {echoed_api_key}"
            )

        # Generate synthetic request number: RQ-2026-NNNN
        request_number = f"RQ-2026-{random.randint(1000, 9999)}"

        return ReportIssueResult(
            status="SUCCESS",
            request_number=request_number,
            message="Report submitted successfully to the 311 Call Center"
        )

    except requests.exceptions.RequestException as e:
        return ReportIssueResult(
            status="FAILED",
            message=f"Network error submitting report: {str(e)}"
        )
    except Exception as e:
        return ReportIssueResult(
            status="FAILED",
            message=f"Unexpected error: {str(e)}"
        )
