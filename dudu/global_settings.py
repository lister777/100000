import boto3

session = boto3.session.Session()
default_region = "ap-southeast-2"

option_dict = {
    'test': ['--option1','--option2'],
    'list': ['--region','--profile'],
    'run': ['--region','--profile', '--vpc-id', '--subnet-id', '--image-id', '--type', '--name', '--iam-role'],
    'configure':['--region','--vpc-id', '--subnet-id', '--image-id', '--instance-type', '--name', '--iam-role', '--ssh-key',
                '--ssh-keypath','--template-name']
    }
    
def option_verify(inp_dict, options):
    if list(inp_dict.values())[-1] and set(inp_dict.keys()).issubset(set(options)):
        return True
    else:
        return False