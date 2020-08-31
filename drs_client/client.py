from drs_client.models import AccessURL, DrsObject, Error, PostDrsObject
from typing import Dict, Union
import logging
import requests

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
    """

    def __init__(
        self, 
        host= 'http://0.0.0.0', 
        port = '8080', 
        base_path= 'ga4gh/drs/v1',
        token = None
    ) -> None:
        self.url = f"{host}:{port}/{base_path}"
        self.token = token
        logger.info(f"url: {self.url}")


    def get_object(self, object_id: str) -> Union[Error, DrsObject]:
        """ Gets the DRS object

        Args:
            object_id: Identifier of DRS object to be retrieved.

        Returns:
            DRS object in the form of `DrsObject`. 
            
            `Error` object in case if request is not successful.
        """
        request_url = f"{self.url}/objects/{object_id}"
        headers = None
        if self.token != None:
            headers = {
                'Content-type': 'application/json',
                'Authorization': 'Bearer ' + self.token
            }
        else:
            headers = {'Content-type': 'application/json'}

        req = requests.get(url=request_url, headers = headers)
        if req.status_code == 200:
            logger.info(f"Retrieved DRSObject with object_id: {object_id}")
            return DrsObject(**req.json())  # validate incoming payload
        else:
            return Error(**req.json())


    def get_access_url(self, object_id: str, access_id: str) -> Union[AccessURL, Error]:
        """ Get access URL of DRS object.
        
        Args:
            object_id: Identifier of DRS object to be retrieved.
            access_id: Identifier of method giving access to DRS object.

        Returns:
            Object with access information for DRS object, containing a URL and
            any relevant header information; response is in `AccessURL` form.

            `Error` object in case if the request is not successful.
        """
        request_url = f"{self.url}/objects/{object_id}/access/{access_id}"
        headers = None
        if self.token != None:
            headers = {
                'Content-type': 'application/json',
                'Authorization': 'Bearer ' + self.token
            }
        else:
            headers = {'Content-type': 'application/json'}
        req = requests.get(url=request_url, headers = headers)
        if req.status_code == 200: 
            logger.info(f"Retrieved AccessURL with object_id: {object_id} and access_id: {access_id}")
            return AccessURL(**req.json())  # validate incoming payload
        else:
            return Error(**req.json())


    def post_object(self, object_data: dict) -> Union[Dict, Error]:
        """ Register new DRS object.

        Args:
            object_data: DRS object in JSON form

        Returns:
            `object_id` of the registered DRS object.
            
            `Error` object in case of unsuccessful request.
        """
        request_url = f"{self.url}/objects"
        headers = None
        if self.token != None:
            headers = {
                'Content-type': 'application/json',
                'Authorization': 'Bearer ' + self.token
            }
        else:
            headers = {'Content-type': 'application/json'}
        PostDrsObject(**object_data)  # validate outgoing payload
        req = requests.post(url=request_url, json = object_data, headers = headers)
        if req.status_code == 200:
            logger.info(f"DRSObject with object_id: {req.json()} registered.")
            return req.json()
        else:
            return Error(**req.json())


    def delete_object(self, object_id: str) -> Union[Dict, Error]:
        """ Delete DRS object.
        
        Args:
            object_id: Identifier of DRS object to be deleted.

        Returns:
            `object_id` of deleted object.

            `Error` object in case if the request is not successful.
        """
        request_url = f"{self.url}/objects/{object_id}"
        headers = None
        if self.token != None:
            headers = {
                'Content-type': 'application/json',
                'Authorization': 'Bearer ' + self.token
            }
        else:
            headers = {'Content-type': 'application/json'}
        req = requests.delete(url=request_url, headers = headers)
        if req.status_code == 200:
            logger.info(f"DRSObject with object_id: {object_id} deleted.")
            return req.json()
        else:
            return Error(**req.json())
