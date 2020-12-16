import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="corsair",
    version="0.1.0",
    author="esynr3z",
    author_email="esynr3z@gmail.com",
    description="Control and Status Register map generator for FPGA/ASIC projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/esynr3z/corsair",
    project_urls={
        'Documentation': 'https://corsair.readthedocs.io'
    },
    packages=setuptools.find_packages(),
    install_requires=[
        'pyyaml'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
