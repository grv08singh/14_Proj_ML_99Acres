from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'
def get_requirements(file_path:str) -> list:
    # This function reads the requirements from the specified file and returns them as a list.
    try:
        with open(file_path, 'r') as f:
            requirements = f.read().splitlines()
            if HYPHEN_E_DOT in requirements:
                requirements.remove(HYPHEN_E_DOT)
            return requirements
    except FileNotFoundError:
        print(f"{file_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []


setup(
    name="Gurgaon Property ML Project",
    version="0.1",
    author='Grv',
    author_email='grv08singh@gmail.com',
    packages=find_packages(),
    
    #install_requires=[
    #    'numpy',
    #    'pandas',
    #    'scikit-learn',
    #    'matplotlib',
    #    'seaborn'
    #]
    # OR a better way is to read the requirements from a file, which is more maintainable:

    install_requires=get_requirements('requirements.txt')
)