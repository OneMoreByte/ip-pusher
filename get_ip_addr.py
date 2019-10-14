#!/usr/bin/env python3
"""A IP pushing tool for headless devices with ephemeral ip addresses. 
Pushes IPs to Discord or Pushbullet.


Usage:
  get_ip_addr.py discord (-t <token> | --token=<token>)  (-i <id> | --id=<id>)
  get_ip_addr.py pushbullet (-t <token> | --token=<token>)
  get_ip_addr.py (-c <file> | --config=<file>)
  get_ip_addr.py


Options:
  -t <token>, --token=<token>  token for discord or pushbullet
  -i <id>, --id=<id>           id for discord
  -c <file>, --config=<file>   [default: /etc/ip-pusher.json]


"""


import os
import json
import requests
from docopt import docopt


def get_config():
    args = docopt(__doc__, version='0.1.0')
    print(args)
    if not args['discord'] and not args['pushbullet']:
        config = load_json_config(args['--config'])
        args[config['type']] = True
        args['--id'] = config['id']
        args['--token'] = config['token']
    return args


def load_json_config(path):
    c = {}
    if os.path.exists(path):
        try:
            with open(path) as f:
                c = json.load(f)
        except Exception as e:
            print("File error", e)
            exit(1)
    else:
        print("No config. Edit config at", path)
        exit(1)
       
    return c


def get_ip():
    r = requests.get('http://ip.42.pl/raw')
    if r.status_code == 200:
        return r.text
    else:
        os.exit(1)
        return ''


def send_discord(webh_id, token, msg):
    d_url = 'https://discordapp.com/api/webhooks/{}/{}'.format(webh_id, token)
    d_data = { 'content': msg }
    res = requests.post(d_url, json=d_data)
    res.raise_for_status()


def send_pushbullet(token, title, msg):
    pb_url = 'https://api.pushbullet.com/v2/pushes'
    pb_data =  { 'type': 'note', 'title': title, 'body': msg } 
    res = requests.post(pb_url, json=pb_data, headers={'Access-Token': token})
    res.raise_for_status()


def main():
    config = get_config()
    host = os.uname()[1]
    ip = get_ip()
    title = "IP from \"{}\"".format(host)
    msg = "IP : {}\nDomain (TTL in 5m): {}.jackhil.de".format(ip, host)

    if config['pushbullet']:
        send_pushbullet(config['--token'], title, msg)
    elif config['discord']:
        send_discord(config['--id'], config['--token'], msg)
    else:
        print("No configured sender")
        exit(1)


if __name__ == '__main__':
    main()

