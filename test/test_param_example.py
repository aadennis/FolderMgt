import hashlib
import io
import pytest

@pytest.mark.parametrize("val_a,val_b,answer", [(1,2,3), (5,7,12), (10,15,25)])
def test_add_numbers(val_a, val_b, answer):
    assert val_a + val_b == answer

def test_2():
    data = "Hello World"
    expectedHashresult = hashlib.new("sha256", data.encode()).hexdigest()
    data2 = "Hello World"
    expectedHashresult2 = hashlib.new("sha256", data2.encode()).hexdigest()
    assert expectedHashresult == expectedHashresult2
