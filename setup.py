import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = fh.read().split()
setuptools.setup(
    name="git_oras",
    version="0.0.1",
    description="LineageOS Builds",
    url="https://gitlab.com/lineageos/builder/ui.git",
    author_email="infra@lineageos.org",
    author="LineageOS Infrastructure Team",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"git_oras": "git_oras"},
    packages=setuptools.find_packages(),
    classifiers=("Programming Language :: Python 3",),
    install_requires=requirements,
    entry_points={'console_scripts': ['git-oras=git_oras.main:cli']}
)

