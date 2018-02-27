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
