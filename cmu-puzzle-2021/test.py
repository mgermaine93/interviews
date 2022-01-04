from io import TextIOWrapper
from platform import system    # For getting the operating system name
from subprocess import STDOUT, check_output  # For executing a shell command
from datetime import datetime, timedelta
from time import sleep, time
from statistics import fmean, median
from alive_progress import alive_bar
from os.path import isfile

# STILL NEED TO FIX THE TIMEOUT VALUE TO BE REFLECTED IN MILLISECONDS RATHER THAN SECONDS


def ping_host(host):
    """
    This does the actual pinging (one ping) of the host.
    """
    # Option for the number of packets as a function of operating system
    param = '-n' if system().lower() == 'windows' else '-c'
    try:
        output = check_output(['ping', param, '1', host],
                              stderr=STDOUT, timeout=10, universal_newlines=True)
        return output
    except:
        return 10000.000


def future(num_minutes=5):
    """ Returns a time and date five minutes ahead of when the function is run. """
    now = datetime.now()
    minutes_ahead = now + timedelta(minutes=num_minutes)  # will change
    return minutes_ahead


def ping_hosts(hosts, seconds_between=30, duration_in_minutes=1):
    """
    Docstring needed
    """
    results = []
    sequence = 1
    future_time = future(duration_in_minutes)
    start_time = datetime.now()
    while future_time > datetime.now():
        for host in hosts:
            output = str(ping_host(host))
            if output != "10000":
                rtt = str(output.splitlines()[
                    1].split(" ")[6].split("=")[1])
            else:
                rtt = output
            results.append({
                "host": host,
                "seq": sequence,
                "rtt": rtt,
            })
        sequence += 1
        # 30 seconds
        sleep(seconds_between - ((datetime.now().second - start_time.second) % 30.0))
    return results


def arrange_raw_results_by_single_host(results, host):
    """
    Docstring needed
    """
    raw_results = []
    for result in results:
        if result['host'] == host:
            raw_results.append({
                "seq": result["seq"],
                "rtt": result["rtt"]
            })
    return raw_results


def find_rtt_values_by_host(host, results):
    """
    Docstring needed
    """
    rtt_values = []
    for result in results:
        if result['host'] == host:
            rtt_values.append(float(result['rtt']))
    return rtt_values


def calculate_avg_rtt(rtt_values, avg_mean=True):
    """
    Returns the average value from a list of rtt values.

    If the 'avg_mean' conditional is set to true, then the arithmetic mean value will be returned.  Otherwise, the arithmetic median value with be returned.
    """
    if avg_mean:
        # rounds to three decimal places
        return f"{round(fmean(rtt_values), 3)}ms"
    else:
        # rounds to three decimal places
        return f"{round(median(rtt_values), 3)}ms"


def read_hosts(hosts):
    """ Parses out the different hosts from either a file or the command line """
    # might be redundant...
    # checks if the the argument exists and is a valid file
    if type(hosts) is list:
        return hosts
    elif isfile(hosts):
        if isinstance(open(hosts), TextIOWrapper):
            with open(hosts) as f:
                contents = f.readlines()
                cleaned_contents = [line.rstrip('\n') for line in contents]
                return cleaned_contents
        else:
            raise FileNotFoundError(f"No such file or directory: {hosts}")
    else:
        raise TypeError(
            "Can only accept arguments of type TextIOWrapper or list")


def find_avg_rtt(item):
    """
    Needs docstring
    """
    return item["average rtt"]


def get_results(hosts, avg_mean=True, ascending=True, seconds_between=30, duration_in_minutes=1):
    """ needs to accept a list of hosts, a mean/median option, and an order option """
    """ Docstring otherwise needed """
    output_dict = {}
    results = []
    # hosts_to_ping = read_hosts(hosts)
    raw_results = ping_hosts(hosts, seconds_between=30, duration_in_minutes=1)
    # progress bar to show status on script
    with alive_bar(len(raw_results)) as bar:
        for host in hosts:
            arranged_results = {
                "host": host,
                "average_rtt": calculate_avg_rtt(find_rtt_values_by_host(host, raw_results), avg_mean),
                "raw_results": arrange_raw_results_by_single_host(raw_results, host)
            }
            results.append(arranged_results)
            bar()
    if ascending:
        output_dict["results"] = sorted(
            results, reverse=False, key=find_avg_rtt)
        return output_dict
    else:
        output_dict["results"] = sorted(
            results, reverse=True, key=find_avg_rtt)
        return output_dict


hosts = ["npr.org", "cmu.edu", "microsoft.com"]
print(get_results(hosts))

# results = [
#     {'host': 'npr.org', 'seq': 1, 'rtt': '24.812'},
#     {'host': 'cmu.edu', 'seq': 1, 'rtt': '59.458'},
#     {'host': 'microsoft.com', 'seq': 1, 'rtt': '10000'},
#     {'host': 'npr.org', 'seq': 2, 'rtt': '26.401'},
#     {'host': 'cmu.edu', 'seq': 2, 'rtt': '56.126'},
#     {'host': 'microsoft.com', 'seq': 2, 'rtt': '10000'},
#     {'host': 'npr.org', 'seq': 3, 'rtt': '30.048'},
#     {'host': 'cmu.edu', 'seq': 3, 'rtt': '55.963'},
#     {'host': 'microsoft.com', 'seq': 3, 'rtt': '10000'}
# ]


# def track_time():
#     start_time = datetime.now()
#     future_time = future(1)
#     while future_time > start_time:
#         print(f"This is the start time: {start_time}")
#         print(f"This is the current time: {datetime.now()}")
#         print(f"This is the future time: {future_time}")
#         sleep(2)


# print(ping_hosts(hosts))
# print(arrange_raw_results_by_single_host(results=results, host='npr.org'))

# results = str(ping_host(host="cmu.edu"))
# # print(results)
# if results == "10000":
#     avg_milliseconds = results
# else:
#     avg_milliseconds = str(results.splitlines()[1].split(" ")[6].split("=")[1])

# print(avg_milliseconds)
# output = 'PING npr.org (216.35.221.76): 56 data bytes\n64 bytes from 216.35.221.76: icmp_seq=0 ttl=242 time=26.307 ms\n\n--- npr.org ping statistics ---\n1 packets transmitted, 1 packets received, 0.0% packet loss\nround-trip min/avg/max/stddev = 26.307/26.307/26.307/0.000 ms\n'
