#!/bin/bash

#install required dependencies
apt update && apt install -y snapd
snap install core && snap refresh core

#install certbot
snap install --classic certbot && ln -s /snap/bin/certbot /usr/bin/certbot
