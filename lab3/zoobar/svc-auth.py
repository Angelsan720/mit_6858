#!/usr/bin/python

import sys
import time
import hashlib
import random

from zoodb import *
from debug import *

req = sys.stdin.read()
msgs = req.split("@#")
action = msgs[0]

if action == "checklogin":
    #msgs[1] username      
    #msgs[2] password
    db = auth_setup()
    auth = db.query(Auth).get(msgs[1])
    if auth.password == hashlib.md5(msgs[2] \
                        + auth.salt).hexdigest():
        print "true"
    else:
        print "false"

elif action == "logincookie":
    #msgs[1] username      
    db = auth_setup()
    auth = db.query(Auth).get(msgs[1])
    print hashlib.md5("%s%.10f"\
          % (auth.password, random.random())).hexdigest()

elif action == "checkcookie":
    #msgs[1] = username
    #msgs[2] = token
    db = auth_setup()
    auth = db.query(Auth).get(msgs[1])
    if auth and auth.token == msgs[2]:
        print auth.token
    else:
        print None 

elif action == "register":
    #msgs[1] = username
    #msgs[2] = password
    db = auth_setup()
    newauth = Auth()
    newauth.username = (msgs[1])
    newauth.salt = "%04x" % random.randint(0, 0xffff)
    newauth.password = hashlib.md5(msgs[2] \
                     + newauth.salt).hexdigest()
    newauth.token = hashlib.md5("%s%.10f" \
                    % (newauth.password, random.random())).hexdigest()
    db.add(newauth)
    db.commit()
    print "%s#%s" % (newauth.username, newauth.token)

else:
    raise Exception("unknown action %s" % msgs[0])
