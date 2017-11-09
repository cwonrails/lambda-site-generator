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

### Create S3 buckets ###

To set up the site generator and test it locally, you'll need four S3 buckets: one for your packaged SAM templates, one for HTML output, one for local testing (this one is optional but recommended), and one for Markdown input. CloudFormation will automatically create the last one for you, so you need to create the other three. For convenience, you may want to use the following naming scheme for the buckets:

* `<my-unique-bucket-name>-templates`
* `<my-unique-bucket-name>-output`
* `<my-unique-bucket-name>-test`

For instructions on creating an S3 bucket, see [Create a Bucket](http://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html).

### Install dependencies ###

The site generator requires several Python libraries. Install them:

    cd src
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt -t .
    deactivate && cd ..

The libraries to be installed (Jinja2, MarkupSafe, and Markdown) are ignored in .gitignore.

### Point the code to your output bucket ###

In main.py, replace `OUTPUT-BUCKET` with the name of your output bucket.

### [Optional] Test your application locally ###

First, upload a Markdown file to your test bucket. Then use [SAM Local](https://github.com/awslabs/aws-sam-local) to test your Lambda function before deploying it:

    sam local generate-event s3 --bucket <TEST-BUCKET> --key <KEY> | sam local invoke "SiteGen"

`<TEST-BUCKET>` is the name of your test bucket, and `<KEY>` is the name of the Markdown file that you uploaded to the test bucket. After running the command, you should find a new `<KEY>.html` file in your output bucket. The Markdown should be transformed to HTML.

### Package artifacts ###

When you're done coding and ready to deploy, run the following command, replacing `<TEMPLATE-BUCKET>` with the name of your templates bucket:

    sam package --template-file template.yaml --s3-bucket <TEMPLATE-BUCKET> --output-template-file packaged-template.yaml

This creates a new template file, packaged-template.yaml, that you will use to deploy your application.

### Deploy to AWS CloudFormation ###

Run the following command, replacing `<MY-NEW-STACK>` with a name for your CloudFormation stack.

    sam deploy --template-file packaged-template.yaml --stack-name <MY-NEW-STACK> --capabilities CAPABILITY_IAM

This uploads your template to an S3 bucket and deploys the specified resources using AWS CloudFormation.

### Get the name of your input bucket ###

When you deploy the site generator, CloudFormation provisions a new bucket where Lambda will listen for new objects to be created. This is your input bucket, where you'll put Markdown files to be converted to HTML. To use the site generator, you'll upload Markdown files to this bucket.

You can find the name of the bucket by opening the CloudFormation console, selecting your new stack, and locating the bucket under **Resources**.

### Test your application in the cloud ###

Upload a Markdown file to your input bucket; the file content will be transformed to HTML and written to a new .html file in the output bucket.

To host static content, you'll need to do some additional configuration of your output bucket. To learn more about configuring a bucket for web hosting, see [Hosting a Static Website on Amazon S3](http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html).

## Build your own site ##

Put your own [Jinja2](jinja.pocoo.org/docs/2.10/) templates in the templates dir, add scripts and styles, and make a real site!

## TODO ##
* Process multiple documents at once, as described [here](https://pythonhosted.org/Markdown/reference.html#the-details).
* Hide Markdown processing details in a class, in case we ever need to change MD parsers.
* Support passing in bucket and file name via command line.
* Script the creation of the S3 buckets with a Python script.
* Script the dependency installation.
* Consider setting output bucket name in ENV VAR.
