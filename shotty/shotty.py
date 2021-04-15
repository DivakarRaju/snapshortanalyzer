import boto3
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
def list_snapshots(project):
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
    return


@snapshots.command("create",
                   help="Creates snapshots of all volumes")
@click.option('--project', default=None,
              help="List the volume of the instances")
def create_snapshots(project):
    "Create snapshots for EC2 instances"

    instances = filter_instances(project)
    for i in instances:
        i.stop()
        for v in i.volumes.all():
            print("Creating snaphots for volume {0}".format(v.id))
            v.create_snapshot(Description="Created by snapshotAlyzer 30000")
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
        i.stop()
    return


@instances.command("start")
@click.option('--project', default=None,
              help="Only instances for project (tag project:<name>)")
def start_instance(project):
    "Starts the instance"
    instances = filter_instances(project)
    for i in instances:
        print("Starting {0} instance".format(i.id))
        i.start()
    return


if __name__ == '__main__':
    cli()
