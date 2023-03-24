# wf-public-profiles

A simple app that ingests Wildflower people info from HolaSpirit and serves it as JSON 

## Production

App is related on Heroku. It is deployed using Heroku + Docker. See the `herkou.yml` file which specifies the Dockerfile that should be run. 

## Development

### Requirements

* [Poetry](https://python-poetry.org/)
* [just](https://github.com/casey/just)

### Install

`poetry install`


#### Install w/ Python Version from PyEnv

```
# Specify pyenv python version
pyenv shell --unset
pyenv local <<VERSION>>

# Set poetry python to pyenv version
poetry env use $(pyenv which python)
poetry cache clear . --all
poetry install
```

## Task list
* TBD
