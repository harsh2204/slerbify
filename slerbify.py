#! /usr/bin/env python
import time, math, random, string
import requests
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

    print(f'Sending {f} to server')
    with requests.post(f"{HOSTNAME}/fileSR", data=fields, files=mp3_file) as res:
        if res.ok:
            print(f'Finished processing {f}')
            return res.json()['finishedLink']
        print(res.content)
        print("Something went wrong!")


# TODO: make this concurrent
def slerbify(file, slow, reverb):
    fields = {
            'uid': get_uid(),
            'speed': slow,
            'reverb': reverb
            }

    f = send_file(file, fields)

    with requests.get(HOSTNAME+f) as res:
        outfilename = f'{file[:-4]}-slerbified.mp3'
        with open(outfilename, 'wb') as outf:
            outf.write(res.content)
        print('Saved slerbified file as', outfilename)


def process_batch(b):
    # We sleep b/w requests to prevent rate limit restrictions
    files = b.files
    for s in files:
        slerbify(s, b.slow, b.reverb)
        if args.sleep:
            print(f'Sleeping for {args.sleep} second(s)')
            time.sleep(args.sleep)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Slerbify(slow + reverb) mp3 files using slowedreverb.com')
    parser.add_argument('-s', dest='slow', type=int, choices=range(75, 101), metavar='[75-100]', default=87, help='The slowness speed. (default: %(default)s)')
    parser.add_argument('-r', dest='reverb', type=int, choices=range(0, 101), metavar='[0-100]', default=80, help='The reverb value. (default: %(default)s)')
    parser.add_argument('-d', '--delay', dest='sleep', type=int, default=2, help=argparse.SUPPRESS)
    parser.add_argument(dest='files', metavar='mp3_file', nargs='+', help='Any mp3 file(s) to be slerbified')
    args = parser.parse_args()
    process_batch(args)
    exit(0)
    slerbify(args)
