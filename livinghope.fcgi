#!/home3/onelivi2/python27/bin/python27
import sys, os

sys.path.insert(0,"/home3/onelivi2/python27")
sys.path.insert(13, "/home3/onelivi2/livinghope")

os.environ['DJANGO_SETTINGS_MODULE'] = 'livinghope_proj.settings'
from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")