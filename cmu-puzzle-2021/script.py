# Given a list of hosts(i.e. google.com, microsoft.com, cmu.edu...), ping each host every 30 seconds.  Capture the results from each ping and after five minutes, write the results out as JSON.  The results should be grouped by host name and the groups sorted by the average rtt for the host.  You can choose to get the list of hosts from a file or accepted as a command line argument.

# figure out how to ping a host
# figure out how to ping a series of hosts
# figure out how to ping hosts on a schedule (every 30 seconds for five minutes)
# figure out how to capture the results of the above pings
# figure out how to parse the results out into JSON


from platform import system    # For getting the operating system name
from subprocess import STDOUT, check_output  # For executing a shell command
from datetime import datetime, timedelta
from time import sleep
from statistics import fmean, median
from alive_progress import alive_bar


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
        return 10


def future(num_minutes=1):
    """ Returns the a time and date five minutes ahead of when the function is run. """
    now = datetime.now()
    five_minutes_ahead = now + timedelta(minutes=num_minutes)  # will change
    return five_minutes_ahead


def get_rtt(host):
    """ This captures the avg rtt value of one ping of one host and returns it as a string """
    output = ping_host(host)
    if output != 10:
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


def get_raw_results(host, seconds_between=30, duration_in_minutes=1):
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
        return fmean(rtt_values)
    else:
        return median(rtt_values)


def get_results_for_single_host(host, avg_mean=True):
    """
    This returns the entire set of results for a single host.

    The arithmetic mean will be the default.  If "avg_mean" is set to False, than the median will be used as the average value rather than the arithmetic mean.
    """
    output = {
        "host": host
    }
    results = get_raw_results(host)
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


def get_results(hosts, avg_mean=True, ascending=True):
    """ needs to accept a list of hosts, a mean/median option, and an order option """
    output_dict = {}
    results = []
    with alive_bar(len(hosts)) as bar:
        for host in hosts:
            print(f"Currently pinging {host}...")
            results.append(
                get_results_for_single_host(host, avg_mean))
            bar()
    print(results)
    # need to make sure that the 'output_dict' dict is updating correctly here.
    # (currently, it is not updating)
    if ascending:
        output_dict["results"] = results.sort(
            reverse=False, key=find_avg_rtt)
        return output_dict
    else:
        output_dict["results"] = results.sort(reverse=True, key=find_avg_rtt)
        return output_dict


hosts = ['google.com', 'cmu.edu', 'doctorofcredit.com']

print(get_results(hosts=hosts))

# ping_host(host='google.edu')

# print(get_raw_results("pnc.com"))


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


# print(main_function(['google.com', 'doctorofcredit.com', 'cmu.edu']))
# hosts = ['harvard.edu', 'google.com', 'pittsburghfoodbank.org', 'doctorofcredit.com']
# get the current time and the time five minutes from now
# begin the 30-second clock
# for each host:
# for each 30-second block:
# ping the host
# capture the rtt (or other results)
# add the sequence number to the json
# add the rtt to the json
# reset the 30 second clock


# floats = [1.234, 5.456, 23.412]

# print(get_mean_rtt(floats))
# print(get_median_rtt(floats))
# five_minutes_ahead = future()
# while datetime.now() < five_minutes_ahead:
#     print(ping(host).split())
#     # every ten seconds
#     sleep(10 - time() % 10)
# return now.timetuple()[5], five_minutes_ahead.timetuple()[5]


# param = '-n' if platform.system().lower() == 'windows' else '-c'
# host = 'google.com'
# output = subprocess.check_output(
#     ['ping', param, '1', host], shell=False, stderr=subprocess.STDOUT, universal_newlines=True)
# avg_rtt = output.splitlines()[5].split(" = ")[1].split("/")[1]
# print(avg_rtt)

# print(output.splitlines()[5])

# for host in hosts:
#     print(ping(host))
# print(ping("wooster.edu"))
# print(expires())
# tick()
# ping("www.google.com")
