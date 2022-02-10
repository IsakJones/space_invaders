<div align="center">
    <img alt="Screenshot" src="https://github.com/sekerez/space_invaders/blob/main/assets/screenshot.png">
</div>

<p align="center">
  <p>
    <img alt="Python" src="https://img.shields.io/badge/Python-3.8.10-green">
  </p> 
  <p>
    <img alt="Pygame" src="https://img.shields.io/badge/Pygame-2.1.2-yellow">
  </p> 
  <p>
    <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-12.9-blue">
  </p> 
  <p>
    <img alt="License" src="https://img.shields.io/badge/License-MIT-red">
  </p>
</p>

### Intro

This is my own take on the classic space invaders retro game! I originally wrote this program when applying to the Recurse Center, but I fleshed out the program because I enjoyed the challenge of writing a retro videogame. I'm quite satisfied of the final product, and I think that this project was overall a great learning experience.

## Table of Contents
- [Installation](#Installation)
- [Usage](#Usage)
- [License](#License)

## Installation

Space Invaders requires no specific installation, though it does require that certain python dependencies be installed. Running a database requires connecting to a [PostgreSQL server](https://www.postgresql.org/).


### Dependencies
Space Invaders was written on a 64-bit [Ubuntu 20.04 LTS OS](https://releases.ubuntu.com/20.04/) using [Python 3.8.10](https://www.python.org/downloads/release/python-3810/). The project uses a few external dependencies, most importantly pygame, which are listed in the requirements.txt file. 

To download all python dependencies with pip, type in the command line:
```bash
$ pip install -r requirements.txt
```

## Usage

To run the game, first connect to a database, then run the program. 

Connecting to a database will require making a `.env` file in the `/src/db` folder with five environmental variables, as indicated in the [sample .env file](https://github.com/sekerez/space_invaders/src/db/sample.env). 

After environmental variables have been set, then the user need only run the main.py file in the project's root directory, as such:
```bash
python3 main.py
```
## License
My Space Invaders project is licensed under the MIT Licence Copyright (c) 2021.

See the [LICENSE](https://github.com/sekerez/space_invaders/LICENSE) for information on the history of this software, terms & conditions for usage, and a DISCLAIMER OF ALL WARRANTIES.

All trademarks referenced herein are property of their respective holders.