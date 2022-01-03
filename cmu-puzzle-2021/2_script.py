# import platform    # For getting the operating system name
# import subprocess  # For executing a shell command
# import os
# from datetime import datetime, timedelta
# from time import time, ctime, sleep
# import requests


def myFunc(result):
    return result["average_rtt"]


results = [
    {
        "host": "www.google.com",
        "average_rtt": "0.123ms",
        "raw_results": []
    },
    {
        "host": "www.cmu.edu",
        "average_rtt": "1.234",
        "raw_results": []
    },
    {
        "host": "www.doctorofcredit.com",
        "average_rtt": "2.345",
        "raw_results": []
    }
]

results.sort(reverse=True, key=myFunc)

print(results)

# def ping_host(host):
#     """
#     This does the actual pinging (one ping) of the host.
#     """
#     # Option for the number of packets as a function of operating system
#     param = '-n' if platform.system().lower() == 'windows' else '-c'
#     # # Building the command. Ex: "ping -c 1 google.com"
#     # Builds the command:
#     # "ping" is the bash command to be run.
#     # "param" is the parameter that depends on the OS used.
#     # "1" is how many times to execute the command
#     # "host" is/are the host(s) to ping
#     output = subprocess.check_output(
#         ['ping', param, '1', host], shell=False, stderr=subprocess.STDOUT, universal_newlines=True)
#     # command = ['ping', param, '1', host]
#     # output = subprocess.run(command)
#     return output
#     # starttime = time.time()
#     # while True:
#     #     print("tick")
#     #     time.sleep(30.0 - ((time.time() - starttime) % 30.0))
