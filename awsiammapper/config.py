"""config - manages the building of application configuration (AppConfig)"""

import argparse
import os
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Application configuration"""

    file_path: str
    services: list[str]


def from_cli():
    """from_cli - retreive config from the cli utilising argparse"""

    parser = argparse.ArgumentParser(
        prog="AWS IAM Mappe",
        description="maps identities access to resources within a given AWS Account",
        usage="awsiammapper [-s SERVICES] -o OUTPUT",
    )

    parser.add_argument(
        "-s",
        "--services",
        dest="services",
        help="comma delimeted list of servics to map access",
    )
    parser.add_argument("-o", "--output", dest="output", help="output location")

    args = parser.parse_args(sys.argv[1:])

    return AppConfig(file_path=args.output, services=str.split(args.services, ","))


def from_env():
    """from_env - create appconfig crom environment variales"""

    return AppConfig(
        file_path=os.getenv("awsiammapper_OUTPUT"),
        services=str.split(os.getenv("awsiammapper_SERVICES"), ","),
    )
