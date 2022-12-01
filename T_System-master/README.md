# T_System


the moving objects tracking system via two axis camera motion for raspberry pi distributions

![A.V.A.](https://raw.githubusercontent.com/MCYBA/T_System/master/docs/img/on_work.gif)

<br>


#### Supported Environments

|                         |                                         |
|-------------------------|-----------------------------------------|
| **Operating systems**   | Linux                                   |
| **Python versions**     | Python 3.x (64-bit)                     |
| **Distros**             | Raspbian         |
| **Package managers**    | APT, pip                                |
| **Languages**           | English                                 |
|                         |                                         |

### Requirements

##### Hardware
  
- Raspberry Pi 2,3 B, B + or higher
- Raspberry Pi Camera
- 2 servo motors
- 2 axis motion system as pan-tilt motions

##### Software

- OpenCV. Install via [here](https://docs.opencv.org/master/df/d65/tutorial_table_of_content_introduction.html) or any other place you want.

### Installation

Download the [latest release](https://github.com/DragonComputer/Dragonfire/releases/latest) (the `.deb` file) and:

```Shell
sudo ./install.sh
```
for development mode: `sudo ./install-dev.sh`


<sup><i>If there is a failure try `sudo -H ./install-dev.sh`</i></sup>

### Usage <a href="https://t-system.readthedocs.io/en/latest/t_system.html"><img src="https://media.readthedocs.com/corporate/img/header-logo.png" align="right" height="25px" /></a>


```
usage: t_system [-h] [-S] [-l] [-s] [-a] [--version]
                 [--cascadefile XML_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -S, --show-stream     Display the camera stream. Enable the stream window.
  -l, --learn           Teach mode. Teach the object tracking parameters with 
                        the trial and error method.
  -s, --security        Security Mode. Scan the around and optionally take 
                        photos of visitors.
  -a, --augmented       Augmented control with the Augmented Virtual Assistant 
                        A.V.A.. 'https://github.com/MCYBA/A.V.A.' is the home 
                        page of the A.V.A. and usage explained into the
                        'AUGMENTED.md'.
  --version             Display the version number of T_System.
  --cascadefile CASCADEFILE    
                        Specify the trained detection algorithm file for the 
                        object detection ability. Sample(And Default):
                        'haarcascade_frontalface_default' for
                        frontalface_default.xml file inside the 'haarcascade'
                        folder. 
```

<br>

### Augmented

Augmented usage explained [here](https://github.com/MCYBA/A.V.A.) into the `AUGMENTED.md`.

<br>

**Supported Distributions:** Raspbian. This release is fully supported. Any other Debian based ARM architecture distributions are partially supported.

