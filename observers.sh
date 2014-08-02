#!/bin/bash

cd `dirname $0`/static/css

sass --compass --style compressed --watch style.scss:style.css > /dev/null &
sass --compass --style compressed --watch print.scss:print.css > /dev/null &

