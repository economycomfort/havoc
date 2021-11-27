#!/usr/bin/env python3

import re
import ast
import json
import argparse
from configparser import ConfigParser
import tabulate
import time as t
from cmd2 import Cmd
import havoc

init_parser = argparse.ArgumentParser(description='havoc CLI')

init_parser.add_argument('--profile', help='Use a specific profile from your credential file')
init_args = init_parser.parse_args()

profile = init_args.profile

# Load the configuration file
config = ConfigParser()
config.read('~/.havoc/config')

# Get api_key and secret_key
if profile:
    api_key = config.get(profile, 'API_KEY')
    secret = config.get(profile, 'SECRET')
    api_region = config.get(profile, 'API_REGION')
    api_domain_name = config.get(profile, 'API_DOMAIN_NAME')
    output = config.get(profile, 'OUTPUT')
else:
    api_key = config.get('default', 'API_KEY')
    secret = config.get('default', 'SECRET')
    api_region = config.get('default', 'API_REGION')
    api_domain_name = config.get('default', 'API_DOMAIN_NAME')
    output = config.get('default', 'OUTPUT')

h = havoc.Connect(api_region, api_domain_name, api_key, secret)


def convert_input(args, inp):
    line = inp.split('--')
    for l in line:
        arg = re.search('([^=]+)=(.*)', l)
        if arg:
            if arg.group(1) in args:
                args[arg.group(1)] = arg.group(2).strip()
    return args


def print_table(command, data):
    for d in data:
        table = []
        if isinstance(data[d], dict):
            table.append(data[d])
            print(f'{command}:')
            print(tabulate(table, headers="keys", tablefmt='pretty'), '\n')


def format_output(command, data):
    if output == 'table':
        print_table(command, data)
    else:
        data_out = {command: data}
        print(json.dumps(data_out))


