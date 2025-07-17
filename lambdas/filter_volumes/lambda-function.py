import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    response = ec2.describe_volumes(
        Filters=[
            {'Name': 'volume-type', 'Values': ['gp2']},
            {'Name': 'tag:AutoConvert', 'Values': ['true']}
        ]
    )

    volumes = []
    for volume in response['Volumes']:
        volumes.append({
            "VolumeId": volume['VolumeId'],
            "Size": volume['Size'],
            "Attachments": volume['Attachments'],
            "Region": ec2.meta.region_name
        })

    return {"Volumes": volumes}
