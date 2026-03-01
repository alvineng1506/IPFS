import os
import json
import requests

PINATA_PIN_JSON_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    jwt = os.getenv("PINATA_JWT") or os.getenv("PINATA_JWT")
    if not jwt:
        raise RuntimeError("PINATA_JWT environment variable not set")

    headers = {"Authorization": f"Bearer {jwt}"}

    r = requests.post(PINATA_PIN_JSON_URL, headers=headers, json=data, timeout=30)
    r.raise_for_status()

    cid = r.json()["IpfsHash"]
    return cid


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
            data = json.loads(r.text)
            assert isinstance(data, dict), f"get_from_ipfs should return a dict"
            return data
        except Exception as e:
            last_err = e

    raise RuntimeError(f"Failed to fetch CID {cid} from gateways.") from last_err