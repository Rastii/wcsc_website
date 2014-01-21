#!/bin/bash

#Check to see if dev.db exists
if [ ! -f dev.db ]; then
  #If it does not exist, let's create it
  touch dev.db
fi

#Setup python virtual environment
python virtualenv.py flask
flask/bin/pip install setuptools --no-use-wheel --upgrade

#Install python dependencies from require.txt
filename="require.txt"
while read -r line
do
  echo "Installing python module $line"
  flask/bin/pip install $line
  #Check to make sure each dependency works properly...
  if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install python module $line -- EXITING"
    echo "This may be caused because python dev tools are not installed"
    echo "Debian: sudo apt-get install python-dev"
    exit 1
  fi
done < $filename

source flask/bin/activate
#Setup the database
python run.py setup

echo "DONE";
