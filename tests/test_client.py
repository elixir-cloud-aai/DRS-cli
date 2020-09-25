"""Unit tests for DRS client."""

import json
import socket
import unittest

import pytest
import requests
import requests_mock

from drs_cli.client import DRSClient
from drs_cli.errors import (
    InvalidResponseError,
    InvalidObjectData,
    InvalidURI
)
from tests.mock_data import (
    MOCK_ACCESS_URL,
    MOCK_BASE_PATH,
    MOCK_DRS_URI,
    MOCK_DRS_URL,
    MOCK_DRS_URI_INVALID,
    MOCK_DRS_URI_LONG,
    MOCK_ERROR,
    MOCK_HOST,
    MOCK_ID,
    MOCK_OBJECT_GET,
    MOCK_OBJECT_GET_INVALID,
    MOCK_OBJECT_POST,
    MOCK_OBJECT_POST_INVALID,
    MOCK_PORT,
    MOCK_TOKEN,
)


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
        cli = DRSClient(
            uri=MOCK_DRS_URI,
            base_path=MOCK_BASE_PATH
        )
        self.assertEqual(
            cli.uri,
            f"{MOCK_HOST}:443/{MOCK_BASE_PATH}"
        )

        with pytest.raises(InvalidURI):
            cli = DRSClient(
                uri=MOCK_DRS_URI_INVALID,
                base_path=MOCK_BASE_PATH
            )

        with pytest.raises(InvalidURI):
            cli = DRSClient(
                uri=MOCK_DRS_URI_LONG,
                base_path=MOCK_BASE_PATH
            )
            print(MOCK_DRS_URI_LONG)

    def test_get_object(self):
        """Test get_object url"""
        with requests_mock.Mocker() as m:
            m.get(
                f"{self.cli.uri}/objects/{MOCK_ID}",
                status_code=200,
                json=MOCK_OBJECT_GET,
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
                f"{MOCK_DRS_URL}/{MOCK_ID}"
            )

            m.get(
                f"{self.cli.uri}/objects/{MOCK_ID}",
                exc=requests.exceptions.ConnectionError
            )
            with pytest.raises(requests.exceptions.ConnectionError):
                self.cli.get_object(object_id=MOCK_ID)

            m.get(
                f"{self.cli.uri}/objects/{MOCK_ID}",
                status_code=404,
                text="mock_text",
            )
            with pytest.raises(InvalidResponseError):
                self.cli.get_object(object_id=MOCK_ID)

            m.get(
                f"{self.cli.uri}/objects/{MOCK_ID}",
                status_code=200,
                json=MOCK_OBJECT_GET_INVALID,
            )
            with pytest.raises(InvalidResponseError):
                self.cli.get_object(object_id=MOCK_ID)

    def test_get_object_token(self):
        """Test get_object url with token"""
        with requests_mock.Mocker() as m:
            m.get(
                f"{self.cli_t.uri}/objects/{MOCK_ID}",
                status_code=200,
                json=MOCK_OBJECT_GET,
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
                f"{self.cli.uri}/objects/{MOCK_ID}/access/{MOCK_ID}",
                status_code=200,
                json=MOCK_ACCESS_URL,
            )
            self.cli.get_access_url(
                object_id=MOCK_ID,
                access_id=MOCK_ID,
            )
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}/{MOCK_ID}/access/{MOCK_ID}",
            )
            m.get(
                f"{self.cli.uri}/objects/{MOCK_ID}/access/{MOCK_ID}",
                status_code=404,
                json=MOCK_ERROR,
            )
            self.cli.get_access_url(
                object_id=MOCK_ID,
                access_id=MOCK_ID,
            )
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}/{MOCK_ID}/access/{MOCK_ID}",
            )

            m.get(
                f"{self.cli.uri}/objects/{MOCK_ID}/access/{MOCK_ID}",
                exc=requests.exceptions.ConnectionError
            )
            with pytest.raises(requests.exceptions.ConnectionError):
                self.cli.get_access_url(
                    object_id=MOCK_ID,
                    access_id=MOCK_ID,
                )

            m.get(
                f"{self.cli.uri}/objects/{MOCK_ID}/access/{MOCK_ID}",
                status_code=404,
                text="mock_text",
            )
            with pytest.raises(InvalidResponseError):
                self.cli.get_access_url(
                    object_id=MOCK_ID,
                    access_id=MOCK_ID,
                )

            m.get(
                f"{self.cli.uri}/objects/{MOCK_ID}/access/{MOCK_ID}",
                status_code=200,
                json=MOCK_OBJECT_GET_INVALID,
            )
            with pytest.raises(InvalidResponseError):
                self.cli.get_access_url(
                    object_id=MOCK_ID,
                    access_id=MOCK_ID,
                )

    def test_get_access_url_token(self):
        """Test get_access_url url with token"""
        with requests_mock.Mocker() as m:
            m.get(
                f"{self.cli_t.uri}/objects/{MOCK_ID}/access/{MOCK_ID}",
                status_code=200,
                json=MOCK_ACCESS_URL,
            )
            self.cli_t.get_access_url(
                object_id=MOCK_ID,
                access_id=MOCK_ID,
                token=MOCK_TOKEN,
            )
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}/{MOCK_ID}/access/{MOCK_ID}",
            )

    def test_post_object(self):
        """Test post_object url"""
        with requests_mock.Mocker() as m:
            m.post(
                f"{self.cli.uri}/objects",
                status_code=200,
                json=MOCK_ID,
            )
            json_string = json.dumps(MOCK_OBJECT_POST)
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
            json_string = json.dumps(MOCK_OBJECT_POST)
            json_data = json.loads(json_string)
            self.cli.post_object(json_data)
            self.assertEqual(
                m.last_request.url,
                f"{MOCK_DRS_URL}",
            )

            m.post(
                f"{self.cli.uri}/objects",
                status_code=200,
                json=MOCK_ID,
            )
            json_string = json.dumps(MOCK_OBJECT_POST_INVALID)
            json_data = json.loads(json_string)
            with pytest.raises(InvalidObjectData):
                self.cli.post_object(json_data)

            m.post(
                f"{self.cli.uri}/objects",
                exc=socket.gaierror
            )
            json_string = json.dumps(MOCK_OBJECT_POST)
            json_data = json.loads(json_string)
            with pytest.raises(requests.exceptions.ConnectionError):
                self.cli.post_object(json_data)

            m.post(
                f"{self.cli.uri}/objects",
                status_code=404,
                text="mock_text",
            )
            with pytest.raises(InvalidResponseError):
                self.cli.post_object(json_data)

            m.post(
                f"{self.cli.uri}/objects",
                status_code=200,
                text="mock_text"
            )
            with pytest.raises(InvalidResponseError):
                self.cli.post_object(json_data)

    def test_post_object_token(self):
        """Test post_object url with token"""
        with requests_mock.Mocker() as m:
            m.post(
                f"{self.cli_t.uri}/objects",
                status_code=200,
                json=MOCK_ID,
            )
            json_string = json.dumps(MOCK_OBJECT_POST)
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

            m.delete(
                f"{self.cli.uri}/objects/{MOCK_ID}",
                exc=requests.exceptions.ConnectionError
            )
            with pytest.raises(requests.exceptions.ConnectionError):
                self.cli.delete_object(object_id=MOCK_ID)

            m.delete(
                f"{self.cli.uri}/objects/{MOCK_ID}",
                status_code=404,
                text="mock_text",
            )
            with pytest.raises(InvalidResponseError):
                self.cli.delete_object(object_id=MOCK_ID)

            m.delete(
                f"{self.cli.uri}/objects/{MOCK_ID}",
                status_code=200,
                text="mock_text",
            )
            with pytest.raises(InvalidResponseError):
                self.cli.delete_object(object_id=MOCK_ID)

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
