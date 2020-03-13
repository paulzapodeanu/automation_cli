#!/home/paulz/scripts/automation_cli/bin/python

import netmiko
import json
import sys
import signal

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  #IOError, broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  #Keyboard interrupt Ctrl+C

if len(sys.argv) < 4:
    print('Usage: cmdrunner.py devices.json credentials.json commands.txt')
    exit()
#Read device list
with open (sys.argv[1]) as devices_file:
    devices = json.load(devices_file)
print ('*'*80)
print ('{:^80s}'.format('**********DEVICES**********')) ###########################
print ('*'*80)
print (devices) ###################
#Read credentials
with open (sys.argv[2]) as credentials_file:
    credentials = json.load(credentials_file)
#Append cerdentials
for device in devices:
    device['username']=credentials[0]['username']
    device['password']=credentials[0]['password']
#Read commands
commands=[]
with open (sys.argv[3]) as commands_file:
    commands=commands_file.readlines()
print ('*'*80)
print ('{:^80s}'.format('**********COMMANDS**********')) ###########################
print ('*'*80)
print (commands)#####################

def execute_diagnostic_list(devices:list, commands:list)->str:
    for device in devices:
        try:
            print ('*' *80)
            print ('Connecting to device: ', device['ip'])
            connection=netmiko.ConnectHandler(**device)
            print ('Connected!')
            for command in commands:
                print ('Executing command:"', command, '" on device: ', device['ip'])
                output=connection.send_command(command)
                print (output)
            connection.disconnect()
        except netmiko.NetMikoAuthenticationException:
            print ('Auth fail for:', device['ip'])
        except netmiko.NetMikoTimeoutException:
            print ('Conn timeout for:', device['ip'])

execute_diagnostic_list(devices, commands)
