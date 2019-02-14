#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, datetime, hashlib
import subprocess, shlex, logging
import common

def genlogger():
    # logger settings
    name = os.path.basename(sys.argv[0])
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # formatter
    fmt = "%(asctime)s : %(lineno)d : %(levelname)s : %(message)s"
    fmtr = logging.Formatter(fmt)
    # file handler
    common.gendir(common.LOG_PATH)
    fn = "{}/{}_{}.log".format(common.LOG_PATH, name, common.getdate())
    fh = logging.FileHandler(fn)
    fh.setFormatter(fmtr)
    logger.addHandler(fh)
    # stream handler
    sh = logging.StreamHandler()
    logger.addHandler(sh)
    sh.setFormatter(fmtr)
    return logger

def execmd(cmd, blocking=True):
    p = subprocess.Popen(shlex.split(cmd),
        stderr=subprocess.PIPE, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    if blocking: p.wait()
    return p
