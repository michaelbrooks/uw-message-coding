#!/bin/bash

source functions.sh

PROJECT_ROOT=$(cd $(script_dir) && cd ../.. && pwd)

loggy "CHECKING SYSTEM SETUP"

if ! exists 'npm'; then
    loggy "Node package manager (npm) not available.\nPlease install node.js on your machine." "error"
    loggy "See: https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager"
    exit 1
fi

if ! exists 'mysql'; then
    loggy "MySQL not installed.\nPlease install MySQl on your machine." "error"
    exit 1
fi

if ! exists 'python2.7'; then
    loggy "Python 2.7 not available.\nPlease install Python 2.7 on your machine." "error"
    exit 1
fi

if ! exists 'bower'; then
    loggy "Bower not installed.\nPlease install Bower on your machine.\nExample: sudo npm install -g bower" "warn"
    exit 1
fi



loggy "PYTHON ENVIRONMENT SETUP"
echo "Requires Python 2.7, pip, and virtualenv (and virtualenvwrapper)"

VENV_NAME="uw-message-coding"
export PIP_DOWNLOAD_CACHE=${PIP_DOWNLOAD_CACHE:-$HOME/.pip_download_cache}

if false && exists 'virtualenvwrapper.sh'; then
    
    loggy "Creating Python virtual environment with virtualenvwrapper"
    
    # Set up virtualenv and virtualenvwrapper
    export VIRTUALENVWRAPPER_PYTHON=${VIRTUALENVWRAPPER_PYTHON:-$(command -v python2.7)}
    export WORKON_HOME=${WORKON_HOME:-$HOME/.virtualenvs}
    source $(which virtualenvwrapper.sh)

    mkvirtualenv $VENV_NAME -a $PROJECT_ROOT
    failif "Could not create virtualenv"
elif exists 'virtualenv'; then
    
    loggy "Creating Python virtual environment with virtualenv in ${PROJECT_ROOT}/.virtualenv"
    virtualenv ${PROJECT_ROOT}/.virtualenv
    failif "Could not create virtualenv"
    
    source ${PROJECT_ROOT}/.virtualenv/bin/activate
    failif "Unable to load virtualenv"
fi

loggy "Installing Python dependencies..."
pip install -r ${PROJECT_ROOT}/requirements/local.txt
failif "Error running pip install... aborting."



loggy "MYSQL DATABASE SETUP\n\nPlease provide information for accessing the database.\nIf the database does not exist, you will be prompted to create it."

DATABASE_HOST=$(prompt "Hostname:" "localhost")
DATABASE_PORT=$(prompt "Port:" "3306")
DATABASE_NAME=$(prompt "Database name:" "message_coding")
DATABASE_USER=$(prompt "User:" "message_coding")
DATABASE_PASS=$(prompt "Password:" $DATABASE_USER)


function test_database {
    # Try and connect to the database using these credentials
    mysql -h $DATABASE_HOST -P $DATABASE_PORT -u $DATABASE_USER -p$DATABASE_PASS $DATABASE_NAME 2> /dev/null << EOF
show tables;
EOF

    if [ $? -gt 0 ]; then
        loggy "The database does not yet exist.\nYou may run the following script to create it:" "warn"
        echo "--------------"
        cat << EOF
CREATE DATABASE IF NOT EXISTS ${DATABASE_NAME}
    DEFAULT CHARACTER SET = 'utf8'
    DEFAULT COLLATE = 'utf8_unicode_ci';
GRANT USAGE ON *.* to ${DATABASE_USER}@localhost identified by '${DATABASE_PASS}';
GRANT ALL PRIVILEGES ON ${DATABASE_NAME}.* TO ${DATABASE_USER}@localhost;
FLUSH PRIVILEGES;
EOF
        echo "--------------"
        
        if ! confirm "Press enter once you have created the database" "yes"; then
            loggy "User cancelled." "warn"
            exit 1
        fi
        
        false
    else
        true
    fi
}

# Keep trying until the database is ready
test_database
while [ $? -gt 0 ];
do
    test_database
done

loggy "Database connection successful."


loggy "Installing project dependencies and migrating database..."

# Bring everything up to date
fab dependencies migrate