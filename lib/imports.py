import paramiko
import fileinput
import os
import json
import sys
import time
import pexpect
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
sys.path.append('../config/')
import config

class RunTimeError(Exception):
            ROBOT_EXIT_ON_FAILURE = True
