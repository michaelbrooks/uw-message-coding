#!/usr/bin/env bash

# User-local one-time setup for the project
# After running this, fab update should do the trick mostly.

# Die on errors
set -e

PROJECT_ROOT=/home/vagrant/uw-message-coding

# Create a .env file
cp $PROJECT_ROOT/setup/templates/vagrant_dot_env $PROJECT_ROOT/.env

# Load virtualenvwrapper functions
source $(which virtualenvwrapper.sh)

# Make a virtualenv
mkvirtualenv message_coding -a $PROJECT_ROOT || true

# Install base python dependencies
pip install -r requirements/local.txt

# Bring everything up to date
fab dependencies update_app

# Add the workon command to the bashrc
if grep -q 'workon' /home/vagrant/.bashrc; then
    echo "workon already in bashrc"
else
    echo "workon message_coding" >> /home/vagrant/.bashrc
    echo "added workon to bashrc"
fi

if grep -q 'remount' /home/vagrant/.bashrc; then
    echo "remount already in bashrc"
else
    echo "alias remount_vagrant='mount -o remount home_vagrant_uw-message-coding'" >> /home/vagrant/.bashrc
    echo "added remount_vagrant to bashrc"
fi
