from cloudscraper import create_scraper

session = create_scraper()

request_key_endpoint = "https://api.mp3youtube.cc/v2/sanity/key"

initiate_download_endpoint = "https://api.mp3youtube.cc/v2/converter"

request_headers = {
    "Content-Type": "application/json",
    "Origin": "https://iframe.y2meta-uk.com",
    "Accept": "*/*",
}

audio_payload = {
    "link": "https://youtu.be/YQHsXMglC9A",
    "format": "mp3",
    "audioBitrate": "320",
    "videoQuality": "720",
    "vCodec": "h264",
}


video_payload = {
    "link": "https://youtu.be/YQHsXMglC9A",
    "format": "mp4",
    "audioBitrate": "128",
    "videoQuality": "720",
    "vCodec": "h264",
}

payload = video_payload


def get_key():
    resp = session.get(request_key_endpoint, headers=request_headers)
    resp.raise_for_status()
    json_response: dict = resp.json()
    assert (
        "key" in json_response.keys()
    ), f"Failed to fetch keys {resp.status_code, resp.reason} - {json_response}"
    return resp.json()["key"]


def get_download_link(key, payload):
    custom_headers = request_headers.copy()
    custom_headers["key"] = key
    resp = session.post(
        initiate_download_endpoint, json=payload, headers=custom_headers
    )
    resp.raise_for_status()
    return resp.json()


download_response_example = {
    "status": "tunnel",
    "url": "https://dl34.yt-dl.click/tunnel?id=iE1WUITlFt0yQEhbXF6Lo&exp=1737541234165&sig=gz1ibhzdvGbbR_IUcKagb3--XMbjTfjQ7wjN1CrVrbs&sec=vIdngUBMcbmgzCdYUCbPAzOwQH00uE6ivqXoEar4MfY&iv=ltEmpFumTwnloA6pBVfKdw",
    "filename": "Adele - Hello (Official Music Video) - AdeleVEVO (720p, h264).mp4",
}


if __name__ == "__main__":
    key = get_key()
    out = get_download_link(key, audio_payload)
    print(out)
    out1 = get_download_link(key, video_payload)
    print(out1)
