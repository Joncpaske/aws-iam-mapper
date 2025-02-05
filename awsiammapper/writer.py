"""Manages the output of policy statements into formats such as csv"""

import csv

from awsiammapper.policy import PolicyStatement


def write_csv(statements: list[PolicyStatement], fp: str) -> None:
    """output resource policy statements as a structued csv with headers

    Keyword arguments:
    statements -- Policy Statement
    fp -- file path you write csv to
    """
    with open(fp, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=_get_field_names(_get_max_conditions(statements))
        )

        writer.writeheader()
        for statement in statements:
            writer.writerow(_build_record(statement))


def _get_max_conditions(statements: list[PolicyStatement]):
    return max((len(statement.conditions) for statement in statements))


def _build_record(statement: PolicyStatement) -> None:
    record = {
        "statement_id": statement.statement_id,
        "principle_authority": statement.principle_authority,
        "principle_ref": statement.principle_ref,
        "action": statement.action,
        "effect": statement.effect,
        "resource": statement.resource,
    }

    for i, condition in enumerate(statement.conditions):
        record[f"key {i+1}"] = condition.key
        record[f"operator {i+1}"] = condition.operater
        record[f"value {i+1}"] = condition.value

    return record


def _get_field_names(max_conditions: int):
    fields = [
        "statement_id",
        "principle_authority",
        "principle_ref",
        "action",
        "effect",
        "resource",
    ]

    for i in range(1, max_conditions + 1):
        fields += [f"key {i}", f"operator {i}", f"value {i}"]

    return fields
