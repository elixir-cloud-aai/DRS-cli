"""Mock input data for unit tests."""

from copy import deepcopy
import uuid

# no dependencies
MOCK_BASE_PATH = "a/b/c"
MOCK_DRS_URI = "drs://fakehost.com/SOME_OBJECT"
MOCK_DRS_URI_INVALID = "dr://fakehost.com/SOME_OBJECT"
MOCK_DRS_URI_LONG = (
    "drs://aaaaaaaaaaaaaaaaaaaaaaaaaaaa.aaaaaaaaaaaaaaaaaaaaaa"
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.aaaaaaaaaaaaaaaaaaaaaa"
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.aaaaaaaaaaaaaaaaaaaaaa"
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.aaaaaaaaaaaaaaaaaaaaaa"
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.aaaaaaaaaaaaaaaaaaaaaa"
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.aaaaaaaaaaaaaaaaaaaaaa"
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.aaaaaaaaaaaaaaaaaaaaaaa"
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.aaaa.com/SOME_OBJECT"
)
MOCK_ERROR = {
    "msg": "mock_message",
    "status_code": "400"
}
MOCK_ERROR_MSG = "SYSTEM HANDLER"
MOCK_ERROR_MSG_CUSTOM_HANDLER = "CUSTOM HANDLER"
MOCK_FILE_URL = "ftp://my.ftp.service/my_path/my_file_01.txt"
MOCK_HOST = "https://fakehost.com"
MOCK_ID = str(uuid.uuid4())
MOCK_PORT = 8080
MOCK_SELF_URI = f"https://fakehost.com/ga4gh/drs/v1/objects/{MOCK_ID}"
MOCK_TOKEN = "MyT0k3n"

# with dependencies
MOCK_ACCESS_URL = {
    "url": MOCK_FILE_URL,
    "headers":  [
        "None"
    ],
}
MOCK_ACCESS_METHODS = [
        {
            "type": "ftp",
            "access_url": MOCK_ACCESS_URL,
        },
]
MOCK_CHECKSUMS = [
    {
        "checksum": "18c2f5517e4ddc02cd57f6c7554b8e88",
        "type": "md5",
    },
]
MOCK_DRS_URL = f"{MOCK_HOST}:{MOCK_PORT}/ga4gh/drs/v1/objects"
MOCK_OBJECT_POST_INVALID = {
    "updated_time": "2019-04-24T05:23:43-06:00",
    "version": "1",
    "size": 5,
    "mime_type": "",
    "checksums": MOCK_CHECKSUMS,
    "access_methods": MOCK_ACCESS_METHODS,
}
MOCK_OBJECT_GET_INVALID = deepcopy(MOCK_OBJECT_POST_INVALID)
MOCK_OBJECT_GET_INVALID['id'] = MOCK_ID
MOCK_OBJECT_GET_INVALID['self_uri'] = MOCK_SELF_URI
MOCK_OBJECT_GET_INVALID['access_methods'][0]['access_id'] = MOCK_ID
MOCK_OBJECT_POST = deepcopy(MOCK_OBJECT_POST_INVALID)
MOCK_OBJECT_POST['created_time'] = "2019-05-20T00:12:34-07:00"
MOCK_OBJECT_GET = deepcopy(MOCK_OBJECT_GET_INVALID)
MOCK_OBJECT_GET['created_time'] = "2019-05-20T00:12:34-07:00"
