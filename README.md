![issues](https://img.shields.io/github/issues/Dylan-Zheng/Rise-of-Kingdoms-Bot)
![forks](https://img.shields.io/github/forks/Dylan-Zheng/Rise-of-Kingdoms-Bot)
![stars](https://img.shields.io/github/stars/Dylan-Zheng/Rise-of-Kingdoms-Bot)
![lincense](https://img.shields.io/github/license/Dylan-Zheng/Rise-of-Kingdoms-Bot)

# Rise of Kingdom Bot

### **Introduction**

Rise of Kingdom Bot can do following job: claim quests/vip/gifts, collecting resource, gathering resource, donate techology, train troops and pass verification.

If you have any problem, suggestions or new features,  please feel free to submit issues directly on GitHub

- Link: https://github.com/Dylan-Zheng/Rise-of-Kingdoms-Bot/issues


If you don't want to set up by yourself, there is executable version for windows

- Link: https://github.com/Dylan-Zheng/Rise-of-Kingdoms-Bot/releases/


If you like this project, give me a star or feedback , that is great help for me. **:smile:**

------

**Current Version v1.4.3.060721_beta (06/07/2021):**

Link: https://github.com/Dylan-Zheng/Rise-of-Kingdoms-Bot/releases/tag/v1.4.3.060721_beta

**Update:**

- Random tasks order.
- fix sometime stuck on pass verification.

Note: Don't forget to move your **'save'**, **'config.json'** and **'devices_config.json'** to new version folder

------

### Requirements

- python

  version 3.7
  
- software

  - ADB  version 29.0.5-5949299 (1.0.41)
  - tesseract 

- libraries

  - opencv-python

  - pytesseract

  - numpy

  - pillow

  - pure-python-adb

  - requests
  
  - requests-toolbelt
  
    

### Functions

| Name                                                   | Status          |
| ------------------------------------------------------ | --------------- |
| Automatically start the game when game is not running  | **<u>Done</u>** |
| Automatically locating building                        | **<u>Done</u>** |
| Collecting resource, troops, and help alliance         | **<u>Done</u>** |
| Produce material                                       | **<u>Done</u>** |
| Open free chest in tavern                              | **<u>Done</u>** |
| Claim quest and daily objectives                       | **<u>Done</u>** |
| Claim VIP chest                                        | **<u>Done</u>** |
| Claim Event                                            | not yet         |
| Collecting allied resource, gifs and donate technology | **<u>Done</u>** |
| Upgrade and train troops                               | <u>**Done**</u> |
| Attack barbarians                                      | <u>**Done**</u> |
| Heal troops                                            | <u>**Done**</u> |
| Gather resource                                        | **<u>Done</u>** |
| Mystery Merchant                                       | <u>**Done**</u> |
| A simple GUI                                           | **<u>Done</u>** |
| Allow bot control multi-devices/emulator               | **<u>Done</u>** |
| Pass verification with haoi API                        | **<u>Done</u>** |
| Pass verification with 2captcha API                    | **<u>Done</u>** |



### Set Up

- Use following commands to install package into you **python** / **python virtual environment** (version 3.7)

  ```
  pip install opencv-python
  pip install pytesseract
  pip install numpy
  pip install pillow
  pip install pure-python-adb
  pip install requests
  pip install requests-toolbelt
  ```

- Download **ADB** version 29.0.5-5949299 (1.0.41) (require for same version or you can change version in adb.py)

  - move all **adb** files under: **project folder/adb/** 

- Download **tesseract** version v5.0.0-alpha.20201127 (no require for same version)

  - move all **tesseract** files under: **project folder/tesseract/** 

- Use following command to run project

  ```
  python main.py
  ```

- Directory Structure Image:

  ![](https://github.com/Dylan-Zheng/Rise-of-Kingdoms-Bot/blob/main/docs/structure.png?raw=true)



### Configurations

- Emulator resolution must be <u>**720x1280**</u> or <u>**1280x720**</u>
- Emulator must **Enable** Android Debug Bridge (ADB)
- Game language must be <u>**English**</u> 



### WARNING

- **Use it at your own risk!**
- **I don't know will your account be banned by using it!**



### Show case

- Locating Building

  ![](https://github.com/Dylan-Zheng/Rise-of-Kingdoms-Bot/blob/main/docs/init_building_pos.gif?raw=true)

- Collection and Help

  ![](https://github.com/Dylan-Zheng/Rise-of-Kingdoms-Bot/blob/main/docs/collecting.gif?raw=true)

- Produce Material

  ![](https://github.com/Dylan-Zheng/Rise-of-Kingdoms-Bot/blob/main/docs/metarials_production.gif?raw=true)

- Upgrade and Train Troops

  ![Train](https://github.com/Dylan-Zheng/Rise-of-Kingdoms-Bot/blob/main/docs/auto_train.gif?raw=true)

- Gather Resource

  ![](https://github.com/Dylan-Zheng/Rise-of-Kingdoms-Bot/blob/main/docs/gather_edit.gif?raw=true)

- Pass verification

  ![](https://github.com/Dylan-Zheng/Rise-of-Kingdoms-Bot/blob/main/docs/pass_verification.gif?raw=true)
