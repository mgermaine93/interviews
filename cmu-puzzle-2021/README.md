# CMU Puzzle 2021-2022

## Table of Contents

- [The Problem](https://github.com/mgermaine93/interviews/tree/master/cmu-puzzle-2021#the-problem)
- [Questions I Asked / Answers I Received](https://github.com/mgermaine93/interviews/tree/master/cmu-puzzle-2021#questions-i-asked--answers-i-received)
- [Considerations](https://github.com/mgermaine93/interviews/tree/master/cmu-puzzle-2021#considerations)
- [Resources I Used](https://github.com/mgermaine93/interviews/tree/master/cmu-puzzle-2021#resources-i-used)
- [Reflection](https://github.com/mgermaine93/interviews/tree/master/cmu-puzzle-2021#reflection)
- [Explanation of Files](https://github.com/mgermaine93/interviews/tree/master/cmu-puzzle-2021#explanation-of-files)

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

The following are thoughts that I had during the process of addressing this coding prompt:

- What operating systems should the script support? (Mac, Windows, etc.?)

I chose to support as many operating systems as I could. I wrote this code on a Mac, but I would be interested to verify whether or not it worked on other operating systems as written.

- How much control should the user have in running the script? (E.g., how many command-line arguments should they be able to provide, and what should each argument do?)

I tried to give the user a lot of control over how the end program would function. In doing so, the main program (as written) accepts a number of arguments, but only one argument does not have a default value, which is the list of hosts itself.

For example, since the coding prompt stated to have the program ping each host every 30 seconds for a total of five minutes, I set these values as defaults accordingly in the appropriate places. However, the user should be able to alter these values to ping each host every `x` seconds for a total of `y` minutes as they see fit.

To address one of the Q/A points above, I also included an option that enables the user to choose how the end results are sorted -- either by ascending or descending `average_rtt` value.

In my opinion, these choices made the program more flexible. If the extra control over the program isn't needed, it can be removed.

- How should the program accept the list of hosts? (.txt file, user-input list, etc.)

Similar to the above point, I decided to have the program accept its list of hosts as either a .txt file or a command-line list in order to provide the user with more control.

## Resources I Used

The following are some key links and resources I consulted while addressing this prompt:

- https://www.geeksforgeeks.org/difference-between-round-trip-time-rtt-and-time-to-live-ttl/
- https://miguendes.me/how-to-use-datetimetimedelta-in-python-with-examples#how-to-use-timedelta-to-add-minutes-to-a-datetime-object
- https://pypi.org/project/pingparsing/
- https://stackoverflow.com/questions/1191374/using-module-subprocess-with-timeout
- https://stackoverflow.com/questions/184814/is-there-some-industry-standard-for-unacceptable-webapp-response-time
- https://stackoverflow.com/questions/12330522/how-to-read-a-file-without-newlines

## Reflection

Overall, I thought this was a great challenge. It provided a valuable opportunity to put what I know to use, and also enabled me to learn a variety of new skills along the way.

I chose to write this solution in Python, since it is the language with which I am most familiar. Python also has the benefit of many libraries and modules, and I used many of them in this solution. I did my best to include detailed docstrings for each function definition so that it is clear to the reader/user what the code is doing.

One thing I regret not including in this solution is a progress bar of some kind to inform the user that the program is indeed running. Given more time, I would have worked to include something like [Alive-Progress](https://github.com/rsalmei/alive-progress) in order to give real-time progress to the user. I feel that adding this feature would enhance the user experience more so than just having a blank CLI for five minutes (or however long the user chose to run the program).

I also discovered the [PingParsing](https://pypi.org/project/pingparsing/) library, which likely would have been of great assistance in addressing this coding prompt. However, I chose not to use it in the end because it is not something I was familiar with prior to working on this project, and I wanted to emulate the feel of a "whiteboard"-type problem as close as possible. In other words, it was a conscious decision I made to demonstrate what I already knew over what I may have learned during this project.

On a different, but related, note, PingParsing also requires Python 3.6, and I wasn't sure what version of Python I should have in mind as I designed my solution. Given that not using PingParsing freed up my program to (ideally) run on versions of Python older than 3.6, I feel this was a knowledgeable decision.

Another thing I needed to figure out was what to do in the event of a ping timeout. One option I considered was to just throw away the ping `seq` that timed out and either move on or try pinging the host again. However, I opted to set a default timeout value so that, if the ping timed out on or after that value, than the `rtt` value would automatically be set to that value and the program would move on to the next iteration. In deciding what this value should be, I found this [link](https://stackoverflow.com/questions/184814/is-there-some-industry-standard-for-unacceptable-webapp-response-time) to be quite helpful.

Had Python not been an option in which to code this solution, I would have used JavaScript because I am currently more familiar with JavaScript than the other languages listed in the prompt.

Lastly, given more time, I would have written a series of unit tests to verify that the code works as expected. I likely would have done this using the [unittest](https://docs.python.org/3/library/unittest.html) module or the [pytest](https://docs.pytest.org/) tool.

## Explanation of Files

- [sample_hosts.txt](https://github.com/mgermaine93/interviews/blob/master/cmu-puzzle-2021/sample_hosts.txt) is a text file of hosts. I used this file to test that my solution could accept a .txt file as an argument.
- [sample_output.json](https://github.com/mgermaine93/interviews/blob/master/cmu-puzzle-2021/sample_output.json) is the output that is printed out to the command line when the [solution.py](https://github.com/mgermaine93/interviews/blob/master/cmu-puzzle-2021/solution.py) file is run as written.
- [solution.py](https://github.com/mgermaine93/interviews/blob/master/cmu-puzzle-2021/solution.py) is the Python code I wrote to solve the coding prompt.
