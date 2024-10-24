"""
This module does all the work using `Ytube` class and 
features `Auto` function for auto-handling the whole 
process of downloading a YouTube video.
"""

import re
import time
import shutil
import logging
import datetime
import typing as t
from tqdm import tqdm
from pathlib import Path
from os import getcwd, path, environ
from cloudscraper import create_scraper
from requests import Response
import ytube_api.constants as const
import ytube_api.models as models
import ytube_api.exceptions as exception

try:
    import click

    cli_deps_installed = True
except ImportError:
    cli_deps_installed = False

session = create_scraper()

session.headers = const.request_headers


class Ytube:
    """This is the sole class for searching, navigating
    and finally downloading any Youtube video of your choice.
    """

    def __init__(self, timeout: int = 20):
        """Initializes `Search`

        Args:
            timeout (int, optional): Http Request timeout. Defaults to 20.
        """
        self.request_timeout = timeout
        self.video_id_patterns = (
            r"^https://youtu.be/(\w{11}).*?",
            r"^https://www.youtube.com/watch\?v=(\w{11})",
            r"^(\w{11})$",
        )

    def get(self, *args, **kwargs) -> Response:
        """Fetch online resource

        Returns:
            Response
        """
        kwargs.setdefault("timeout", self.request_timeout)
        resp = session.get(*args, **kwargs)
        resp.raise_for_status()
        return resp

    def post(self, *args, **kwargs) -> Response:
        """Send data online

        Returns:
            Response
        """
        kwargs.setdefault("timeout", self.request_timeout)
        resp = session.post(*args, **kwargs)
        resp.raise_for_status()
        return resp

    def get_thumbnail(self, item: models.SearchResultsItem) -> bytes:
        """Get thumbnail of a particular video

        Args:
            item (models.SearchResultsItem)
        Returns:
            bytes: Video thumbnail
        """
        if not isinstance(item, models.SearchResultsItem):
            raise ValueError(
                f"Item should be an instance of {models.SearchResultsItem} "
                f"not {type(item)}"
            )
        return self.get(const.video_thumbnail_url % dict(video_id=item.id)).content

    def suggest_queries(self, query: str) -> list[str]:
        """Suggest search queries"""
        text = self.get(const.suggest_queries_url % dict(query=query)).text
        pattern = r'"([^"]+)",0'
        return re.findall(
            pattern,
            text,
        )

    def extract_video_id(self, query: str) -> None | str:
        """Check if query contains youtube video id

        Args:
            query (str): Search query

        Returns:
            None|str: Video ID or None
        """
        for pattern in self.video_id_patterns:
            if re.match(pattern, query):
                return re.findall(pattern, query)[0]

    def search_video_by_title(self, query: str) -> models.SearchResults:
        """Tries to locate video by it's title"""
        assert query, "Query cannot be empty"
        video_id_from_query = self.extract_video_id(query)
        if video_id_from_query:
            return models.SearchResults(
                query=query,
                items=list[
                    models.SearchResultsItem(
                        title=None,
                        id=video_id_from_query,
                        size=None,
                        duration=None,
                        channelTitle=None,
                        source=None,
                    )
                ],
                from_link=True,
            )
        resp = self.get(const.search_video_by_title_url, params=dict(q=query))
        resp.raise_for_status()
        results = resp.json()
        results_items: list[models.SearchResultsItem] = []
        for item in results["items"]:
            results_items.append(models.SearchResultsItem(**item))
        return models.SearchResults(
            query=re.sub(r"\+", " ", results["query"]), items=results_items
        )

    def get_download_link(
        self,
        item: models.SearchResultsItem,
        type: t.Literal["mp3", "mp4"] = "mp4",
        quality: t.Literal[
            "128", "320", "144", "240", "360", "480", "720", "1080"
        ] = "128|720",
    ) -> models.DownloadLink:
        """Get page containing download links

        Args:
            item (models.SearchResultsItem): Item to download.
            type (t.Literal['mp3', 'mp4'], optional): Media type. Defaults to 'mp4'.
            quality (t.Literal['128',320', '144', '240', '360', '480', '720', '1080'], optional): Download quality. Defaults to '720|128'.

        Returns:
            models.DownloadLink: Download link and other metadata
        """
        assert isinstance(item, models.SearchResultsItem), (
            f"Item must be an instance of {models.SearchResultsItem} "
            f"not {type(item)}"
        )
        assert type in [
            const.audio_download_type,
            const.video_download_type,
        ], f"Type '{type}' is not one of {[const.audio_download_type, const.video_download_type],}"
        if quality == "128|720":
            if type == const.audio_download_type:
                quality = "128"
            else:
                quality = "720"
        else:
            assert (
                quality in const.download_qualities
            ), f"Quality '{quality}' is not one of {const.download_qualities}"
            if type == const.audio_download_type:
                assert (
                    quality in const.audio_download_qualities
                ), f"Audio quality '{quality}' is not one of {const.audio_download_qualities}"
            if type == const.video_download_type:
                assert (
                    quality in const.video_download_qualities
                ), f"Video quality '{quality}' is not one of {const.video_download_qualities}"
        payload = dict(videoid=item.id, downtype=type, vquality=quality)
        resp_data = self.post(const.to_download_page_url, data=payload).json()
        if resp_data.get("status", "") == "error":
            raise exception.VideoProccessingError(
                str(
                    resp_data.get(
                        "error",
                        "Unknown error occurred while processing video for download.",
                    )
                )
            )
        return models.DownloadLink(**resp_data)

    def download(
        self,
        download_link: models.DownloadLink,
        filename: str | Path = None,
        dir: str = getcwd(),
        progress_bar=True,
        quiet: bool = False,
        chunk_size: int = 512,
        resume: bool = False,
        leave: bool = True,
        colour: str = "cyan",
        simple: bool = False,
    ):
        """Donload and save the media in disk
        Args:
            download_link (models.DownloadLink): Downloadlink
            filename (str|Path): Filename to save the downloaded contents under.
            dir (str, optional): Directory for saving the contents Defaults to current directory.
            progress_bar (bool, optional): Display download progress bar. Defaults to True.
            quiet (bool, optional): Not to stdout anything. Defaults to False.
            chunk_size (int, optional): Chunk_size for downloading files in KB. Defaults to 512.
            resume (bool, optional):  Resume the incomplete download. Defaults to False.
            leave (bool, optional): Keep all traces of the progressbar. Defaults to True.
            colour (str, optional): Progress bar display color. Defaults to "cyan".
            simple (bool, optional): Show percentage and bar only in progressbar. Deafults to False.

        Raises:
            FileExistsError:  Incase of `resume=True` but the download was complete
            Exception: _description_

        Returns:
            str: Path where the movie contents have been saved to.
        """
        assert isinstance(download_link, models.DownloadLink), (
            f"download_link must be an instance of {models.DownloadLink} "
            f"not {type(download_link)}"
        )
        current_downloaded_size = 0
        current_downloaded_size_in_mb = 0
        filename = filename or download_link.filename
        save_to = Path(dir) / filename
        media_file_url = download_link.url

        def pop_range_in_session_headers():
            if session.headers.get("Range"):
                session.headers.pop("Range")

        if resume:
            assert path.exists(save_to), f"File not found in path - '{save_to}'"
            current_downloaded_size = path.getsize(save_to)
            # Set the headers to resume download from the last byte
            session.headers.update({"Range": f"bytes={current_downloaded_size}-"})
            current_downloaded_size_in_mb = current_downloaded_size / 1_000_000

        default_content_length = 0

        resp = session.get(media_file_url, stream=True)
        size_in_bytes = int(resp.headers.get("content-length", default_content_length))
        if not size_in_bytes:
            if resume:
                raise FileExistsError(
                    f"Download completed for the file in path - '{save_to}'"
                )

        if resume:
            assert (
                size_in_bytes != current_downloaded_size
            ), f"Download completed for the file in path - '{save_to}'"

        size_in_mb = (size_in_bytes / 1_000_000) + current_downloaded_size_in_mb
        chunk_size_in_bytes = chunk_size * 1_000

        saving_mode = "ab" if resume else "wb"
        if progress_bar:
            if not quiet:
                print(f"{filename}")
            if not size_in_bytes:
                # Prevent tqdm from showing progressbar

                def find_range(start, end, hms: bool = False):
                    in_seconds = round(end - start, 1)
                    return (
                        str(datetime.timedelta(seconds=in_seconds))
                        .split(".")[0]
                        .zfill(8)
                        if hms
                        else in_seconds
                    )

                def get_screen_width():
                    try:
                        return shutil.get_terminal_size().columns
                    except AttributeError:
                        # Fallback for older Python versions
                        return environ.get("COLUMNS", 80)

                downloaded_size_in_bytes = 0
                start_time = time.time()
                with open(save_to, saving_mode) as fh:
                    for chunks in resp.iter_content(chunk_size=chunk_size_in_bytes):
                        fh.write(chunks)
                        downloaded_size_in_bytes += len(chunks)
                        text_to_display = f"> Downloaded {round(downloaded_size_in_bytes / 1_000_000, 2)} MB "
                        ellipses = "..."
                        len_of_more_text_to_display = (
                            int(
                                get_screen_width()
                                - len(text_to_display)
                                - len(ellipses)
                            )
                            - 11
                        )
                        whole_text_to_display = f"{text_to_display}{'#'*len_of_more_text_to_display}~[{find_range(start_time, time.time(),True)}]{ellipses}"
                        print(whole_text_to_display, end="\r")

                print(
                    f"> Download completed successfully ({round(downloaded_size_in_bytes/ 1_000_000, 2)}MB, {find_range(start_time, time.time(), True)})"
                )
                return save_to

            with tqdm(
                desc="Downloading",
                total=round(size_in_mb, 1),
                bar_format=(
                    "{l_bar}{bar} | %(size)s MB" % (dict(size=round(size_in_mb, 1)))
                    if simple
                    else "{l_bar}{bar}{r_bar}"
                ),
                initial=current_downloaded_size_in_mb,
                unit="Mb",
                colour=colour,
                leave=leave,
            ) as p_bar:
                with open(save_to, saving_mode) as fh:
                    for chunks in resp.iter_content(chunk_size=chunk_size_in_bytes):
                        fh.write(chunks)
                        p_bar.update(round(chunk_size_in_bytes / 1_000_000, 1))
                pop_range_in_session_headers()
                return save_to
        else:
            with open(save_to, saving_mode) as fh:
                for chunks in resp.iter_content(chunk_size=chunk_size_in_bytes):
                    fh.write(chunks)

            logging.info(f"{filename} - {size_in_mb}MB ✅")
            pop_range_in_session_headers()
            return save_to


