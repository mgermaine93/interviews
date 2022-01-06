# CMU Puzzle 2021-2022

## The Problem

Given a list of hosts (i.e. google.com, microsoft.com, cmu.edu...), ping each host every 30 seconds. Capture the results from each ping and after five minutes, write the results out as JSON. The results should be grouped by host name and the groups sorted by the average rtt for the host. You can choose to get the list of hosts from a file or accepted as a command line argument.

It's preferred that you complete this challenge using either Python, Ruby, or Node.JS. Completing it using C, C#, Rust, or Java is also acceptable. Use any resources that you would typically rely on when working on something like this. If you have any questions about completing the challenge, please ask.

## Questions I Asked / Answers I Received

### Question

Are you able to provide an example of the JSON format in which you'd like the results to be returned? I'm imagining you're looking for something like [this](https://gist.githubusercontent.com/mgermaine93/67ee269a73edaa142294a52011448334/raw/1dbdb10c368ed5b43599b0eb2231672995ff0627/sample.json), but wanted to clarify. (Here's another [link](https://gist.github.com/mgermaine93/67ee269a73edaa142294a52011448334) to the same example in case you couldn't access the other one.)

#### Answer

I always like to go with the approach that more is better. My thought is that the details can always be omitted later on if they aren't needed. That being the case, I would include the individual results nested inside of your groupings. Something like this:

```JSON
{
  "results": [
    {
      "host" : "www.google.com",
      "average rtt" : "0.123ms",
      "raw_results" : [
        {
          "seq" : 1,
          "rtt" : "0.234"
        },
        {
          "seq" : 2,
          "rtt" : "0.091"
        },
        {
          "seq" : 3,
          "rtt" : "0.082"
        }
      ]
    },
    {
      "host" : "www.cmu.edu",
      "average rtt" : "0.456ms",
      "raw_results" : [
        ...
      ]
    },
    {
      "host" : "www.microsoft.com",
      "average rtt" : "0.789ms",
      "raw_results" : [
        ...
      ]
    },
    ...
  ]
}
```

### Question

I understand that the results should be grouped by host name and the groups should be sorted by the average RTT for the host, but how would you like the sorting by average RTT time to occur? (E.g., shortest RTT time first, longest RTT times last, or vice versa?)

#### Answer

Why not both? Maybe by default it sorts lowest to highest, but you could take a command-line argument to reverse that order if desired. Similar to how the `journalctl` command on Linux systems allows the logs to be read in reverse chronological order.

## Considerations

- What operating systems should the script support? (Mac, Windows, etc.?)
- How much control should the user have in running the script? (E.g., how many command-line arguments should they be able to provide, and what should each argument do?)
- How should the program accept the list of hosts? (txt file, user-input list, etc.)
- What version of Python should I consider? (subprocess.run() vs. subprocess.call(). etc.)?

## Resources I Used

- https://www.geeksforgeeks.org/difference-between-round-trip-time-rtt-and-time-to-live-ttl/
- https://miguendes.me/how-to-use-datetimetimedelta-in-python-with-examples#how-to-use-timedelta-to-add-minutes-to-a-datetime-object
- https://pypi.org/project/pingparsing/
- https://stackoverflow.com/questions/1191374/using-module-subprocess-with-timeout
- https://stackoverflow.com/questions/184814/is-there-some-industry-standard-for-unacceptable-webapp-response-time
- https://stackoverflow.com/questions/12330522/how-to-read-a-file-without-newlines

## Reflection

Mention the following:

- Having a progress bar, similar to what [Alive-Progress](https://github.com/rsalmei/alive-progress) does.
- General efficiency (e.g., first solution vs. second solution).
- Should timeouts have been included? If not, was the default value I used acceptable? If so, how would that factor into calculating the average? (E.g., discard the timeouts, or somehow include them?)
