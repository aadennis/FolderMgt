
import pytest

@pytest.mark.parametrize("val_a,val_b,answer", [(1,2,3), (5,7,12), (10,15,25)])
def test_add_numbers(val_a, val_b, answer):
    assert val_a + val_b == answer
