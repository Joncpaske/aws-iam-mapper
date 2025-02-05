"""test application outputs defined by the write module"""

import tempfile

from awsiammapper.policy import Condition
from awsiammapper.writer import write_csv
from tests.helper import build_policy_statement


def test_csv():
    """happy pather csv test"""

    with tempfile.TemporaryDirectory() as temp_dir:
        write_csv(
            [build_policy_statement(), build_policy_statement(effect="Allow")],
            f"{temp_dir}/output.csv",
        )

        expected_output = """statement_id,principle_authority,principle_ref,action,effect,resource
DefaultPolicy,*,*,s3:*,Deny,*
DefaultPolicy,*,*,s3:*,Allow,*
"""
        with open(f"{temp_dir}/output.csv", "r", encoding="utf-8") as f:
            assert f.read() == expected_output


def test_csv_with_conditions():
    """test writer with a condition option within the policy statement"""

    with tempfile.TemporaryDirectory() as temp_dir:
        write_csv(
            [
                build_policy_statement(
                    conditions=[
                        Condition(
                            key="S3:Prefix", operater="StringLike", value="janedoe/*"
                        )
                    ]
                ),
                build_policy_statement(effect="Allow"),
            ],
            f"{temp_dir}/output.csv",
        )

        # pylint: disable=line-too-long
        expected_output = """statement_id,principle_authority,principle_ref,action,effect,resource,key 1,operator 1,value 1
DefaultPolicy,*,*,s3:*,Deny,*,S3:Prefix,StringLike,janedoe/*
DefaultPolicy,*,*,s3:*,Allow,*,,,
"""
        with open(f"{temp_dir}/output.csv", "r", encoding="utf-8") as f:
            assert f.read() == expected_output
