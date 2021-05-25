import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="dicom_to_cnn",                     # This is the name of the package
    version="0.63",                        # The initial release version
    author="",                     # Full name of the author
    description="Python Library to handle Input / Output conversion in Dicom <=> Convolutional Neural Network ",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    url = 'https://github.com/wendyrvllr/Dicom-To-CNN',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/wendyrvllr/Dicom-To-CNN/archive/refs/tags/62.tar.gz',
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.7',                # Minimum version requirement of the package
    install_requires=['cycler==0.10.0',
                    'decorator==4.4.2',
                    'docopt==0.6.2',
                    'imageio==2.9.0',
                    'kiwisolver==1.3.1',
                    'matplotlib==3.4.2',
                    'networkx==2.5.1',
                    'numpy>=1.19',
                    'Pillow==8.2.0',
                    'pydicom==2.1.2',
                    'pykwalify==1.8.0',
                    'pyparsing==2.4.7',
                    'pyradiomics==3.0.1',
                    'python-dateutil==2.8.1',
                    'PyWavelets==1.1.1',
                    'ruamel.yaml==0.17.4',
                    'ruamel.yaml.clib==0.2.2',
                    'scikit-image==0.18.1',
                    'scipy==1.6.3',
                    'SimpleITK==2.0.2',
                    'tifffile==2021.4.8']                     # Install other dependencies if any
)