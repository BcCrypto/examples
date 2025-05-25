import httpx

GITHUB_ISSUE_API = "https://rfdelta.com/githubapp/create-issue"
INSTALLATION_ID = "12345678"
REPO = "RFDX_admin/trading-algos"


async def report_issue(signal_name: str, confidence: float, timestamp: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            GITHUB_ISSUE_API,
            json={
                "installation_id": INSTALLATION_ID,
                "repo": REPO,
                "title": f"[Anomaly] {signal_name} deviation detected",
                "body": f"Confidence: {confidence}, Timestamp: {timestamp}",
                "labels": ["anomaly", "dashboard", "model-review"],
                "assignees": ["RFDX_admin"],
            },
        )
