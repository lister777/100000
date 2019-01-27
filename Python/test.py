import boto3
import os, json

session = boto3.session.Session()
default_region = "ap-southeast-2"  

def configure_template():
    
    region          =  input("region: ")
    vpc_id          =  input("vpc_id: ")
    subnet_id       =  input("subnet_id: ")
    image_id        =  input("image_id: ")
    type            =  input("instance_type: ")
    name            =  input("instance_name: ")
    iam_role        =  input("EC2_role: ")
    ssh_key         =  input("SSH_Key: ")
    ssh_key_path    =  input("SSH_Key_Path: ")
    template_name   =  input("template_name: ")
    
    template = {
        "region":region,
        "vpc_id":vpc_id,
        "subnet_id":subnet_id,
        "image_id":image_id,
        "type":type,
        "name":name,
        "iam_role":iam_role,
        "ssh_key":ssh_key,
        "ssh_key_path":ssh_key_path
    }
   
    path = os.path.expanduser("~") + '/.dudu'
    file = '/instance_template.json'
    file_path = path + file
    
    if not os.path.exists(file_path):
        if not os.path.isdir(path):
            os.mkdir(path)
        open(file_path, 'a').close()
    
    with open(file_path, 'r') as f:
        template_file = f.read()
        if template_file:
            template_dict = json.loads(template_file)
            template_dict[template_name] = template
        else:
            template_dict = {template_name:template}
            
    with open(file_path, 'w') as f:
        template_file = json.dumps(template_dict, sort_keys=True, indent=4)
        f.write(template_file)
        
    print("{} is saved.".format(template_name))
    print(template_file)
    
configure_template()

