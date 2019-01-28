from cmd import Cmd
import boto3
import subprocess
import itertools
import json
import os

session = boto3.session.Session()
default_region = "ap-southeast-2"

option_dict = {
    'test': ['--option1','--option2'],
    'list': ['--region','--profile'],
    'run': ['--region','--profile', '--vpc-id', '--subnet-id', '--image-id', '--type', '--name', '--iam-role'],
    'configure':['--region','--vpc-id', '--subnet-id', '--image-id', '--instance-type', '--name', '--iam-role', '--ssh-key',
                '--ssh-keypath','--template-name']
    }
        
def list_instances(region=default_region, profile=None):
    global instances
    try:
        if profile is None:
            ec2 = session.resource('ec2', region_name=region)
        else:
            ec2 = session.resource('ec2', region_name=region, profile_name=profile)

        def check_tag(tags):
            if tags:
                for tag in tags:
                    if tag['Key'] == "Name":
                        return tag['Value']
            return " "

        instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running','pending']}])
        
        print("{:<5} {:<30} {:<23} {:<18} {:<12} {:<10} {:<15} {:<18} {:<10}".format("No.", "Name", 
            "Id", "Public IP", "Type", "State", "VPC_id", "Subnet_id", "Image_id"))
            
        for i, instance in enumerate(instances):
            print("{:<5} {:<30} {:<23} {:<18} {:<12} {:<10} {:<15} {:<18} {:<10}".format(
                i, check_tag(instance.tags), instance.id, instance.public_ip_address, instance.instance_type,
                list(instance.state.values())[-1], instance.vpc_id, instance.subnet_id, instance.image_id))
    except Exception as e:
        print(e)

def run_instances(region=default_region, **kwargs):
    try:
        ec2 = session.resource('ec2', region_name=region)
        default_vpc = list(ec2.vpcs.filter(Filters=[{'Name': 'isDefault', 'Values': ['true']}]))[0].id
        default_subnet = list(ec2.subnets.filter(Filters=[{'Name': 'vpc-id', 'Values': [default_vpc]}]))[0].id
        default_type = 't2.micro'
        if kwargs.get('--profile'):
            ec2 = session.client('ec2', region_name=region, profile_name=kwargs.get('--profile'))
        else:
            ec2 = session.client('ec2', region_name=region)
    
        print(default_vpc)
        print(default_subnet)
    except Exception as e:
        print(e)
        
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

def option_verify(inp_dict, options):
    if list(inp_dict.values())[-1] and set(inp_dict.keys()).issubset(set(options)):
        return True
    else:
        return False
    
def remote_ssh(number, user):
    instance    =   list(instances)[int(number)]
    key_path    =   "/Users/admin/Documents/Key_Chain/{}.pem".format(instance.key_name)
    command     =   "ssh -i {} {}@{}".format(key_path, user, instance.public_ip_address)
    subprocess.call(command, shell=True)


class MyPrompt(Cmd):
    prompt = 'pb> '
    intro = "Welcome! Type ? to list commands"
    
    def traverse(self,tokens,tree):
        if tree is None:
            return []
        elif len(tokens) == 1:
            if tokens[0] in tree:
                return []
            else:
                return [x[2:] for x in tree if x.startswith(tokens[0])]
        else:
            if tokens[0] in tree:
                tree.remove(tokens[0])
            return self.traverse(tokens[1:],tree)
            
    def command_complete(self, command_name, line):
        options = option_dict[command_name]
        try:
            tokens = [t for t in line.split() if t.startswith('--')]
            if len(tokens) == 0:
                return []
            else:
                results = self.traverse(tokens,options)
                return results
        except Exception as e:
            print(e)

    def do_exit(self, inp):
        # exit the application. Shorthand: x q.
        print("Bye")
        return True
    
    def do_configure(self, inp):
        options = option_dict['configure']
        warning = "Invaild options. Example: configure --template-name"
        if inp:
            inp_dict = dict(itertools.zip_longest(*[iter(inp.split())] * 2, fillvalue=""))
            if option_verify(inp_dict, options):
                configure_template_options(inp_dict)
            else:
                print(warning)
        else:
            configure_template()
            
    def complete_configure(self, text, line, start_index, end_index):
        return self.command_complete('configure', line)
            
    def do_setregion(self, inp):
        global default_region
        default_region = inp


    def do_list(self, inp):
        options = option_dict['list']
        warning = "Invaild options. Example: list --region us-east-1"
        
        if inp:
            inp_dict = dict(itertools.zip_longest(*[iter(inp.split())] * 2, fillvalue=""))
            if option_verify(inp_dict, options):
                try:
                    list_instances(region=inp_dict.get('--region'), profile=inp_dict.get('--profile'))
                except Exception as e:
                    print(e)
            else:
                print(warning)
        else:
            list_instances()
          
          
    def complete_list(self, text, line, start_index, end_index):
        return self.command_complete('list', line)
            
    def do_ssh(self, inp, user="ec2-user"):
        remote_ssh(inp, user)

    def do_shell(self, inp):
        subprocess.call(inp, shell=True)

    def do_add(self, inp):
        print("Adding '{}".format(inp))

    def help_add(self):
        print("Add a new entry to the system")

    def default(self, inp):
        if inp == ':x' or inp == ':q':
            return self.do_exit(inp)

        print("Default: {}".format(inp))

    def emptyline(self):
        pass


t = MyPrompt()
t.cmdloop()