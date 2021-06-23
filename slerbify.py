#! /usr/bin/env python
import time, math, random, string
import requests
from requests_toolbelt import MultipartEncoder
import argparse

HOSTNAME = 'https://slowedreverb.com'


def get_uid():
    return str(int(time.time()) + math.floor(999 * random.random() + 1))


def check_status(uid):
    with requests.post(f'{HOSTNAME}/checkstatus', data={'uid', uid}) as res:
        if res.ok:
            return res.json()['status']


def send_file(f, fields):
    mp3_file = {'file': (f, open(f, 'rb'), 'audio/mpeg')}

    with requests.post(f"{HOSTNAME}/fileSR", data=fields, files=mp3_file) as res:
        if res.ok:
            return res.json()['finishedLink']
        print(res.content)
        print("Something went wrong!")


# TODO: make this concurrent
def slerbify(args):
    fields = {
            'uid': get_uid(),
            'speed': args.slow,
            'reverb': args.reverb
            }

    f = send_file(args.mp3_file, fields)

    with requests.get(HOSTNAME+f) as res:
        outfilename = f'{args.mp3_file[:-4]}-slerbified.mp3'
        with open(outfilename, 'wb') as outf:
            outf.write(res.content)
        print('Saved slerbified file as', outfilename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Slerbify(slow + reverb) mp3 files using slowedreverb.com')
    parser.add_argument('mp3_file', metavar='filename', help='Any mp3 file to be slerbified')
    parser.add_argument('-s', dest='slow', type=int, choices=range(75, 101), default=87, help='The slowness speed. (default: %(default)s)')
    parser.add_argument('-r', dest='reverb', type=int, choices=range(0, 101), default=80, help='The reverb value. (default: %(default)s)')
    args = parser.parse_args()
    slerbify(args)
