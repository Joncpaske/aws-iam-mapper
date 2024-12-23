[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Joncpaske_aws-iam-mapper&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Joncpaske_aws-iam-mapper) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Joncpaske_aws-iam-mapper&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Joncpaske_aws-iam-mapper)
# aws-iam-mapper
When working on long lived environments, understanding the state of access is paramount to ensure least privelege. Over time access needs can change with existing permissions no longer needed. In order to adhere to the least privilege principle regular access reviews are needed to maintain an active security posture.

The core focus of this tool is to support organisations / account managers where the access controls have not been built in a centralised manner, resulting in a greater complexity to decipher access controls. For example instead of being centralised under IAM Roles or Lake Formation, decentralised resource policises such as S3 bucket policies could have been used.

## Running aws-iam-map

This tool is configured to either run as a commandline tool either locally with a direct pip install or via docker.

```shell
#Python package via Pypi
python3 -m pip install awsiammapper
python3 -m awsiammapper -h

#Docker
docker run awsiammapper -h
```

### Access Requirements
The tool requires read only access limited to listing resources and getting associated policies.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AwsIamMapper",
      "Action": [
        "s3:GetBucketPolicy",
        "s3:ListBucket"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```

## Supporting new resouces

The IAM Mapper tool is built with extendability in mind, to add a new resource type add a new class within the `clients.py` module adhearing the the `BaseClient` interface. To then make it available the service needs to be added to the factory dictionary within the `mapper.py` module.

```python
#awsiammapper.client
class BaseClient:
    """interface to AWS Services to list specific resources and their policies"""

    def list(self) -> list[str]:
        """list - list resources (does not use pagination)"""
        raise NotImplementedError()

    def get_policies(self, resources, exit_on_error=True):
        """get_policies - get a list of policies for each resources"""
        raise NotImplementedError()
```

```python
#awsiammapper.mapper
clients = {"s3": S3Client}
```

Currently clients are written predominently as a boto3 wrapper making requests to AWS to retreive live information. This however is not strictly necessary although gives the truest snapshot in time of identity access mappings. Alternatively a client could be written to interpret sources code such as [Terraform](https://www.terraform.io) or [CloudFormation](https://aws.amazon.com/it/cloudformation).

## Roadmap (Priority Items)

The priorisation of this tool from a personal perspective has bias towards prioritising data related services. Having said that happy to accept changes to any AWS Services given it is flexible to be extended a technical perspective. Longer term this tool may spread across multiple cloud services or I may buid a dedicated one per major cloud providers.

| # | overview       | value                                                                                    |
|---|----------------|------------------------------------------------------------------------------------------|
| 0 | IAM Service    | coverage increase - most access management controls are configured centrally within IAM  |
| 1 | LakeFormation  | coverage increase - Data services leverage LakeFormation to manage access to datasets    |
| 2 | Glue ecosystem | coverage increase - core AWS Data Service                                                |


## Development Approach

### Repository setup
This project utilises Python 3.10 and [Poetry](https://python-poetry.org/) with [Pre-commit](https://pre-commit.com/) to management code checks.
```shell
poetry shell #activates local shell
poetry install #install project dependencies (including dev)

pre-commit install #add precommit hooks
pre-commit run --all-files #check repo state
```

### Git
Trunk based Git branch strategy.

### Tooling
- GitHub Actions
- Snyk
- SonarCloud
- DockerHub

## Raise an issue
If there is a bug or change request please raise them on the associated [GitHub board](https://github.com/joncpaske/aws-iam-mapper/issues).