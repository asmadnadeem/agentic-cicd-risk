import pytest

def test_database_connection_timeout():
    """Regression test for fallback timeout config."""
    from db import get_connection
    conn = get_connection(timeout=None)
    assert conn.timeout == 30, "Default timeout should be 30 seconds"