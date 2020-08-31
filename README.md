# DRS-cli

[![Apache License](https://img.shields.io/badge/license-Apache%202.0-orange.svg?style=flat&color=important)](http://www.apache.org/licenses/LICENSE-2.0)
![GitHub: latest tag](https://flat.badgen.net/github/tag/elixir-cloud-aai/DRS-cli?color=cyan&icon=github)

This repository contains a client for an implementation of the 
[Data Repository Service] API schema of the [Global Alliance for Genomics
and Health], as described in the [drs-filer] repository.

## Usage

To use the client import it as follows in your Python code after
[installation](#Installation):

```py
import drs_client

client = drs_client.client.DRSClient(
        host = "my-drs.app", 
        port = "80", 
        base_path = "ga4gh/drs/v1"
        )
```

It is possible to supply a Bearer token, which will then be added to the
`Authentication` header (prepended by `Bearer`) for every outbound call:

```py
import drs_client

client = drs_client.client.DRSClient(
        host = "https://my-drs.app", 
        port = "80", 
        base_path = "ga4gh/drs/v1"
        token = "<some_token>"
        )
```

The DRS `GET /objects/{object_id}` endpoint can then accessed with, e.g.,:

```py
response = client.get_object("a001")
```
The DRS `POST /objects` endpoint can be access with, e.g.:

```py
response = client.post_object(object_data={
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
                "url": "drs://ftp.ensembl.org/pub/release-81/bed/ensembl-compara/11_teleost_fish.gerp_constrained_eleme",
                "headers":  [
                "None"
                ]
            }
            }
        ]
    })
```

## Installation

You can install `DRS-cli` in one of two ways:

### Installation via package manager

```bash
pip install drs_client
```

or (for development version)

```bash
pip install -e git+https://github.com/elixir-cloud-aai/DRS-cli.git#egg=drs_client
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
AAI][org-elixir-cloud]. Follow the link to get in touch with us via chat or
email. Please mention the name of this service for any inquiry, proposal,
question etc.

![logo banner]

[license]: LICENSE
[license-apache]: <https://www.apache.org/licenses/LICENSE-2.0>
[org-elixir-cloud]: <https://github.com/elixir-cloud-aai/elixir-cloud-aai>
[res-elixir-cloud-contributing]: <https://github.com/elixir-cloud-aai/elixir-cloud-aai/blob/dev/CONTRIBUTING.md>
[drs-filer]: <https://github.com/elixir-cloud-aai/drs-filer>
[Data Repository Service]: <https://github.com/ga4gh/data-repository-service-schemas>
[res-semver]: <https://semver.org/>
[res-elixir-cloud-contributing]: <https://github.com/elixir-cloud-aai/elixir-cloud-aai/blob/dev/CONTRIBUTING.md>
[res-elixir-cloud-coc]: <https://github.com/elixir-cloud-aai/elixir-cloud-aai/blob/dev/CODE_OF_CONDUCT.md>