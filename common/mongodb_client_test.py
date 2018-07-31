"""Test MongoDB client"""

import mongodb_client as client

def test_basic():
    """Test MongoDB client basically"""
    database = client.get_db('test')
    database.test.drop()
    assert database.test.count() == 0

    database.test.insert({'test': 1})
    assert database.test.count() == 1

    database.test.drop()
    assert database.test.count() == 0

    print('test_basic passed!')

if __name__ == "__main__":
    test_basic()
