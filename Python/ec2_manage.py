from cmd import Cmd
import boto3

region = "us-east-1"
def list_instances():
    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        print(filter(lambda tag: tag['Key'] == 'Name', instance.tags)[0]["Value"], instance.id, instance.public_ip_address, instance.instance_type,)
 
        
class MyPrompt(Cmd):
    prompt = 'pb> '
    intro = "Welcome! Type ? to list commands"
    
    def do_exit(self, inp):
        # exit the application. Shorthand: x q.
        print("Bye")
        return True
        
    def do_setregion(self, inp):
        global region
        region = inp
        
    def do_list(self, inp):
        list_instances()
        
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

#list_instances()
t= MyPrompt()
t.cmdloop()
print("after")