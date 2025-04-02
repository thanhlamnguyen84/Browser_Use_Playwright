def add(a, b):
    return a + b
# @pytest.mark.smoke
def test_addition():
    assert add(2, 3) == 5  # Pass
    assert add(2, 2) == 4  # Fail
