#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, datetime, hashlib
from os.path import join, dirname
from dotenv import load_dotenv
import subprocess, shlex, logging

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

HOME_PATH = os.environ.get('HOME_PATH')
LOG_PATH = "{}/log".format(HOME_PATH)
TMP_PATH = "{}/tmp".format(HOME_PATH)
BAG_PATH = "{}/bag".format(HOME_PATH)
BAG_PREFIX = "autologger"


def normpath(path):
    return os.path.normpath(os.path.expanduser(path))

def gendir(path):
    if not os.path.exists(path): os.makedirs(path)

def getdate(ns=False):
    fmt = "%Y-%m-%d-%H-%M-%S"
    fmt = fmt + "-%f" if ns else fmt    # add nsec
    return datetime.datetime.now().strftime(fmt)
