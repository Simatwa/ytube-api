"""
This module contains strongly-typed variables
that are fundamental to the functionality of
Ytube-api package.
"""

search_videos_url = "https://wwd.mp3juice.blog/search.php"
"""Get request is made to this endpoint in searching of 
videos"""

suggest_queries_url = (
    "https://suggestqueries.google.com/complete/search?hl=en&ds="
    "yt&client=youtube&hjson=t&cp=1&q=%(query)s"
)
"""
Link template to YouTube's endpoint for query suggestion
requires `query` to be complete
"""

video_thumbnail_url = "https://i.ytimg.com/vi/%(video_id)s/0.jpg"
"""Link template to a Youtube video thumbnail"""

video_download_qualities: tuple[str] = ("144", "240", "360", "480", "720", "1080")
"""Video download qaulities without p"""

default_video_download_quality = "720"
""""""

audio_download_qualities: tuple[str] = ("128", "320")
"""Audio download qualities without Kbps"""

default_audio_download_quality = "128"
""""""

download_qualities: tuple[str] = tuple(
    audio_download_qualities + video_download_qualities + ("128|720",)
)
"""Combined video and audio download qualities """

video_download_format = "mp4"
"""String for specifying video"""

audio_download_format = "mp3"
"""String for specifying audio"""

format_quality_map: dict[str, tuple[str]] = {
    video_download_format: video_download_qualities,
    audio_download_format: audio_download_qualities,
}

download_formats: tuple[str] = (video_download_format, audio_download_format)
"""Combined  audio and video specifiers"""

request_key_endpoint = "https://api.mp3youtube.cc/v2/sanity/key"
"""Where download keys are secured from"""

initiate_download_endpoint = "https://api.mp3youtube.cc/v2/converter"
"""Where POST request is made to initiate download process"""

request_header_origin = "https://iframe.y2meta-uk.com"
"""Value for 'Origin' key in request headers"""

request_referer = request_header_origin + "/"
"""Referer value in request headers"""

request_headers: dict[str, str] = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept": "*/*",
    "Content-Type": "application/json",
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    # "Accept-Language": "en-US,en;q=0.9",
    "Origin": request_header_origin,
    "Referer": request_referer,
}
"""Http request headers"""
