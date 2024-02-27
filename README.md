# SmartClimb
A system for helping visually impaired people climb


## Getting Started

You will need a RaspberryPi with the sensors (which are listed below) in order to utilize the code of this project.
For actual deployment and usage of the SmartClimb system you simply have to:

1. Copy the `smartClimb.py`-file to a RaspberryPi
2. Run `sudo python3 smartClimb.py`

## Setup to autolaunch after powering on the RaspberryPi

1. Run `sudo crontab -e`
2. Choose an editor of your choice
3. To the bottom of the now opened file, enter: `@reboot sleep10; python3 home/pi/Desktop/smartClimb.py &`
   
   _(Of cource you need to adjust the path `home/pi/Desktop/` to the location of your smartClimb.py-file)_

This command launches after the RaspberryPi has been powered on. `sleep10` waits 10 seconds before running the script, to give the RaspberryPi time to load all dependencies first. Then the `smartClimb.py` is launched and after it the `&` signalized that the RaspberryPi should run everything else as normal.

## Hardware

The SmartClimb-System was developed and tested with the following hardware:

1. Raspberry Pi 3 Model B+
2. Joy-It RFID-RC522
3. Joy-It KY-004 Button
4. Joy-It KY-006 Passive Piezo Buzzer
5. Joy-It KY-009 RGB SMD-LED
6. Speaker/Headphones connected to the RaspberryPi's 3.5mm stereo output and composite video port

The picture below shows the circuit diagram so you can recreate the whole system by yourself.

![UbiComp](https://github.com/JuHardtung/SmartClimb/assets/15029310/fd33ae10-0aa4-40c1-ae2a-13f58aa8efe9)

## Testing

The Prototype was tested in the  [2t Kletter- und Boulderhalle](https://www.2tklettern.de/). A video of this testing can be found [here](https://youtu.be/4ytUx1dRwLQ?si=VMUUZwbRYJnUahgd).


## Authors

- Aileen Jurkosek
- Oliver Mertens
- Tobias Mink
- Julian Hardtung

## License
This project is licensed under the MIT license - see the LICENSE.md file for details

## Acknowledgments

This project was created within the [_Ubiquitous Computing_](https://www.medieninformatik.th-koeln.de/study/master/moduls/ma_wpf_ubiquitous_computing/) course by Prof. Dr. Matthias Böhmer and Vimal Darius Seetohul as part of the Media Informatics Master program.
