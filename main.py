# from hashid import HashID

import http.client
import datetime
import subprocess

HASHCAT_COMMANDS = "hashcat_commands.txt"

try:
    PUSH_MORE_TOKEN = open("push_more_tokena.txt", "r").read().strip()
except FileNotFoundError as e:
    PUSH_MORE_TOKEN = None
    print("no push_more_token.txt => no telegram notifications")

def message_telegram(msg):
    connection = http.client.HTTPSConnection('pushmore.io')
    connection.request('POST', "/webhook/" + PUSH_MORE_TOKEN, msg)
    response = connection.getresponse()
    print(response.read().decode())

def log_message(msg):
    print("\n====== sending via webhook ({0} UTC) ======\n".format(str(datetime.datetime.now())))
    print(msg)

    if PUSH_MORE_TOKEN:
        message_telegram(msg)

    print("\n")

def run_command(command):
    log_message("starting: " + command)

    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = process.communicate()
        return_value = process.wait()
        output = "\n".join([ line.decode('UTF-8') for line in out.splitlines() ])

        log_message("return value: {0}\ncommand output:\n {1}\n".format(return_value, output))
    except subprocess.CalledProcessError as e:
        log_message(e.output)

    return command


def main():
    try:
        commands = open(HISTORY_FILE_NAME, "r").read().strip().split("\n")
    except FileNotFoundError as e:
        print("no commands file named " + HASHCAT_COMMANDS)
        return 1

    commands_run = []

    for command in commands:
        command = run_command(command)
        commands_run.append(command)

    return 0

if __name__== "__main__":
    main()
