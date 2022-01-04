# Given a list of hosts(i.e. google.com, microsoft.com, cmu.edu...), ping each host every 30 seconds.  Capture the results from each ping and after five minutes, write the results out as JSON.  The results should be grouped by host name and the groups sorted by the average rtt for the host.  You can choose to get the list of hosts from a file or accepted as a command line argument.

# figure out how to ping a host
# figure out how to ping a series of hosts
# figure out how to ping hosts on a schedule (every 30 seconds for five minutes)
# figure out how to capture the results of the above pings
# figure out how to parse the results out into JSON


from io import TextIOWrapper
from platform import system    # For getting the operating system name
from subprocess import STDOUT, check_output  # For executing a shell command
from datetime import datetime, timedelta
from time import sleep
from statistics import fmean, median
from alive_progress import alive_bar
from os.path import isfile


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
        return 10000


def future(num_minutes=5):
    """ Returns the a time and date five minutes ahead of when the function is run. """
    now = datetime.now()
    five_minutes_ahead = now + timedelta(minutes=num_minutes)  # will change
    return five_minutes_ahead


def get_rtt(host):
    """ This captures the avg rtt value of one ping of one host and returns it as a string """
    output = ping_host(host)
    if output != 10000:
        try:
            # this parsing can likely be done better (regex?)
            avg_rtt = output.splitlines()[5].split(" = ")[1].split("/")[1]
            return str(avg_rtt)
        except Exception as e:
            return e
    else:
        return str(output)


def get_raw_result(host, sequence):
    """ Docstring needed """
    return {
        "seq": sequence,
        "rtt": get_rtt(host)
    }


def get_raw_results(host, seconds_between=30, duration_in_minutes=5):
    """ Docstring needed """
    raw_results = []
    sequence = 1
    future_time = future(duration_in_minutes)
    while future_time > datetime.now():
        # get_rtt has ping_host built-in
        raw_results.append(get_raw_result(host, sequence))
        sequence += 1
        sleep(seconds_between)  # 30 seconds
    return raw_results


def get_avg_rtt(rtt_values, avg_mean=True):
    """
    Returns the average value from a list of rtt values.

    If the 'avg_mean' conditional is set to true, then the arithmetic mean value will be returned.  Otherwise, the arithmetic median value with be returned.

    """
    if avg_mean:
        # rounds to three decimal places
        return round(fmean(rtt_values), 3)
    else:
        # rounds to three decimal places
        return round(median(rtt_values), 3)


def get_results_for_single_host(host, avg_mean=True, seconds_between=30, duration_in_minutes=5):
    """
    This returns the entire set of results for a single host.

    The arithmetic mean will be the default.  If "avg_mean" is set to False, than the median will be used as the average value rather than the arithmetic mean.
    """
    output = {
        "host": host
    }
    results = get_raw_results(host, seconds_between, duration_in_minutes)
    # results = [{'seq': 1, 'rtt': '28.727'}, {'seq': 2, 'rtt': '18.751'}]
    avg_rtt = get_avg_rtt([float(item['rtt']) for item in results], avg_mean)
    output["avg_rtt"] = f"{avg_rtt}ms"
    output["raw_results"] = results
    return output


def find_avg_rtt(group):
    """ Docstring needed """
    # omits the "ms" from the end so that the string can be converted into a float
    rtt_value = group['avg_rtt']
    return float(rtt_value[:-2])


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


def get_results(hosts, avg_mean=True, ascending=True, seconds_between=30, duration_in_minutes=5):
    """ needs to accept a list of hosts, a mean/median option, and an order option """
    """ Docstring otherwise needed """
    output_dict = {}
    results = []
    hosts_to_ping = read_hosts(hosts)
    # progress bar to show status on script
    with alive_bar(len(hosts)) as bar:
        for host in hosts_to_ping:
            print(f"Currently pinging {host}...")
            results.append(
                get_results_for_single_host(host, avg_mean, seconds_between, duration_in_minutes))
            bar()
    if ascending:
        output_dict["results"] = sorted(
            results, reverse=False, key=find_avg_rtt)
        return output_dict
    else:
        output_dict["results"] = sorted(
            results, reverse=True, key=find_avg_rtt)
        return output_dict


# print(read_hosts(['google.com', 'cmu.edu', 'doctorofcredit.com']))
# hosts = ['google.com', 'cmu.edu', 'doctorofcredit.com']
print(get_results('sample_hosts.txt'))


# print(get_results(hosts=hosts))
# print(get_avg_rtt([1, 2, 3, 4, 5.095943845, 6]))

# SAMPLE OUTPUT:
#
#   "results": [
#     {
#       "host" : "www.google.com",
#       "average rtt" : "0.123ms",
#       "raw_results" : [
#         {
#           "seq" : 1,
#           "rtt" : "0.234"
#         },
#         {
#           "seq" : 2,
#           "rtt" : "0.091"
#         },
#         {
#           "seq" : 3,
#           "rtt" : "0.082"
#         }
#       ]
#     },
