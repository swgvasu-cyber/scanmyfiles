import logging
from typing import Any, Dict

import httpx
from mcp.server.fastmcp import FastMCP

# -------------------------------------------------
# Logging
# -------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------------------------
# MCP Server
# -------------------------------------------------
mcp = FastMCP("ScanMyFile")

# -------------------------------------------------
# API Config (matches curl exactly)
# -------------------------------------------------
BASE_URL = "http://localhost:8000"
ENDPOINT = "/scan/hash"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Saraneya and Devudu",
}


# -------------------------------------------------
# HTTP POST (curl-equivalent)
# -------------------------------------------------
async def post_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Equivalent to:
    curl -X POST <url> -H 'Content-Type: application/json' -d '<payload>'
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(
                url=url,
                headers=HEADERS,
                json=payload,   # EXACT match to curl -d
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(
                "HTTP %s error: %s",
                e.response.status_code,
                e.response.text,
            )
            return None

        except httpx.RequestError as e:
            logger.error("Request error: %s", str(e))
            return None


# -------------------------------------------------
# MCP Tool
# -------------------------------------------------
@mcp.tool()
async def scan_my_file(sha256_hash: str) -> str:
    """
    Submit a SHA256 hash to the scanning service
    """
    url = f"{BASE_URL}{ENDPOINT}"

    payload = {
        "hash": sha256_hash
    }

    result = await post_json(url, payload)

    if result is None:
        return "ERROR: Scan service unreachable or returned an error"

    return str(result)


# -------------------------------------------------
# Entry Point
# -------------------------------------------------
def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

