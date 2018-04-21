# nike_Raffle_FR
Script made to mass register accounts to Nike Raffle, optimized for French raffles but can be easily adapted to UK,US, etc...

# Steps:

There's 2 scripts, one using Selenium and one using Requests Python Module (faster).
I recommend using Selenium as Nike uses New Relic Browser tech on raffles websites to monitor user time spend on front-end, back-end, browser type version, etc...

I had no time to try simulate JavaScript logs for New Relic Browser so I'll recommend to stick with selenium even if it's not as fast as requests. 

1. Add your accounts at the end of the script (keep the syntax as shown)
2. Run the captchaharvester.py in the same folder as the main script
3. Run the script

## REQUIREMENTS:
- requests
- beautifulsoup
- pickle
- selenium

## TO DO:
- proxy support

## Installation 
Been asked a lot

- Check your Python version, must be 2.7
```python --version```

- Install pip:
```sudo easy_install pip```

Reboot terminal
Install modules BeautifulSoup, requests, selenium:
sudo pip requests selenium pickle

Download Chromedriver:
https://sites.google.com/a/chromium.org/chromedriver/

Place it in Python path (or PATH):

```/Library/Python/2.7```

## Use
- Modify your API key in captchaharvester.py & add your accounts in main or main2.py

- Launch main script 

```python main.py``` or ```python main2.py```

- Launch Captcha Harvester:

```python captchaharvester.py```

Take notes that I won't include an option to generate dot gmail or domain mails, you'll need to generate them first and then add them.
