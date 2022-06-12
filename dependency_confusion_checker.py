from logging import WARNING
import requests

# for colored output
WARNING = '\033[93m'
OKGREEN = '\033[92m'
FAIL = '\033[91m'


def get_npm_version():
    # get url from user
    url = input("Enter the URL of package.json file : ")
    # url = url.replace("https://github.com/","https://raw.githubusercontent.com/")
    # url = url.replace("/blob/master/package.json", "/master/package.json")
    # 

    # call the url and parse the json file and get dependencies and version
    response = requests.get(url)
    data = response.json()
    print("\n\n")

    npm_url = "https://registry.npmjs.org/"
    # append each dependency with npm_url and get the status code of the response
    if(data['dependencies'] == None):
        print("No dependencies found in package.json")
    else:
        print("\nDependencies Version Checker\n")
        for i in data['dependencies']:
            npm_url_dep = npm_url + i
            response = requests.get(npm_url_dep)
            npm_json = response.json()
            if response.status_code == 200:

                package_json_dev_depenedency_version = data['dependencies'][i]
                npm_dependency_version = npm_json['dist-tags']['latest']

                package_json_dev_depenedency_version = package_json_dev_depenedency_version.replace(
                    "^", "")
                package_json_dev_depenedency_version = package_json_dev_depenedency_version.replace(
                    "@", "")
                if package_json_dev_depenedency_version != npm_dependency_version:
                    print(WARNING, "Old Version Found: ", i + " : " +
                          package_json_dev_depenedency_version + ", Current Version is : " + npm_dependency_version)
                else:
                    print(OKGREEN, "Up to date: ", i +
                          " : " + data['dependencies'][i])

            else:
                print(FAIL, "RCE FOUND! PACKAGE HAS BEEN REMOVED FROM THE NPM   => ", i)

    if(data['devDependencies'] == None):
        print("No devDependencies found in package.json")
    else:
        print("\nDev Dependency Version Checker\n")
        for i in data['devDependencies']:
            npm_url_dep = npm_url + i
            response = requests.get(npm_url_dep)
            npm_json = response.json()
            if response.status_code == 200:

                package_json_dev_depenedency_version = data['devDependencies'][i]
                npm_dependency_version = npm_json['dist-tags']['latest']

                package_json_dev_depenedency_version = package_json_dev_depenedency_version.replace(
                    "^", "")
                package_json_dev_depenedency_version = package_json_dev_depenedency_version.replace(
                    "@", "")
                if package_json_dev_depenedency_version != npm_dependency_version:
                    print(WARNING, "Old Version Found: ", i + " : " +
                          package_json_dev_depenedency_version + ", Current Version is : " + npm_dependency_version)
                else:
                    print(OKGREEN, "Up to date: ", i +
                          " : " + data['devDependencies'][i])

            else:
                print(FAIL, "RCE FOUND! PACKAGE HAS BEEN REMOVED FROM THE NPM   => ", i)


def main():
    while True:
        get_npm_version()
        print("Press q to quit.\n")
        ip = input("Package name: ")
        if ip == "q":
            break


main()
