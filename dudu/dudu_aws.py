from cmd import Cmd

import subprocess
import itertools

import listec2_module
import configure_module
from global_settings import option_dict, option_verify


'''
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
'''


    
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
                configure_module.configure_template_options(inp_dict)
            else:
                print(warning)
        else:
            configure_module.configure_template()
            
    def complete_configure(self, text, line, start_index, end_index):
        return self.command_complete('configure', line)

    def do_listec2(self, inp):
        options = option_dict['list']
        warning = "Invaild options. Example: list --region us-east-1"
        
        if inp:
            inp_dict = dict(itertools.zip_longest(*[iter(inp.split())] * 2, fillvalue=""))
            if option_verify(inp_dict, options):
                try:
                    listec2_module.list_instances(region=inp_dict.get('--region'), profile=inp_dict.get('--profile'))
                except Exception as e:
                    print(e)
            else:
                print(warning)
        else:
            listec2_module.list_instances()
          
          
    def complete_listec2(self, text, line, start_index, end_index):
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