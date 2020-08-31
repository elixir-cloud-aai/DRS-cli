# DRS-cli

[![License][badge-license]][badge-url-license]
[![Build_status][badge-build-status]][badge-url-build-status]
[![Coverage][badge-coverage]][badge-url-coverage]
[![GitHub_tag][badge-github-tag]][badge-url-github-tag]
[![PyPI_release][badge-pypi]][badge-url-pypi]

This repository contains a client for an implementation of the [Data Repository
Service][res-ga4gh-drs] API schema of the [Global Alliance for Genomics and
Health][res-ga4gh], including support for additional endpoints defined in
[ELIXIR Cloud & AAI's][res-elixir-cloud]
[DRS-Filer][res-elixir-cloud-drs-filer] DRS implementation.

## Usage

To use the client import it as follows in your Python code after
[installation](#Installation):

### Create client instance

```py
from drs_cli.client import DRSClient

client = DRSClient(
    host="https://my-drs.app",
    port=80,
    base_path="ga4gh/drs/v1",
)
```

It is possible to supply a Bearer token, which will then be added to the
`Authentication` header (prepended by `Bearer`) for every outbound call:

```py
from drs_cli.client import DRSClient

client = DRSClient(
    host="https://my-drs.app",
    port=80,
    base_path="ga4gh/drs/v1",
    token = "<some_token>",
)
```

### Access endpoints

> **NOTES:**
>  
> * All endpoint access methods accept an optional `token` argument that
>   allows overwriting any token supplied when creating the client instance.
> * Responses that do not return the object ID as a single string return
>   [Pydantic][res-pydantic] models instead. If dictionaries are preferred
>   instead, they can be obtained with `response.dict()`. See the [Pydantic
>   export documentation][res-pydantic-docs-export] for further details.

#### `GET` endpoints

The [DRS][res-ga4gh-drs] `GET /objects/{object_id}` endpoint can then be
accessed with, e.g.:

```py
response = client.get_object(
    object_id="A3SF4B",
)
```

Similarly, the [DRS][res-ga4gh-drs] `GET
/objects/{object_id}/access/{access_id}` endpoint can be accessed with, e.g.:

```py
response = client.get_access_url(
    object_id="A3SF4B",
    access_id="B44FG9",
)
```

#### `POST` endpoint

The [DRS-Filer][res-elixir-cloud-drs-filer] `POST /objects` endpoint can be
accessed with, e.g.:

```py
response = client.post_object(
    object_data={
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
                "url": "ftp://my.ftp.server/my_path/my_file_01.txt",
                "headers":  [
                "None"
                ]
            }
            }
        ]
    }
)
```

#### `DELETE` endpoint

The [DRS-Filer][res-elixir-cloud-drs-filer] `DELETE /objects/{object_id}`
endpoint can be accessed with, e.g.:

```py
response = client.delete_object(
    object_id="A3SF4B",
)
```

## API docs

Automatically built [API documentation][docs-api] is available.

## Installation

You can install `DRS-cli` in one of two ways:

### Installation via package manager

```bash
pip install drs_cli

# Or for latest development version:
pip install -e git+https://github.com/elixir-cloud-aai/DRS-cli.git#egg=drs_cli
```

### Manual installation

```bash
git clone https://github.com/elixir-cloud-aai/DRS-cli.git
cd DRS-cli
python setup.py install
```

## Contributing

This project is a community effort and lives off your contributions, be it in
the form of bug reports, feature requests, discussions, or fixes and other code
changes. Please refer to our organization's [contributing
guidelines][res-elixir-cloud-contributing] if you are interested to contribute.
Please mind the [code of conduct][res-elixir-cloud-coc] for all interactions
with the community.

## Versioning

The project adopts the [semantic versioning][res-semver] scheme for versioning.
Currently the service is in beta stage, so the API may change without further
notice.

## License

This project is covered by the [Apache License 2.0][license-apache] also
[shipped with this repository][license].

## Contact

The project is a collaborative effort under the umbrella of [ELIXIR Cloud &
AAI][res-elixir-cloud]. Follow the link to get in touch with us via chat or
email. Please mention the name of this service for any inquiry, proposal,
question etc.

![logo_banner][]

[badge-build-status]:<https://travis-ci.com/elixir-cloud-aai/DRS-cli.svg?branch=dev>
[badge-coverage]:<https://img.shields.io/coveralls/github/elixir-cloud-aai/DRS-cli>
[badge-github-tag]:<https://img.shields.io/github/v/tag/elixir-cloud-aai/DRS-cli?color=C39BD3>
[badge-license]:<https://img.shields.io/badge/license-Apache%202.0-blue.svg>
[badge-pypi]:<https://img.shields.io/pypi/v/drs-cli.svg?style=flat&color=C39BD3>
[badge-url-build-status]:<https://travis-ci.com/elixir-cloud-aai/DRS-cli>
[badge-url-coverage]:<https://coveralls.io/github/elixir-cloud-aai/DRS-cli>
[badge-url-github-tag]:<https://github.com/elixir-cloud-aai/DRS-cli/releases>
[badge-url-license]:<http://www.apache.org/licenses/LICENSE-2.0>
[badge-url-pypi]:<https://pypi.python.org/pypi/drs-cli>
[docs-api]: <https://drs-cli.readthedocs.io/en/latest/>
[license]: LICENSE
[license-apache]: <https://www.apache.org/licenses/LICENSE-2.0>
[logo_banner]: images/logo-banner.png
[res-elixir-cloud]: <https://github.com/elixir-cloud-aai/elixir-cloud-aai>
[res-elixir-cloud-coc]: <https://github.com/elixir-cloud-aai/elixir-cloud-aai/blob/dev/CODE_OF_CONDUCT.md>
[res-elixir-cloud-contributing]: <https://github.com/elixir-cloud-aai/elixir-cloud-aai/blob/dev/CONTRIBUTING.md>
[res-elixir-cloud-drs-filer]: <https://github.com/elixir-cloud-aai/drs-filer>
[res-ga4gh-drs]: <https://github.com/ga4gh/data-repository-service-schemas>
[res-ga4gh]: <https://www.ga4gh.org/>
[res-pydantic]: <https://pydantic-docs.helpmanual.io/>
[res-pydantic-docs-export]: <https://pydantic-docs.helpmanual.io/usage/exporting_models/>
[res-semver]: <https://semver.org/>
