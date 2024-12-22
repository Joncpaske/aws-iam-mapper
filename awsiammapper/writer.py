"""Manages the output of policy statements into formats such as csv"""

import csv
import dataclasses


def write_csv(statements, fp):
    """output resource policy statements as a structued csv with headers

    Keyword arguments:
    statements -- Policy Statement
    fp -- file path you write csv to
    """
    with open(fp, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = dataclasses.asdict(statements[0]).keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for statement in statements:
            writer.writerow(dataclasses.asdict(statement))
