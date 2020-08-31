from drs_client.client import DRSClient
import requests
import requests_mock
import unittest
import uuid
import json


OBJECT_JSON_POST_DATA = {
    "created_time": "2019-05-20T00:12:34-07:00",
    "updated_time": "2019-04-24T05:23:43-06:00",
    "version": "1",
    "size": 5,
    "mime_type": "",
    "checksums": [
        {
            "checksum": "18c2f5517e4ddc02cd57f6c7554b8e88",
            "type": "md5"
        }
    ],
    "access_methods": [
        {
            "type": "ftp",
            "access_url": {
                "url": "drs://ftp.ensembl.org/pub/release-81/bed/ensembl-compara/11_teleost_fish.gerp_constrained_eleme",
                "headers":  [
                    "None"
                ]
            }
        }
    ]
}

OBJECT_JSON_GET_DATA = {
    "id": "abc",
    "self_uri": "drs://abc.com",
    "created_time": "2019-05-20T00:12:34-07:00",
    "updated_time": "2019-04-24T05:23:43-06:00",
    "version": "1",
    "size": 5,
    "mime_type": "",
    "checksums": [
        {
          "checksum": "18c2f5517e4ddc02cd57f6c7554b8e88",
          "type": "md5"
        }
    ],
    "access_methods": [
        {
            "type": "ftp",
            "access_url": {
                "url": "drs://ftp.ensembl.org/pub/release-81/bed/ensembl-compara/11_teleost_fish.gerp_constrained_eleme",
                "headers":  [
                    "None"
                ]
            },
            "access_id": "def"
        }
    ]
}

ACCESS_URL_GET_DATA = {
    "url": "drs://ftp.ensembl.org/pub/release-81/bed/ensembl-compara/11_teleost_fish.gerp_constrained_eleme",
    "headers":  [
        "None"
    ]
}

MOCK_ERROR = {
    "msg": "mock_message",
    "status_code": "400"
}


