"""Generating CloudFormation template."""

from ipaddress import ip_network

from ipify import get_ip

from troposphere import (
    Base64,
    ec2,
    GetAtt,
    Join,
    Output,
    Parameter,
    Ref,
    Template,
)

ApplicationName = "Chapter03/helloworld"
ApplicationPort = "3000"
GithubAccount = "fabiotaormina"
GithubAnsibleURL = "https://github.com/{}/Ansible".format(GithubAccount)

PublicCidrIp = str(ip_network(get_ip()))

AnsiblePullCmd = \
    "/usr/bin/ansible-pull --url {} -i localhost -e ansible_python_interpreter=/usr/bin/python2.7 --sleep 60 {}.yml".format(
        GithubAnsibleURL,
        ApplicationName
    )

t = Template()

# commented out - begin: 'Template' object has no attribute 'add_description' in Python 3
#t.add_description("Effective DevOps in AWS: HelloWorld web application")
# commented out - end

t.add_parameter(Parameter(
    "KeyPair",
    Description="Name of an existing EC2 KeyPair to SSH",
    Type="AWS::EC2::KeyPair::KeyName",
    ConstraintDescription="must be the name of an existing EC2 KeyPair.",
))

t.add_resource(ec2.SecurityGroup(
    "SecurityGroup",
    GroupDescription="Allow SSH and TCP/{} access".format(ApplicationPort),
    SecurityGroupIngress=[
        ec2.SecurityGroupRule(
            IpProtocol="tcp",
            FromPort="22",
            ToPort="22",
            CidrIp=PublicCidrIp,
        ),
        ec2.SecurityGroupRule(
            IpProtocol="tcp",
            FromPort=ApplicationPort,
            ToPort=ApplicationPort,
            CidrIp="0.0.0.0/0",
        ),
    ],
))

ud = Base64(Join('\n', [
    "#!/bin/bash",
    "yum install --enablerepo=epel -y git",
    "yum install --enablerepo=epel -y ansible",
    AnsiblePullCmd,
    "echo '*/10 * * * * {}' > /etc/cron.d/ansible-pull".format(AnsiblePullCmd)
]))

t.add_resource(ec2.Instance(
    "instance",
    ImageId="ami-cfe4b2b0",
    InstanceType="t2.micro",
    SecurityGroups=[Ref("SecurityGroup")],
    KeyName=Ref("KeyPair"),
    UserData=ud,
))

t.add_output(Output(
    "InstancePublicIp",
    Description="Public IP of our instance.",
    Value=GetAtt("instance", "PublicIp"),
))

t.add_output(Output(
    "WebUrl",
    Description="Application endpoint",
    Value=Join("", [
        "http://", GetAtt("instance", "PublicDnsName"),
        ":", ApplicationPort
    ]),
))

print(t.to_json())
