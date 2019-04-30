# COOPER to MQTT

[![Travis](https://img.shields.io/travis/hardwario/cp2mqtt/master.svg)](https://travis-ci.org/hardwario/cp2mqtt)
[![Release](https://img.shields.io/github/release/hardwario/cp2mqtt.svg)](https://github.com/hardwario/cp2mqtt/releases)
[![License](https://img.shields.io/github/license/hardwario/cp2mqtt.svg)](https://github.com/hardwario/cp2mqtt/blob/master/LICENSE)

## Installing

You can install **cp2mqtt** directly from PyPI:

```sh
sudo pip3 install -U cp2mqtt
```

## Usage

Update config.yml and run

```sh
cp2mqtt -c config.yml
```

### Systemd

Insert this snippet to the file /lib/systemd/system/cp2mqtt.service:
```
[Unit]
Description=COOPER cp2mqtt
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/usr/local/bin/cp2mqtt -c /etc/cooper/cp2mqtt.yml
Restart=always
RestartSec=5
StartLimitIntervalSec=0

[Install]
WantedBy=multi-user.target
```

Start the service:

    sudo systemctl start cp2mqtt.service

Enable the service start on boot:

    sudo systemctl enable cp2mqtt.service

View the service log:

    journalctl -u cp2mqtt.service -f


## License

This project is licensed under the [**MIT License**](https://opensource.org/licenses/MIT/) - see the [**LICENSE**](LICENSE) file for details.
