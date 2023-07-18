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
# VPC_ID =  'vpc-03948d2'
# app = cdk.App()
# ec2_isolate_stack_test = IsolateEc2Stack(app, "IsolateEc2Stack", env=cdk.Environment(account="306131", region="eu-al-1"), vpc_id=VPC_ID)
# ec2_isolate_stack_template = assertions.Template.from_stack(ec2_isolate_stack_test)



# class TestEC2Management(unittest.TestCase):
    
#     def test_check_and_enable_termination_protection(self):
#         # Mock the describe_instance_attribute response
#         response ={
#             'DisableApiTermination': {
#                 'Value': False 
#             },
#         }
# # #    check_and_enable_termination_protection('i-00abe0f74')
#     # def test_tag_ec2_instance(self):
#     # # Create an instance.
#     #     env=cdk.Environment(account="31131", region="eu-central-1")
#     #     stack = Ec2IsolationCdkDemoStack(app, "ec2-isolation-cdk-demo", env= env,vpc_id=VPC_ID)
#     #     template = assertion.Template.from_stack(stack)
#     #         # Assert that the instance is tagged.
#     #     assert cdk.Tags.of(instance).get("status") == "quarantined"

#     def test_stack_creation(self):
#         stack = ec2_isolate_stack_test
#         template = assertions.Template.from_stack(ec2_isolate_stack_test)
#         # Assert that the stack has been created
#         self.assertIsNotNone(ec2_isolate_stack_test)

#         # Assert the number of resources in the stack
#         self.assertEqual(len(ec2_isolate_stack_test.node.children),30)  # Assuming only one construct in the stack

#         # Assert the specific resources created in the stack
#         # Modify the assertions based on your specific resource expectations
#         self.assertIsInstance(ec2_isolate_stack_test.node.children[0], sns.Topic)  # SNS Topic
#         self.assertIsInstance(ec2_isolate_stack_test.node.children[1], tasks.CallAwsService)  # Instance Metadata task
