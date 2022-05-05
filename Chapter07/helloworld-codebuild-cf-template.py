"""Generating CloudFormation template."""

from awacs.aws import (
    Allow,
    Policy,
    Principal,
    Statement
)

from awacs.sts import AssumeRole

from troposphere import (
    Join,
    Ref,
    Template
)

from troposphere.codebuild import (
    Artifacts,
    Environment,
    Project,
    Source
)

from troposphere.iam import Role

t = Template()

# commented out - begin: 'Template' object has no attribute 'add_description' in Python 3
# t.add_description("Effective DevOps in AWS: CodeBuild - Helloworld container")
# commented out - end

t.add_resource(Role(
    "ServiceRole",
    AssumeRolePolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[AssumeRole],
                Principal=Principal("Service", ["codebuild.amazonaws.com"])
            )
        ]
    ),
    Path="/",
    ManagedPolicyArns=[
        'arn:aws:iam::aws:policy/AWSCodePipelineReadOnlyAccess',
        'arn:aws:iam::aws:policy/AWSCodeBuildDeveloperAccess',
        'arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser',
        'arn:aws:iam::aws:policy/AmazonS3FullAccess',
        'arn:aws:iam::aws:policy/CloudWatchLogsFullAccess'
    ]
))

environment = Environment(
    ComputeType='BUILD_GENERAL1_SMALL',
    Image='aws/codebuild/docker:1.12.1',
    # Image='aws/codebuild/standard:4.0',
    # Image='aws/codebuild/amazonlinux2-x86_64-standard:3.0',
    Type='LINUX_CONTAINER',
    EnvironmentVariables=[
        {'Name': '_BUILDAH_STARTED_IN_USERNS', 'Value': ''},
        {'Name': 'BUILDAH_ISOLATION', 'Value': 'chroot'},
        {'Name': 'REPOSITORY_NAME', 'Value': 'helloworld'},
        {'Name': 'REPOSITORY_URI',
            'Value': Join("", [
                Ref("AWS::AccountId"),
                ".dkr.ecr.",
                Ref("AWS::Region"),
                ".amazonaws.com",
                "/",
                "helloworld"])},
    ],
)

