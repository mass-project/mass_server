#!/bin/bash

sudo docker-compose down
sudo docker-compose up -d
sudo docker exec -it massserver_mass_server_1 python3 /demo_state.py
