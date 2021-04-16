import boto3
import botocore
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')


def filter_instances(project):
    "Filters instaces based on the tags"
    instances = []
    if project:
        filters = [{'Name': 'tag:project', 'Values': [project]}]
        instances = ec2.instances.filter(Filters=filters)

    else:
        instances = ec2.instances.all()
    return instances


@click.group()
def cli():
    "Shotty manages these snapshots"


@cli.group("snapshots")
def snapshots():
    "commands for snapshots"


@snapshots.command("list")
@click.option('--project', default=None,
              help="List the volume of the instances")
@click.option("--all",'list_all', default=False , is_flag=True,
              help="Lists all snapshots for each volume not just the recent one")
def list_snapshots(project, list_all):
    "List the snapshots of the volumes"
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(', '.join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))
                if s.state == "completed" and not list_all : break
    return


@snapshots.command("create",
                   help="Creates snapshots of all volumes")
@click.option('--project', default=None,
              help="List the volume of the instances")
def create_snapshots(project):
    "Create snapshots for EC2 instances"

    instances = filter_instances(project)
    for i in instances:
        print("Stopping {0} instance".format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            print(" Creating snaphots for volume {0}".format(v.id))
            v.create_snapshot(Description="Created by snapshotAlyzer 30000")

        print("Starting back {0} instance".format(i.id))
        i.start()
        i.wait_until_running()
    return


@cli.group("volumes")
def volumes():
    "command for volumes"


@volumes.command("list")
@click.option('--project', default=None,
              help="List the volume of the instances")
def list_volumes(project):
    "List the volumes of the instances"
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(', '.join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))

    return


@cli.group("instances")
def instances():
    "Command for instances"


@instances.command("list")
@click.option('--project', default=None,
              help="Only instances for project (tag project:<name>)")
def list_instances(project):
    "List EC2 instances"
    instances = filter_instances(project)
    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        print(','.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('project', '<no project>'))))

    return


@instances.command("stop")
@click.option('--project', default=None,
              help="Only instances for project (tag project:<name>)")
def stop_instances(project):
    "Stops the instances"
    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0} instance".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print(" Could not stop {0}. ".format(i.id) + str(e))
            continue
    return


@instances.command("start")
@click.option('--project', default=None,
              help="Only instances for project (tag project:<name>)")
def start_instance(project):
    "Starts the instance"
    instances = filter_instances(project)
    for i in instances:
        print("Starting {0} instance".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print(" Could not start {0}. ".format(i.id) + str(e))
            continue
    return


if __name__ == '__main__':
    cli()
