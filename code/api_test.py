import argparse
import json
from pathlib import Path

import requests

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "sample_requests.json"


def sendrequest(host):
    with open(FIXTURE_PATH) as f:
        sample_data = json.load(f)

    url = f"http://{host}:9696/predict"
    result = requests.post(url, json=sample_data)

    print(result.status_code)
    print(result.content)


if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument("host")
    arg = arg.parse_args()
    sendrequest(arg.host)
