#!/bin/bash

# Expects 1 argument, the full path to the project files

set -e
PROJECT_ROOT=$1
source ${PROJECT_ROOT}/setup/scripts/functions.sh
set +e


# Make sure the machine is updated
loggy "Updating system..."
buffer_fail "apt-get update" "ERROR: Could not update system."

# Install some global NPM modules we might need
loggy "Installing global npm packages..."
buffer_fail "npm install -g bower grunt-cli" "ERROR: Error installing NPM packages."

# Make sure the mysql service is started
loggy "Starting MySQL service..."
service mysql start

# Fail if error after this
set -e

# Create a database table
DBHOST=localhost
DBPORT=3306
DBNAME=codingdb
DBUSER=dbuser
DBPASS=dbpass

loggy "Creating database..."

# Create a database just for the project
cat <<EOF | mysql -u root -h $DBHOST
CREATE DATABASE IF NOT EXISTS \`$DBNAME\` CHARACTER SET utf8 COLLATE utf8_general_ci;
GRANT ALL PRIVILEGES ON \`$DBNAME\`.* TO '$DBUSER'@'$DBHOST' IDENTIFIED BY '$DBPASS';
GRANT USAGE ON *.* TO '$DBUSER'@'$DBHOST';
EOF

echo "    DATABASE_URL=mysql://$DBUSER:$DBPASS@$DBHOST:$DBPORT/$DBNAME"

loggy "Running development setup script...\n-----------------------------------"

VENV_NAME=$(basename $PROJECT_ROOT)
su --login -c "${PROJECT_ROOT}/setup/scripts/dev_setup.sh $PROJECT_ROOT $DBHOST $DBPORT $DBNAME $DBUSER $DBPASS" vagrant

loggy "-----------------------------------"

# Add the workon command to the bashrc
loggy "Augmenting user's bashrc file..."

VAGRANT_HOME=/home/vagrant
if grep -q 'workon' ${VAGRANT_HOME}/.bashrc; then
    echo "workon already in bashrc"
else
    echo "workon $VENV_NAME" >> ${VAGRANT_HOME}/.bashrc
    echo "added workon to bashrc"
fi

if grep -q 'remount' ${VAGRANT_HOME}/.bashrc; then
    echo "remount already in bashrc"
else
    echo "alias remount_vagrant='sudo mount -o remount home_vagrant_uw-message-coding'" >> ${VAGRANT_HOME}/.bashrc
    echo "added remount_vagrant to bashrc"
fi
