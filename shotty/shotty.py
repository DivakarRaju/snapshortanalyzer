import boto3

if __name__ == '_main_':
session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

for i in ec2.instances.all():
    print(i)