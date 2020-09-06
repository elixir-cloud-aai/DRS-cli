"""Class implementing DRS client."""

import logging
import requests
import re
from typing import (Dict, Optional, Tuple, Union)

from drs_cli.models import (AccessURL, DrsObject, Error, PostDrsObject)
from drs_cli.errors import DRS_URI_FORMAT_ERROR

logger = logging.getLogger(__name__)

DRS_URI_PATTERN = r'^drs:\/\/([A-Za-z0-9.]+)\/([A-Za-z0-9.-_~]+$)'

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
        host: str = 'http://0.0.0.0',
        port: int = 80,
        base_path: str = 'ga4gh/drs/v1',
        token: Optional[str] = None,
    ) -> None:
        self.url = f"{host}:{port}/{base_path}"
        self.base_path = base_path
        self.token = token
        self._get_headers()
        logger.info(f"API URL: {self.url}")

    def get_object(
        self,
        object_id: Optional[str] = None,
        drs_uri: Optional[str] = None,
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
        
        if drs_uri:
            if _check_drs_regex(drs_uri):
                host_and_id = _get_host_and_id(drs_uri)
                object_id = host_and_id[1]
                self.url = f"http://{host_and_id[0]}/{self.base_path}"
            else:
                return Error(**DRS_URI_FORMAT_ERROR)
        
        request_url = f"{self.url}/objects/{object_id}"
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
            logger.info(f"Retrieved object '{object_id}'")
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


def _check_drs_regex(uri) -> bool:
    isMatch = re.fullmatch(DRS_URI_PATTERN, uri)
    if isMatch:
        return True
    else:
        return False

def _get_host_and_id(uri) -> Tuple:
    searchObj = re.search( DRS_URI_PATTERN, uri, re.M|re.I)
    return (searchObj.group(1), searchObj.group(2))
