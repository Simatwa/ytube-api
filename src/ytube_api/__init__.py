"""
This package does the holy work of
downloading a YouTube video in `1080p` quality
and below as well as the audio version of the
video in `320kpbs` or `128kbps` qualities.

1. By default downloads video in `720p`

```python
from ytube_api import Auto
Auto(
  query = "Alan Walker - Alone"
)
```

2. Download video in `1080p`

```python
from ytube_api import Auto
Auto(
  query = "Alan Walker - Alone",
  quality="1080"
)
```

3. Download audio in `128kpbs`

```python
from ytube_api import Auto
Auto(
  query = "Alan Walker - Alone",
  format="mp3"
)
```

4. Download audio in `320kpbs`

```python
from ytube_api import Auto
Auto(
  query = "Alan Walker - Alone",
  format="mp3",
  quality="320"
)
```

"""

from ytube_api.main import Ytube, Auto
from importlib import metadata

try:
    __version__ = metadata.version("ytube-api")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__author__ = "Smartwa"
__repo__ = "https://github.com/Simatwa/ytube"
__info__ = "Unofficial wrapper for y2mate.tube"

__all__ = ["Ytube", "Auto"]
