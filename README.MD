# Comics Uploader
The script download random comics from [xkcd](https://xkcd.com/) and upload it in your VK group.

# How to install
Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:
```bash
$ pip install -r requirements.txt
```
For script correct working (VK API access) you should get your personal VK ACCESS TOKEN
from ['How to get access token'](https://vk.com/dev/access_token) 
and put this ACCESS TOKEN into .env file in local folder.
```text
VK_ACCESS_TOKEN=your_access_token
```

Run comics-uploader.py for creating tables with all needed data:
```bash
$ python3 comics-uploader.py
```

# Project Goals
The code is written for educational purposes on online-course for web-developers [DEVMAN.org](https://devman.org)