# Malware Analysis and Storage System

## Introduction

The Malware Analysis and Storage System (MASS) is a joint research project by the [Communication and Network Systems Group @ University of Bonn](https://net.cs.uni-bonn.de/start-page/) and [Fraunhofer FKIE](https://www.fkie.fraunhofer.de/). The goal of our project is to create a flexible and reusable platform for malware analysis which empowers collaboration between malware researchers.

The **MASS server** contains a database of all submitted malware samples and all the gathered analysis data. **Analysis systems** are connected to the MASS server and automatically receive new samples in order to execute an analysis. Researchers can obtain the analysis results via the MASS web interface or the **REST API**.

MASS is **free and open source software** licensed under the terms of the MIT license. Other researchers are invited to contribute to the MASS development!

## Prerequisites

Coming soon!

## Installation

1. `git clone git@github.com:mass-project/mass_server.git && cd mass_server`
2. `git submodule init && git submodule update`
3. Install Python dependencies using a) `./make_venv.sh` to build a virtual environment, or b) `pip install -r requirements.txt` to install the necessarry packages directly to your Python 3 installation. If any error is reported, make sure you have followed the **Prerequisites** section closely.

## Startup in development mode

1. Change to the MASS server directory
2. If you have created a virtual enviroment, run `source venv_mass/bin/activate` to activate it
3. Run `python mass_server_flask.py` to start up the MASS server in development mode

## Documentation

Coming soon!

## License

MASS is licensed under the terms of the MIT license. For additional details, please take a look at the `LICENSE` file.
