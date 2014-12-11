#!/bin/sh

# Die on errors
set -e

# Make sure the machine is updated
apt-get update

# Install some global NPM modules we might need
npm install -g bower grunt-cli

# Make sure the mysql service is started
service mysql start || true

# Create a database table
DBHOST=localhost
DBPORT=3306
DBNAME=database
DBUSER=dbuser
DBPASS=dbpass
echo "Creating database $DBNAME on $DBHOST:$DBPORT with user $DBUSER and password '$DBPASS'"

# Create a database just for the project
# use this to set utf8mb4 charset:
# CREATE DATABASE IF NOT EXISTS $DBNAME CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
cat <<EOF | mysql -u root -h $DBHOST
CREATE DATABASE IF NOT EXISTS $DBNAME;
GRANT ALL PRIVILEGES ON $DBNAME.* TO '$DBUSER'@'$DBHOST' IDENTIFIED BY '$DBPASS';
GRANT USAGE ON *.* TO '$DBUSER'@'$DBHOST';
EOF
