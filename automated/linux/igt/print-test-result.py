#!/usr/bin/python
import argparse
import sys
import json


def print_result(results):
    try:
        for test, content in results['tests'].iteritems():
            print '************************************************************************************************************************************'
            print '%-15s %s' % ('Test:', test)
            print '%-15s %s' % ('Result:', content['result'])
            print '%-15s %s' % ('Command:', content['command'])
            print '%-15s %s' % ('Environment:', content['environment'])
            print '%-15s %s' % ('Returncode:', content['returncode'])
            print '%-15s %s' % ('Stdout:', content['out'].replace('\n', '\n                '))
            print '%-15s %s' % ('Stderr:', content['err'].replace('\n', '\n                '))
            print '%-15s %s' % ('dmesg:', content['dmesg'].replace('\n', '\n                '))
    except:
        print "Can not find required data"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",
                        "--json-file",
                        nargs='?',
                        default=sys.stdin,
                        type=argparse.FileType('r'),
                        help="Test result file in json format")

    args = parser.parse_args()
    with args.json_file as data:
        results = json.load(data)

    print_result(results)


