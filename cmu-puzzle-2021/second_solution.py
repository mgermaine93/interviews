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
    """Pings a single host and returns the results of the ping.

    Args:
        host (str) : the host to ping, e.g. "cmu.edu".
    Returns:
        output (str) : the results of the ping to the given host.
    """
    # Option for the number of packets as a function of operating system
    param = '-n' if system().lower() == 'windows' else '-c'
    try:
        output = check_output(['ping', param, '1', host],
                              stderr=STDOUT, timeout=10, universal_newlines=True)
        return str(output)
    except:
        return "10000.000"


def future(num_minutes=5):
    """Calculates a time/date x minutes in the future.

    Args:
        num_minutes (int) : the number of minutes to be added to the current time.
        (The default value is 5 unless otherwise specified.)

    Returns:
        minutes_ahead (datetime.datetime) : a datetime x minutes ahead of the current time.

    """
    now = datetime.now()
    minutes_ahead = now + timedelta(minutes=num_minutes)  # will change
    return minutes_ahead


def ping_hosts(hosts, seconds_between=30, duration_in_minutes=1):
    """Pings a user-input list of hosts over every x seconds over the course of y minutes and returns the results.

    Args:

        hosts (list) : a list of hosts, where each host is of type string, e.g. `['google.com', 'microsoft.com', 'cmu.edu']`.
        seconds_between (int) : the amount of time, in seconds, that should occur in-between pings to a host (default value is 30).
        duration_in_minutes (int) : the amount of time, in minutes, that should elapse before the results are returned (default value is 5).

    Returns:

        results (list) : a list of dictionaries.  Each dictionary appears like so:
            {
                'host' : the host that was pinged (str),
                'seq' : a number in a sequence of how many times the host will be pinged (int),
                'rtt' : the round-trip-time of the ping, in milliseconds, rounded to the nearest thousandths place (str)
            }

        If the ping of a given host takes ten seconds or longer, than the rtt value will be '10000.000'.

        The results are returned ordered sequence first, than by the order in which hosts were entered in the 'hosts' argument.  E.g., for a 'hosts' argument of ['npr.org', 'cmu.edu'], the results would appear as follows:

            [
                {'host': 'npr.org', 'seq': 1, 'rtt': '21.658'}, 
                {'host': 'cmu.edu', 'seq': 1, 'rtt': '56.592'}, 
                {'host': 'npr.org', 'seq': 2, 'rtt': '38.629'}, 
                {'host': 'cmu.edu', 'seq': 2, 'rtt': '19.624'},
                etc...
            ]

    Raises:
        TypeError : if hosts is not of type list.

    """
    if isinstance(hosts, list):
        results = []
        sequence = 1
        start_time = datetime.now()
        future_time = future(duration_in_minutes)
        while future_time > datetime.now():
            for host in hosts:
                # output = str(ping_host(host))
                output = ping_host(host)
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
            sleep(seconds_between -
                  ((datetime.now().second - start_time.second) % 30.0))
        return results
    else:
        raise TypeError(
            f"The 'hosts' argument needs to be of type list, but is of type {type(hosts)}")


def arrange_raw_results_by_single_host(results, host):
    """Filters out the returned value of ping_hosts() function to retrieve the 'seq' and 'rtt' values pertaining to a user-input host.

    Args:

        results (list) : a list of dictionaries containing the following key/value pairs:
            {
                'host' : the host that was pinged (str),
                'seq' : a number in a sequence of how many times the host will be pinged (int),
                'rtt' : the round-trip-time of the ping, in milliseconds, rounded to the nearest thousandths place (str)
            }
        host (str) : the host for which you want to find the 'seq' and 'rtt' values.

    Returns:

        raw_results (list) : a list of dictionaries containing the following key/value pairs specific to the 'host' argument:
            {
                'seq' : a number in a sequence of how many times the host will be pinged (int),
                'rtt' : the round-trip-time of the ping, in milliseconds, rounded to the nearest thousandths place (str)
            }

        If no results are found matching the 'host' argument, an empty list will be returned.

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
    """Docstring needed."""
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
results = [{'host': 'npr.org', 'seq': 1, 'rtt': '21.658'}, {'host': 'cmu.edu', 'seq': 1, 'rtt': '56.592'}, {'host': 'microsoft.com', 'seq': 1, 'rtt': '10000.000'}, {'host': 'www.facebook.com', 'seq': 1, 'rtt': '17.555'}, {
    'host': 'npr.org', 'seq': 2, 'rtt': '10000.000'}, {'host': 'cmu.edu', 'seq': 2, 'rtt': '10000.000'}, {'host': 'microsoft.com', 'seq': 2, 'rtt': '10000.000'}, {'host': 'www.facebook.com', 'seq': 2, 'rtt': '19.624'}]
# print(type(ping_host("doctorofcredit.com")))
# print(ping_hosts(hosts))
print(arrange_raw_results_by_single_host(host='blah.org', results=results))
