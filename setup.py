#This is what your ‘setup.py’ file should look like.
 
from setuptools import setup, find_packages
 
setup(
    name="mediapipe", #Name
    # version="19.22.1", #Version
    packages = find_packages()  # Automatically find the packages that are recognized in the '__init__.py'.
)

# 10.1.0 Pillow