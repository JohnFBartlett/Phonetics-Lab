#! bin/bash

find $1 -depth -name '* *' -execdir bash -c 'mv "$1" "${1// /_}"' _ {} \;