from setuptools import find_packages  # or find_namespace_packages

import os
import re
import json


source_root = "deviceos"

version_pattern = r"__version__\s*=\s*['\"](.*)['\"]"  # chatGPT, modifed


packages=find_packages(
    where=source_root,
    # include=['mypackage*'],  # ['*'] by default
    # exclude=['mypackage.tests'],  # empty by default
) + [""]  # add "root" package, for collecting __init__.py


output = {
    "urls": [],
    "deps": ["umqtt.simple"],
}
for package in packages:

    path = os.path.join(source_root, package.replace(".", "/"))

    files = os.listdir(path)

    for file in files:

        if file == "__pycache__":
            continue

        source_path = f"{path}/{file}".replace("\\", "/")
        url = f"github:ljbeal/DeviceOS/{source_path}"

        output["urls"].append([source_path, url])

        if file == "__init__.py":
            with open(source_path, encoding="utf8") as o:
                source = o.read()

                match = re.search(version_pattern, source)
                if match:
                    output["version"] = match.group(1)

if "version" not in output:
    raise RuntimeError("version was not extracted")


with open("package.json", "w+", encoding="utf8") as o:
    json.dump(output, o, indent=2)
