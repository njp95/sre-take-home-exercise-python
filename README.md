# Nick Polsin's submission for the Fetch SRE take home exercise
## Installing and running
1. From the project home directory, start the python venv, and install requirements
   
`python3 -m venv fetch`

`source fetch/bin/activate`

`pip3 install -r requirements.txt` 

2. Run the program from the command line with the provided sample yaml file
`python3 main.py sample.yml`

## Issues identified and changes made
The initial code provided did not account for the 500ms response time, and only output the cumulative availability, rather than availability by domain.
1. The inclusion of `timeout=.5` on line 23 accounts for the timeout condition
2. Lines 25, 28, and 31 are print statements to output the availability including reason for unavailability. This is to address `Must return availability by domain` in the project requirements.

The code did not initially ignore port numbers when determining domain.
1. Lines 15-17 and 41 address this issue to strip the port number from the domain

The code did not initially pass along request headers, method or body. 
1. Lines 18-20 address this

The code did not properly load the request body
1. Lines 4 and 20 utilize the `json` package to pass along the body properly
