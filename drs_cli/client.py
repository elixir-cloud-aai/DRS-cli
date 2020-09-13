"""Class implementing DRS client."""

import logging
import requests
from typing import (Dict, Optional, Union)

from drs_cli.utils import (
    check_drs_uri_regex,
    check_http_uri_regex,
    check_https_uri_regex,
    check_drs_id_regex,
    get_drs_uri_host_and_id,
    get_http_uri_host,
    get_https_uri_host
)
from drs_cli.models import (AccessURL, DrsObject, Error, PostDrsObject)
from drs_cli.errors import DRS_URI_FORMAT_ERROR

logger = logging.getLogger(__name__)


class DRSClient():
    """Client to communicate with a GA4GH DRS instance.
    Supports additional endpoints defined in DRS-filer.
    (https://github.com/elixir-cloud-aai/drs-filer)

    Args:
        host: Base URL of DRS instance.
        port: Port at which DRS instance can be accessed.
        base-path: Path at which DRS endpoints can be accessed.
        token: Bearer token for authentication.

    Attributes:
        url: URL to DRS endpoints, composed of `host`, `port` and `base_path`,
            e.g.,"https://my-drs.app:8080/ga4gh/drs/v1"
        token: Bearer token for authentication.
        headers: Dictionary of request headers.
    """

    def __init__(
        self,
        uri: str = 'http://0.0.0.0',
        port: int = 443,
        base_path: str = 'ga4gh/drs/v1',
        token: Optional[str] = None,
    ) -> Union[None, Error]:
        
        if check_drs_uri_regex(uri):
            drs_host = get_drs_uri_host_and_id(uri)[0]
            if port is self.__init__.__defaults__[1]:
                self.url = f"https://{drs_host}/{base_path}"
            else:
                self.url = f"http://{drs_host}:{port}/{base_path}"
        elif check_http_uri_regex(uri):
            drs_host = get_http_uri_host(uri)
            self.uri = f"http://{drs_host}:{port}/{base_path}"
        elif check_https_uri_regex(uri):
            drs_host = get_https_uri_host(uri)
            self.uri = f"https://{drs_host}/{base_path}"
        else:
            return Error(**DRS_URI_FORMAT_ERROR)
        self.token = token
        self._get_headers()
        logger.info(f"API URL: {self.url}")

    def get_object(
        self,
        drs_object: str,
        token: Optional[str] = None,
    ) -> Union[Error, DrsObject]:
        """Access DRS object.

        Args:
            object_id: Identifier of DRS object to be retrieved.
            token: Bearer token for authentication.

        Returns:
            Unmarshalled DRS response as either an instance of `DRSObject`
            in case of a `200` response, or an instance of `Error` for all
            other reponses.

        Raises:
            pydantic.ValidationError: The returned response does not conform
                to the models defined in the API specification.
        """
        if check_drs_id_regex(drs_object):
            drs_object_id = drs_object
        elif check_drs_uri_regex(drs_object):
            drs_object_id = get_drs_uri_host_and_id(drs_object)[1]
        else:
            return Error(**DRS_URI_FORMAT_ERROR)
        request_url = f"{self.url}/objects/{drs_object_id}"
        # print(request_url)
        logger.info(f"Request URL: {request_url}")      
        if token:
            self.token = token
            self._get_headers()
        response = requests.get(
            url=request_url,
            headers=self.headers,
        )
        if response.status_code == 200:
            logger.info(f"Retrieved object '{drs_object_id}'")
            return DrsObject(**response.json())
        else:
            return Error(**response.json())

    def get_access_url(
        self,
        object_id: str,
        access_id: str,
        token: Optional[str] = None,
    ) -> Union[AccessURL, Error]:
        """Obtain access URL of DRS object.

        Args:
            object_id: Identifier of DRS object to be retrieved.
            access_id: Identifier of method giving access to DRS object.
            token: Bearer token for authentication.

        Returns:
            Unmarshalled DRS response as either an instance of `AccessURL`
            in case of a `200` response, or an instance of `Error` for all
            other reponses.

        Raises:
            pydantic.ValidationError: The returned response does not conform
                to the models defined in the API specification.
        """
        request_url = f"{self.url}/objects/{object_id}/access/{access_id}"
        if token:
            self.token = token
            self._get_headers()
        response = requests.get(
            url=request_url,
            headers=self.headers,
        )
        if response.status_code == 200:
            logger.info(
                f"Retrieved access URL of object '{object_id}' (access ID: "
                f"'{access_id}')")
            return AccessURL(**response.json())
        else:
            return Error(**response.json())

    def post_object(
        self,
        object_data: Dict,
        token: Optional[str] = None,
    ) -> Union[Dict, Error]:
        """Register DRS object.

        Args:
            object_data: DRS object data.
            token: Bearer token for authentication.

        Returns:
            ID of registered DRS object in case of a `200` response, or an
            instance of `Error` for all other responses.

        Raises:
            pydantic.ValidationError: The built request or the returned
                response do not conform to the models defined in the API
                specification.
            TypeError: The returned `200` response object is invalid.
        """
        request_url = f"{self.url}/objects"
        if token:
            self.token = token
            self._get_headers()
        # validate outgoing payload
        PostDrsObject(**object_data).dict()
        response = requests.post(
            url=request_url,
            json=object_data,
            headers=self.headers,
        )
        if response.status_code == 200:
            object_id = str(response.json())
            logger.info(f"Object '{object_id}' registered")
            return object_id
        else:
            return Error(**response.json())

    def delete_object(
        self,
        object_id: str,
        token: Optional[str] = None,
    ) -> Union[Dict, Error]:
        """Delete DRS object.

        Args:
            object_id: Identifier of DRS object to be deleted.
            token: Bearer token for authentication.

        Returns:
            ID of previously registered DRS object in case of a `200`
            response, or an instance of `Error` for all other responses.

        Raises:
            pydantic.ValidationError: The built request or the returned
                response do not conform to the models defined in the API
                specification.
            TypeError: The returned `200` response object is invalid.
        """
        request_url = f"{self.url}/objects/{object_id}"
        if token:
            self.token = token
            self._get_headers()
        response = requests.delete(
            url=request_url,
            headers=self.headers,
        )
        if response.status_code == 200:
            object_id = str(response.json())
            logger.info(f"Object '{object_id}' deleted")
            return object_id
        else:
            return Error(**response.json())

    def _get_headers(self):
        """Set dictionary of request headers in `self.headers`."""
        self.headers: Dict = {
            'Content-type': 'application/json',
        }
        if self.token:
            self.headers['Authorization'] = 'Bearer ' + self.token


