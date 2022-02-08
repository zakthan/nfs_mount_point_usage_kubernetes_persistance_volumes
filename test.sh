#!/bin/bash
##echo $0|tr -d 'test.sh'
echo $0|sed 's/\/test.sh//g'
