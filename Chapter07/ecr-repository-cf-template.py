"""Generating CloudFormation template."""

from troposphere import (
    Export,
    Join,
    Output,
    Parameter,
    Ref,
    Template
)
from troposphere.ecr import Repository

t = Template()

# commented out - begin: 'Template' object has no attribute 'add_description' in Python 3
# t.add_description("Effective DevOps in AWS: ECR Repository")
# commented out - end

t.add_parameter(Parameter(
    "RepoName",
    Type="String",
    Description="Name of the ECR repository to create"
))

t.add_resource(Repository(
    "Repository",
    RepositoryName=Ref("RepoName")
))

t.add_output(Output(
    "Repository",
    Description="ECR repository",
    Value=Ref("RepoName"),
    Export=Export(Join("-", [Ref("RepoName"), "repo"])),
))

print(t.to_json())
