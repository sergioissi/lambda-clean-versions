# Clean Serverless versions

Created with Aws CDK, this lambda will run every first day of the month to delete old lambda versions (keeping the last 10).
This is necessary when deploying with Serverless framework because it creates (by default but it can be disabled) a new version
of your function every time you deploy. Please take a look at <a href="https://docs.aws.amazon.com/lambda/latest/dg/limits.html">
Lambda limits</a>.

## Setup

### Installing the CDK CLI

```sh
$ npm install -g aws-cdk
$ cdk --version
```

### Create your python virtual env

```sh
$ python -m venv .env
$ source .env/bin/activate
$ make requirements
```

### Bootstrapping your AWS Environment

Before you can use the AWS CDK you must bootstrap your AWS environment to create the infrastructure that the AWS CDK CLI needs to deploy your AWS CDK app. Currently the bootstrap command creates only an Amazon S3 bucket.

```sh
$ cdk bootstrap
```

You incur any charges for what the AWS CDK stores in the bucket. Because the AWS CDK does not remove any objects from the bucket, the bucket can accumulate objects as you use the AWS CDK. You can get rid of the bucket by deleting the CDKToolkit stack from your account.

## Commands to manage and create/update infrastructure:

Synthesizes and prints the CloudFormation template for this stack in the 'cdk.out' folder.
```sh
$ cdk synth
```

Compares the specified stack with the deployed stack or a local template file, and returns with status 1 if any difference is found.
```sh
$ cdk diff
```

Deploys (create and update) the stack(s) named STACKS into your AWS account.
```sh
$ cdk deploy
```

Destroy the stack(s) named STACKS.
```sh
$ cdk destroy
```