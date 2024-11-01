from setuptools import setup, find_packages


setup(
    name="openaiflow",
    version="0.1.3-alpha",
    description="A Python wrapper for OpenAI API interactions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ikotun Collins",
    author_email="",
    url="https://github.com/ikotun-dev/openaiflow",
    packages=find_packages(),
    install_requires=[
        "annotated-types",
        "anyio",
        "certifi",
        "charset-normalizer",
        "distro",
        "h11",
        "httpcore",
        "httpx",
        "idna",
        "jiter",
        "openai",
        "pydantic",
        "pydantic-core",
        "python-dotenv",
        "requests",
        "sniffio",
        "tqdm",
        "typing_extensions",
        "urllib3",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
)
