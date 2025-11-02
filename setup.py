'''
It defines the project’s configuration, including metadata and dependencies, using setuptools.
'''

from setuptools import setup,find_packages
from typing import List

def get_requirements():
    lt = []
    try:
        with open("requirements.txt","r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement!="" and requirement!="-e .":
                    lt.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file is not present")   

    return lt    

setup(
    name = "Network Security Project",
    version = "0.0.1",
    author= "Devansh Pratap Singh",
    packages = find_packages(),
    install_reqires = get_requirements()
)          