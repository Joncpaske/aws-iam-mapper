"""Test helper builder fuctions"""

from awsiammapper.policy import PolicyStatement


def build_statement(
    sid="DefaultPolicy", principal="*", action="s3:*", effect="Deny", resource="*"
):
    """Policy statement dictionary builder"""
    return {
        "Sid": sid,
        "Principal": principal,
        "Action": action,
        "Effect": effect,
        "Resource": resource,
    }


def build_statement_with_condition(
    sid="DefaultPolicy",
    principal="*",
    action="s3:*",
    effect="Deny",
    resource="*",
    condition=None,
):
    """Policy statement dictionary builder"""
    return {
        "Sid": sid,
        "Principal": principal,
        "Action": action,
        "Effect": effect,
        "Resource": resource,
        "Condition": (
            condition if condition else {"StringLike": {"S3:Prefix": "janedoe/*"}}
        ),
    }


def build_policy_statement(
    statement_id="DefaultPolicy",
    principle_authority="*",
    principle_ref="*",
    action="s3:*",
    effect="Deny",
    resource="*",
    conditions=None,
):
    """PolicyStatement class builder"""
    return PolicyStatement(
        statement_id=statement_id,
        principle_authority=principle_authority,
        principle_ref=principle_ref,
        action=action,
        effect=effect,
        resource=resource,
        conditions=conditions if conditions else [],
    )
