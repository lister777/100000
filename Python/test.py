import boto3
import os, json

session = boto3.session.Session()
default_region = "ap-southeast-2"  

test = {'default': {'iam-role': 'asda', 'image-id': 'asd', 'instance-type': 'asad', 'name': 'aasd', 'region': 'asdsa', 'ssh-key': 'sda', 'ssh-keypath': 'adas', 'subnet-id': 'sad', 'vpc-id': 'asd'}, 'test': {'iam-role': 'asd', 'image-id': 'asd', 'instance-type': 'asd', 'name': 'as', 'region': 'sad', 'ssh-key': '', 'ssh-keypath': 'asd', 'subnet-id': 'da', 'vpc-id': 'a'}}
inp_options = {'--iam-role': 'test'}
for k, v in inp_options:
    test['default'][k[2:]] = v
print(test['default'])