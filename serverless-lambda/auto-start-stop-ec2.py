import json
import boto3
import botocore
ec2 = boto3.client("ec2", region_name="ap-southeast-1")

def lambda_handler(event, context):
    # TODO implement
    
    instance_id = event['instance_id']
    action = event['action']
    
    if action == 'START':
        # Dry run succeeded, run start_instances without dryrun
        try:
            response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except Exception as e:
            print(e)
    if action == 'STOP':
        try:
            response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except Exception as e:
            print(e)
            
    return {
        'statusCode': 200,
        'body': json.dumps('Complete modify EC2 status as your requested!')
    }
    
# To trigger this fucntion, input below json:
# {
#     "instance_id": "<Your instance ID>",
#     "action": "<START or STOP>"
# }
# Example 1
# {
#     "instance_id": "i-08364cc10f525e95c",
#     "action": "STOP"
# }
# Example 2
# {
#     "instance_id": "i-08364cc10f525e95c",
#     "action": "START"
# }