# buildspec = """version: 0.1
buildspec = """version: 0.2
phases:
  install:
    commands:
      - uname -a
    #   - sestatus -v
    #   - ps -ef | grep selinux
    #   - cat /etc/selinux/config
    #   - sed -i s/^SELINUX=.*$/SELINUX=permissive/ /etc/selinux/config
    #   - cat /etc/selinux/config
    #   - touch /.autorelabel
    #   - shutdown -r now
    #   - getenforce
    #  - curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable.repo https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/CentOS_7/devel:kubic:libcontainers:stable.repo
    #  - yum -y update
    #  - rpm --restore shadow-utils 2>/dev/null
    #  - yum -y install yum-plugin-copr
    #  - yum -y copr enable lsm5/container-selinux
    #  - yum -y install buildah fuse-overlayfs
    #  - yum -y install fuse-overlayfs
    #  - mkdir -p /var/lib/shared/overlay-images /var/lib/shared/overlay-layers /var/lib/shared/vfs-images /var/lib/shared/vfs-layers
    #  - touch /var/lib/shared/overlay-images/images.lock
    #  - touch /var/lib/shared/overlay-layers/layers.lock
    #  - touch /var/lib/shared/vfs-images/images.lock
    #  - touch /var/lib/shared/vfs-layers/layers.lock
    #   - cat /etc/containers/storage.conf
    #  - sed -i -e 's|^#mount_program|mount_program|g' -e '/additionalimage.*/a "/var/lib/shared",' -e 's/^mountopt =.*/mountopt = "nodev,fsync=0"/g' /etc/containers/storage.conf
    #   - cat /etc/containers/storage.conf
    #  - curl -L -o /etc/containers/containers.conf https://raw.githubusercontent.com/containers/buildah/main/contrib/buildahimage/stable/containers.conf
    #   - cat /etc/containers/containers.conf
    #   - useradd build
    #   - echo -e "build:1:999" >> /etc/subuid
    #   - echo -e "build:1001:64535" >> /etc/subuid
    #   - cat /etc/subuid
    #   - echo -e "build:1:999" >> /etc/subgid
    #   - echo -e "build:1001:64535" >> /etc/subgid
    #   - cat /etc/subgid
    #   - mkdir -p /home/build/.local/share/containers
    #   - chown -R build:build /home/build
    #
    #   - yum -y install make golang bats btrfs-progs-devel device-mapper-devel glib2-devel gpgme-devel libassuan-devel libseccomp-devel git bzip2 go-md2man runc containers-common fuse-overlayfs
    #   - sed -i 's/^mountopt =.*/mountopt = "nodev,fsync=0"/g' /etc/containers/storage.conf
    #   - yum -y install containernetworking-cni
    #   - mkdir ~/buildah
    #   - cd ~/buildah
    #   - export GOPATH=`pwd`
    #   - git clone https://github.com/containers/buildah ./src/github.com/containers/buildah
    #   - cd ./src/github.com/containers/buildah
    #   - make
    #   - make install
    #   - buildah --help
    #
    #
    #   - apt-get -y install software-properties-common
    #   - add-apt-repository -y ppa:alexlarsson/flatpak
    #   - add-apt-repository -y ppa:gophers/archive
    #   - apt-add-repository -y ppa:projectatomic/ppa
    #   - apt-get -y -qq update
    #   - apt-get -y install bats btrfs-tools git libapparmor-dev libdevmapper-dev libglib2.0-dev libgpgme11-dev libseccomp-dev libselinux1-dev skopeo-containers go-md2man
    #   - apt-get -y install golang-1.13
    #   - apt-get -y install containernetworking-plugins
    #   - mkdir ~/buildah
    #   - cd ~/buildah
    #   - export GOPATH=`pwd`
    #   - git clone https://github.com/containers/buildah ./src/github.com/containers/buildah
    #   - cd ./src/github.com/containers/buildah
    #   - PATH=/usr/lib/go-1.13/bin:$PATH make runc all SECURITYTAGS="apparmor seccomp"
    #   - make install install.runc
    #   - buildah --help
    #
    #   - apt-get -y install buildah
    #   - useradd build
  pre_build:
    commands:
    #   - aws --version
    #   - echo "${CODEBUILD_INITIATOR##*/}"
      - aws codepipeline get-pipeline-state --name "${CODEBUILD_INITIATOR##*/}" --query stageStates[?actionStates[0].latestExecution.externalExecutionId==\`$CODEBUILD_BUILD_ID\`].latestExecution.pipelineExecutionId --output=text > /tmp/execution_id.txt
    #   - cat /tmp/execution_id.txt
      - aws codepipeline get-pipeline-execution --pipeline-name "${CODEBUILD_INITIATOR##*/}" --pipeline-execution-id $(cat /tmp/execution_id.txt) --query 'pipelineExecution.artifactRevisions[0].revisionId' --output=text > /tmp/tag.txt
    #   - cat /tmp/tag.txt
      - printf "%s:%s" "$REPOSITORY_URI" "$(cat /tmp/tag.txt)" > /tmp/build_tag.txt
    #   - cat /tmp/build_tag.txt
      - printf '{"tag":"%s"}' "$(cat /tmp/tag.txt)" > /tmp/build.json
    #   - cat /tmp/build.json
      - $(aws ecr get-login --no-include-email)
  build:
    commands:
      - docker login --username=actarus1272 --password=43FabTa86!
    #   - docker build -t "$(cat /tmp/build_tag.txt)" .
      - docker build --isolation=default -t "$(cat /tmp/build_tag.txt)" .
    #   - buildah bud -f Dockerfile -t "081052550542.dkr.ecr.us-east-1.amazonaws.com/helloworld:8e2a2affcdbafbb1f122edb8a3fa347b11b613eb" .
    #   - buildah bud --isolation=chroot --cap-add SYS_ADMIN --security-opt seccomp=/usr/share/containers/seccomp.json --security-opt apparmor=unconfined --device=/dev/fuse -f Dockerfile -t "$(cat /tmp/build_tag.txt)" .
    #   - buildah bud --isolation=chroot --security-opt seccomp=unconfined --security-opt apparmor=unconfined -f Dockerfile -t "$(cat /tmp/build_tag.txt)" .
  post_build:
    commands:
      - docker push "$(cat /tmp/build_tag.txt)"
    #   - buildah push "081052550542.dkr.ecr.us-east-1.amazonaws.com/helloworld:8e2a2affcdbafbb1f122edb8a3fa347b11b613eb"
    #   - buildah push "$(cat /tmp/build_tag.txt)"
    #   - aws ecr batch-get-image --repository-name $REPOSITORY_NAME --image-ids imageTag="$(cat /tmp/tag.txt)" --output json | jq --raw-output --join-output '.images[0].imageManifest' | tee /tmp/latest_manifest.json
      - aws ecr batch-get-image --repository-name $REPOSITORY_NAME --image-ids imageTag="$(cat /tmp/tag.txt)" --query 'images[].imageManifest' --output text | tee /tmp/latest_manifest.json
      - aws ecr put-image --repository-name $REPOSITORY_NAME --image-tag latest --image-manifest "$(cat /tmp/latest_manifest.json)"
artifacts:
  files: /tmp/build.json
  discard-paths: yes
"""

t.add_resource(Project(
    "CodeBuild",
    Name='HelloWorldContainer',
    Environment=environment,
    ServiceRole=Ref("ServiceRole"),
    Source=Source(
        Type="CODEPIPELINE",
        BuildSpec=buildspec
    ),
    Artifacts=Artifacts(
        Type="CODEPIPELINE",
        Name="output"
    ),
))

print(t.to_json())
