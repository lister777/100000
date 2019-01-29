import listec2_module
import subprocess

def remote_ssh(number, user):
    instance    =   list(listec2_module.instances)[int(number)]
    key_path    =   "/Users/admin/Documents/Key_Chain/{}.pem".format(instance.key_name)
    command     =   "ssh -i {} {}@{}".format(key_path, user, instance.public_ip_address)
    subprocess.call(command, shell=True)