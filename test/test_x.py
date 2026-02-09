import pytest

@pytest.mark.parametrize("val_a, val_b, answer", [(1,2,3), (7,11,18)])
def test_it(val_a, val_b, answer):
    assert val_a + val_b == answer
