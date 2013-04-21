import sys, time
import os
import json
## We have to do this here, because 'import site' (i.e., omitting -S)
## can sometimes fail, because getpwnam() might fail, and we want to
## avoid requiring a fully-populated passwd file in the chroot jail.
sys.path += ['/usr/lib/pymodules/python2.6']

def parse_kv(argv):
    kv = {}
    for arg in argv:
        pos = arg.find('=')
        if pos < 0:
            continue
        k = arg[:pos]
        v = arg[pos+1:]
        kv[k] = v
    return kv

def get_param(key):
    kv = parse_kv(sys.argv)
 #   log("-------- ARGV = %s" % (sys.argv).__str__() )
    return kv.get(key)

def get_xfers(username):
    fd = os.open('/tmp/xfers#%s'%username, os.O_RDONLY)
    ret = os.read(fd, -1)
    return json.loads(ret)

def get_user(username):
    fd = os.open('/tmp/user#%s'%username, os.O_RDONLY)
    ret = os.read(fd, -2)
    return json.loads(ret)

def xfer(rcptname, zoobars):
    selfname = get_param('ZOOBAR_SELF')
    token = get_param('SELF_TOKEN') 
    fd = os.open('/tmp/xfer#%s#%d#%s#%s'\
            %(rcptname, zoobars, \
            selfname, token), os.O_RDONLY)
    os.read(fd, -3)

