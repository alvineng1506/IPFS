import json
import requests

PINATA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIxN2YwNWZhZS0wNmIzLTRkOTQtYWM1MS1jZDFlODFiZjE3ZjEiLCJlbWFpbCI6ImVuZ2hhbndlbmFsdmluQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6IkZSQTEifSx7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6Ik5ZQzEifV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiJmMTdhNzU1M2UyZTNmNGYzOTJhMiIsInNjb3BlZEtleVNlY3JldCI6IjdhMDVkNmU0M2ZlMGU5NGUzNjI1OTIzNTI0YjUyZjFjYzk5MDExNDRlZWQyMTY1ZmE5MGVkNWVlYzE0NWVjMTYiLCJleHAiOjE4MDM5MDU2MzR9.fHHhzH29_ZOuKzBrzQCUrHoysyRyPL8hNm7UdJsXgus"

PINATA_PIN_JSON_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    headers = {
        "Authorization": f"Bearer {PINATA_JWT}",
        "Content-Type": "application/json",
    }

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