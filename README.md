# Pyhon Ingest Example Code
Example source code for Europython 2020 talk by George Zisopoulos and Theofanis Petkos.

## Requirements
Docker (> 19.03) and docker-compose (> 3.7) are required to run the python-ingest from a container.

## Pre Installation Notes

* Create a root project folder and get inside. On linux:
```
mkdir your_folders_name
cd your_folders_name
```
* Clone project's source code from gihub.

### Installation

* Create database on PostgreSQL:
```
>>> CREATE DATABASE ingest_db;
```
* Create venv on project folder and install requirements:
```
$ python3 -m venv venv
$ pip3 install -r requirements.txt
```
* Run necessary db migrations;
```
$ flask db init
$ flask db migrate
$ flask db upgrade
```
* Go to .env file inside config folder and change environment variable values according to your credentials.

* Now you can build your docker image.
```
docker build -t python-ingest:v1 .
```

## Usage

Python-ingest runs as a part of python-iot-data-integrity docker-compose.yml file

## Contributing

Pull requests are welcome. Feel free to take this code for your own project.

## Troubleshooting

For any problems please open an issue to my repo.

Best regards,
### Theofanis A. Petkos, Software Engineer.
### George T. Zisopoulos, Software Engineer.