
# iGlass-infinity
This project aims to provide an intelligent visual aid for blind and visually impaired to help them navigate their environment, read newpapers, books and magazines and also browse the internet
![alt text](https://github.com/mustious/iGlass/blob/master/iGlass_workflow.jpg)
         iGlass v2.0 workflow
## Packages Installation
Linux: All the installations where run and tested on a linux OS of both the system and raspberry pi. It will likely work on a Windows OS.
Open-source Libraries Used:
* Chatterbot: an offline chatbot system
* beautifulsoup: python webscraping engine
* pyttsx3: python based offline speech-to-text
* SpeechRecognition: speech recongition library with apis from google, ibm, pocketsphinx
* pico2wave: text-to-speech based on android system (this is smoother than pyttsx3 which is based on espeak)
* picamera: Python interface to the Raspberry Pi camera modules
* google-cloud-vision
* espeak: speech synthesizer

### Installing pip and pip3
```sh
sudo apt-get update
sudo apt-get updgrade
sudo apt-get python3-pip3
sudo apt-get python-pip
```
### picamera v1.13:
```sh
pip3 install picamera
```
### Chatterbot v1.0.2:
```sh
pip3 install Chatterbot==1.0.2
```
   Documentation: <https://chatterbot.readthedocs.io/en/stable/>
### oauth2client and other google-auth libraries
```
sudo pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
```
sudo pip3 install --upgrade oauth2client google-auth
```
   
### google-cloud-vision v1.0.0:
```
pip3 install google-cloud-vision
```
### beautifulsoup v4.8.2:
```
pip3 install beautifulsoup4
```
   Documentation: <http://www.crummy.com/software/BeautifulSoup/bs4/doc/>

### pyttsx3 v2.7:
```sh
pip3 install pyttsx3==2.7
```
   Documentation: <https://pyttsx3.readthedocs.io/en/latest/>

### SpeechRecognition v3.8.1:
```sh
pip3 install SpeechRecognition
```
   Documentation: <https://pypi.org/project/SpeechRecognition/>
            Reference: <https://realpython.com/python-speech-recognition/>
### pyaudio
```
sudo apt-get install python-pyaudio python3-pyaudio
```
or
```
sudo pip install pyaudio
```
### eSpeak
```
sudo apt-get install espeak
```

### pico2wave
```
cd /
sudo wget http://incrediblepbx.com/picotts-raspi.tar.gz
tar zxvf picotts-raspi.tar.gz
sudo rm -f picotts-raspi.tar.gz
sudo -i
cd /root
echo "Installing Pico TTS..."
./picotts-install.sh
exit
```
#### Credit: <http://nerdvittles.com/?p=16463>

Note: if the file does not exist, download file from my google drive shareable link: https://drive.google.com/open?id=1sS_KsSReNerkX0pRMtqTlFPPwjLm8-mZ and use filezilla, WinSCP(Windows Machine) or <i>scp</i> command to move the picotts-raspi.tar.gz to the root directory of your pi.  
##### Error1: "sed: can't read /etc/asterisk/extensions_custom.conf: No such file or directory"
##### Solution:
```
sudo apt-get install asterisk
cd /etc/asterisk
cp extensions.conf extensions_customs.conf
chown asterisk:asterisk extensions_custom.conf  # changes ownership user_group=asterisk and user=asterisk
```
### Setting Up Google Cloud Environment
* Installations

### Setting Up ReSpeaker 2-Mics Pi Hat
#### Official Documentation: http://wiki.seeedstudio.com/ReSpeaker_2_Mics_Pi_HAT/

### Connecting to raspberry pi using USB: 
#### https://desertbot.io/blog/headless-pi-zero-ssh-access-over-usb-windows

### setting up seeed-voicecard as the default audio devices
* disabled/black default audio card
    ```
    > echo 'blacklist snd_bcm2835' > /etc/modprobe.d/raspi-blacklist.conf
    ```
* Open /lib/modprobe.d/aliases.conf and comment out the line options snd-usb-audio index=-2

### storing alsa sound state and loading it on boot
* modify the alsamixer settings before saving
    ```
    > alsamixer
    ```
* store the modifications to a file
    ```
    > alsactl --file asound.state store
    ```
* command to load alsa state
    ```
    > alsactl --file asound.state restore
    ```
## Issues and Fixes
### ALSA springing up errors like:
```
ALSA lib confmisc.c:768:(parse_card) cannot find card '0'
ALSA lib conf.c:4292:(_snd_config_evaluate) function snd_func_card_driver returned error: No such file or directory
ALSA lib confmisc.c:392:(snd_func_concat) error evaluating strings
ALSA lib conf.c:4292:(_snd_config_evaluate) function snd_func_concat returned error: No such file or directory
ALSA lib confmisc.c:1251:(snd_func_refer) error evaluating name
...
```
This is likely occurs from incorrect configuration when setting up ALSA
* confirm the proper card number, device number and subdevice number using the command:
    ```
    > aplay -l
    ```
    ```
    **** List of CAPTURE Hardware Devices ****
    card 0: seeed2micvoicec [seeed-2mic-voicecard], device 0: bcm2835-i2s-wm8960-hifi wm8960-hifi-0 []
      Subdevices: 1/1
      Subdevice #0: subdevice #0
    
    ```
* edit the file ~/.asoundrc with proper device numbers
    ```
    > sudo nano ~/.asoundrc
    ```
    into:
    ```
    pcm.!default {
      type plug
      slave {
        pcm "hw:0,0"
      }
    }
    
    ctl.!default {
        type hw
        card 0
    }
    ```
* also, edit the file /usr/share/alsa/alsa.conf
    ```
    sudo nano /usr/share/alsa/alsa.conf
    ```
    search and replace the following lines with proper numbers
    ```
    ...
    defaults.ctl.card 0
    defaults.pcm.card 0
    ...
    ```
