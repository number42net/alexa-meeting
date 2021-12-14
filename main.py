# Copyright 2021 by Martin Miedema ()
# All rights reserved.
# This file is part of the THAPBI Phytophthora ITS1 Classifier Tool (PICT),
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

import subprocess
import logging
import yaml
import requests
import sys

logger = logging.getLogger("Main")

class Config:
    def __init__(self):
        # Open configuration file
        with open('config.yaml', "r") as file:
            self._raw = yaml.safe_load(file)

        # Check if all required fields are present 
        required = ["monkey_access_token", "monkey_secret_token", "monkey_on", "monkey_off"]
        if not all(key in self._raw for key in required):
            logger.critical(
                f"Not all required fields are present in configuration! Required fields are: {required} "
                f"{[key in self._raw for key in required]}"
            )
            exit()
        
        # Set configuration parameters as attributes
        self.processes = self._raw.get("processes",[
            "cpthost.app", 
            "Meeting Center.app", 
            "Microsoft Teams.app"
        ])
        self.log_level = self._raw.get("log_level", 20)
        self.monkey_access_token = self._raw["monkey_access_token"]
        self.monkey_secret_token = self._raw["monkey_secret_token"]
        self.monkey_url = self._raw.get("monkey_url", "https://api-eu.voicemonkey.io/trigger")
        self.monkey_on = self._raw["monkey_on"]
        self.monkey_off = self._raw["monkey_off"]
        self.current_state = False

class Monkey:
    def __init__(self, access_token, secret_token, url):
        self._access_token = access_token
        self._secret_token = secret_token
        self._url = url
        self._monkeys = {}

    def register(self, name, id):
        self._monkeys[name] = id

    def send(self, monkey, message=""):
        if not self._monkeys.get(monkey):
            raise ValueError(f"Unregistered monkey: {monkey}")

        logger.debug(f"Sending Monkey: {self._monkeys[monkey]}")
        params = {
            "access_token": self._access_token,
            "secret_token": self._secret_token,
            "monkey": self._monkeys[monkey],
            "announcement": message
        }

        response = requests.get(self._url, params=params)
        text = response.text.replace('\n', ' ')

        if not response.status_code == 200:
            logger.warning(
                f"Unable to send monkey. Status code: {response.status_code} "
                f"Message: {text}"
            )
        else:
            logger.debug(f"Successfully sent monkey: {text}")

def test_list(line, triggers):
    for i in triggers:
        if i in line:
            # Found a match
            return i
    
    # Nothing found
    return False

def check_processes():
    process = subprocess.Popen(['ps' ,'aux'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)

    line=True           
    while line:
        line = process.stdout.readline().decode("ascii")
        for trigger in conf.processes:
            if trigger in line:
                process.terminate()
                return trigger

    # Nothing found
    process.terminate()
    return False

if __name__ == "__main__":
    # Read configuration file
    conf = Config()

    # Configure logger
    logger_format = logging.Formatter(
        fmt='%(asctime)s %(levelname)s %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S'
    )

    logger.setLevel(conf.log_level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logger_format)
    logger.addHandler(ch)

    # Create Monkey instance and register monkeys
    monkey = Monkey(
        access_token=conf.monkey_access_token,
        secret_token=conf.monkey_secret_token,
        url = conf.monkey_url
    )
    monkey.register("on", conf.monkey_on)
    monkey.register("off", conf.monkey_off)

    logger.info("Starting main loop")
    while True:
        trigger = check_processes()
        if trigger and not conf.current_state == True:
            # We triggered on a process:
            logger.info(f"Triggered on: {trigger}")
            monkey.send("on")
            conf.current_state = True
        elif (not trigger) and conf.current_state == True:
            # Unset do not disturb
            logger.info("No longer triggered")
            monkey.send("off")
            conf.current_state = False
            
    