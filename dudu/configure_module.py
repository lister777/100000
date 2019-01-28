from global_settings import session, default_region
import json
import os
import itertools

def configure_template():
   # configure the instance launch template
   
    region          =  input("region: ")
    vpc_id          =  input("vpc-id: ")
    subnet_id       =  input("subnet-id: ")
    image_id        =  input("image-id: ")
    instance_type   =  input("instance-type: ")
    name            =  input("instance-name: ")
    iam_role        =  input("EC2-role: ")
    ssh_key         =  input("SSH-Key: ")
    ssh_keypath     =  input("SSH-KeyPath: ")
    template_name   =  input("template-name: ")
    
    template = {
        "region":       region,
        "vpc-id":       vpc_id,
        "subnet-id":    subnet_id,
        "image-id":     image_id,
        "instance-type":instance_type,
        "name":         name,
        "iam-role":     iam_role,
        "ssh-key":      ssh_key,
        "ssh-keypath":  ssh_keypath
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
            template_json = json.loads(template_file)
            template_json[template_name] = template
        else:
            template_json = {template_name:template}
            
    with open(file_path, 'w') as f:        
        template_file = json.dumps(template_json, sort_keys=True, indent=4)
        f.write(template_file)
    
    print(template_name, "is saved.")
    print(template_file)
    
    
    
def configure_template_options(inp_options):
    # configure/modify instance launch template with options
    
    path = os.path.expanduser("~") + '/.dudu'
    file = '/instance_template.json'
    file_path = path + file
    
    try:
        with open(file_path, 'r') as f:
            template_file = f.read()
            template_name = inp_options.pop('--template-name', 'default')

            if template_file:
                template_json = json.loads(template_file)
                print(template_json)
                for k, v in inp_options.items():
                    template_json[template_name][k[2:]] = v
            else:
                template_json = {template_name:inp_options}
                
        with open(file_path, 'w') as f:   
            template_file = json.dumps(template_json, sort_keys=True, indent=4)
            f.write(template_file)

        print(template_name, "is updated.")
        print(template_file)
            
    except Exception as e:
        print(e)