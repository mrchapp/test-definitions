#!/usr/bin/python

import argparse
from pysnmp.hlapi import *
import time

CONTROL_OID='.1.3.6.1.4.1.318.1.1.4.4.2.1.3.'
SWITCH={"on": 1, "off": 2}

def send_cmd(hostname, port, cmd):
    print("Turn {} port {} {}".format(hostname, port, cmd))
    oid=CONTROL_OID + str(port)
    errorIndication, errorStatus, errorIndex, varBinds = next(
        setCmd(SnmpEngine(),
               CommunityData('private', mpModel=0),
               UdpTransportTarget((hostname, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid), Integer(SWITCH[cmd])))
    )
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind])) 

def main():
    parser = argparse.ArgumentParser()
#    parser.add_argument("cmnd", help="")
    parser.add_argument("--hostname", help="The pdu you wish to control - e.g. pdu05", required=True)
    parser.add_argument("--port", help="The pdu port you wish to control, e.g. 4 or 15", required=True)
    parser.add_argument("--command", help="What you wish to do with the port 'off', 'on', 'reboot'",
                        required=True, choices=['off', 'on', 'reboot'], default='reboot')
    parser.add_argument("--delay", type=int, default=10,
                        help="Delay in seconds when rebooting between power off and power on (default 10 seconds)")

    args = parser.parse_args()

    if args.command == 'reboot':
        send_cmd(args.hostname, args.port, 'off')
        time.sleep(args.delay)
        send_cmd(args.hostname, args.port, 'on')
    else:
        send_cmd(args.hostname, args.port, args.command)

if __name__ == '__main__':
    main()
