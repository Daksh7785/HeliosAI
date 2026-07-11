import argparse
import requests
import json
from structlog import get_logger

logger = get_logger(__name__)

API_BASE_URL = "http://localhost:8000/api/v1"

def status():
    """Check API health."""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        response.raise_for_status()
        print("API Status:", response.json())
    except requests.RequestException as e:
        logger.error("api_status_failed", error=str(e))
        print("Error connecting to API.")

def nowcast(last: int):
    """Fetch latest catalogue events."""
    try:
        response = requests.get(f"{API_BASE_URL}/catalogue?limit={last}")
        response.raise_for_status()
        print(f"Latest {last} Detections:")
        print(json.dumps(response.json(), indent=2))
    except requests.RequestException as e:
        logger.error("api_catalogue_failed", error=str(e))
        print("Error connecting to API.")

def forecast():
    """Fetch predictive forecasts."""
    try:
        response = requests.get(f"{API_BASE_URL}/forecasts")
        response.raise_for_status()
        print("Active Forecasts:")
        print(json.dumps(response.json(), indent=2))
    except requests.RequestException as e:
        logger.error("api_forecasts_failed", error=str(e))
        print("Error connecting to API.")

def main():
    parser = argparse.ArgumentParser(description="HeliosAI CLI Operations")
    subparsers = parser.add_subparsers(dest="command")

    # Status
    subparsers.add_parser("status", help="Check the serving layer health")

    # Nowcast
    nowcast_parser = subparsers.add_parser("nowcast", help="Fetch nowcasted events")
    nowcast_parser.add_argument("--last", type=int, default=5, help="Number of events to retrieve")

    # Forecast
    subparsers.add_parser("forecast", help="Fetch predictive forecasts")

    args = parser.parse_args()

    if args.command == "status":
        status()
    elif args.command == "nowcast":
        nowcast(args.last)
    elif args.command == "forecast":
        forecast()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
