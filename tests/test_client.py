"""test awsiammapper clients"""

import json

import moto
import pytest

from tests.helper import build_policy_statement, build_statement


def test_s3_list(s3, s3_client):
    """happy path test listing S3 buckets"""

    s3.create_bucket(Bucket="my-bucket-1")
    s3.create_bucket(Bucket="my-bucket-2")

    buckets = s3_client.list()
    expected_buckets = ["my-bucket-1", "my-bucket-2"]

    assert buckets == expected_buckets


def test_s3_list_no_buckets(s3_client):
    """test listing buckets with none present"""

    with moto.mock_aws():
        buckets = s3_client.list()
        expected_buckets = []

        assert buckets == expected_buckets


def test_s3_no_policy_continue_on_error(s3, s3_client):
    """test continue on error flag with error present"""

    s3.create_bucket(Bucket="my-bucket-1")

    policies = s3_client.get_policies(["my-bucket-1"], exit_on_error=False)
    expect_policies = []

    assert policies == expect_policies


def test_s3_no_policy_fail_on_error(s3, s3_client):
    """test fail on error flag with error present"""

    s3.create_bucket(Bucket="my-bucket-1")

    with pytest.raises(KeyError) as e:
        s3_client.get_policies(["my-bucket-1"])

    assert str(e.value) == "'Resource not found'"


def test_s3_no_bucket_fail_on_error(s3, s3_client):
    """test continue on error flag with error present due to no bucket"""

    s3.create_bucket(Bucket="my-bucket-1")

    with pytest.raises(KeyError) as e:
        s3_client.get_policies(["my-non-existent-bucket"])

    assert str(e.value) == "'Resource not found'"


def test_s3_bucket_policy_read(s3, s3_client):
    """happy path read S3 bucket policy"""

    bucket_name = "my-test-bucket"
    s3.create_bucket(Bucket=bucket_name)
    bucket_policy = {"Version": "2012-10-17", "Statement": [build_statement()]}
    s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))

    policy = s3_client.get_policies([bucket_name])

    expected_policies = [build_policy_statement()]

    assert policy == expected_policies
