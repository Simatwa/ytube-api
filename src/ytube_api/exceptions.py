"""
This module contains exception classes
used across ytube-api
"""


class VideoProccessingError(Exception):
    """Raised when unable to process video for download"""


class ZeroSearchResults(Exception):
    """Raised when a search returns 0 videos"""


class MediaDownloadError(Exception):
    """Raised when server fails to respond with actual video/audio content"""
