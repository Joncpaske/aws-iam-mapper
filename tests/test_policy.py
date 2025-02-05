"""test policy statement generation"""

from awsiammapper.policy import Condition, flattern
from tests.helper import (
    build_policy_statement,
    build_statement,
    build_statement_with_condition,
)


def test_flattern_multi_resource():
    """test statement with 2 defined resources create two statements"""
    policy = flattern(
        build_statement(resource=["arn:aws:s3:::resource1", "arn:aws:s3:::resource2"])
    )

    expected_policy = [
        build_policy_statement(resource="arn:aws:s3:::resource1"),
        build_policy_statement(resource="arn:aws:s3:::resource2"),
    ]

    assert policy == expected_policy


def test_flattern_single_resource():
    """test single resource only creates a single policy statement"""

    policy = flattern(build_statement(resource="arn:aws:s3:::resource1"))

    expected_policy = [build_policy_statement(resource="arn:aws:s3:::resource1")]

    assert policy == expected_policy


def test_flattern_multi_actions():
    """test two actions creates two policy statements"""

    policy = flattern(build_statement(action=["s3:ListObject", "s3:GetObject"]))

    expected_policy = [
        build_policy_statement(action="s3:ListObject"),
        build_policy_statement(action="s3:GetObject"),
    ]

    assert policy == expected_policy


def test_flattern_single_actions():
    """test single attribute action creates single policy statement"""

    policy = flattern(build_statement(action="s3:*"))

    expected_policy = [build_policy_statement(action="s3:*")]

    assert policy == expected_policy


def test_flattern_multi_actions_resources():
    """test two actions and resources results in four policy statments"""

    policy = flattern(
        build_statement(
            action=["s3:ListObject", "s3:GetObject"],
            resource=["arn:aws:s3:::resource1", "arn:aws:s3:::resource2"],
        )
    )

    expected_policy = [
        build_policy_statement(
            action="s3:ListObject", resource="arn:aws:s3:::resource1"
        ),
        build_policy_statement(
            action="s3:GetObject", resource="arn:aws:s3:::resource1"
        ),
        build_policy_statement(
            action="s3:ListObject", resource="arn:aws:s3:::resource2"
        ),
        build_policy_statement(
            action="s3:GetObject",
            resource="arn:aws:s3:::resource2",
        ),
    ]

    assert policy == expected_policy


def test_any_principle():
    """test special case * principle produces single statement with * principle"""

    policy = flattern(build_statement(principal="*"))

    expected_policy = [
        build_policy_statement(principle_authority="*", principle_ref="*")
    ]

    assert policy == expected_policy


def test_aws_principal_single():
    """test happy path aws principle"""

    policy = flattern(build_statement(principal={"aws": "*"}))

    expected_policy = [
        build_policy_statement(principle_authority="aws", principle_ref="*")
    ]

    assert policy == expected_policy


def test_aws_principal_muliple():
    """test happy path aws principle with multiple aws principles"""

    policy = flattern(
        build_statement(
            principal={"aws": ["arn:aws:iam::123456789012:root", "999999999999"]}
        )
    )

    expected_policy = [
        build_policy_statement(
            principle_authority="aws", principle_ref="arn:aws:iam::123456789012:root"
        ),
        build_policy_statement(principle_authority="aws", principle_ref="999999999999"),
    ]

    assert policy == expected_policy


def test_multi_principal_types():
    """test multiple principles with difference types"""

    policy = flattern(
        build_statement(
            principal={
                "aws": ["arn:aws:iam::123456789012:root", "999999999999"],
                "Service": ["ecs.amazonaws.com", "elasticloadbalancing.amazonaws.com"],
            }
        )
    )

    expected_policy = [
        build_policy_statement(
            principle_authority="aws", principle_ref="arn:aws:iam::123456789012:root"
        ),
        build_policy_statement(principle_authority="aws", principle_ref="999999999999"),
        build_policy_statement(
            principle_authority="Service", principle_ref="ecs.amazonaws.com"
        ),
        build_policy_statement(
            principle_authority="Service",
            principle_ref="elasticloadbalancing.amazonaws.com",
        ),
    ]

    assert policy == expected_policy


def test_flattern_with_conditional():
    """happy path test for condition statement within the AWS Policy document statement"""

    policy = flattern(build_statement_with_condition())

    expected_policy = [
        build_policy_statement(
            conditions=[
                (Condition(key="S3:Prefix", operater="StringLike", value="janedoe/*"))
            ]
        )
    ]

    assert policy == expected_policy


def test_flattern_with_conditional_multi_val():
    """condition test with multiple values for a given operater"""

    policy = flattern(
        build_statement_with_condition(
            condition={"StringLike": {"S3:Prefix": ["janedoe/*", "samedoe/*"]}}
        )
    )

    expected_policy = [
        build_policy_statement(
            conditions=[
                Condition(key="S3:Prefix", operater="StringLike", value="janedoe/*"),
                Condition(key="S3:Prefix", operater="StringLike", value="samedoe/*"),
            ]
        )
    ]

    assert policy == expected_policy


def test_flattern_with_conditional_multi_operators():
    """condition test with multiple codition operators"""

    policy = flattern(
        build_statement_with_condition(
            condition={
                "StringLike": {"S3:Prefix": "janedoe/*"},
                "StringNotLike": {"S3:Prefix": "janedoe/dev/*"},
            }
        )
    )

    expected_policy = [
        build_policy_statement(
            conditions=[
                Condition(key="S3:Prefix", operater="StringLike", value="janedoe/*"),
                Condition(
                    key="S3:Prefix", operater="StringNotLike", value="janedoe/dev/*"
                ),
            ]
        )
    ]

    assert policy == expected_policy
