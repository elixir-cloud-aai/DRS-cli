"""Class implementing DRS client."""

import json
import logging
import re
import requests
import socket
import sys
from typing import (Dict, Optional, Tuple, Union)
from urllib.parse import quote
import urllib3

import pydantic

from drs_cli.models import (AccessURL, DrsObject, Error, PostDrsObject)
from drs_cli.errors import (
    InvalidObjectData, exception_handler,
    InvalidResponseError,
    InvalidURI,
)

logger = logging.getLogger(__name__)
sys.excepthook = exception_handler


class DRSClient():
    """Client to communicate with a GA4GH DRS instance. Supports additional
    endpoints defined in DRS-filer
    (https://github.com/elixir-cloud-aai/drs-filer).

    Arguments:
        uri: Either the base URI of the DRS instance to connect to in either
            'https' or 'http' schema (note that fully compliant DRS instances
            will use 'https' exclusively), e.g., `https://my-drs.app`, OR a
            hostname-based DRS URI, cf.
            https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_hostname_based_drs_uris.
        port: Override default port at which the DRS instance can be accessed.
            Only required for DRS instances that are not fully spec-compliant,
            as the default port is defined in the DRS documentation, cf.
            https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_hostname_based_drs_uris.
        base-path: Override default path at which the DRS API is accessible at
            the given DRS instance. Only required for DRS instances that are
            not fully spec-compliant, as the default port is defined in the DRS
            documentation, cf.
            https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_hostname_based_drs_uris.
        use_http: Set the URI schema of the DRS instance to `http` instead of
            `https`when a DRS URI was provided to `uri`.
        token: Bearer token to send along with DRS API requests. Set if
            required by DRS implementation. Alternatively, specify in API
            endpoint access methods.

    Attributes:
        uri: URI to DRS endpoints, built from `uri`, `port` and `base_path`,
            e.g.,"https://my-drs.app:443/ga4gh/drs/v1".
        token: Bearer token for gaining access to DRS endpoints.
        headers: Dictionary of request headers.
    """
    # set regular expressions as private class variables
    _RE_DOMAIN_PART = r'[a-z0-9]([a-z0-9-]{1,61}[a-z0-9]?)?'
    _RE_DOMAIN = rf"({_RE_DOMAIN_PART}\.)+{_RE_DOMAIN_PART}\.?"
    _RE_DRS_ID = r'.+'
    _RE_HOST = rf"^(?P<schema>drs|http|https):\/\/(?P<host>{_RE_DOMAIN})\/?"
    _RE_OBJECT_ID = rf"^(drs:\/\/{_RE_DOMAIN}\/)?(?P<obj_id>{_RE_DRS_ID})$"

    def __init__(
        self,
        uri: str,
        port: int = None,
        base_path: str = 'ga4gh/drs/v1',
        use_http: bool = False,
        token: Optional[str] = None,
    ) -> Union[None, Error]:
        """Class constructor."""
        schema, host = self._get_host(uri)
        if schema == 'drs':
            schema = 'http' if use_http else 'https'
        if port is None:
            port = 80 if schema == 'http' else 443
        self.uri = f"{schema}://{host}:{port}/{base_path}"
        self.token = token
        self.headers = self._get_headers()
        logger.info(f"Instantiated client for: {self.uri}")

    def get_object(
        self,
        object_id: str,
        token: Optional[str] = None,
    ) -> Union[Error, DrsObject]:
        """Retrieve DRS object.

        Arguments:
            object_id: Implementation-specific DRS identifier OR hostname-based
               DRS URI pointing to a given object, cf.
               https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_hostname_based_drs_uris.
            token: Bearer token for authentication. Set if required by DRS
                implementation and if not provided when instatiating client or
                if expired.

        Returns:
            Unmarshalled DRS response as either an instance of `DRSObject`
            in case of a `200` response, or an instance of `Error` for all
            other JSON reponses.

        Raises:
            requests.exceptions.ConnectionError: A connection to the provided
                DRS instance could not be established.
            drs_cli.errors.InvalidResponseError: The response could not be
                validated against the API schema.
        """
        obj_id = self._get_object_id(object_id=object_id)
        url = f"{self.uri}/objects/{obj_id}"
        logger.info(f"Request URL: {url}")
        if token:
            self.token = token
            self._get_headers()
        try:
            response = requests.get(
                url=url,
                headers=self.headers,
            )
        except (
            requests.exceptions.ConnectionError,
            socket.gaierror,
            urllib3.exceptions.NewConnectionError,
        ):
            raise requests.exceptions.ConnectionError(
                "Could not connect to API endpoint."
            )
        if not response.status_code == 200:
            try:
                response_val = Error(**response.json())
            except (
                json.decoder.JSONDecodeError,
                pydantic.ValidationError,
            ):
                raise InvalidResponseError(
                    "Response could not be validated against API schema."
                )
            logger.warning("Received error response.")
        else:
            try:
                response_val = DrsObject(**response.json())
            except pydantic.ValidationError:
                raise InvalidResponseError(
                    "Response could not be validated against API schema."
                )
            logger.info(f"Retrieved object: {object_id}")
        return response_val

    def get_access_url(
        self,
        object_id: str,
        access_id: str,
        token: Optional[str] = None,
    ) -> Union[AccessURL, Error]:
        """Retrieve access URL of DRS object.

        Arguments:
            object_id: Implementation-specific DRS identifier OR hostname-based
               DRS URI pointing to a given object, cf.
               https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_hostname_based_drs_uris.
            access_id: Identifier of one of a DRS object's access methods.
            token: Bearer token for authentication. Set if required by DRS
                implementation and if not provided when instatiating client or
                if expired.

        Returns:
            Unmarshalled DRS response as either an instance of `AccessURL`
            in case of a `200` response, or an instance of `Error` for all
            other reponses.

        Raises:
            requests.exceptions.ConnectionError: A connection to the provided
                DRS instance could not be established.
            drs_cli.errors.InvalidResponseError: The response could not be
                validated against the API schema.
        """
        obj_id = self._get_object_id(object_id=object_id)
        acc_id = quote(string=access_id, safe='')
        url = f"{self.uri}/objects/{obj_id}/access/{acc_id}"
        logger.info(f"Request URL: {url}")
        if token:
            self.token = token
            self._get_headers()
        try:
            response = requests.get(
                url=url,
                headers=self.headers,
            )
        except (
            requests.exceptions.ConnectionError,
            socket.gaierror,
            urllib3.exceptions.NewConnectionError,
        ):
            raise requests.exceptions.ConnectionError(
                "Could not connect to API endpoint."
            )
        if not response.status_code == 200:
            try:
                response_val = Error(**response.json())
            except (
                json.decoder.JSONDecodeError,
                pydantic.ValidationError,
            ):
                raise InvalidResponseError(
                    "Response could not be validated against API schema."
                )
            logger.warning("Received error response.")
        else:
            try:
                response_val = AccessURL(**response.json())
            except pydantic.ValidationError:
                raise InvalidResponseError(
                    "Response could not be validated against API schema."
                )
            logger.info(f"Retrieved access URL: {response_val.url}")
        return response_val

    def post_object(
        self,
        object_data: Dict,
        token: Optional[str] = None,
    ) -> Union[str, Error]:
        """Register DRS object.

        Arguments:
            object_data: DRS object data.
            token: Bearer token for authentication. Set if required by DRS
                implementation and if not provided when instatiating client or
                if expired.

        Returns:
            ID of registered DRS object in case of a `200` response, or an
            instance of `Error` for all other responses.

        Raises:
            requests.exceptions.ConnectionError: A connection to the provided
                DRS instance could not be established.
            drs_cli.errors.InvalidObjectData: The object data payload could not
                be validated against the API schema.
            drs_cli.errors.InvalidResponseError: The response could not be
                validated against the API schema.
        """
        url = f"{self.uri}/objects"
        logger.info(f"Request URL: {url}")
        if token:
            self.token = token
            self._get_headers()
        try:
            PostDrsObject(**object_data).dict()
        except pydantic.ValidationError:
            raise InvalidObjectData(
                "Object data could not be validated against API schema."
            )
        try:
            response = requests.post(
                url=url,
                json=object_data,
                headers=self.headers,
            )
        except (
            requests.exceptions.ConnectionError,
            socket.gaierror,
            urllib3.exceptions.NewConnectionError,
        ):
            raise requests.exceptions.ConnectionError(
                "Could not connect to API endpoint."
            )
        if not response.status_code == 200:
            try:
                response_val = Error(**response.json())
            except (
                json.decoder.JSONDecodeError,
                pydantic.ValidationError,
            ):
                raise InvalidResponseError(
                    "Response could not be validated against API schema."
                )
            logger.warning("Received error response.")
        else:
            try:
                response_val = str(response.json())
            except json.decoder.JSONDecodeError:
                raise InvalidResponseError(
                    "Response could not be validated against API schema."
                )
            logger.info(f"Object registered: {response_val}")
        return response_val

    def delete_object(
        self,
        object_id: str,
        token: Optional[str] = None,
    ) -> Union[str, Error]:
        """Delete DRS object.

        Arguments:
            object_id: Implementation-specific DRS identifier OR hostname-based
               DRS URI pointing to a given object, cf.
               https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_hostname_based_drs_uris.
            token: Bearer token for authentication. Set if required by DRS
                implementation and if not provided when instatiating client or
                if expired.

        Returns:
            ID of previously registered DRS object in case of a `200`
            response, or an instance of `Error` for all other responses.

        Raises:
            requests.exceptions.ConnectionError: A connection to the provided
                DRS instance could not be established.
            drs_cli.errors.InvalidResponseError: The response could not be
                validated against the API schema.
        """
        obj_id = self._get_object_id(object_id=object_id)
        url = f"{self.uri}/objects/{obj_id}"
        logger.info(f"Request URL: {url}")
        if token:
            self.token = token
            self._get_headers()
        try:
            response = requests.delete(
                url=url,
                headers=self.headers,
            )
        except (
            requests.exceptions.ConnectionError,
            socket.gaierror,
            urllib3.exceptions.NewConnectionError,
        ):
            raise requests.exceptions.ConnectionError(
                "Could not connect to API endpoint."
            )
        if not response.status_code == 200:
            try:
                response_val = Error(**response.json())
            except (
                json.decoder.JSONDecodeError,
                pydantic.ValidationError,
            ):
                raise InvalidResponseError(
                    "Response could not be validated against API schema."
                )
            logger.warning("Received error response.")
        else:
            try:
                response_val = str(response.json())
            except json.decoder.JSONDecodeError:
                raise InvalidResponseError(
                    "Response could not be validated against API schema."
                )
            logger.info(f"Object deleted: {object_id}")
        return response_val

    def _get_headers(self) -> Dict:
        """Build dictionary of request headers.

        Returns:
            A dictionary of request headers
        """
        headers: Dict = {
            'Content-type': 'application/json',
        }
        if self.token:
            headers['Authorization'] = 'Bearer ' + self.token
        return headers

    def _get_host(
        self,
        uri: str,
    ) -> Tuple[str, str]:
        """Extract URI schema and domain or IP from HTTP, HTTPS or DRS URI.

        Arguments:
            uri: HTTP or HTTPS URI pointing to the root domain/IP of a DRS
                instance OR a hostname-based DRS URI to a given object, cf.
                https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_hostname_based_drs_uris.
                Anything after a slash following the domain/IP will be ignored.

        Returns:
            Tuple of URI schema (e.g., 'https', 'drs') and host domain or IP
            (e.g., 'my-drs.app', '0.0.0.0').

        Raises:
            drs_cli.errors.InvalidURI: input URI cannot be parsed.

        Examples:
           >>> DRSClient.get_host(uri="https://my-drs.app/will-be-ignored")
           ('https', 'my-drs.app')
           >>> DRSClient.get_host(uri="drs://my-drs.app/My0bj3ct")
           ('drs', 'my-drs.app')
        """
        match = re.search(self._RE_HOST, uri, re.I)
        if match:
            schema = match.group('schema')
            host = match.group('host').rstrip('\\')
            if len(host) > 253:
                raise InvalidURI
            return (schema, host)
        else:
            raise InvalidURI

    def _get_object_id(
        self,
        object_id: str,
    ) -> str:
        """
        Arguments:
            object_id: Implementation-specific DRS identifier OR hostname-based
               DRS URI pointing to a given object, cf.
               https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_hostname_based_drs_uris.
               Note that if a DRS URI is passed, only the DRS identifier part
               will be evaluated. To reset the hostname, create a new client
               with the `DRSClient()` constructor.

        Returns:
            Validated, percent-encoded object ID.

        Raises:
            drs_cli.errors.InvalidObjectIdentifier: input object ID cannot be
                parsed.
        """
        match = re.search(self._RE_OBJECT_ID, object_id, re.I)
        return quote(string=match.group('obj_id'), safe='')
