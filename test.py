import unittest

from app import client


class TestCRUDMethods(unittest.TestCase):
    def test_simple(self):
        my_list = [1, 2, 3, 4, 5]

        assert 1 in my_list

    def test_get(self):
        res = client.get("/tutorials")
        assert res.status_code == 200
        assert len(res.get_json()) == 2
        assert res.get_json()[0]["id"] == 1

    def test_post(self):
        data = {"id": 3, "title": "Test 3 video", "description": "Test test"}
        res = client.post("/tutorials", json=data)
        assert res.status_code == 200
        assert len(res.get_json()) == 3
        assert res.get_json()[-1]["title"] == data["title"]


if __name__ == "__main__":
    unittest.main()
