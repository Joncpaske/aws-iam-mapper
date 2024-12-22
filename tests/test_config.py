"""Test interfaces to the iam mapping service"""

import sys

from awsiammapper import config


def test_cli_abbrivated(monkeypatch):
    """test cli configuration setting with abbreviations"""

    monkeypatch.setattr(
        sys, "argv", ["awsiammapper", "-s", "s3,ksm", "-o", "./myfile.csv"]
    )

    app_config = config.from_cli()

    expected_app_config = config.AppConfig(
        file_path="./myfile.csv", services=["s3", "ksm"]
    )

    assert app_config == expected_app_config


def test_cli_long_form(monkeypatch):
    """test cli configuration setting with long form entry"""

    monkeypatch.setattr(
        sys,
        "argv",
        ["awsiammapper", "--services", "s3,ksm", "--output", "./myfile.csv"],
    )

    app_config = config.from_cli()

    expected_app_config = config.AppConfig(
        file_path="./myfile.csv", services=["s3", "ksm"]
    )

    assert app_config == expected_app_config


def test_environment_var(monkeypatch):
    """test reading config through environment variables"""

    monkeypatch.setenv("awsiammapper_OUTPUT", "./output.csv")
    monkeypatch.setenv("awsiammapper_SERVICES", "s3,kms")

    app_config = config.from_env()
    expect_app_config = config.AppConfig(
        file_path="./output.csv", services=["s3", "kms"]
    )

    assert app_config == expect_app_config
