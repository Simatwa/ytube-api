import click
from os import getcwd
import ytube_api.constants as const


@click.group()
def ytube():
    """Download YouTube videos in mp4 and mp3 formats"""


@ytube.command()
@click.argument("query")
@click.options(
    "-q",
    "--quality",
    type=click.Choice(const.download_qualities + ["128|720"]),
    help="Media download quality - 128|720",
)
@click.option(
    "--mp4/--mp3", default=True, help="Download audio (mp3) or video (mp4) - mp4"
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
def download(query, quality, mp4, dir, output, quiet, resume):
    """Search and download video in mp4 or mp3"""
    from ytube_api import Auto

    saved_to = Auto(
        query=query,
        type="mp4" if mp4 else "mp3",
        quality=quality,
        filename=output,
        dir=dir,
        quiet=quiet,
    )
    if not quiet:
        print(saved_to)


def main():
    ytube()
