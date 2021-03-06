import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="labdrivers",
    version="0.1.0",
    author="Callum Doolin, Hugh Ramp",
    author_email="doolin@ualberta.ca",
    description="Collection of scripts for running experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires = ['numpy', 'scipy', 'websocket-client', 'pyserial'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent",
    ],
)