class TestDRSClient(unittest.TestCase):

    mock_id = str(uuid.uuid4())
    mock_host = "http://fakehost"
    mock_port = "8080"

    cli = DRSClient(host=mock_host, port=mock_port)

    def test_cli(self):
        """Test url attribute"""
        cli = DRSClient(host="http://0.0.0.0", port="80", base_path="a/b/c")
        self.assertEqual(cli.url, "http://0.0.0.0:80/a/b/c")


    def test_get_object(self):
        """Test get_object url"""
        with requests_mock.Mocker() as m:
            mock_id = "abc"
            m.get(
                f"{self.cli.url}/objects/{mock_id}",
                status_code=200,
                json=OBJECT_JSON_GET_DATA
            )
            self.cli.get_object("abc")
            self.assertEqual(
                m.last_request.url, f"http://fakehost:8080/ga4gh/drs/v1/objects/{mock_id}")
            
            m.get(
                f"{self.cli.url}/objects/{mock_id}",
                status_code=404,
                json = MOCK_ERROR
            )
            self.cli.get_object("abc")
            self.assertEqual(
                m.last_request.url, f"http://fakehost:8080/ga4gh/drs/v1/objects/{mock_id}")


    def test_get_object_token(self):
        """Test get_object url with token"""
        cli = DRSClient(host=self.mock_host, port=self.mock_port, token="123")
        with requests_mock.Mocker() as m:
            mock_id = "abc"
            m.get(
                f"{cli.url}/objects/{mock_id}",
                status_code=200,
                json=OBJECT_JSON_GET_DATA
            )
            cli.get_object("abc")
            self.assertEqual(
                m.last_request.url, f"http://fakehost:8080/ga4gh/drs/v1/objects/{mock_id}")
    

    def test_get_access_url(self):
        """Test get_access_url url"""
        with requests_mock.Mocker() as m:
            mock_id = "abc"
            mock_access_id = "def"
            m.get(
                f"{self.cli.url}/objects/{mock_id}/access/{mock_access_id}",
                status_code=200,
                json=ACCESS_URL_GET_DATA
            )
            self.cli.get_access_url("abc", "def")
            self.assertEqual(
                m.last_request.url, f"http://fakehost:8080/ga4gh/drs/v1/objects/{mock_id}/access/{mock_access_id}")

            m.get(
                f"{self.cli.url}/objects/{mock_id}/access/{mock_access_id}",
                status_code=404,
                json=MOCK_ERROR
            )
            self.cli.get_access_url("abc", "def")
            self.assertEqual(
                m.last_request.url, f"http://fakehost:8080/ga4gh/drs/v1/objects/{mock_id}/access/{mock_access_id}")


    def test_get_access_url_token(self):
        """Test get_access_url url with token"""
        cli = DRSClient(host=self.mock_host, port=self.mock_port, token="123")
        with requests_mock.Mocker() as m:
            mock_id = "abc"
            mock_access_id = "def"
            m.get(
                f"{cli.url}/objects/{mock_id}/access/{mock_access_id}",
                status_code=200,
                json=ACCESS_URL_GET_DATA
            )
            cli.get_access_url("abc", "def")
            self.assertEqual(
                m.last_request.url, f"http://fakehost:8080/ga4gh/drs/v1/objects/{mock_id}/access/{mock_access_id}")


    def test_post_object(self):
        """Test post_object url"""
        with requests_mock.Mocker() as m:
            m.post(
                f"{self.cli.url}/objects",
                status_code=200,
                json="abc"
            )
            json_string = json.dumps(OBJECT_JSON_POST_DATA)
            json_data = json.loads(json_string)
            self.cli.post_object(json_data)
            self.assertEqual(m.last_request.url, f"http://fakehost:8080/ga4gh/drs/v1/objects")

            m.post(
                f"{self.cli.url}/objects",
                status_code=400,
                json=MOCK_ERROR
            )
            json_string = json.dumps(OBJECT_JSON_POST_DATA)
            json_data = json.loads(json_string)
            self.cli.post_object(json_data)
            self.assertEqual(m.last_request.url, f"http://fakehost:8080/ga4gh/drs/v1/objects")


    def test_post_object_token(self):
        """Test post_object url with token"""
        cli = DRSClient(host=self.mock_host, port=self.mock_port, token="123")
        with requests_mock.Mocker() as m:
            m.post(
                f"{cli.url}/objects",
                status_code=200,
                json="abc"
            )
            json_string = json.dumps(OBJECT_JSON_POST_DATA)
            json_data = json.loads(json_string)
            cli.post_object(json_data)
            self.assertEqual(m.last_request.url, f"http://fakehost:8080/ga4gh/drs/v1/objects")


    def test_delete_object(self):
        """Test delete_object url"""
        with requests_mock.Mocker() as m:
            mock_id = "abc"
            m.delete(
                f"{self.cli.url}/objects/{mock_id}",
                status_code=200,
                json="abc"
            )
            self.cli.delete_object("abc")
            self.assertEqual(
                m.last_request.url, f"http://fakehost:8080/ga4gh/drs/v1/objects/{mock_id}")

            m.delete(
                f"{self.cli.url}/objects/{mock_id}",
                status_code=400,
                json=MOCK_ERROR
            )
            self.cli.delete_object("abc")
            self.assertEqual(
                m.last_request.url, f"http://fakehost:8080/ga4gh/drs/v1/objects/{mock_id}")


    def test_delete_object_token(self):
        """Test delete_object url with token"""
        cli = DRSClient(host=self.mock_host, port=self.mock_port, token="123")
        with requests_mock.Mocker() as m:
            mock_id = "abc"
            m.delete(
                f"{cli.url}/objects/{mock_id}",
                status_code=200,
                json="abc"
            )
            cli.delete_object("abc")
            self.assertEqual(
                m.last_request.url, f"http://fakehost:8080/ga4gh/drs/v1/objects/{mock_id}")