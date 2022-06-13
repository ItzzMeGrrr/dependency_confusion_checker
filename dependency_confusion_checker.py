import os
import argparse
import json
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
parser.add_argument('url',help="URL of package.json file.")
parser.add_argument("-o", "--output", help="Output file name.", type=str)
parser.add_argument(
    "-t", "--type", help="Output only certain type of packages.", choices=["outdated", "updated", "phantom"], type=str)
args = parser.parse_args()


def custom_print(text, color):
    '''Prints the text in the specified color'''
    print(color, text, RESET)


def check_deps(deps):
    '''Checks the dependencies version and returns a dictionary of packages grouped by their type'''
    npm_url = "https://registry.npmjs.org/"
    out_dict = {"updated": [], "outdated": [], "phantom": []}
    if deps == None:
        custom_print("[-] No dependencies found in package.json", WARNING)
        return out_dict
    custom_print("[+] Checking dependencies version", INFO)
    for dep in deps:
        dep_url = npm_url + dep
        res = requests.get(dep_url)
        custom_print(f"[+] Checking dependency: {OKGREEN}{dep}", INFO)
        if res.status_code == 200:
            latest_version = version.parse(res.json()["dist-tags"]["latest"])
            package_version = version.parse(
                deps[dep].replace("^", "").replace("@", ""))
            custom_print(
                f"\t[+] Latest version: {OKGREEN}{latest_version}", INFO)
            custom_print(
                f"\t[+] Package version: {OKGREEN}{package_version}", INFO)
            if latest_version == package_version:
                out_dict["outdated"].append(dep)
            else:
                out_dict["updated"].append(dep)
        elif res.status_code == 404:
            out_dict["phantom"].append(dep)
        else:
            custom_print(
                f"[-]Error: Unknow status code {res.status_code}", ERROR)
    return out_dict


def get_packages_by_version(url):
    '''Resturns a dictionary of packages grouped by their type'''
    res = requests.get(url)
    res_json = res.json()
    out_dict = {"updated": [], "outdated": [], "phantom": []}
    if(res_json.get("dependencies") != None):
        deps = res.json()["dependencies"]
        out_dict.update(check_deps(deps))
    if(res_json.get("devDependencies") != None):
        dev_deps = res.json()["devDependencies"]
        out_dict.update(check_deps(dev_deps))
    return out_dict


if __name__ == "__main__":
    '''Entry point'''
    custom_print("=== Dependency Confusion Checker ===", INFO)
    custom_print("Press Ctrl + C to exit", INFO)
    try:
        url = args.url
        output = args.output
        if(os.path.exists(output)):
            custom_print(f"[-] Output file {output} already exists", ERROR)
            choice = input(f"{INFO}Do you want to overwrite it? [y/n] {RESET}")
            if not (choice == "y" or choice == "Y"):
                custom_print("[-] Exiting...", ERROR)
                exit(1)
        out_type = args.type
        packages_version = get_packages_by_version(url)
        if output != None:
            with open(output, "w") as f:
                if out_type == None:
                    f.write(json.dumps(packages_version))
                else:
                    f.write(json.dumps(packages_version[out_type]))
        elif out_type != None:
            custom_print(
                f"[+] Output filename not provided, defaulting to 'out.json'", WARNING)
            with open("out.json", "w") as f:
                f.write(json.dumps(packages_version[out_type]))

        if packages_version.get("phantom").__len__() > 0:
            custom_print("[💀] Phantom package(s) found!", EXCITEMENT)
            for package in packages_version.get("phantom"):
                custom_print(f"[+] {EXCITEMENT}{package}", INFO)

        if packages_version.get("updated").__len__() > 0:
            custom_print("[👍] Up to date packages:", OKGREEN)
            for package in packages_version.get("updated"):
                custom_print(f"[+] {OKGREEN}{package}", INFO)

        if packages_version.get("outdated").__len__() > 0:
            custom_print("[👎] Outdated packages:", WARNING)
            for package in packages_version.get("outdated"):
                custom_print(f"[+] {WARNING}{package}", INFO)
    except KeyboardInterrupt:
        custom_print(f"\n[-] User Interrupt!  Exiting...", ERROR)
        exit(0)
