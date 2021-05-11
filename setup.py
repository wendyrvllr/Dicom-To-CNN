import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="dicom_to_cnn",                     # This is the name of the package
    version="0.59",                        # The initial release version
    author="",                     # Full name of the author
    description="Python Library to handle Input / Output conversion in Dicom <=> Convolutional Neural Network ",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    url = 'https://github.com/wendyrvllr/Dicom-To-CNN',   # Provide either the link to your github or to your website
<<<<<<< HEAD
    download_url = 'https://github.com/wendyrvllr/Dicom-To-CNN/archive/refs/tags/57.tar.gz',
=======
    download_url = 'https://github.com/wendyrvllr/Dicom-To-CNN/archive/refs/tags/58.tar.gz',
>>>>>>> 72aadc067ed28d8194cffd0c0bcfbf9bdfbc1fe2
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.7',                # Minimum version requirement of the package
    install_requires=[]                     # Install other dependencies if any
)