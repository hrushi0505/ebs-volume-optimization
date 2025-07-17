import boto3
import datetime
import json
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('VolumeConversionLogs')

    for vol in event['Volumes']:
        vol_id = vol['VolumeId']
        try:
            ec2.modify_volume(VolumeId=vol_id, VolumeType='gp3')
            
            table.put_item(Item={
                "VolumeId": vol_id,
                "ConvertedAt": datetime.datetime.utcnow().isoformat(),
                "Region": vol['Region']
            })

            sns.publish(
                TopicArn='arn:aws:sns:us-east-1:123456789012:MyTopic',
                Subject="EBS Volume Converted",
                Message=f"Successfully converted volume {vol_id} from gp2 to gp3 in {vol['Region']}"
            )
        except ClientError as e:
            sns.publish(
                TopicArn='arn:aws:sns:us-east-1:123456789012:MyTopic',
                Subject="EBS Volume Conversion Failed",
                Message=f"Failed to convert volume {vol_id}: {str(e)}"
            )
