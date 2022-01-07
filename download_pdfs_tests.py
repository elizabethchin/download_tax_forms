import unittest
import download_pdfs
import os

class TestDownloadPDFS(unittest.TestCase):

    def test_download_pdfs(self):
        self.assertEqual(download_pdfs.download_pdfs("", ""), None)
        
        self.assertEqual(download_pdfs.download_pdfs("Form W-2", "2018-2020"), 
        (os.path.exists("Form W-2")))




if __name__ == '__main__':
    unittest.main()