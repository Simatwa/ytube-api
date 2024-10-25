"""
This module provides various templates
for generating search results and download links.
"""

from dataclasses import dataclass
import re

duration_patterns: dict[str, str] = {
    "hour": r"^(\d{1,2}):(\d{1,2}):(\d{1,2})$",
    "minute_seconds": r"^(\d{1,2}):(\d{1,2})$",
    "seconds": r"^0:(\d{1,2})$",
}


@dataclass
class SearchResultsItem:
    """Metadata for individual video in results"""

    title: str
    id: str
    size: str
    duration: str
    channelTitle: str
    source: str

    @property
    def duration_in_seconds(self) -> int:
        """Video's running time in seconds"""
        resp = 0
        if self.duration:
            hour_match = re.findall(duration_patterns["hour"], self.duration)
            minute_seconds_match = re.findall(
                duration_patterns["minute_seconds"], self.duration
            )
            seconds_match = re.findall(duration_patterns["seconds"], self.duration)
            if hour_match:
                hours, minutes, seconds = hour_match[0]
                resp = (int(hours) * 60 * 60) + (int(minutes) * 60) + int(seconds)
            elif minute_seconds_match:
                minutes, seconds = minute_seconds_match[0]
                resp = (int(minutes) * 60) + int(seconds)
            elif seconds_match:
                seconds = seconds_match[0]
                resp = int(seconds)
            return resp
        return resp


@dataclass
class SearchResults:
    """Video search results"""

    query: str
    items: list[SearchResultsItem]
    from_link: bool = False


@dataclass
class DownloadLink:
    """Download link other media/processing metadata"""

    status: str
    url: str
    filename: str
