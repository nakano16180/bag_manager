#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, datetime, hashlib
import subprocess, shlex, logging

HOME_PATH = os.path.expanduser("~/autologger")
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
