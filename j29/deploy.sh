#!/usr/bin/bash

expect -c "
spawn git pull origin master
expect \"Password for\"
send \"foobar\n\"
expect \"\\\$\"
exit 0
"

