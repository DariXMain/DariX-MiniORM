from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="DariX-MiniORM",
    version="1.0.0",
    author="DariXmain",
    author_email="DariXMain9@gmail.com",
    description="Lightweight MySQL ORM wrapper for rapid backend development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DariXmain/DariX-MiniORM",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Database :: Front-Ends",
    ],
    python_requires=">=3.7",
    install_requires=[
        "mysql-connector-python>=8.0.0",
    ],
    keywords="mysql orm database wrapper",
)
