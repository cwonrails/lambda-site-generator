import boto3
import markdown
import uuid
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

BUCKET = "MY-BUCKET"

s3 = boto3.resource('s3')

# create jinja2 environment
env = Environment(
    loader=FileSystemLoader('./templates'),
    trim_blocks=True,
    lstrip_blocks=True
)

def generate(fname, content):
    template = env.get_template('default.html')
    output = template.render(content)
    s3.Bucket(BUCKET).put_object(Key=fname, Body=output)

def handler(event, context):

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        s3.Bucket(bucket).download_file(key, download_path)
        with open(download_path) as md_file:
            body = markdown.markdown(md_file.read())
        content = { 'body': body }
        fname = os.path.splitext(key)[0]+'.html'
        generate(fname, content)

    return "Finished processing markdown."
