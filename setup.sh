#!/bin/bash

sleep 30

sudo mv /tmp/id_ed25519.pub ~/key.pub

sudo apt-get update -y

sudo apt-get install docker.io -y 

sudo docker pull jenkins/jenkins


sudo addgroup bach && sudo useradd -m -s /bin/bash -g bach bach && sudo usermod -aG sudo bach


sudo mkdir -p /home/bach/.ssh && sudo mv ~/key.pub /home/bach/.ssh/authorized_keys && sudo chown -R bach:bach /home/bach/.ssh && sudo chmod 700 /home/bach/.ssh  && sudo chmod 600 /home/bach/.ssh/authorized_keys








