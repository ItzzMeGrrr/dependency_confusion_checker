# dependency_confusion_checker
A tool to check dependency confusion vulnerability 

```
usage: dependency_confusion_checker.py [-h] -u URL [-o OUTPUT] [-t {outdated,updated,phantom}]

Dependency Confusion Checker

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL of package.json file.
  -o OUTPUT, --output OUTPUT
                        Output file name.
  -t {outdated,updated,phantom}, --type {outdated,updated,phantom}
                        Output only certain type of packages.

```