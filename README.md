# dependency_confusion_checker
A tool to check dependency confusion vulnerability.


What is Dependency Confustion?
A Dependency Confusion attack or supply chain substitution attack occurs when a software installer script is tricked into pulling a malicious code file from a public repository instead of the intended file of the same name from an internal repository.

For more info read this [article](https://dhiyaneshgeek.github.io/web/security/2021/09/04/dependency-confusion/)
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
