# WATERVERSE-to-Turtle

# Folder structure
The folder structure of the repository cotnaining the tool to convert JSON-LD files to ttl-syntax and/or ttl files is given below.
```
WATERVERSE-TO-TURTLE
|---examples
    |---__init__.py
    |---sample_NL_KNMI.json
    |---sample_UK_rain.json
|---waterverse_jsonld_to_turtle_deployment
    |---src
        |---api.py
        |---json_to_ttl_converter.py
    |---Dockerfile
    |---requirements.txt
|---LICENSE.md
|---README.md
|---post_sample_data.py
```

# Docker installation
The components of the tool are packeged to through the use of Docker. Hence, the system that will be used for deploying the tool
must have Docker installed. See more information about the installation of Docker [over here](https://docs.docker.com/desktop/setup/install/windows-install/).

# Deployement
This tool is a docker based service. The api.py contains the API that processes the incoming request (JSON-LD file) and returns the desired
Turtle-syntax. A Docker container with this API can be build by first navigating to the directory where the api.py is located:

```bash
cd waterverse_jsonld_to_turtle_deployment
```
Build the Docker container by calling

```bash
docker build -t turtle_converter .
```
Run the Docker container by calling

```bash
docker run -p 80:80 turtle_converter
```

# License
Shield: [![MIT License][mit-shield]][mit-license]

This work is licensed under the 
[MIT License][mit-license].

[![MIT License][mit-image]][mit-license]

[mit-license]: https://opensource.org/licenses/MIT
[mit-image]: https://img.shields.io/badge/License-MIT-brightgreen.svg
[mit-shield]: https://img.shields.io/badge/License-MIT-brightgreen.svg

Details on the licensing related to this code can be found in the file [LICENSE.md](LICENSE.md)

# Contact details
email address: tessa.vrijhoeven@kwrwater.nl 

# Acknowledgments
This project has been funded by the WATERVERSE project of the European Union’s Horizon Europe programme under Grant Agreement no 101070262.

WATERVERSE is a project that promotes the use of FAIR (Findable, Accessible, Interoperable, and Reusable) data principles to improve water sector data management and sharing.
