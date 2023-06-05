# import unittest

# #from basicinfradev import Ec2IsolationcdkDemoStack
# import aws_cdk as cdk
# from constructs import Construct
# from aws_cdk import (
#     Stack,
#     aws_stepfunctions as sfn,
#     aws_stepfunctions_tasks as tasks,
#     aws_ec2 as ec2,
#     aws_sns as sns,
#     aws_sns_subscriptions as subscriptions,
#     )
# from aws_cdk import (Fn, CfnOutput,Duration)
# import aws_cdk.assertions as assertions
# from ec2_isolation_cdk_demo.ec2_isolate import IsolateEc2Stack
# from ec2_isolation_cdk_demo.basicinfradev import Ec2IsolationCdkDemoStack
# VPC_ID =  'vpc-03941e18a3dde38d2'
# app = cdk.App()
# ec2_isolate_stack_test = IsolateEc2Stack(app, "IsolateEc2Stack", env=cdk.Environment(account="317623606131", region="eu-central-1"), vpc_id=VPC_ID)
# ec2_isolate_stack_template = assertions.Template.from_stack(ec2_isolate_stack_test)
# import boto3

# def check_and_delete_security_group(security_group_id):
#     ec2_client = boto3.client('ec2')
    
#     try:
#         response = ec2_client.describe_security_groups(GroupIds=[security_group_id])
#         if response['SecurityGroups']:
#             # Security group exists, delete it
#             ec2_client.delete_security_group(GroupId=security_group_id)
#             print(f"Security group {security_group_id} deleted successfully.")
#         else:
#             print(f"Security group {security_group_id} does not exist.")
#     except ec2_client.exceptions.ClientError as e:
#         if e.response['Error']['Code'] == 'InvalidGroup.NotFound':
#             print(f"Security group {security_group_id} does not exist.")
#         else:
#             # Handle other errors if needed
#             print(f"Error occurred: {e}")

# # Provide the security group ID you want to test
# security_group_id = 'sg-0394c7bd577a615be'