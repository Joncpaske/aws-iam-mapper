"""Manage integrations to list resources and retreive their policies"""

import ast
import logging
from typing import Literal

import boto3

from awsiammapper.policy import flattern

Service = Literal["s3", "iam"]


class BaseClient:
    """interface to AWS Services to list specific resources and their policies"""

    def list(self) -> list[str]:
        """list - list resources (does not use pagination)"""
        raise NotImplementedError()

    def get_policies(self, resources, exit_on_error=True):
        """get_policies - get a list of policies for each resources"""
        raise NotImplementedError()


class S3Client(BaseClient):
    """AWS S3 client - list buckets and get associated bucket policies"""

    def __init__(self, client=None):
        self.client = client if client else boto3.client("s3")

    def list(self) -> list[str]:
        """list - list S3 buckets contained within the associated AWS account"""
        return [bucket["Name"] for bucket in self.client.list_buckets()["Buckets"]]

    def get_policies(self, resources, exit_on_error=True):
        """get policies for each specified bucket

        Keyword arguments:
        resources -- list of buckets to retreive bucket policies
        exit_on_error --- default True, on True ignore errors such as no bucket policy
        """

        policies = []
        for policy_document in self._get_bucket_policy_document(
            resources, exit_on_error
        ):
            for statement in policy_document:
                policies += flattern(statement)

        return policies

    def _get_bucket_policy_document(self, resources, exit_on_error=True):
        try:
            for resource in resources:
                yield ast.literal_eval(
                    self.client.get_bucket_policy(Bucket=resource)["Policy"]
                )["Statement"]
        except self.client.exceptions.from_code("noSuchBucketPolicy") as e:
            logging.debug(
                "bucket [%s] does not exist or does not contain a bucket policy",
                resource,
            )

            if exit_on_error:
                raise KeyError("Resource not found") from e


class IAMRoleClient(BaseClient):
    """boto3 client wrapper for the AWS IAM Role interaction"""

    def __init__(self, client=None):
        self.client = client if client else boto3.client("iam")

    def list(self) -> list[str]:
        """list - list resources (does not use pagination)"""

    def get_policies(self, resources, exit_on_error=True):
        """get_policies - get a list of policies for each resources"""


def get_client(service: Service) -> BaseClient:
    """Factory function for AWS resource clients

    Keyword Arguments:
    service - an aws service - [s3, iam]
    """
    clients = {"s3": S3Client, "iam": IAMRoleClient}

    return clients[service]()
