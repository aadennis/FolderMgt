import pytest

@pytest.mark.parametrize('val1, val2, answer',[(1,2,3),(4,90,13),(23,48,71)])
def test_add(val1, val2, answer):
	x = val1 + val2
	assert x == answer