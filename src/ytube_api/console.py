import click
from os import getcwd
import ytube_api.constants as const


@click.group()
@click.version_option(package_name="ytube-api")
def ytube():
    """Download YouTube videos in mp4 and mp3 formats"""


@ytube.command()
@click.argument("query")
@click.option(
    "-q",
    "--quality",
    type=click.Choice(const.download_qualities + ("128|720",)),
    help="Media download quality - 128|720",
    default="128|720",
)
@click.option(
    "--mp4/--mp3", default=True, help="Download audio (mp3) or video (mp4) - mp4"
)
@click.option(
    "--enable-progressbar/--disable-progressbar",
    default=True,
    help="Show or hide progressbar",
)
@click.option(
    "-l",
    "--limit",
    type=click.INT,
    help="Total number of items to be downloaded that matched the search - 1",
    default=1,
)
@click.option(
    "-t",
    "--timeout",
    type=click.INT,
    help="Http request timeout - 20",
    default=20,
)
@click.option(
    "-c",
    "--channels",
    help="Download videos posted by this channel titles - None.",
    metavar="Name",
    multiple=True,
)
@click.option(
    "-d",
    "--dir",
    help="Directory for saving the contents to - pwd.",
    type=click.Path(exists=True, file_okay=False),
    default=getcwd(),
)
@click.option("-o", "--output", help="Filename to save the contents under - None")
@click.option("--quiet", is_flag=True, help="Do not stdout informative messages")
@click.option("--resume", is_flag=True, help="Resume incomplete download")
@click.option(
    "--confirm", is_flag=True, help="Ask user for permission to download a video/audio"
)
def download(
    query,
    quality,
    mp4,
    enable_progressbar,
    limit,
    timeout,
    channels,
    dir,
    output,
    quiet,
    resume,
    confirm,
):
    """Search and download video in mp4 or mp3 formats"""
    from ytube_api import Auto

    saved_to = Auto(
        query=query,
        format="mp4" if mp4 else "mp3",
        limit=limit,
        confirm=confirm,
        quality=quality,
        timeout=timeout,
        channels=channels,
        filename=output,
        dir=dir,
        quiet=quiet,
        resume=resume,
        progress_bar=enable_progressbar,
    )
    if not quiet and saved_to:
        print(
            "## Saved to : \n" + "\n".join([str(path) for path in saved_to])
            if isinstance(saved_to, list)
            else "## Saved to : " + str(saved_to)
        )


def main():
    try:
        ytube()
    except Exception as e:
        print(
            f"> Error occured - {e.args[1] if e.args and len(e.args)>1 else e}. \nQuitting."
        )
        from sys import exit

        exit(1)
