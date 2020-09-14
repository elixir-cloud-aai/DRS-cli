"""Unit tests for DRS client."""

import requests_mock
import unittest
import uuid
import json

from drs_cli.client import DRSClient

MOCK_ID = str(uuid.uuid4())
MOCK_ACCESS_ID = str(uuid.uuid4())
MOCK_HOST = "http://fakehost.com"
MOCK_PORT = 8080
MOCK_BASE_PATH = "a/b/c"
MOCK_TOKEN = "MyT0k3n"
MOCK_DRS_URL = f"{MOCK_HOST}:{MOCK_PORT}/ga4gh/drs/v1/objects"
ACCESS_URL_GET_DATA = {
    "url": "ftp://my.ftp.service/my_path/my_file_01.txt",
    "headers":  [
        "None"
    ],
}
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
            "access_url": ACCESS_URL_GET_DATA,
        }
    ]
}
OBJECT_JSON_GET_DATA = {
    "id": MOCK_ID,
    "self_uri": "drs://abc.com",
    **OBJECT_JSON_POST_DATA,
    "access_methods": [
        {
            "type": "ftp",
            "access_url": ACCESS_URL_GET_DATA,
            "access_id": MOCK_ACCESS_ID,
        }
    ],
}
MOCK_ERROR = {
    "msg": "mock_message",
    "status_code": "400"
}


class TestDRSClient(unittest.TestCase):

    cli = DRSClient(
        uri=MOCK_HOST,
        port=MOCK_PORT,
    )
    cli_t = DRSClient(
        uri=MOCK_HOST,
        port=MOCK_PORT,
        token=MOCK_TOKEN,
    )

    def test_cli(self):
        """Test url attribute"""
        cli = DRSClient(
            uri=MOCK_HOST,
            port=MOCK_PORT,
            base_path=MOCK_BASE_PATH,
        )
        self.assertEqual(
            cli.uri,
            f"{MOCK_HOST}:{MOCK_PORT}/{MOCK_BASE_PATH}",
        )

    def test_get_object(self):
        """Test get_object url"""
        with requests_mock.Mocker() as m:
            m.get(
                f"{self.cli.uri}/objects/{MOCK_ID}",
                status_code=200,
                json=OBJECT_JSON_GET_DATA,
            )
            self.cli.get_object(object_id=MOCK_ID)
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}/{MOCK_ID}",
            )

            m.get(
                f"{self.cli.uri}/objects/{MOCK_ID}",
                status_code=404,
                json=MOCK_ERROR,
            )
            self.cli.get_object(object_id=MOCK_ID)
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}/{MOCK_ID}",
            )

    def test_get_object_token(self):
        """Test get_object url with token"""
        with requests_mock.Mocker() as m:
            m.get(
                f"{self.cli_t.uri}/objects/{MOCK_ID}",
                status_code=200,
                json=OBJECT_JSON_GET_DATA,
            )
            self.cli_t.get_object(
                object_id=MOCK_ID,
                token=MOCK_TOKEN,
            )
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}/{MOCK_ID}",
            )

    def test_get_access_url(self):
        """Test get_access_url"""
        with requests_mock.Mocker() as m:
            m.get(
                f"{self.cli.uri}/objects/{MOCK_ID}/access/{MOCK_ACCESS_ID}",
                status_code=200,
                json=ACCESS_URL_GET_DATA,
            )
            self.cli.get_access_url(
                object_id=MOCK_ID,
                access_id=MOCK_ACCESS_ID,
            )
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}/{MOCK_ID}/access/{MOCK_ACCESS_ID}",
            )
            m.get(
                f"{self.cli.uri}/objects/{MOCK_ID}/access/{MOCK_ACCESS_ID}",
                status_code=404,
                json=MOCK_ERROR,
            )
            self.cli.get_access_url(
                object_id=MOCK_ID,
                access_id=MOCK_ACCESS_ID,
            )
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}/{MOCK_ID}/access/{MOCK_ACCESS_ID}",
            )

    def test_get_access_url_token(self):
        """Test get_access_url url with token"""
        with requests_mock.Mocker() as m:
            m.get(
                f"{self.cli_t.uri}/objects/{MOCK_ID}/access/{MOCK_ACCESS_ID}",
                status_code=200,
                json=ACCESS_URL_GET_DATA,
            )
            self.cli_t.get_access_url(
                object_id=MOCK_ID,
                access_id=MOCK_ACCESS_ID,
                token=MOCK_TOKEN,
            )
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}/{MOCK_ID}/access/{MOCK_ACCESS_ID}",
            )

    def test_post_object(self):
        """Test post_object url"""
        with requests_mock.Mocker() as m:
            m.post(
                f"{self.cli.uri}/objects",
                status_code=200,
                json=MOCK_ID,
            )
            json_string = json.dumps(OBJECT_JSON_POST_DATA)
            json_data = json.loads(json_string)
            self.cli.post_object(json_data)
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}",
            )
            m.post(
                f"{self.cli.uri}/objects",
                status_code=400,
                json=MOCK_ERROR,
            )
            json_string = json.dumps(OBJECT_JSON_POST_DATA)
            json_data = json.loads(json_string)
            self.cli.post_object(json_data)
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}",
            )

    def test_post_object_token(self):
        """Test post_object url with token"""
        with requests_mock.Mocker() as m:
            m.post(
                f"{self.cli_t.uri}/objects",
                status_code=200,
                json=MOCK_ID,
            )
            json_string = json.dumps(OBJECT_JSON_POST_DATA)
            json_data = json.loads(json_string)
            self.cli_t.post_object(
                object_data=json_data,
                token=MOCK_ID,
            )
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}",
            )

    def test_delete_object(self):
        """Test delete_object url"""
        with requests_mock.Mocker() as m:
            m.delete(
                f"{self.cli.uri}/objects/{MOCK_ID}",
                status_code=200,
                json=MOCK_ID,
            )
            self.cli.delete_object(object_id=MOCK_ID)
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}/{MOCK_ID}",
            )

            m.delete(
                f"{self.cli.uri}/objects/{MOCK_ID}",
                status_code=400,
                json=MOCK_ERROR,
            )
            self.cli.delete_object(object_id=MOCK_ID)
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}/{MOCK_ID}",
            )

    def test_delete_object_token(self):
        """Test delete_object url with token"""
        with requests_mock.Mocker() as m:
            m.delete(
                f"{self.cli_t.uri}/objects/{MOCK_ID}",
                status_code=200,
                json=MOCK_ID,
            )
            self.cli_t.delete_object(
                object_id=MOCK_ID,
                token=MOCK_TOKEN,
            )
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}/{MOCK_ID}",
            )
