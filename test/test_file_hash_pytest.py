import hashlib
import io
import pytest
from src.index_images import file_hash   # SUT

@pytest.mark.parametrize("data,algo", [
    (b"hello world", "sha256"),
    (b"abc123", "md5"),
    (b"abc123", "sha1"),
    (b"abc123", "sha256"),
])
def test_file_hash_bytesio(data, algo):
    """Test file_hash against known content using BytesIO streams."""
    stream = io.BytesIO(data)
    expected = hashlib.new(algo, data).hexdigest()
    result = file_hash(stream, algo=algo)
    assert result == expected

@pytest.mark.parametrize("size", [1024, 10_000, 1_000_000])
def test_large_bytesio(size):
    """Test file_hash with large in-memory streams."""
    data = b"A" * size
    stream = io.BytesIO(data)
    result = file_hash(stream, algo="sha256")
    assert isinstance(result, str) and len(result) > 0