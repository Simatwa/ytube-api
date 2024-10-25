import unittest
from os import remove
from ytube_api import Ytube, Auto
import ytube_api.models as models


class TestYtube(unittest.TestCase):

    def setUp(self):
        self.query = "happy birthday"
        self.query_link = "https://youtu.be/Ns623Ibl5l8?si=TW2dmgUBZ3X1jusA"
        self.ytube = Ytube()

    def test_queries_suggestion(self):
        self.assertIsInstance(self.ytube.suggest_queries(self.query), list)

    def test_search_video(self):
        s = self.ytube.search_videos(self.query)
        self.assertIsInstance(s, models.SearchResults)

    def test_search_video_by_link(self):
        s = self.ytube.search_videos(self.query_link)
        self.assertIsInstance(s, models.SearchResults)
        self.assertTrue(s.from_link)

    def test_get_thumbail(self):
        item = self.ytube.search_videos(self.query).items[0]

        self.assertIsInstance(self.ytube.get_thumbnail(item), bytes)

    def test_default_download_link(self):
        item = self.ytube.search_videos(self.query).items[0]

        self.assertIsInstance(self.ytube.get_download_link(item), models.DownloadLink)

    def test_mp3_download_link(self):
        item = self.ytube.search_videos(self.query).items[0]

        self.assertIsInstance(
            self.ytube.get_download_link(
                item,
                format="mp3",
            ),
            models.DownloadLink,
        )

    def test_mp4_download_link(self):
        item = self.ytube.search_videos(self.query).items[0]

        self.assertIsInstance(
            self.ytube.get_download_link(
                item,
                format="mp4",
            ),
            models.DownloadLink,
        )

    def test_mp3_download(self):
        item = self.ytube.search_videos(self.query).items[0]

        download_link = self.ytube.get_download_link(item, format="mp3", quality="128")
        saved_to = self.ytube.download(download_link, progress_bar=False)
        self.assertTrue(saved_to.exists() and saved_to.is_file())
        remove(saved_to)

    def test_mp4_download(self):
        item = self.ytube.search_videos(self.query).items[0]

        download_link = self.ytube.get_download_link(item, format="mp4", quality="144")
        saved_to = self.ytube.download(download_link, progress_bar=False)
        self.assertTrue(saved_to.exists() and saved_to.is_file())
        remove(saved_to)

    def test_auto(self):
        saved_to = Auto(self.query, progress_bar=False)
        self.assertTrue(saved_to.exists() and saved_to.is_file())
        remove(saved_to)


if __name__ == "__main__":
    unittest.main()
