from setuptools import setup

setup(
    name = "snapshotanalyzer",
    version='0.1',
    author="Divakar Raju",
    author_email="divakarrj875@gmail.com",
    description="snapshotanalyzer is a tool to manage AWS EC2 snapshots",
    packages=['shotty'],
    url="https://github.com/DivakarRaju/snapshortanalyzer",
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
    ''',

 )