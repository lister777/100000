from cmd import Cmd
import boto3
import subprocess
import itertools

session = boto3.session.Session()
#default_region = "ap-southeast-2"

option_dict = {
    'test': ['--option1','--option2'],
    'list': ['--region','--profile']
    }
        
def list_instances(region=None, profile=None):
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

        instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        print("{:<5} {:<30} {:<25} {:<20} {:<15}".format("No.", "Name", "Id", "Public IP", "Type"))
        for i, instance in enumerate(instances):
            print("{:<5} {:<30} {:<25} {:<20} {:<15}".format(
                i, check_tag(instance.tags), instance.id,
                instance.public_ip_address, instance.instance_type))
    except Exception as e:
        print(e)


def remote_ssh(number, user):
    instance = list(instances)[int(number)]
    key_path = "/Users/admin/Documents/Key_Chain/{}.pem".format(instance.key_name)
    command = "ssh -i {} {}@{}".format(key_path, user, instance.public_ip_address)
    subprocess.call(command, shell=True)


class MyPrompt(Cmd):
    prompt = 'pb> '
    intro = "Welcome! Type ? to list commands"

    def do_exit(self, inp):
        # exit the application. Shorthand: x q.
        print("Bye")
        return True

    def do_setregion(self, inp):
        global default_region
        default_region = inp

    def do_list(self, inp):
        options = option_dict['list']
        warning = "Invaild options. Example: list --region us-east-1"
        if inp:
            try:
                inp_dict = dict(itertools.zip_longest(*[iter(inp.split()[1:])] * 2, fillvalue=""))
                if list(inp_dict.values())[-1]: #and set(inp_dict.keys()).issubset(set(options)):
                    list_instances(region=inp_dict.get('--region', 'ap-southeast-2'), profile=inp_dict.get('--profile'))
                else:
                    print(warning)
            except Exception as e:
                print(e)
        else:
            list_instances()
            
    def complete_list(self, text, line, start_index, end_index):
        options = option_dict['list']
        try:
            tokens = [t for t in line.split() if t.startswith('--')]
            if len(tokens) == 0:
                return []
            else:
                results = self.traverse(tokens,options)
                return results
        except Exception as e:
            print(e)
        
    def traverse(self,tokens,tree):
        if tree is None:
            return []
        elif len(tokens) == 1:
            return [x[2:] for x in tree if x.startswith(tokens[0])]
        else:
            return self.traverse(tokens[1:],tree)

    def do_test(self, inp):
        print(inp)
            
    def complete_test(self, text, line, start_index, end_index):
        options = option_dict['test']
        try:
            tokens = [t for t in line.split() if t.startswith('--')]
            if len(tokens) == 0:
                return []
            else:
                results = self.traverse(tokens,options)
                return results
        except Exception as e:
            print(e)
            
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