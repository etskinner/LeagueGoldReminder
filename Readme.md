# LeagueGoldReminder
A text-to-speech reminder of how much gold you have in League of Legends

If you have trouble remembering to spend your gold in League of Legends, this can help! 
It reminds via text-to-speech you when you go over certain thresholds (1000, 1500, 2000, and so on). 
The reminders get more frequent the higher you go. 

## Install

### LeagueGoldReminder.exe / Portable
The easiest way to run this is to download and run LeagueGoldReminder.exe from the [Releases](https://github.com/etskinner/LeagueGoldReminder/releases) page. 

Windows will probably complain that it's a dangerous file, because I haven't signed it or anything. If you don't trust it, follow the Python install option below. Otherwise, bypass the warnings.

### Python
If you're familiar with python and git:
- Clone the repository
- Install requirements.txt
- Run LeagueGoldReminder.py

## Usage
Just run the file (.py or .exe)! When you start a game, on the loading screen the TTS will say 'Connected'. From there on, it will give you reminders when you have 1000+ gold.

There isn't any configurability right now. Maybe there will be in the future. The window shows some info log messages, but that's about it.

## Issues? Ideas?
I'm all ears, just put in an issue or pull request if you have ideas / improvements / bugs.
