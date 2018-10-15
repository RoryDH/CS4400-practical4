# from hashid import HashID

import http.client
import datetime
import subprocess

HASHCAT_EXECUTABLE = "./hashcat"
HISTORY_FILE_NAME = "hashcat_history.txt"

try:
    PUSH_MORE_TOKEN = open("push_more_tokena.txt", "r").read().strip()
except FileNotFoundError as e:
    PUSH_MORE_TOKEN = None
    print("no push_more_token.txt => no telegram notifications")

ALGO_NUMS = [
    "500", # md5
    "1500", # DES
    "1800", # sha512crypt
    "7400", # sha256crypt
    # "10000" # PBKDF2-SHA256
]

# mode -> files
ATTACK_MODE_FILES = {
    0: "rockyou.txt web2.txt eng.txt",
    3: "nating.hcmask",
    # "3 -1 '?l' '?1?1?1?1?1'",
}

# def get_hashcat_algo(h):
#     hashID = HashID()
#     return list(hashID.identifyHash(h))[0].hashcat

def message_telegram(msg):
    connection = http.client.HTTPSConnection('pushmore.io')
    connection.request('POST', "/webhook/" + PUSH_MORE_TOKEN, msg)
    response = connection.getresponse()
    print(response.read().decode())

def log_command(msg):
    print("\n====== sending via webhook ({0} UTC) ======\n".format(str(datetime.datetime.now())))
    print(msg)

    if PUSH_MORE_TOKEN:
        message_telegram(msg)

    print("\n")

def run_hashcat(algo_num, attack_mode, history_to_skip):
    command = "{executable} -m {num} -a {attack_mode} -O -o {num}.broken {num}.hashes {files}".format(
        num=algo_num,
        executable=HASHCAT_EXECUTABLE,
        attack_mode=attack_mode,
        files=ATTACK_MODE_FILES[attack_mode]
    )

    if command in history_to_skip:
        print("in history: " + command + " SKIPPING\n")
        return command

    log_command("starting: " + command)

    return command

    try:
        out, err = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
        return_value = p.wait()
        output = "\n".join([ line.decode('UTF-8') for line in out.splitlines() ])

        log_command("return value: {0}\ncommand output:\n {1}\n".format(return_value, output))
    except subprocess.CalledProcessError as e:
        log_command(e.output)

    return command


def main():
    try:
        commands_history = open(HISTORY_FILE_NAME, "r").read().strip().split("\n")
    except FileNotFoundError as e:
        commands_history = []

    commands_run = []

    for num in ALGO_NUMS:
        for attack in ATTACK_MODE_FILES.keys():
            command = run_hashcat(num, attack, commands_history)
            commands_run.append(command)

    history_file_string = "\n".join(
        [ c for c in commands_run if isinstance(c, str) and c.startswith(HASHCAT_EXECUTABLE) ]
    )

    wr = open(HISTORY_FILE_NAME, 'w')
    wr.write(history_file_string)

if __name__== "__main__":
    main()
