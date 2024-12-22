"""test awsiammapper mapper module"""

import json
import sys
import tempfile
from pathlib import Path

from awsiammapper import mapper
from awsiammapper.config import AppConfig
from tests.helper import build_statement


def test_mapper(s3):
    """happy path test with mocked S3 setup"""

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = f"{temp_dir}/mapping.csv"
        s3.create_bucket(Bucket="my-bucket-1")
        bucket_policy = {"Version": "2012-10-17", "Statement": [build_statement()]}
        s3.put_bucket_policy(Bucket="my-bucket-1", Policy=json.dumps(bucket_policy))
        mapper.map_iam(AppConfig(file_path=file_path, services=["s3"]))

        expected_output = """statement_id,principle_authority,principle_ref,action,effect,resource
DefaultPolicy,*,*,s3:*,Deny,*
"""

        assert Path(file_path).is_file()

        with open(file_path, mode="r", encoding="utf-8") as fp:
            output = fp.read()
            assert output == expected_output


def test_lambda_handler(monkeypatch, s3):
    """happy path test with mocked S3 setup"""

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = f"{temp_dir}/mapping.csv"
        s3.create_bucket(Bucket="my-bucket-1")
        bucket_policy = {"Version": "2012-10-17", "Statement": [build_statement()]}
        s3.put_bucket_policy(Bucket="my-bucket-1", Policy=json.dumps(bucket_policy))

        monkeypatch.setenv("awsiammapper_OUTPUT", file_path)
        monkeypatch.setenv("awsiammapper_SERVICES", "s3")

        mapper.lambda_handler(None, None)

        expected_output = """statement_id,principle_authority,principle_ref,action,effect,resource
DefaultPolicy,*,*,s3:*,Deny,*
"""

        assert Path(file_path).is_file()

        with open(file_path, mode="r", encoding="utf-8") as fp:
            output = fp.read()
            assert output == expected_output


def test_main(monkeypatch, s3):
    """happy path test with mocked S3 setup"""

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = f"{temp_dir}/mapping.csv"
        s3.create_bucket(Bucket="my-bucket-1")
        bucket_policy = {"Version": "2012-10-17", "Statement": [build_statement()]}
        s3.put_bucket_policy(Bucket="my-bucket-1", Policy=json.dumps(bucket_policy))

        monkeypatch.setattr(
            sys, "argv", ["awsiammapper", "-o", file_path, "-s", "s3"]
        )

        mapper.main()

        expected_output = """statement_id,principle_authority,principle_ref,action,effect,resource
DefaultPolicy,*,*,s3:*,Deny,*
"""

        assert Path(file_path).is_file()

        with open(file_path, mode="r", encoding="utf-8") as fp:
            output = fp.read()
            assert output == expected_output
