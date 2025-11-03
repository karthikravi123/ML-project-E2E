from setuptools import find_packages,setup
from typing import List

HYEN_E_DOT ='-e .'

def get_requirements(file_path:str)->List[str]:
    
    """
    this function will return list of requiremnts
    """
    requirements= []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        ##it wil have \n will replace with blank
        requirements =  [req.replace("\n","") for req in requirements]

        if HYEN_E_DOT in requirements:
            requirements.remove(HYEN_E_DOT)
           

setup(
    name= 'mlproject',
    version='0.0.1',
    author='karthik',
    author_email='geokarthik09@gmail.com',
    packages=find_packages(),
    install_requires= get_requirements('requirements.txt'),

)