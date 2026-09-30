DEFAULT_TRANSMISSION_URL = "http://192.168.1.103:9093/transmission/rpc"


def transmission_request(session, url, payload):
    headers = {"Content-Type": "application/json"}
    response = session.post(url, json=payload, headers=headers, timeout=30)

    if response.status_code == 409 and "X-Transmission-Session-Id" in response.headers:
        session.headers["X-Transmission-Session-Id"] = response.headers[
            "X-Transmission-Session-Id"
        ]
        response = session.post(url, json=payload, headers=headers, timeout=30)

    response.raise_for_status()
    try:
        return response.json()
    except ValueError:
        return {"raw": response.text}


def add_to_transmission(session, download_dir, magnet_url, rpc_url):
    payload = {
        "jsonrpc": "2.0",
        "method": "free_space",
        "params": {"path": download_dir},
        "id": "webui",
    }
    free_space = transmission_request(session, rpc_url, payload)
    size_bytes = free_space.get("result", {}).get("size_bytes")
    if size_bytes is not None:
        size_gb = size_bytes / 1_000_000_000
        print(f"Free space at {download_dir}: {size_gb:.2f} GB")

    payload = {
        "jsonrpc": "2.0",
        "method": "torrent_add",
        "params": {
            "download_dir": download_dir,
            "filename": magnet_url,
            "paused": False,
        },
        "id": "webui",
    }
    return transmission_request(session, rpc_url, payload)
