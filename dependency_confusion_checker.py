import os
import argparse
import json
from tabnanny import verbose
try:
    from packaging import version
    import requests
    from colorama import Fore
except ImportError as e:
    print("Please install the required packages by typing:")
    print("pip install -r requirements.txt")
    exit(1)

# for colored output
WARNING = Fore.YELLOW
OKGREEN = Fore.GREEN
INFO = Fore.LIGHTBLUE_EX
EXCITEMENT = Fore.LIGHTGREEN_EX
ERROR = Fore.RED
RESET = Fore.RESET

parser = argparse.ArgumentParser(description="Dependency Confusion Checker")
group_inputfile = parser.add_mutually_exclusive_group(required=True)
group_inputfile.add_argument(
    "-u", '--url', help="URL of package.json file.", type=str)
group_inputfile.add_argument(
    "-f", '--file', help="Path to package.json file.", type=str)
parser.add_argument(
    "-o", "--output", help="Write output to a file. (default = stdout)", type=str)
parser.add_argument(
    "-t", "--type", help="Write only certain type of packages to file. (default = all)", choices=["outdated", "updated", "phantom"], type=str)
parser.add_argument("-q", "--quiet", help="Suppress output",
                    action="store_true")
parser.add_argument("-cv", "--check-vulns",
                    help="Check packages for known vulnerabilities (default = off)", action="store_true")
parser.add_argument("-v", "--verbose", help="Verbose", action="store_true")
args = parser.parse_args()

# setting options
url = args.url
file = args.file
output_file = args.output
out_type = args.type
check_vulns = args.check_vulns
quiet_mode = args.quiet
verbose = args.verbose


def custom_print(text, color):
    '''Prints the `text` in the specified color'''
    if not quiet_mode:
        print(color, text, RESET)


def check_deps(deps):
    '''Checks the dependencies version and returns a dictionary of packages, grouped by their type'''
    npm_url = "https://registry.npmjs.org/"
    out_dict = {"updated": [], "outdated": [], "phantom": []}
    if deps == None:
        custom_print("[-] No dependencies found in package.json", WARNING)
        return out_dict
    custom_print("[+] Checking package versions...", INFO)
    for dep in deps:
        dep_url = npm_url + dep
        res = requests.get(dep_url)
        custom_print(f"[+] Checking package: {OKGREEN}{dep}", INFO)
        if res.status_code == 200:
            latest_version = version.parse(res.json()["dist-tags"]["latest"])
            package_version = version.parse(
                deps[dep].replace("^", "").replace("@", ""))
            if verbose:
                custom_print(
                    f"\t[+] Latest version: {OKGREEN}{latest_version}", INFO)
                if latest_version > package_version:
                    sign = f"{ERROR}-{OKGREEN}"
                else:
                    sign = f"="
                custom_print(
                    f"\t[+] Package version: {OKGREEN}{package_version} [{sign}]", INFO)
            if latest_version == package_version:
                out_dict["updated"].append(dep)
            else:
                out_dict["outdated"].append(dep)
        elif res.status_code == 404:
            out_dict["phantom"].append(dep)
        else:
            custom_print(
                f"[-]Error: Unknown status code {res.status_code}", ERROR)
    return out_dict


def get_packages_by_version(url):
    '''Resturns a dictionary of packages, grouped by their type'''

    if url != None:
        res = requests.get(url)
        input_json = res.json()
    elif file != None:
        with open(file) as f:
            input_json = json.load(f)
    else:
        print("[-] Error: No input file or url specified", ERROR)
        exit(1)
    out_dict = {"updated": [], "outdated": [], "phantom": []}
    if (input_json.get("dependencies") == None) and (input_json.get("devDependencies") == None):
        return None
    if(input_json.get("dependencies") != None):
        deps = input_json["dependencies"]
        out_dict.update(check_deps(deps))
    if(input_json.get("devDependencies") != None):
        dev_deps = input_json["devDependencies"]
        out_dict.update(check_deps(dev_deps))
    return out_dict


if __name__ == "__main__":
    '''Entry point'''
    print(f"{INFO}=== Dependency Confusion Checker ==={RESET}")
    print(f"{INFO}Press Ctrl + C to exit{RESET}")
    if quiet_mode and output_file != None:
        print(f"{INFO}Quiet mode enabled, suppressing output.{RESET}")
    elif quiet_mode and output_file == None:
        print(
            f"{ERROR}[-] Quite mode requires output filename (-o option) to write.{RESET}")
        exit(1)
    try:
        if output_file != None:
            if(os.path.exists(output_file)):
                custom_print(
                    f"[-] Output file {output_file} already exists", ERROR)
                choice = input(
                    f"{INFO}Do you want to overwrite it? [y/n] {RESET}")
                if not (choice.lower() == "y"):
                    custom_print("[-] Exiting...", ERROR)
                    exit(1)
        packages_version = get_packages_by_version(url)
        if output_file != None:
            with open(output_file, "w") as f:
                if out_type == None:
                    f.write(json.dumps(packages_version))
                else:
                    f.write(json.dumps(packages_version[out_type]))
        elif out_type != None:
            custom_print(
                f"[-] Output filename not provided, defaulting to 'out.json'", WARNING)
            with open("out.json", "w") as f:
                f.write(json.dumps(packages_version[out_type]))
        custom_print(f"\n\r=== Results ===", INFO)
        if packages_version == None:
            custom_print("[+] No packages found in package.json", INFO)
        else:
            if packages_version.get("phantom").__len__() > 0:
                custom_print("[💀] Phantom package(s) found!", EXCITEMENT)
                for package in packages_version.get("phantom"):
                    custom_print(f"[+] {EXCITEMENT}{package}", INFO)
            else:
                custom_print("[+] No phantom packages found", INFO)

            if packages_version.get("updated").__len__() > 0:
                custom_print("[👍] Up to date packages:", OKGREEN)
                for package in packages_version.get("updated"):
                    custom_print(f"[+] {OKGREEN}{package}", INFO)
            else:
                custom_print("[+] No up to date packages found", INFO)

            if packages_version.get("outdated").__len__() > 0:
                custom_print("[👎] Outdated packages:", WARNING)
                for package in packages_version.get("outdated"):
                    custom_print(f"[+] {WARNING}{package}", INFO)
            else:
                custom_print("[+] No outdated packages found", INFO)

    except KeyboardInterrupt:
        print(f"\n{ERROR}[-] User Interrupt!  Exiting...{RESET}")
        exit(0)
