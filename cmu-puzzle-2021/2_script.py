
def sorting(results, ascending=True):
    output_dict = {}
    if ascending:
        output_dict["results"] = sorted(results, reverse=False)
        return output_dict
    else:
        output_dict["results"] = sorted(results, reverse=True)
        return output_dict


cars = ['Ford', 'BMW', 'Volvo']
cars.sort()
print(cars)
res = [1, 4, 5, 7, 8, 1]
res.sort()
print(res)
print(sorting([1, 6, 71, 906, 14, 5]))

# import platform    # For getting the operating system name
# from subprocess import STDOUT, check_output  # For executing a shell command


# def ping_host(host):
#     """
#     This does the actual pinging (one ping) of the host.
#     """
#     # Option for the number of packets as a function of operating system
#     param = '-n' if platform.system().lower() == 'windows' else '-c'
#     try:
#         output = check_output(['ping', param, '1', host],
#                               stderr=STDOUT, timeout=10, universal_newlines=True)
#         return output
#     except:
#         return 10


# print(ping_host('wooster.edu'))

# # import subprocess  # For executing a shell command
# # num = '22.896ms'
# # print(num[:-2])


# # # import platform    # For getting the operating system name
# # # import os
# # # from datetime import datetime, timedelta
# # # from time import time, ctime, sleep
# # # import requests

# # # ping_output = subprocess.check_output(['ping', '-c', '1', 'google.com'])
# # # print(ping_output.splitlines())

# # # def ping_host(host):
# # #     """
# # #     This does the actual pinging (one ping) of the host.
# # #     """
# # #     # Option for the number of packets as a function of operating system
# # #     param = '-n' if platform.system().lower() == 'windows' else '-c'
# # #     # # Building the command. Ex: "ping -c 1 google.com"
# # #     # Builds the command:
# # #     # "ping" is the bash command to be run.
# # #     # "param" is the parameter that depends on the OS used.
# # #     # "1" is how many times to execute the command
# # #     # "host" is/are the host(s) to ping
# # #     output = subprocess.check_output(
# # #         ['ping', param, '1', host], shell=False, stderr=subprocess.STDOUT, universal_newlines=True)
# # #     # command = ['ping', param, '1', host]
# # #     # output = subprocess.run(command)
# # #     return output
# # #     # starttime = time.time()
# # #     # while True:
# # #     #     print("tick")
# # #     #     time.sleep(30.0 - ((time.time() - starttime) % 30.0))
