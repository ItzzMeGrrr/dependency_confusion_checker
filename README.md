# dependency_confusion_checker
A tool to check dependency confusion vulnerability 

```
usage: dependency_confusion_checker.py [-h] [-o OUTPUT] [-t {outdated,updated,phantom}] url

Dependency Confusion Checker

positional arguments:
  url                   URL of package.json file.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file name.
  -t {outdated,updated,phantom}, --type {outdated,updated,phantom}
                        Output only certain type of packages.

```