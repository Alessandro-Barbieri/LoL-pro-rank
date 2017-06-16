#!/usr/bin/env python3
from subprocess import Popen, PIPE

log = print
log("Launch slave process...")
with Popen(['ruby', 'slave.rb'], stdin=PIPE, stdout=PIPE, 
           universal_newlines=True) as ruby:
    while True:
        line = input("Enter expression or exit:")
        # send request
        print(line, file=ruby.stdin, flush=True)
        # read reply
        result = []
        for line in ruby.stdout:
            line = line.rstrip('\n')
            if line == "[end]":
                break
            result.append(line)
        else: # no break, EOF
            log("Slave has terminated.")
            break
        log("result:" + "\n".join(result))
