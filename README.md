<h1 align="center">ytube-api</h1>

<p align="center">
<a href="#"><img alt="Python version" src="https://img.shields.io/pypi/pyversions/ytube-api"/></a>
<a href="https://github.com/Simatwa/ytube-api/actions/workflows/python-test.yml"><img src="https://github.com/Simatwa/ytube-api/actions/workflows/python-test.yml/badge.svg" alt="Python Test"/></a>
<a href="LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=MIT&color=Blue&message=MIT&label=License"/></a>
<a href="https://pypi.org/project/ytube-api"><img alt="PyPi" src="https://img.shields.io/pypi/v/ytube-api"></a>
<a href="https://github.com/Simatwa/ytube-api/releases"><img src="https://img.shields.io/github/v/release/Simatwa/ytube-api?label=Release&logo=github" alt="Latest release"></img></a>
<a href="https://github.com/Simatwa/ytube-api/releases"><img src="https://img.shields.io/github/release-date/Simatwa/ytube-api?label=Release date&logo=github" alt="release date"></img></a>
<a href="https://github.com/psf/black"><img alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"/></a>
<a href="https://github.com/Simatwa/ytube-api/actions/workflows/python-publish.yml"><img src="https://github.com/Simatwa/ytube-api/actions/workflows/python-publish.yml/badge.svg" alt="Python-publish"/></a>
<a href="https://pepy.tech/project/ytube-api"><img src="https://static.pepy.tech/personalized-badge/ytube-api?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" alt="Downloads"></a>
<a href="https://github.com/Simatwa/ytube-api/releases/latest"><img src="https://img.shields.io/github/downloads/Simatwa/ytube-api/total?label=Asset%20Downloads&color=success" alt="Downloads"></img></a>
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com/Simatwa/ytube-api"/></a>
</p>

> Download YouTube videos in `mp4` or `mp3` formats.

```python
from ytube_api import Auto
Auto(
  query = "Alan Walker - Alone"
)
# Alan Walker - Alone - Alan Walker (720p, h264, youtube).mp4
# > Downloaded 15.68 MB ############ ~ Elapsed (00:00:32) [■■■█■]
# ## Saved to : /home/smartwa/y2mate/Alan Walker - Alone - Alan Walker (720p, h264, youtube).mp4
```

```python
from ytube_api import Auto
Auto(
  query = "Alan Walker - Alone",
  format = "mp3"
)
# Alan Walker - Alone - Alan Walker (youtube).mp3
# > Downloaded 2.61 MB ############ ~ Elapsed (00:00:06) [■█■■■]
# ## Saved to : /home/smartwa/y2mate/Alan Walker - Alone - Alan Walker (youtube).mp3
```

# Pre-requisite

