# raspi-ip-pusher
## Simple python script to send the user a Pushbullet or Discord notification with the host device's IP address

To set up this script to auto-push ip on startup:
1. Clone the repo to your machine
2. Move get\_ip\_addr.py file in /usr/bin/
3. Edit the ip_pusher.json file and insert your Pushbullet [Access Token](https://www.pushbullet.com/#settings) to replace the `<pushbullet auth here>` string
3. Move ip-pusher.service to `/usr/lib/systemd/system/`
4. Run `sudo systemctl daemon-reload'
5. Run `sudo systemctl enable ip-pusher.service`

See `./get\_ip\_addr.py --help` for more usage
