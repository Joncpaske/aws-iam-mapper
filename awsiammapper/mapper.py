"""Service module defining the application logic dependant on the interfaces and clients"""

import functools

from awsiammapper import config
from awsiammapper.client import S3Client
from awsiammapper.writer import write_csv

clients = {"s3": S3Client}


def _map(service_clients, output, app_config):

    policies = []

    for service in app_config.services:
        client = service_clients[service]()
        policies += client.get_policies(client.list())

    output(policies, app_config.file_path)


map_iam = functools.partial(_map, clients, write_csv)


def lambda_handler(event, context):
    # pylint: disable=unused-argument
    """AWS Lambda entrypoint"""

    map_iam(config.from_env())


def main():
    """commandline entrypoint"""

    map_iam(config.from_cli())
