#!/bin/bash

INSTALL_DIR=~/Library/Application\ Support/alexa-meeting
PYTHON=$(which python3)
LAUNCH_AGENT=~/Library/LaunchAgents/com.n-42.alexa-meeting.plist

echo "Starting installation..."

mkdir -p "$INSTALL_DIR"
mkdir -p "~/Library/LaunchAgents"

cat <<EOT >> $LAUNCH_AGENT
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
	<dict>
		<key>Label</key>
			<string>com.n-42.alexa-meeting</string>
		<key>StandardOutPath</key>
			<string>$INSTALL_DIR/log.stdout</string>
		<key>StandardErrorPath</key>
			<string>$INSTALL_DIR/log.stderr</string>
		<key>WorkingDirectory</key>
			<string>$INSTALL_DIR</string>
		<key>ProgramArguments</key>
				<array>
					<string>$PYTHON</string>
					<string>main.py</string>
				</array>

		<key>KeepAlive</key>
			<true/>
		<key>RunAtLoad</key>
			<true/>
	</dict>
</plist>
EOT

curl --silent --show-error "https://raw.githubusercontent.com/number42net/alexa-meeting/main/main.py" -o "$INSTALL_DIR/main.py"
curl --silent --show-error "https://raw.githubusercontent.com/number42net/alexa-meeting/main/config.yaml" -o "$INSTALL_DIR/config.yaml"

echo
echo "Please fill in the following configuration details:"
read -p "Voice Monkey access token: " ACCESS_TOKEN
read -p "Voice Monkey secure token: " SECURE_TOKEN
read -p "Monkey to enable Do Not Disturb: " MONKEY_ON
read -p "Monkey to disable Do Not Disturb: " MONKEY_OFF

sed -I '' "s/REPLACE_WITH_ACCESS_TOKEN/$ACCESS_TOKEN/g" "$INSTALL_DIR/config.yaml"
sed -I '' "s/REPLACE_WITH_SECURE_TOKEN/$SECURE_TOKEN/g" "$INSTALL_DIR/config.yaml"
sed -I '' "s/REPLACE_WITH_MONKEY_ON_ID/$MONKEY_ON/g" "$INSTALL_DIR/config.yaml"
sed -I '' "s/REPLACE_WITH_MONKEY_OFF_ID/$MONKEY_OFF/g" "$INSTALL_DIR/config.yaml"

echo
echo "Enabling and starting daemon..."
launchctl load $LAUNCH_AGENT
launchctl start com.n-42.alexa-meeting

echo
echo "Installation complete."
echo "You can modify the configuration by editting the following file:"
echo $INSTALL_DIR/config.yaml
echo
echo "Logs can be found at: $INSTALL_DIR/log.stdout"
echo "and $INSTALL_DIR/log.stderr"