<!-- Hey Matt,

Thanks for reaching out.  Good questions, and the answers are actually quite simple: It's up to you.  :-)

Part of this is seeing what decisions you make in the absence of certain specifics.  Since you did reach out, and it is the holiday season, I'll give you a couple hints/tips.

The data structure: I always like to go with the approach that more is better.  My thought is that the details can always be omitted later on if they aren't needed.  That being the case, I would include the individual results nested inside of your groupings.  Something like this:
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
Sorting: Why not both?  Maybe by default it sorts lowest to highest, but you could take a command-line argument to reverse that order if desired.  Similar to how the journalctl command on Linux systems allows the logs to be read in reverse chronological order.
Hopefully this helps, and I'm looking forward to seeing what you come up with.

Good luck and happy holidays! -->
