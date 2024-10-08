## Getting Started

Clone this repository.

```bash
mkdir code #(optional)
cd code #(optional)
git clone https://github.com/jettblu/rugged_cam.git
```

Before running this project, install required system dependencies.

```bash
sudo apt-get install -y libcamera-dev
sudo apt-get install -y libclang-dev
```

## Add Requirments

**Version Control**

```bash
# install git
sudo apt-get install git
# (optional) if pushing changes set user name and email
git config --global user.name "<name>"
git config --global user.email "<email>"
```

**Battery**
Install pisugar battery application.

```bash
wget https://cdn.pisugar.com/release/pisugar-power-manager.sh
bash pisugar-power-manager.sh -c release
```

After finished, you can manage the battery by visiting http://<your raspberry ip>:8421 in your browser.

**Logs**
Create required directories. _No longer required as of 9-30-24._

```bash
sudo mkdir -p /etc/rugged_cam/{logs,radio/{loading_dock/{compressed,original},receiving_dock}} /etc/rugged_cam/logs/health
# radio directors
```

**Add any additional wifi networks**

```bash
# add networks with below ui
sudo nmtui
# view connection priority
nmcli -f autoconnect-priority,name c
# now adjust priority
sudo nmcli connection modify "preconfigured" connection.autoconnect-priority 10
sudo nmcli connection modify "post" connection.autoconnect-priority 9
sudo nmcli connection modify "tbone_hotspot" connection.autoconnect-priority 8
sudo nmcli connection modify "tbone_cabin" connection.autoconnect-priority 7
```

**Meshtastic**
Install required packages for meshtastic.

```bash
sudo apt install libdbus-1-dev pkg-config
```

## Python Environment Setup

```bash
# install virtual environment
sudo apt update
sudo apt install pipx
pipx ensurepath # this adds pipx to path. will need to restart terminal for path changes to take effect.
pipx install virtualenv
```

Now in the rugged_cam/radio directory, run the followiung command. This creates a new virtual environment called env_radio.

```bash
# in the radio subdirectory run
virtualenv env_rugged_cam
source env_rugged_cam/bin/activate #activates environment
which python3 #(optional) to verify the environmenty has been activated
```

Now let's install the required packages for communicating with our radio.

```bash
pip install -r requirements.txt
# only if base station
pip install PyDrive==1.3.1
```

[Systemd with virtual environments example](https://gist.github.com/dunkelstern/5bfe7414fc0b7e8a9f6e1c4c78fd2543)

# Run Examples

```bash
# motion detection loop
cargo run -p motion_detection --bin motion_detection_loop --release
```

```bash
# camera capture... single snapshot
cargo run -p camera_capture --bin snapshot --release
```

```bash
# smart cam (swap oak and 41_40338-2_17403 with your device name and coordinates respectively)
cargo run -p smart_cam --bin run_smart_cam --release oak 41_40338-2_17403 0
```

```bash
# file transfer examples
python3 sender.py --path=file_transfer/file_examples/image-file-compressed.webp --shortname_destination_radio=palm # SENDER (from within radio subdirectory)
python3 receiver.py  # receiver (from within radio subdirectory)
python3 unloader.py  # polls output image directory and sends new files (from within radio subdirectory)
```

## Helpful Commands

**Pisugar**

```bash
# get battery
echo "get battery" | nc -q 0 127.0.0.1 8423

# get rtc time
echo "get rtc_time" | nc -q 0 127.0.0.1 8423

# reload daemon
sudo systemctl daemon-reload

# check status
sudo systemctl status pisugar-server

# start service
sudo systemctl start pisugar-server

# stop service
sudo systemctl stop pisugar-server

# disable service
sudo systemctl disable pisugar-server

# enable service
sudo systemctl enable pisugar-server

#uninstall pisugar package
sudo dpkg -P pisugar-server
```

**Linux Automation**

```bash
# list all services on computer
systemctl list-units --type=service

# view system file contents
systemctl cat <fle_name>

# copy service file to systemd
sudo cp <service file path> /etc/systemd/system/

# copy binary file to rugged cam binary directory
sudo cp <binary file path> /usr/bin/rugged_cam

# remove file
sudo rm <file_name>

# measure file ize in kilobytes
du -k <file_name>

# stop smart cam service
sudo systemctl stop smart-cam

# restart services
sudo systemctl start smart-cam
sudo systemctl start unloader
```

**Logs**

```bash
# restart health logs service
sudo systemctl restart cam-health

# enter rugged cam logs directory
cd /etc/rugged_cam/logs

# clear all logs in health directory
sudo rm -r /etc/rugged_cam/logs/health/*
```
