# DRS-cli

[![License][badge-license]][badge-url-license]
[![Build_status][badge-build-status]][badge-url-build-status]
[![Coverage][badge-coverage]][badge-url-coverage]
[![GitHub_tag][badge-github-tag]][badge-url-github-tag]
[![PyPI_release][badge-pypi]][badge-url-pypi]

Client for implementations of the [Global Alliance for Genomics and
Health (GA4GH)][res-ga4gh] [Data Repository Service API][res-ga4gh-drs] schema,
including support for additional endpoints defined in [ELIXIR Cloud &
AAI's][res-elixir-cloud] generic [DRS-Filer][res-elixir-cloud-drs-filer] DRS
implementation.

## Usage

To use the client import it as follows in your Python code after
[installation](#Installation):

### Create client instance

#### Via DRS hostname

A client instance can be created by specifying the domain name of a DRS
instance, including the URL schema:

```py
from drs_cli.client import DRSClient

client = DRSClient(uri="https://my-drs.app")
# Client instantiated for URL: https://my-drs.app:443/ga4gh/drs/v1
```

Fully [spec-compliant][res-ga4gh-drs] DRS implementations will always be
available at `https` URLs, served at port `443` and at the base path
`ga4gh/drs/v1`. However, to allow the client to be used against development
versions of DRS implementations, `http` URLs are supported as well (default
port `80`), and the port and base path at which the API endpoints are served
can be overridden with the `port` and `base_path` arguments:

```py
from drs_cli.client import DRSClient

client = DRSClient(
    uri="http://my-drs.app",
    port=8080,
    base_path="my/api/route",
)
# Client instantiated for URL: http://my-drs.app:8080/my/api/route
```

#### Via DRS URI

Clients can also be created by passing a [hostname-based DRS
URI][res-ga4gh-drs-uri]:

```py
from drs_cli.client import DRSClient

client = DRSClient(uri="drs://my-drs.app/SOME_OBJECT")
# Client instantiated for URL: https://my-drs.app:443/ga4gh/drs/v1
```

> **NOTE:** Only the hostname part of the DRS URI is evaluated, not the object
> ID.

Port and base path can be overridden as described above. In addition, the
client constructor also defines the `use_http` flag, which instantiates a
client for an `http` URL when a DRS URI is passed. The flag has no effect
when a DRS hostname URL is provided instead of a DRS URI:

```py
from drs_cli.client import DRSClient

client = DRSClient(
    uri="drs://my-drs.app/SOME_OBJECT",
    use_http=True,
)
# Client instantiated for URL: http://my-drs.app:443/ga4gh/drs/v1
```

### Access endpoints

> **NOTES:**
>  
> * All endpoint access methods require a [client
>   instance](#create-client-instance).
> * For accessing endpoints that require authorization, see the
>   [dedicated section](#authorization).
> * Responses that do not return the object ID as a single string return
>   [Pydantic][res-pydantic] models instead. If dictionaries are preferred
>   instead, they can be obtained with `response.dict()`. See the [Pydantic
>   export documentation][res-pydantic-docs-export] for further details.

#### `GET` endpoints

The [DRS][res-ga4gh-drs] `GET /objects/{object_id}` endpoint can be accessed
with, e.g.:

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

### Authorization

Authorization [bearer tokens][res-bearer-token] can be provided either during
client instantiation or when calling an endpoint access method. The bearer
token is sent along as an `Authorization` header with every request sent from
the instantiated client instance.

> **NOTE:** Whenever a token is specified when calling an API endpoint, the
> `token` variable of that particular client instance is overridden. Thus,
> subsequent calls from that client will all carry the new token value, unless
> overridden again.

The following example illustrates this behavior:

```py
from drs_cli.client import DRSClient

# No token passed during client instantiation
client = DRSClient(uri="https://my-drs.app")
# Value of client.token: None

# Token passed during API call
client.get_object(
    object_id="SOME_OBJECT",
    token="N3wT0k3n",
)
# Value of client.token: N3wT0k3n

# Token passed during client instantiation
client_2 = DRSClient(
    uri="https://my-drs.app",
    token="MyT0k3n",
)
# Value of client_2.token: MyT0k3n

# Token passed during API call
client_2.get_object(
    object_id="SOME_OBJECT",
    token="N3wT0k3n",
)
# Value of client_2.token: N3wT0k3n
```

## API docs

Automatically built [API documentation][docs-api] is available.

## Installation

You can install `DRS-cli` in one of two ways:

### Installation via package manager

```bash
pip install drs_cli

# Or for latest development version:
pip install git+https://github.com/elixir-cloud-aai/DRS-cli.git#egg=drs_cli
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
[res-bearer-token]: <https://tools.ietf.org/html/rfc6750>
[res-elixir-cloud]: <https://github.com/elixir-cloud-aai/elixir-cloud-aai>
[res-elixir-cloud-coc]: <https://github.com/elixir-cloud-aai/elixir-cloud-aai/blob/dev/CODE_OF_CONDUCT.md>
[res-elixir-cloud-contributing]: <https://github.com/elixir-cloud-aai/elixir-cloud-aai/blob/dev/CONTRIBUTING.md>
[res-elixir-cloud-drs-filer]: <https://github.com/elixir-cloud-aai/drs-filer>
[res-ga4gh]: <https://www.ga4gh.org/>
[res-ga4gh-drs]: <https://github.com/ga4gh/data-repository-service-schemas>
[res-ga4gh-drs-uri]: <https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_hostname_based_drs_uris>
[res-pydantic]: <https://pydantic-docs.helpmanual.io/>
[res-pydantic-docs-export]: <https://pydantic-docs.helpmanual.io/usage/exporting_models/>
[res-semver]: <https://semver.org/>