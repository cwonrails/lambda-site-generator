# Lambda Simple Site Generator #

A simple site generator that transforms Markdown into HTML.

## Requirements ##

* An AWS account
* Python and virtualenv
* The AWS Command Line Interface (AWS CLI)
* Docker
* SAM Local
* An Amazon S3 bucket

To install a virtualenv, see [virtualenv](https://virtualenv.pypa.io/en/stable/).

To install the AWS CLI, follow the instructions at [Installing the AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).

To install Docker and SAM Local, follow the instructions at [Requirements for Using SAM Local](http://docs.aws.amazon.com/lambda/latest/dg/test-sam-local.html#sam-cli-requirements).

## Usage ##

To create and deploy the site generator, first ensure that you've installed the requirements. Then follow the steps below.

### Install local dependencies ###

    cd src
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt -t .
    deactivate && cd ..

The libraries to be installed (Jinja2, MarkupSafe, and Markdown) are ignored in .gitignore.

### Create an S3 bucket ###

Create an S3 bucket to store your packaged template, Markdown input, and HTML output. For instructions on creating an S3 bucket, see [Create a Bucket](http://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html).

### Upload a Markdown file to your content bucket ###

Upload a Markdown file to your bucket. You can use the **test.md** file in this package, or any other Markdown file.

For more info on uploading to S3, see [How Do I Upload Files and Folders to an S3 Bucket?](http://docs.aws.amazon.com/AmazonS3/latest/user-guide/upload-objects.html)

### Point to your bucket ###

In main.py, set `BUCKET` to the name of your content bucket.

### Test your application locally ###

Use [SAM Local](https://github.com/awslabs/aws-sam-local) to run your Lambda function locally:

   sam local generate-event s3 --bucket <BUCKET>- --key <KEY> | sam local invoke "SiteGen"

`<BUCKET>` should be the name of your bucket, and `<KEY>` should be the name of the Markdown file that you uploaded. You should find a `<KEY>.html` in your bucket.

### Package artifacts ###

Run the following command, replacing `<BUCKET>` with the name of your bucket:

    sam package --template-file template.yaml --s3-bucket <BUCKET> --output-template-file packaged-template.yaml

This creates a new template file, packaged-template.yaml, that you will use to deploy your serverless application.

### Deploy to AWS CloudFormation ###

Run the following command, replacing `MY-NEW-STACK` with a name for your CloudFormation stack.

    sam deploy --template-file packaged-template.yaml --stack-name MY-NEW-STACK --capabilities CAPABILITY_IAM

This uploads your template to an S3 bucket and deploys the specified resources using AWS CloudFormation.

### Test your application in the cloud ###

When you deploy the site generator, CloudFormation provisions a new bucket where Lambda will listen for new objects to be created. To test the site generator in the cloud, you'll need to upload a Markdown file to this new bucket.

You can find the bucket by opening the CloudFormation console, selection your stack, and locating the bucket under **Resources**. When you upload a Markdown file to this bucket, it will be transformed to HTML output in the bucket referenced by your code.

Note that your HTML output and your packaged templates are currently living in the same bucket. In a real world scenario where you want to host static content in an S3 bucket, you'll want to have a separate bucket for your site. To learn more about configuring a bucket for web hosting, see: [Hosting a Static Website on Amazon S3](http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html).

## TODO ##
* Process multiple documents at once, as described [here](https://pythonhosted.org/Markdown/reference.html#the-details).
* Hide Markdown processing details in a class, in case we ever need to change MD parsers.
* Support passing in bucket and file name via command line.
