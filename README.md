# DEEPL POC

## Pre-requisites

1. Python version 3 and pip
2. pipenv (pip install pipenv)

## Deployment

1. pipenv install --ignore-pipfile
2. pipenv shell

## Execution

Desktop

behave -i features/testWording.feature --no-capture -f json -o reports/report.json

Mobile

behave -D mobile -i features/testWording.feature --no-capture -f json -o reports/report.json

## Project lay out

Since it is a BDD project, it uses "feature" files for tests definition. The test plan is stored at "features/" folder 

BDD needs a "glue" code, a decoder, in order to understand the "feature" files language. This code is stored at "steps/"
folder. This code performs the orchestrating of the test steps

There is also a "sut/" folder, which stores the code which controls the system under tests.

Under "sut/" folder there are two subfolders
- "model/": this one hosts the pages objects, which provides "gears" to perform actions and get information
- "selectors/": this one hosts the selectors of the web elements in order to find them by the model. 
  They are kept separated in order to use them as configuration files, easier to maintain.

## Feature 1: Wording

Uses a set of different words in order to check translation single result, alternative results and complete list of meanings

## Feature 2: Language

Selects different languages in order to check results

### Feature 3: Lemmas and meanings

Checks all stored info is shown

### Feature 4: Topics

Uses a word selection in order to try terms from different topics: engineering, legal, sport, etc


Only Feature 1 is automated
Data source is just a hardcoded dict

## POC Goal
This POC works on

- BDD
- feature files
- Page Object Model with one dedicated file for code and another one for selectors
- Desktop / Mobile ambivalence
- Reports with screenshots


## REPORT

Json report can be found at "reports/report.json"


## Exiting virtual env

1. exit