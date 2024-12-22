"""Pytest fixtures"""

import boto3
import pytest
from moto import mock_aws

from awsiammapper.client import S3Client


@pytest.fixture(scope="function")
def s3():
    """function fixture to mock AWS Boto3 clients"""
    with mock_aws():
        yield boto3.client("s3")


@pytest.fixture(scope="function")
def s3_client():
    """fixture that provides and S3 client to for testing"""
    yield S3Client()
