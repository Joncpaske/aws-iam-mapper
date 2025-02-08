"""manages the definition and creation of a standardised policy statement"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Condition:
    """AWS Policy statement Condition"""

    key: str
    operater: str
    value: str


@dataclass(frozen=True)
class PolicyStatement:
    """Standardised resource policy statement"""

    statement_id: str
    principle_authority: str
    principle_ref: str
    action: str
    effect: str
    resource: str
    conditions: list[Condition]


def flattern(aws_statement) -> list[PolicyStatement]:
    """denormalises an AWS Policy Statement into multiple single statements with repition

    Keyword arguments:
    aws_statement -- AWS Policy statement
    """

    conditions = get_conditions(aws_statement)

    return [
        PolicyStatement(
            statement_id=aws_statement["Sid"],
            principle_authority=principle_authority,
            principle_ref=principle_ref,
            action=action,
            effect=aws_statement["Effect"],
            resource=resource,
            conditions=conditions,
        )
        for resource in get_resources(aws_statement)
        for action in get_actions(aws_statement)
        for principle_authority, principle_refs in get_principals(aws_statement).items()
        for principle_ref in principle_refs
    ]


def get_resources(statement) -> list[str]:
    """return a list of resources defined in the AWS Policy Statment

    Keyword arguments:
    statement -- AWS Policy statement
    """
    return (
        statement["Resource"]
        if isinstance(statement["Resource"], list)
        else [statement["Resource"]]
    )


def get_actions(statement) -> list[str]:
    """return a list of actions defined in the AWS Policy Statment

    Keyword arguments:
    statement -- AWS Policy statement
    """
    return (
        statement["Action"]
        if isinstance(statement["Action"], list)
        else [statement["Action"]]
    )


def get_principals(statement) -> dict[str, str]:
    """return a dict of principles defined in the AWS Policy Statment

    Keyword arguments:
    statement -- AWS Policy statement
    """
    if statement["Principal"] == "*":
        return {"*": ["*"]}

    return {
        key: [val] if isinstance(val, str) else val
        for key, val in statement["Principal"].items()
    }


def get_conditions(statement) -> list[Condition]:
    """flattern conditions into a list

    Keyword arguments:
    statement -- AWS Policy statement
    """
    if "Condition" not in statement:
        return []

    return [
        Condition(key=key, operater=operater, value=val)
        for operater, operater_val in statement["Condition"].items()
        for key, vals in operater_val.items()
        for val in (vals if not isinstance(vals, str) else [vals])
    ]
