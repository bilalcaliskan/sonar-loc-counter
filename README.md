# Sonar Loc Counter
This project aims to count the number of lines of projects on [Sonarqube](https://www.sonarqube.org/) using [Sonarqube API](https://docs.sonarqube.org/latest/extend/web-api/). 
This is useful when you need to know how large your codebase is, especially when need to use enterprise software tools.

### Prerequisites
  - [Python 3](https://www.python.org/downloads/)
  - A running [Sonarqube](https://www.sonarqube.org/) instance

### Usage
This project is written with Python, so all you need to do is running the below command, also you need Python 3:
```
$ python3 src/application.py
```

### Configuration
Configuration parameters are taken at the runtime as inputs:
```
sonar_user    An authorized sonarqube user which has read access
sonar_pass    An authorized sonarqube password which has read access
sonar_url     Target sonarqube instance. (ex: https://sonarqube.example.com)
```