def Auto(
    query: str,
    type: t.Literal["mp3", "mp4"] = "mp4",
    quality: t.Literal[
        "128", "320", "144", "240", "360", "480", "720", "1080"
    ] = "128|720",
    limit: int = 1,
    confirm: bool = False,
    timeout: int = 20,
    **kwargs,
) -> Path | list[Path]:
    """Search, navigate and download first video of every results

    Args:
        query (str): Video title or video url
            type (t.Literal['mp3', 'mp4'], optional): Media type. Defaults to 'mp4'.
            quality (t.Literal['128',320', '144', '240', '360', '480', '720', '1080'], optional): Download quality. Defaults to '720|128'.
            limit (int, optional): Total number of videos to handle. Defaults to 1.
            confirm (bool, optional): Ask user permission to proceed with the download. Defaults to False.
            timeout (int, optional): Http request timeout. Defaults to 20.
        The rest are kwargs for `Ytube.download`
    Returns:
          Path : Path where the file has been saved to
    """
    if kwargs.get("filename") and limit > 1:
        raise RuntimeError(
            f"Limit should be 1 when you have specified filename of the item to be downloaded."
        )
    yt = Ytube(timeout=timeout)
    y = yt.search_video_by_title(query)
    if not y.items:
        raise Exception(f"Your query matched zero results")
    saved_to: list[Path] = []
    for count, item in enumerate(y.items, start=1):
        if confirm and not y.from_link:
            if not cli_deps_installed:
                raise RuntimeError(
                    f"Looks like cli dependencies are not installed. "
                    f"Reinstall ytube-api along with cli extras ie. "
                    "pip install ytube-api[cli]"
                )
            if not click.confirm(
                f'Are you sure to download "{item.title}" by "{item.channelTitle} : [{item.duration}]"'
            ):
                continue
        d = yt.get_download_link(item, type=type, quality=quality)
        saved_to.append(yt.download(d, **kwargs))
        if count >= limit:
            break
    return saved_to[0] if len(saved_to) == 1 else saved_to
