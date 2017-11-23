# Lambda Simple Site Generator #

A simple site generator that transforms Markdown into HTML.

## Requirements ##

* An AWS account
* Python and [virtualenv](https://virtualenv.pypa.io/en/stable/)
* The AWS Command Line Interface (AWS CLI)
* Docker
* SAM Local

To install the AWS CLI, follow the instructions at [Installing the AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).

To install Docker and SAM Local, follow the instructions at [Requirements for Using SAM Local](http://docs.aws.amazon.com/lambda/latest/dg/test-sam-local.html#sam-cli-requirements).

## Usage ##

To create and deploy the site generator, first ensure that you've installed the requirements. Then follow the steps below.

### Create an S3 bucket ###

If you don't already have one, create an S3 bucket for your SAM templates:

    aws s3 mb s3://<my-unique-template-bucket-name>

### Install dependencies ###

The site generator requires several Python libraries. Install them:

    cd src
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt -t .
    deactivate && cd ..

The libraries to be installed (Jinja2, MarkupSafe, and Markdown) are ignored in .gitignore.

### Package artifacts ###

When you're done coding and ready to deploy, run the following command, replacing `<TEMPLATE-BUCKET>` with the name of your templates bucket:

    sam package --template-file template.yaml --s3-bucket <TEMPLATE-BUCKET> --output-template-file packaged-template.yaml

This creates a new template file, packaged-template.yaml, that you will use to deploy your application.

### Deploy to AWS CloudFormation ###

Run the following command, replacing `<my-unique-stack-name>` with a name for your CloudFormation stack.

    sam deploy --template-file packaged-template.yaml --stack-name <my-unique-stack-name> --capabilities CAPABILITY_IAM

CloudFormation will create S3 buckets named after the stack, so use a stack name that a) is globally unique b) contains only lowercase letters, numbers, and hyphens.

### Test your application in the cloud ###

Upload a Markdown file to your input bucket; the file content will be transformed to HTML and written to a new .html file in the output bucket.

### [Optional] Test your application locally ###

First, upload a Markdown file to your test bucket. Then use [SAM Local](https://github.com/awslabs/aws-sam-local) to test your Lambda function before deploying it:

    sam local generate-event s3 --bucket <TEST-BUCKET> --key <KEY> | sam local invoke "SiteGen"

`<TEST-BUCKET>` is the name of your test bucket, and `<KEY>` is the name of the Markdown file that you uploaded to the test bucket. After running the command, you should find a new `<KEY>.html` file in your output bucket. The Markdown should be transformed to HTML.

## Build your own site ##

Put your own [Jinja2](jinja.pocoo.org/docs/2.10/) templates in the templates dir, add scripts and styles, and make a real site!

To host static content, you'll need to do some additional configuration of your output bucket. To learn more about configuring a bucket for web hosting, see [Hosting a Static Website on Amazon S3](http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html).

## TODO ##
* Process multiple documents at once, as described [here](https://pythonhosted.org/Markdown/reference.html#the-details).
* Hide Markdown processing details in a class, in case we ever need to change MD parsers.
* Support passing in bucket and file name via command line.
* Script the creation of the S3 buckets with a Python script.
* Script the dependency installation.
* Consider setting output bucket name in ENV VAR.
