"""test application outputs defined by the write module"""

import tempfile

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
