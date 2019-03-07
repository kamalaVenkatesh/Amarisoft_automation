import paramiko
import fileinput
import os
import json
import sys
import time
import pexpect
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
sys.path.append('../Config/')
import epcconfig
import enbconfig
import ueconfig

class RunTimeError(Exception):
            ROBOT_EXIT_ON_FAILURE = True
