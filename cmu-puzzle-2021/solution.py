from io import TextIOWrapper
from platform import system    # For getting the operating system name
from subprocess import STDOUT, check_output  # For executing a shell command
from datetime import datetime, timedelta
from time import sleep
from statistics import fmean, median
from os.path import isfile
from decimal import Decimal, ROUND_UP
import json


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


def ping_hosts(hosts, seconds_between=30, duration_in_minutes=5):
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
        future_time = future(duration_in_minutes=duration_in_minutes)
        while future_time > datetime.now():
            for host in hosts:
                output = ping_host(host=host)
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


def find_rtt_values_by_host(host, ping_results):
    """Accepts the output of the 'ping_hosts' function (list) and filters out the rtt_values corresponding to a single user-input host.

    Args:
        host (str) : a single host, e.g. 'npr.org'.
        ping_results (list) : a list of dictionaries, each with 'host', 'seq', and 'rtt' keys and corresponding values.  This is similar to what the 'ping_hosts()' function outputs, like so:

            [
                {'host': 'npr.org', 'seq': 1, 'rtt': '21.658'}, 
                {'host': 'cmu.edu', 'seq': 1, 'rtt': '56.592'}, 
                {'host': 'npr.org', 'seq': 2, 'rtt': '38.629'}, 
                {'host': 'cmu.edu', 'seq': 2, 'rtt': '19.624'},
                etc...
            ]

    Returns:
        rtt_values (list) : a list of floats, with each float representing the rtt value of a single ping to the user-input host.

    """
    rtt_values = []
    for result in ping_results:
        if result['host'] == host:
            rtt_values.append(float(result['rtt']))
    return rtt_values


def calculate_avg_rtt(rtt_values, avg_mean=True):
    """Calculates the average value from a list of rtt values, rounded to three decimal places.

    Args:
        rtt_values (list) : a list of floats, each representing an rtt value in milliseconds.
        avg_mean (bool) : sets the type of average value to be returned.  If set to 'True', then the arithmetic mean will be returned.  If set to 'False', then the arithmetic median will be returned.  The default value is 'True'.

    Returns:
        The arithmetic mean or median, rounded to three decimal places, as a string and appended with "ms" to represent the units in milliseconds.

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
    """A helper function that parses out host names from either a .txt file or a list entered from the command line.

    Args:
        hosts (str or list) : a series of hosts (e.g., google.com, cmu.edu, etc.).  Must be in the form of a .txt file or a list.

    Returns:
        A list containing a series of hosts to ping.

    Raises:
        FileNotFoundError : If the file passed in is not found or is not valid.
        TypeError : If the 'hosts' value passed in is not of type str or list.

    """
    # checks if the argument exists AND if it is a valid file
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
    """A helper function used in the sorting process of the main 'get_results' function.  Returns the value (of type decimal) associated with the 'avg_rtt' key found in a series of formatted ping results from a single hosts.

    Args:
        result (dict) : a formatted set of ping results from a single hosts, e.g.:

            {
                "host": "npr.org",
                "average_rtt": "25.273ms",
                "raw_results": [
                    {
                        "seq": 1,
                        "rtt": "21.466"
                    },
                    {
                        "seq": 2,
                        "rtt": "29.081"
                    }
                ]
            }

    Returns:
        rounded_rtt (decimal) : the value corresponding to the 'avg_rtt' key in the results, but of type decimal and without the 'ms' units at the end.

    """
    rtt = float(result["average_rtt"][:-2])
    rounded_rtt = Decimal(rtt).quantize(Decimal('.001'), rounding=ROUND_UP)
    return rounded_rtt


def get_results(hosts, avg_mean=True, ascending=True, seconds_between=30, duration_in_minutes=5):
    """The main function to be run.  It does the following:
        * Pings each host in 'hosts' every 'x' seconds for a total of 'y' minutes.
        * Returns the results as JSON data.  The data is grouped by host name, with each group sorted by the average rtt for the host.

    Args:
        hosts (str or list) : a series of hosts (e.g., google.com, cmu.edu, etc.).  Must be in the form of a .txt file or a list.
        avg_mean (bool) : sets the type of average value to be returned.  If set to 'True', then the arithmetic mean will be returned.  If set to 'False', then the arithmetic median will be returned.  The default value is 'True'.
        ascending (bool) : sorts the results by each host's 'avg_rtt' value.  If set to 'True', the results are sorted from lowest to highest, i.e., smaller rtt values to larger rtt values.  If set to 'False', the results are sorted from highest to lower rtt values.  Default value is 'True'.
        seconds_between (int) : the amount of time, in seconds, that should occur in-between pings to a host (default value is 30).
        duration_in_minutes (int) : the amount of time, in minutes, that should elapse before the results are returned (default value is 5).

    Returns:
        output_dict (json) : JSON data representing the full set of results from pinging each host every 'x' seconds over the course of 'y' minutes.  The data is grouped by host name, with each group sorted by the average rtt for the host.

    """
    output_dict = {}
    results = []
    list_of_hosts = read_hosts(hosts)
    ping_results = ping_hosts(
        hosts=list_of_hosts,
        seconds_between=seconds_between,
        duration_in_minutes=duration_in_minutes
    )
    for host in list_of_hosts:
        arranged_results = {
            "host": host,
            "average_rtt": calculate_avg_rtt(find_rtt_values_by_host(host, ping_results), avg_mean),
            "raw_results": arrange_raw_results_by_single_host(ping_results, host)
        }
        results.append(arranged_results)
    if ascending:
        output_dict["results"] = sorted(
            results, reverse=False, key=find_avg_rtt)
        return json.dumps(output_dict)
    else:
        output_dict["results"] = sorted(
            results, reverse=True, key=find_avg_rtt)
        return json.dumps(output_dict)


# enter the hosts that you want to ping here
hosts = ["npr.org", "cmu.edu", "microsoft.com", "www.facebook.com"]

# this will print out the results to the command line once you run this file.
print(get_results(hosts=hosts))
