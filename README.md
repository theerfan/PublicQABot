# PublicQABot

A telegram bot in python which gets questions from users, sends it to a responder and finally sends the question and its answer to a public channel. 

## Getting Started

First things first, clone the project to any directory on your local machine that you want.
```
git clone https://github.com/theerfan/PublicQABot.git
```

### Prerequisites

In order to make use of the project, you'll need to install [Python 3](https://www.python.org/downloads/).
After adding pip and python to your PATH (for windows users), execute the following command in the project's local folder to install the necessary packages.

```
pip install -r requirements.txt
```

## Starting the bot

After putting your token, replace the "REDACTED" parts with the username of the responder, username of the developer (the one who recieves errors as messages if something goes wrong), and the id of the channel in the code (which should be done by hand),
run the program like this (put python3 instead of python if you have python 2 and 3 simultaneously), the reason for running it in interactive mode is that you'll probably want to kill it gracefully when you're done with it.

```
python -i bot.py
```

## Stopping the bot

Because you've ran in interactive mode, in order to kill it with grace, you'll need to first enter the follwing command:
```
updater.stop()
```
And then proceed to kill the process.


## Built With

* [Python 3](https://www.python.org) 
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Everything that's handled by the bot.
* [More Features to come!]


## Authors

* **Erfan Abedi** - *all the work :)))* - [TheErfan](https://github.com/TheErfan)
* **Mahdi Sadeghzadeh Ghamsary** - *the starting idea* - [MSadeghzadehG](https://github.com/MSadeghzadehG)
* **MohammadMahdi Khancherly** - *Debugging, future features.* - [MMKH](https://github.com/mmkhmmkh)

## License

This project is masalan licensed under the MIT License

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

