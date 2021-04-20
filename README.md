# snapshortanalyzer

This Project is used to manage AWS EC2 instance snapshots

## About

This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots

## Configuring 

shotty uses the configuration file created by the AWS cli. e.g

`aws configure --profile shotty`

## Running

`pipenv run python shotty/shotty.py <command> <sub-command> <--project=PROJECT>`

*command* is instances, volumes, snapshots
*sub-command* - depends on command
*PROJECT*  is optional
 
