import re
from typing import Tuple, Optional

DRS_URI_PATTERN = r'^drs:\/\/([A-Za-z0-9.]+)\/([A-Za-z0-9.-_~]+$)'
HTTP_URI_PATTERN = r'^http:\/\/([A-Za-z0-9.]+$)'
HTTPS_URI_PATTERN = r'^https:\/\/([A-Za-z0-9.]+$)'
DRS_ID_PATTERN = r'[A-Za-z0-9._~-]+$'

def check_drs_uri_regex(uri) -> bool:
    """Check regular expression for DRS URI"""
    isMatch = re.fullmatch(DRS_URI_PATTERN, uri)
    if isMatch:
        return True
    else:
        return False

def check_http_uri_regex(uri: str) -> bool:
    """Check regular expression for HTTP URI"""
    isMatch = re.fullmatch(HTTP_URI_PATTERN, uri)
    if isMatch:
        return True
    else:
        return False


def check_https_uri_regex(uri: str) -> bool:
    """Check regular expression for HTTPS URI"""
    isMatch = re.fullmatch(HTTP_URI_PATTERN, uri)
    if isMatch:
        return True
    else:
        return False

def check_drs_id_regex(id: str) -> bool:
    """Check regular expression for DRS ID"""
    isMatch = re.fullmatch(DRS_ID_PATTERN, id)
    if isMatch:
        return True
    else:
        return False

def get_drs_uri_host_and_id(uri: str) -> Tuple:
    """Gets the host uri and id from a DRS URI"""
    searchObj = re.search(DRS_URI_PATTERN, uri, re.M|re.I)
    return (searchObj.group(1), searchObj.group(2))


def get_http_uri_host(uri: str) -> str:
    """Gets the host name from an HTTP URI"""
    searchObj = re.search( HTTP_URI_PATTERN, uri, re.M|re.I)
    return searchObj.group(1)


def get_https_uri_host(uri: str) -> str:
    """Gets the host name from an HTTPS URI"""
    searchObj = re.search( HTTPS_URI_PATTERN, uri, re.M|re.I)
    return searchObj.group(1)