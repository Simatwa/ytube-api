"""
This module provides various templates
for generating search results and download links.
"""

from dataclasses import dataclass


@dataclass
class SearchResultsItem:
    """Metadata for individual video in results"""

    title: str
    id: str
    size: str
    duration: str
    channelTitle: str
    source: str


@dataclass
class SearchResults:
    """Video search results"""

    query: str
    items: list[SearchResultsItem]


@dataclass
class DownloadLink:
    """Download link other media/processing metadata"""

    status: str
    url: str
    filename: str
