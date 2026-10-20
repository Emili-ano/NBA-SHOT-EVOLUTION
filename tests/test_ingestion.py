import hashlib
import tempfile
import unittest
from pathlib import Path

from src.ingestion.download_data import sha256_file


class TestIngestion(unittest.TestCase):

    def test_sha256(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "prueba.txt"
            content = b"NBA SHOT IQ"
            path.write_bytes(content)

            expected = hashlib.sha256(content).hexdigest()
            self.assertEqual(sha256_file(path), expected)


if __name__ == "__main__":
    unittest.main()
