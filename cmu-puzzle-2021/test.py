from io import TextIOWrapper
from platform import system    # For getting the operating system name
from subprocess import STDOUT, check_output  # For executing a shell command
from datetime import datetime, timedelta
from time import sleep, time
from statistics import fmean, median
from alive_progress import alive_bar
from os.path import isfile
from decimal import Decimal, ROUND_UP


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
        return "10000.000"


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
    start_time = datetime.now()
    future_time = future(duration_in_minutes)
    while future_time > datetime.now():
        for host in hosts:
            output = str(ping_host(host))
            if output != "10000.000":
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
        arithmetic_mean = round(fmean(rtt_values), 3)
        return f"{arithmetic_mean:.3f}ms"
    else:
        # rounds to three decimal places
        arithmetic_median = round(median(rtt_values), 3)
        return f"{arithmetic_median:.3f}ms"


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


def find_avg_rtt(result):
    """ Helper function used in the sorting process.  Returns a decimal """
    rtt = float(result["average_rtt"][:-2])
    rounded_rtt = Decimal(rtt).quantize(Decimal('.001'), rounding=ROUND_UP)
    return rounded_rtt


def get_results(hosts, avg_mean=True, ascending=True, seconds_between=30, duration_in_minutes=1):
    """ needs to accept a list of hosts, a mean/median option, and an order option """
    """ Docstring otherwise needed """
    output_dict = {}
    results = []
    raw_results = ping_hosts(hosts, seconds_between=30, duration_in_minutes=1)
    for host in hosts:
        arranged_results = {
            "host": host,
            "average_rtt": calculate_avg_rtt(find_rtt_values_by_host(host, raw_results), avg_mean),
            "raw_results": arrange_raw_results_by_single_host(raw_results, host)
        }
        results.append(arranged_results)
    if ascending:
        output_dict["results"] = sorted(
            results, reverse=False, key=find_avg_rtt)
        return output_dict
    else:
        output_dict["results"] = sorted(
            results, reverse=True, key=find_avg_rtt)
        return output_dict


hosts = ["npr.org", "cmu.edu", "microsoft.com", "www.facebook.com"]

print(get_results(hosts))
