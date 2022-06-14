# dependency_confusion_checker
A tool to check dependency confusion vulnerability 

```
usage: dependency_confusion_checker.py [-h] [-w WRITE] [-t {outdated,updated,phantom}] [-q] [-cv] url

Dependency Confusion Checker

positional arguments:
  url                   URL of package.json file.

optional arguments:
  -h, --help            show this help message and exit
  -w WRITE, --write WRITE
                        Write output to a file. (default = stdout)
  -t {outdated,updated,phantom}, --type {outdated,updated,phantom}
                        Write only certain type of packages to file. (default = all)
  -q, --quiet           Suppress output
  -cv, --check-vulns    Check packages for known vulnerabilities (default = off)
```