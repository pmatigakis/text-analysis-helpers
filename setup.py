from setuptools import setup, find_packages


def get_long_description():
    with open("README.md", "r") as f:
        return f.read()


def read_requirements_file(filename):
    with open(filename) as f:
        return [
            line.strip()
            for line in f
            if not line.startswith("-e")
        ]


setup(
    name="text-analysis-helpers",
    version="0.1.0",
    author="Panagiotis Matigakis",
    author_email="pmatigakis@gmail.com",
    description="Collection of classes and functions for text analysis",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/pmatigakis/text-analysis-helpers",
    packages=find_packages(exclude=["tests"]),
    install_requires=read_requirements_file("requirements.txt"),
    tests_require=read_requirements_file("requirements-test.txt"),
    test_suite="nose.collector",
    zip_safe=False,
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
