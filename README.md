# Alexa Meeting
Automatically place Alexa in Do Not Disturb mode during meetings.

This application currently only works with MacOS

### Installation:

+ Register an account at [voicemonkey.io](https://voicemonkey.io/)
+ Create two 'monkeys', one to enable Do Not Disturb and one to disable it
+ Follow the instructions on [voicemonkey.io](https://voicemonkey.io/docs) to add their Skill to Alexa
+ Make notes of the monkey IDs, access token and secure token, you will need those in the next step

+ Run the following command from a terminal:

```
bash <(curl -s https://raw.githubusercontent.com/number42net/alexa-meeting/main/install.sh)
```

+ Follow the instructions to update the configuration file

### Uninstall

To completely remove the application, run these commands:

```
launchctl stop com.n-42.alexa-meeting
launchctl remove com.n-42.alexa-meeting

rm ~/Library/LaunchAgents/com.n-42.alexa-meeting.plist
rm -R ~/Library/Application\ Support/alexa-meeting
```