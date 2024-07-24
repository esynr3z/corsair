import setuptools
from pkg_resources import parse_version

VERSION = "1.0.4"


# Based on https://github.com/tulip-control/dd/blob/885a716a56e82bfee54b0178d0ce38298b85eb6a/setup.py#L68
def git_version(version):
    """Return version with local version identifier."""
    import git

    try:
        repo = git.Repo('.git')
    except git.NoSuchPathError:
        # Not in a git repo, assume install through PyPI / source distribution
        return version

    repo.git.status()
    # assert versions are increasing
    try:
        latest_tag = repo.git.describe(
            match='v[0-9]*', tags=True, abbrev=0)
    except git.exc.GitCommandError:
        # No tags found
        latest_tag = version
    assert parse_version(latest_tag) <= parse_version(version), (
        latest_tag, version)
    sha = repo.head.commit.hexsha[:8]
    if repo.is_dirty():
        return '{v}.dev0+{sha}.dirty'.format(
            v=version, sha=sha)
    # commit is clean
    # is it release of `version` ?
    try:
        tag = repo.git.describe(
            match='v[0-9]*', exact_match=True,
            tags=True, dirty=True)
    except git.GitCommandError:
        return '{v}.dev0+{sha}'.format(
            v=version, sha=sha)
    assert tag == 'v' + version, (tag, version)
    return version


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Get version
VERSION_FILE = 'corsair/_version.py'
try:
    version = git_version(VERSION)
except AssertionError:
    print('No git info: Assume release.')
    version = VERSION
with open(VERSION_FILE, 'w') as f:
    f.write("version = '%s'\n" % version)

# Install package
setuptools.setup(
    name="corsair",
    version=version,
    author="esynr3z",
    author_email="esynr3z@gmail.com",
    description="Control and Status Register map generator for FPGA/ASIC projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/esynr3z/corsair",
    project_urls={
        'Documentation': 'https://corsair.readthedocs.io'
    },
    packages=setuptools.find_packages(exclude='tests'),
    package_data={'corsair': ['templates/*.j2']},
    entry_points={
        'console_scripts': [
            'corsair = corsair.__main__:main',
        ],
    },
    install_requires=[
        'pyyaml>=5.1',
        'jinja2',
        'wavedrom',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# Clear version info
with open(VERSION_FILE, 'w') as f:
    f.write("")
