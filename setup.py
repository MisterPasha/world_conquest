from setuptools import setup, find_packages

setup(
    name="World Conquest",
    version="0.1",
    packages=find_packages(),
    long_description=open("README.md").read(),
    install_requires=[
        "numpy",
        "requests",
        "pygame",
    ],
    extras_require={
        "dev": [
            "pytest",
            "sphinx",
        ]
    },
    classifiers=[],
)
# Finished
