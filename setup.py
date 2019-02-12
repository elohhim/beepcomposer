"""Setup beepcomposer module."""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='beepcomposer',
    version="0.1.0",
    author="Jan Kumor",
    author_email='elohhim@gmail.com',
    license='MIT',
    description="Small module to play melodies with OS beep functionality.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/elohhim/beepcomposer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ],
)
