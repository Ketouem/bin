# awsconsolelogin

Log easily into the AWS Console based on the credentials available into `~/.aws/credentials`.

## Installation

### Virtual Environment

In order to avoid messing up with your distribution's Python create a virtual environment dedicated to this tool, this can be achieved with the tool [`virtualenv`](https://virtualenv.pypa.io/en/stable/)

Simply run `make install`.

## Run the (debug) server

`make run` and access it at `http://localhost:5000`

## Launch a (dumb) CLI

`make console`
