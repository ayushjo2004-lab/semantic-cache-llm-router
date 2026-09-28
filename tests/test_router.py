from app.router import route

def test_simple():
    assert route("What is Python?") == "small"

def test_complex():
    assert route("Compare and analyze SQL vs NoSQL architecture trade-offs") == "large"
