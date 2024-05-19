from setuptools import find_packages, setup
from typing import List

# Constant for hyphen dot e
HYPHEN_E_DOT = "-e ."

# Function to read the requirements file
def get_requirements(file_path:str) -> List[str]:
    '''
    This function will return the list of requirements
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements

# Setup will also be developed as a package
setup(
    name = "MLOps-Car-Price-Prediction", # Project Name
    version = "0.0.1",
    author = "Mayank Sharma",
    author_email = "mayank.sharma2410@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)