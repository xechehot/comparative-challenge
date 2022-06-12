# comparative-challenge
Take Home challenge solution.

## Installation
I am using pipenv to manage virtualenv and packages, so you need to have it on your system.

To install all required packages, run:
```
pipenv install
```
Then to spawn a shell with virtualenv, run:
```commandline
pipenv shell
```
## Usage
There is only one parameter: `path` to the file with the user data in csv format.
Here is an example:
```commandline
python main.py --path data/users_data.csv
```