class HavocCMD(Cmd):

    prompt = 'havoc> '
    intro = "havoc CLI - Type ? to list commands"

    def emptyline(self):
        pass

    def do_exit(self):
        print('Bye')
        return True

    def help_exit(self):
        print('\nExit the application. Shorthand: x q Ctrl-D.\n')

    def do_list_tasks(self):
        list_tasks_response = h.list_tasks()
        format_output('list_tasks', list_tasks_response)

    def help_list_tasks(self):
        print('\nList all running tasks.')

    def do_get_task(self, inp):
        args = {'task_name': ''}
        command_args = self.convert_input(args, inp)
        get_task_response = h.get_task(**command_args)
        format_output('get_task', get_task_response)

    def help_get_task(self):
        print('\nGet details of a given task.')
        print('\n--task_name=<string> - (required) the name of the task to retrieve details for')

    def do_kill_task(self, inp):
        args = {'task_name': ''}
        command_args = self.convert_input(args, inp)
        kill_task_response = h.kill_task(**command_args)
        format_output('kill_task', kill_task_response)

    def help_kill_task(self):
        print('\nForce quit a running task.')
        print('\n--task_name=<string> - (required) the name of the task to kill')

    def do_list_task_types(self):
        list_task_types_response = h.list_task_types()
        format_output('list_task_types', list_task_types_response)

    def help_list_task_types(self):
        print('\nList all available task types.')

    def do_get_task_type(self, inp):
        args = {'task_type': ''}
        command_args = self.convert_input(args, inp)
        get_task_type_response = h.get_task_type(**command_args)
        format_output('get_task_type', get_task_type_response)

    def help_get_task_type(self):
        print('\nGet details of a given task type.')
        print('\n--task_type=<string> - (required) the name of the task type to get')

    def do_create_task_type(self, inp):
        args = {'task_type': '', 'source_image': '', 'capabilities': '', 'cpu': '', 'memory': ''}
        command_args = self.convert_input(args, inp)
        create_task_type_response = h.create_task_type(**command_args)
        format_output('create_task_type', create_task_type_response)

    def help_create_task_type(self):
        print('\nCreate a new task type with the given parameters.')
        print('\n--task_type=<string> - (required) a name to refer to the task type')
        print('\n--source_image=<string> - (required) URL of the source container image')
        print('\n--capabilities=<list> - (required) list of commands accepted by the task')
        print('\n--cpu=<integer> - (required) number of CPU cores to allocate to the task')
        print('\n--memory=<integer> - (required) amount of memory to allocate to the task')

    def do_delete_task_type(self, inp):
        args = {'task_type': ''}
        command_args = self.convert_input(args, inp)
        delete_task_type_response = h.delete_task_type(**command_args)
        format_output('delete_task_type', delete_task_type_response)

    def help_delete_task_type(self):
        print('\nDelete the given task type.')
        print('\n--task_type=<string> - (required) the name of the task type to delete')

    def do_list_users(self):
        list_users_response = h.list_users()
        format_output('list_users', list_users_response)

    def help_list_users(self):
        print('\nList all ./havoc users.')

    def do_get_user(self, inp):
        args = {'user_id': ''}
        command_args = self.convert_input(args, inp)
        get_user_response = h.get_user(**command_args)
        format_output('get_user', get_user_response)

    def help_get_user(self):
        print('\nGet details of a given user.')
        print('\n--user_id=<string> - (required) the ID of the user to get')

    def do_create_user(self, inp):
        args = {'user_id': '', 'admin': ''}
        command_args = self.convert_input(args, inp)
        create_user_response = h.create_user(**command_args)
        format_output('create_user', create_user_response)

    def help_create_user(self):
        print('\nCreate a new user with the given parameters.')
        print('\n--user_id=<string> - (required) a unique identifier to associate with the user')
        print('\n--admin=[yes|no] - (optional) specify whether or not the user has admin privileges (defaults to no)')

    def do_update_user(self, inp):
        args = {'user_id': '', 'new_user_id': '', 'admin': '', 'reset_keys': ''}
        command_args = self.convert_input(args, inp)
        update_user_response = h.update_user(**command_args)
        format_output('update_user', update_user_response)

    def help_update_user(self):
        print('\nUpdate an existing user.')
        print('\n--user_id=<string> - (required) the user_id associated with the user to make updates to')
        print('\n--new_user_id=<string> - (optional) a new unique identifier to associate with the user')
        print('\n--admin=[yes|no] - (optional) - add or remove admin privileges for the user (defaults to no change)')
        print('\n--reset_keys=yes - (optional) - forces a reset of the user\'s API key and secret (if not present, '
              'keys are not changed)')

    def do_delete_user(self, inp):
        args = {'user_id': ''}
        command_args = self.convert_input(args, inp)
        delete_user_response = h.delete_user(**command_args)
        format_output('delete_user', delete_user_response)

    def help_delete_user(self):
        print('\nDelete an existing user.')
        print('\n--user_id=<string> - (required) the user_id of the user to be deleted')

    def do_list_files(self):
        list_files_response = h.list_files()
        format_output('list_files', list_files_response)

    def help_list_files(self):
        print('\nList all files in the shared workspace.')

    def do_get_file(self, inp):
        args = {'file_name': '', 'file_path': ''}
        command_args = self.convert_input(args, inp)
        file_path = command_args['file_path']
        file_name = command_args['file_name']
        f = open(f'{file_path}/{file_name}', 'wb')
        del command_args['file_path']
        get_file_response = h.get_file(**command_args)
        file_contents = get_file_response['file_contents']
        f.write(file_contents)
        f.close()
        del get_file_response['file_contents']
        get_file_response['file_path'] = file_path
        format_output('get_file', get_file_response)

    def help_get_file(self):
        print('\nDownload a file from the shared workspace.')
        print('\n--file_name=<string> - (required) the name of the file to download.')
        print('\n--file_path=<string> - (required) the path to the local directory to download the file to')

    def do_create_file(self, inp):
        args = {'file_name': '', 'file_path': ''}
        command_args = self.convert_input(args, inp)
        file_path = command_args['file_path']
        file_name = command_args['file_name']
        f = open(f'{file_path}/{file_name}', 'rb')
        raw_file = f.read()
        command_args['raw_file'] = raw_file
        del command_args['file_path']
        create_file_response = h.create_file(**command_args)
        format_output('create_file', create_file_response)

    def help_create_file(self):
        print('\nUpload a file to the shared workspace.')
        print('\n--file_name=<string> - (required) the name of the file to upload.')
        print('\n--file_path=<string> - (required) the path to the local directory where the file resides')

    def do_delete_file(self, inp):
        args = {'file_name': ''}
        command_args = self.convert_input(args, inp)
        delete_file_response = h.delete_file(**command_args)
        format_output('delete_file', delete_file_response)

    def help_delete_file(self):
        print('\nDelete a file in the shared workspace.')
        print('\n--file_name=<string> - (required) the name of the file to be deleted.')

    def do_list_portgroups(self):
        list_portgroups_response = h.list_portgroups()
        format_output('list_portgroups', list_portgroups_response)

    def help_list_portgroups(self):
        print('\nList all existing portgroups.')

    def do_get_portgroup(self, inp):
        args = {'portgroup_name': ''}
        command_args = self.convert_input(args, inp)
        get_portgroup_response = h.get_portgroup(**command_args)
        format_output('get_portgroup', get_portgroup_response)

    def help_get_portgroup(self):
        print('\nGet details of a given portgroup.')
        print('\n--portgroup_name=<string> - (required) the name of the portgroup to retrieve details for')

    def do_create_portgroup(self, inp):
        args = {'portgroup_name': '', 'portgroup_description': ''}
        command_args = self.convert_input(args, inp)
        create_portgroup_response = h.create_portgroup(**command_args)
        format_output('create_portgroup', create_portgroup_response)

    def help_create_portgroup(self):
        print('\nCreate a new portgroup with the given parameters.')
        print('\n--portgroup_name=<string> - (required) a unique identifier to associate with the portgroup')
        print('\n--porgroup_description=<string> - (required) a description containing the purpose of the portgroup')

    def do_update_portgroup_rule(self, inp):
        args = {'portgroup_name': '', 'portgroup_action': '', 'ip_ranges': '', 'port': '', 'ip_protocol': ''}
        command_args = self.convert_input(args, inp)
        update_portgroup_rule_response = h.update_portgroup_rule(**command_args)
        format_output('update_portgroup_rule', update_portgroup_rule_response)

    def help_update_portgroup_rule(self):
        print('\nAdd or remove a rule to or from a given portgroup.')
        print('\n--portgroup_name=<string> - (required) the name of the portgroup to modify')
        print('\n--portgroup_action=[add|remove] - (required) indicate whether to add or remove a rule')
        print('\n--ip_ranges=<string> - (required) the IP address range that is allowed access by the portgroup rule')
        print('\n--port=<integer> - (required) the port number that the IP ranges are allowed to access')
        print('\n--ip_protocol=[udp|tcp|icmp] - (required) the IP protcols that IP ranges are allowed to use')

    def do_delete_portgroup(self, inp):
        args = {'portgroup_name': ''}
        command_args = self.convert_input(args, inp)
        delete_portgroup_response = h.delete_portgroup(**command_args)
        format_output('delete_portgroup', delete_portgroup_response)

    def help_delete_portgroup(self):
        print('\nDelete an existing portgroup.')
        print('\n--portgroup_name=<string> - (required) the name of the portgroup to be deleted')

    def do_list_domains(self):
        list_domains_response = h.list_domains()
        format_output('list_domains', list_domains_response)

    def help_list_domains(self):
        print('\nList all existing domains.')

    def do_get_domain(self, inp):
        args = {'domain_name': ''}
        command_args = self.convert_input(args, inp)
        get_domain_response = h.get_domain(**command_args)
        format_output('get_domain', get_domain_response)

    def help_get_domain(self):
        print('\nGet details of a given domain.')
        print('\n--domain_name=<string> - (required) the name of the domain to retrieve details for')

    def do_create_domain(self, inp):
        args = {'domain_name': '', 'hosted_zone': ''}
        command_args = self.convert_input(args, inp)
        create_domain_response = h.create_domain(**command_args)
        format_output('create_domain', create_domain_response)

    def help_create_domain(self):
        print('\nCreate a new domain with the given parameters.')
        print('\n--domain_name=<string> - (required) the domain name associated with the domain to be created')
        print('\n--hosted_zone=<string> - (required) the zone ID of the hosted zone associated with the domain')

    def do_delete_domain(self, inp):
        args = {'domain_name': ''}
        command_args = self.convert_input(args, inp)
        delete_domain_response = h.delete_domain(**command_args)
        format_output('delete_domain', delete_domain_response)

    def help_delete_domain(self):
        print('\nDelete an existing domain.')
        print('\n--domain_name=<string> - (required) the name of the domain to be deleted')

    def do_run_task(self, inp):
        args = {'task_name': '', 'task_type': '', 'task_host_name': '', 'task_domain_name': '', 'portgroups': '',
                'end_time': ''}
        command_args = self.convert_input(args, inp)
        run_task_response = h.run_task(**command_args)
        format_output('run_task', run_task_response)

    def help_run_task(self):
        print('\nRun a ./havoc Attack Container as an ECS task.')
        print('\n--task_name=<string> - (required) a unique identifier to associate with the task')
        print('\n--task_type=<string> - (required) the type of Attack Container to be executed')
        print('\n--task_host_name=<string> - (optional) a host name to associate with the task')
        print('\n--task_domain_name=<string> - (optional) a domain name to associate with the task')
        print('\n--portgroups=<string> - (optional) a list of portgroups to associate with the task')
        print('\n--end_time=<string> - (optional) terminate the task at the given time')

    def do_instruct_task(self, inp):
        args = {'task_name': '', 'instruct_instance': '', 'instruct_command': '', 'instruct_args': ''}
        command_args = self.convert_input(args, inp)
        instruct_task_response = h.instruct_task(**command_args)
        format_output('instruct_task', instruct_task_response)

    def help_instruct_task(self):
        print('\nInteract with a running task.')
        print('\n--task_name=<string> - (required) the name of the task you want to instruct')
        print('\n--instruct_instance=<string> - (required) a unique string to associate with the instruction (defaults '
              'to \'havoc\')')
        print('\n--instruct_command=<string> - (required) the command to send to the task')
        print('\n--instruct_args=<string> - (optional) a dictionary of arguments to pass with the command')

    def do_get_task_results(self, inp):
        args = {'task_name': '', 'instruct_command': '', 'instruct_instance': ''}
        command_args = self.convert_input(args, inp)
        get_task_results_response = h.get_task_results(**command_args)
        if 'queue' not in get_task_results_response:
            format_output('get_task_results', get_task_results_response)
        else:
            instruct_command, instruct_instance = None, None
            if 'instruct_command' in command_args and command_args['instruct_command']:
                instruct_command = command_args['instruct_command']
            if 'instruct_instance' in command_args and command_args['instruct_instance']:
                instruct_instance = command_args['instruct_instance']
            filtered_results = []
            if instruct_command and not instruct_instance:
                for result in get_task_results_response['queue']:
                    if result['instruct_command'] == instruct_command:
                        filtered_results.append(result)
            if instruct_instance and not instruct_command:
                for result in get_task_results_response['queue']:
                    if result['instruct_instance'] == instruct_instance:
                        filtered_results.append(result)
            if instruct_command and instruct_instance:
                for result in get_task_results_response['queue']:
                    if result['instruct_command'] == instruct_command and result[
                        'instruct_instance'] == instruct_instance:
                        filtered_results.append(result)
            del get_task_results_response['queue']
            get_task_results_response['queue'] = filtered_results
            format_output('get_task_results', get_task_results_response)

    def help_get_task_results(self):
        print('\nGet results of an instruct_command.')
        print('\n--task_name=<string> - (required) the name of the task to retrieve results from')
        print('\n--instruct_instance=<string> - (optional) the instruct_instance to retrieve results for')
        print('\n--instruct_command=<string> - (optional) the command to retrieve results for')

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit()

        print("Default: {}".format(inp))

    do_EOF = do_exit
    help_EOF = help_exit

if __name__ == '__main__':

    print('         _ _         _    _  _____   ______ ')
    print('        / | |      \| |  | |/ ___ \ / _____)')
    print('       / /| |__  /  \ |  | | |   | | /      ')
    print('      / / |  __)/ /\ \ \/ /| |   | | |      ')
    print('     / /  | |  / |__| \  / | |___| | \_____ ')
    print('  ()/_/   |_| / ______|\/   \_____/ \______)')


    havoc_cmd = HavocCMD()
    havoc_cmd.cmdloop()
