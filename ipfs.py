import requests
import json

def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    # Convert dict -> JSON bytes
    payload = json.dumps(data).encode("utf-8")

    # Try common public IPFS API endpoints
    api_endpoints = [
        "https://ipfs.infura.io:5001/api/v0/add",
        "https://dweb.link/api/v0/add",
        "http://127.0.0.1:5001/api/v0/add",
    ]

    files = {"file": ("data.json", payload, "application/json")}
    params = {"pin": "true"}

    last_err = None
    for url in api_endpoints:
        try:
            r = requests.post(url, files=files, params=params, timeout=30)
            r.raise_for_status()

            cid = None
            for line in r.text.splitlines():
                if line.strip():
                    cid = json.loads(line).get("Hash")
            if not cid:
                raise ValueError("IPFS add response missing Hash/CID")

            return cid
        except Exception as e:
            last_err = e

    raise RuntimeError("pin_to_ipfs failed: no working IPFS API endpoint available") from last_err


def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), f"get_from_ipfs accepts a cid in the form of a string"

    gateways = [
        "https://gateway.moralisipfs.com/ipfs/{cid}",
        "https://ipfs.io/ipfs/{cid}",
        "https://cloudflare-ipfs.com/ipfs/{cid}",
    ]

    last_err = None
    for g in gateways:
        url = g.format(cid=cid)
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            data = json.loads(r.text)  # assume valid JSON per assignment
            assert isinstance(data, dict), f"get_from_ipfs should return a dict"
            return data
        except Exception as e:
            last_err = e

    raise RuntimeError(f"Failed to fetch CID {cid} from gateways.") from last_err