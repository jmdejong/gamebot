#!/bin/sh
cd "`dirname "$0"`"
socat - UNIX-CONNECT:./adminsocket.sock

