#!/usr/bin/env python3

import argparse
from collections import namedtuple
import logging
import os
import requests
import sys
import http.client
import json

API_TOKEN_ENVVAR = 'METERIAN_API_TOKEN'

TIMEOUT = namedtuple('literal', 'text status_code')(text='{"status":"timeout"}', status_code=999)

LANGUAGES = [ 'java', 'javascript', 'nodejs', 'python', 'dotnet', 'ruby', 'scala', 'php', 'swift', 'golang', 'rust', 'erlang', 'perl', 'linux', 'cpp', 'r']


class HelpingParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.stderr.write('\n')
        sys.exit(-1)


def _logHttpRequests():
    http.client.HTTPConnection.debuglevel = 1

    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

    logging.debug('Full debug log for HTTP requests enabled')

def _parseArgs():
    parser = HelpingParser()

    parser.add_argument('language', help='The language of the library\n (i.e. nodejs) %s' % LANGUAGES)
    parser.add_argument('name', help='The full name of the library\n (i.e. axios)')
    parser.add_argument('version', help='The version of the library\n (i.e. 1.7.6 or 0 if unknown)')

    token = os.environ[API_TOKEN_ENVVAR] if API_TOKEN_ENVVAR in os.environ else None
    parser.add_argument(
        '-t',
        '--token',
        metavar='API-TOKEN',
        default=token,
        help=(
            'Allows you to specify the API token to use directly on the command line. '
            'You can create your token with a bootstrap+ plan at https://meterian.com/account/#tokens'
        )
    )

    parser.add_argument(
        '-l',
        '--log',
        default='warning',
        metavar='LOGLEVEL',
        help='Sets the logging level (default is warning)'
    )

    return parser.parse_args()


def _initLogging(args):
    levels = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }
    level = levels.get(args.log.lower())
    if level is None:
        raise ValueError('Invalid log level requested - must be in '+levels.keys())

    logging.basicConfig(level=level)
    logging.basicConfig(format='%(time)s-%(levelname)s-%(message)s')

    if level == logging.DEBUG:
        _logHttpRequests()
    else:
        logging.getLogger('requests').setLevel(logging.WARNING)

    logging.debug('Logging initiated')


def _loadCopyright(args):

    url = 'https://www.meterian.com/api/v1/licenses/library/%s/%s/%s/copyright?useCache=false' % (args.language, args.name.replace("/", "|"), args.version)
    logging.debug('Loading copyright info from url [%s]...', url)

    try:
        result = requests.get(url, timeout=30, headers={'Authorization':'Token %s' % args.token})
        logging.info('Result %s' % result.text )
    except:
        result = TIMEOUT

    if result.status_code != 200:
        print('Unable to succesfully contact the meterian server: %s' % str(result))
    elif len(result.text) == 0:
        return None
    else:
        return json.loads(result.text)



#
# CLI entry point
#

if __name__ == '__main__':

    args = _parseArgs()
    _initLogging(args)

    if not args.language in LANGUAGES:
        sys.stderr.write('invalid language: %s\n' % args.language)
        sys.stderr.write('available languages: %s\n' % str(LANGUAGES))
        sys.stderr.write('\n')
        sys.exit(-1)

    token = args.token
    if token == None:
        sys.stderr.write('No API token found.\nPlease specify it using the "%s" environment variable or use --token on the command line' % API_TOKEN_ENVVAR)
        sys.stderr.write('\n')
        sys.exit(-1)

    print('Looking for copyright attribution about "%s" version "%s" in the "%s" space...' % (args.name, args.version, args.language))
    copy = _loadCopyright(args)

    if copy != None:
        print('Found copyright attribution:')
        print('  text:   ' + copy["text"])
        print('  source: ' + copy["source"])
    else:
        print('No copyright attributions found')
