"""Service module defining the application logic dependant on the interfaces and clients"""

import functools

from awsiammapper import config
from awsiammapper.client import get_client
from awsiammapper.writer import write_csv


def _map(get_service_client, output, app_config):

    policies = []

    for service in app_config.services:
        client = get_service_client(service)
        policies += client.get_policies(client.list())

    output(policies, app_config.file_path)


map_iam = functools.partial(_map, get_client, write_csv)


def lambda_handler(event, context):
    # pylint: disable=unused-argument
    """AWS Lambda entrypoint"""

    map_iam(config.from_env())


def main():
    """commandline entrypoint"""

    map_iam(config.from_cli())
