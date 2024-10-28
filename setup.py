from setuptools import setup, find_packages

setup(
    name="openaiflow",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "requests",
        "python-dotenv",
    ],
    test_suite="tests",
)
