#! /usr/bin/env sh
#
# Setup virtualenv

if [ $# -ne 1 ]; then
  command=`basename $0`
  echo "Usage: ${command} <enviroment name>" 1>&2
  exit 1
fi

ENV_NAME=$1
VIRTUALENV="virtualenv-15.0.0"

# Download virtualenv
curl -O https://pypi.python.org/packages/source/v/virtualenv/${VIRTUALENV}.tar.gz
tar xvfz ${VIRTUALENV}.tar.gz

# Setup virtualenv
python ${VIRTUALENV}/virtualenv.py ${ENV_NAME}

#${ENV_NAME}/bin/pip install numpy
#${ENV_NAME}/bin/pip install -r requirements.txt
${ENV_NAME}/bin/pip install bdflib

# Link if installed opencv3 from homebrew
# ln -s /usr/local/opt/opencv3/lib/python2.7/site-packages/cv2.so ./opencv/lib/python2.7/site-packages/

# Cleanup
rm -rf ${VIRTUALENV} ${VIRTUALENV}.tar.gz

echo "You can use virtualenv by typing \"source ${ENV_NAME}/bin/activate\"."
echo "Disable virtuallenv \"deactivate\"."