- [x] [Python>=3.9](https://python.org) (optional)

# Installation

Either of the following ways will get you ready.

1. From pypi:

   ```sh
   $ pip install -U "ytube-api[cli]"
   ```

2. From source:

   ```sh
   $ pip install git+http://github.com/Simatwa/ytube-api.git
   ```

Alternatively, you can download standalone executable for your system from [here](https://github.com/Simatwa/ytube-api/releases/latest).

## Usage

<details>

<summary>
<h2>1. Developers</h2>
</summary>

### Search videos

#### By Title

   ```python
   from ytube_api import Ytube
   yt = Ytube()
   videos = yt.search_videos(
      "Alan Walker songs"
   )
   print(videos)
   """
   SearchResults(query='Alan Walker songs', items=[SearchResultsItem(title='Alan Walker, Putri Ariani, Peder Elias - Who I Am (Official Music Video)', id='ccu6JuC21rk', size='2.91 MB', duration='3:32', channelTitle='Alan Walker', source='yt'), SearchResultsItem(title='Alan Walker - Faded', id='60ItHLz5WEA', size='2.93 MB', duration='3:33', channelTitle='Alan Walker', source='yt')], from_link=False)
   """
   ```

#### By Video URL

   ```python
   from ytube_api import Ytube
   yt = Ytube()
   videos = yt.search_videos(
      "https://youtu.be/oociIYNVdVQ?si=v1Ic_mcBq2bb_j8J"
   )
   print(videos)
   """
   SearchResults(query='https://youtu.be/oociIYNVdVQ?si=v1Ic_mcBq2bb_j8J', items=[SearchResultsItem(title=None, id='oociIYNVdVQ', size=None, duration=None, channelTitle=None, source=None)], from_link=True)
   """
   ```

### Get Download Link

#### Video

   ```python
   from ytube_api import Ytube
   yt = Ytube()
   search_results = yt.search_videos(
      "Alan Walker songs"
   )
   target_video = search_results.items[0]
   download_link = yt.get_download_link(
      target_video,
      format="mp4",
      quality="1080"
      )
   print(
      download_link
   )
   """
   DownloadLink(status='tunnel', url='https://vgbh.nmnm.store/tunnel?id=svqwnZ5CJOJJZi12yXq0b&exp=1729856312453&sig=kcY69-AGCv--0t5cY0RZ93lyyI_rDDe88iGQo_fpJTc&sec=rrJnEyYU9sETaZG8kEbobbhGGfae7rU0SQNCkBidT90&iv=t9YVnta7aLw0qEh5GJW8Lg', filename='Alan Walker, Putri Ariani, Peder Elias - Who I Am (Official Music Video) - Alan Walker (1080p, h264, youtube).mp4')
   """
   ```

#### Audio

   ```python
   from ytube_api import Ytube
   yt = Ytube()
   search_results = yt.search_videos(
      "Alan Walker songs"
   )
   target_video = search_results.items[0]
   download_link = yt.get_download_link(
      target_video,
      format="mp3",
      quality="320"
      )
   print(
      download_link
   )
   """
   DownloadLink(status='tunnel', url='https://xdcf.nmnm.store/tunnel?id=5K8ZukESJDx0ov3liUj_N&exp=1729856389952&sig=D9ejkqecxpkBsxcXmBtIrYXo1BMIFyawLoBC1_X3J3Q&sec=L5EpDuWoxXk6dK2pLqK9jYyqNF0X06_YKtb9gLB6SVs&iv=YGnrLa_v5qh9uVQSe1x_Og', filename='Alan Walker, Putri Ariani, Peder Elias - Who I Am (Official Music Video) - Alan Walker (youtube).mp3')
   """
   ```

### Download

   ```python
   from ytube_api import Ytube
   yt = Ytube()
   search_results = yt.search_videos(
      "Alan Walker songs"
   )
   target_video = search_results.items[0]
   download_link = yt.get_download_link(
      target_video,
      format="mp3",
      quality="320"
      )
   saved_to = yt.download(
      download_link,
      progress_bar=True,
      quiet=False
   )
   print(saved_to)
   """
   /home/smartwa/git/smartwa/ytube-api/Alan Walker, Putri Ariani, Peder Elias - Who I Am (Official Music Video) - Alan Walker (youtube).mp3
   """
   ```

### Query suggestions

```python
from ytube_api import Ytube
yt = Ytube()

suggestions = yt.suggest_queries(
    'Hello wor'
)

print(
    suggestions
)

"""
['hello world', 'hello world song', 'hello world bump of chicken', 'hello world gwen stefani', 'hello worker', 'hello world louie zong', 'hello world in assembly language', 'hello world in different languages', 'hello world trailer', 'hello world english cover', 'hello world belle perez', 'hello world anime', 'hello world kekkai sensen', 'hello world lost game']
"""
```

</details>

<details>
  <summary>
   <h2>2. CLI</h2>
  </summary>

`$ python -m ytube_api --help`

```
Usage: ytube [OPTIONS] COMMAND [ARGS]...

  Download YouTube videos in mp4 and mp3 formats

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  download     Search and download video in mp4 or mp3 formats
  interactive  Search and download videos/audio interactively
  suggest      Suggest videos based on your query

```

> [!NOTE]
> Shorthand for `python -m pytube_api` is `pytube`.

### Download

   ```sh
   $ ytube download <QUERY>
   # e.g ytube download "Alan walker songs"
   ```
   
   _$ ytube download --help_
   
   ```
   Usage: ytube download [OPTIONS] QUERY

  Search and download video in mp4 or mp3 formats

Options:
  -q, --quality [128|320|144|240|360|480|720|1080|128|720]
                                  Media download quality - 128|720
  --mp4 / --mp3                   Download audio (mp3) or video (mp4) -
                                  mp4
  --enable-progressbar / --disable-progressbar
                                  Show or hide progressbar
  -l, --limit INTEGER             Total number of items to be downloaded
                                  that matched the search - 1
  -t, --timeout INTEGER           Http request timeout - 20
  -c, --channels Name             Download videos posted by this channel
                                  titles - None.
  -d, --dir DIRECTORY             Directory for saving the contents to -
                                  pwd.
  -o, --output TEXT               Filename to save the contents under -
                                  None
  -b, --busy-bar INTEGER RANGE    Busy bar index - ['', '/','■█■■■',
                                  '⡿'] - 2  [0<=x<=3]
  --quiet                         Do not stdout informative messages
  --resume                        Resume incomplete download
  --confirm                       Ask user for permission to download a
                                  video/audio
  --help                          Show this message and exit.

   ```

## Interactive

- Features live search 🔴 etc.

```
Welcome to interactive ytube. Type 'help' or 'h' for usage info.
Submit any bug at https://github.com/Simatwa/ytube/issues/new
╭─[Smartwa@YTUBE]~[🕒18:07:27-💻00:00:00-⚡0.0s] 
╰─>Alan Walker
               alan walker                 
               alan walker faded           
               alan walker on my way live  
               alan walker sad sometimes   
               alan walker spectre         
               alan walker alone           
               alan walker mix             

```

<details>
<summary><code>ytube interactive --help</code></summary>

```
Usage: ytube interactive [OPTIONS] [QUERY]

  Search and download videos/audio interactively

Options:
  -q, --quality [128|320|144|240|360|480|720|1080|128|720|128|720]
                                  Media download quality - 128|720
  --mp4 / --mp3                   Download audio (mp3) or video (mp4) -
                                  mp4
  -s, --suggestions-limit INTEGER
                                  Query suggestions limit - 10
  -l, --limit INTEGER             Total number of items to be downloaded
                                  that matched the search - 1
  -t, --timeout INTEGER           Http request timeout - 20
  -b, --busy-bar INTEGER RANGE    Busy bar index - ['', '/','■█■■■',
                                  '⡿'] - 2  [0<=x<=3]
  -d, --dir DIRECTORY             Directory for saving the contents to -
                                  pwd.
  --disable-coloring              Stdout interactive texts in white font
                                  color
  --select                        Prompt user download format and
                                  quality every time.
  --confirm                       Ask user for permission to download a
                                  video/audio
  --play                          Play the video/audio after completing
                                  download process
  --help                          Show this message and exit.
```

</details>

> [!NOTE]
> **Interactive** is the default option incase no command/argument is supplied.
> `$ ytube` is enough to kickoff.

</details>

# Disclaimer

This software is not affiliated with or endorsed by y2mate.tube or its parent company. By using this tool, you assume all risks associated with using this unofficial tool.It is your responsibility to ensure compliance with all relevant laws and regulations when using this tool. This software is provided "as-is" without warranty of any kind, express or implied.