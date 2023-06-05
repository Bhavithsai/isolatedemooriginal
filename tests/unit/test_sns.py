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
# # ec2_isolate_stack_test = IsolateEc2Stack(app, "IsolateEc2Stack", env=cdk.Environment(account="317623606131", region="eu-central-1"), vpc_id=VPC_ID)
# # ec2_isolate_stack_template = assertions.Template.from_stack(ec2_isolate_stack_test)

# class TestEc2IsolationCdkDemoStack(unittest.TestCase):
    
    # def test_sns_topic_configuration(self):
    #     stack = ec2_isolate_stack_test
    #     template = assertions.Template.from_stack(ec2_isolate_stack_test)    
    #     self.assertIsNotNone(stack.notification_SNS_topic)
    #     self.assertIsNotNone(stack.notification_SNS_topic.subscriptions)
    #     self.assertEqual(len(stack.notification_SNS_topic.subscriptions), 1)
    #     subscription = stack.notification_SNS_topic.subscriptions[0]
    #     self.assertIsInstance(subscription, sns.CfnSubscription)
    #     self.assertEqual(subscription.protocol, 'email')
    #     self.assertEqual(subscription.endpoint, 'bhavith.sai.poola@op.fi')

    # def test_sns_topic_configuration(self):
    #     ec2_isolate_stack_test = IsolateEc2Stack(app, "IsolateEc2Stack",env=cdk.Environment(account="317623606131", region="eu-central-1"), vpc_id=VPC_ID)
    #     ec2_isolate_stack_template = assertions.Template.from_stack(ec2_isolate_stack_test)

    #     self.assertIsNotNone(ec2_isolate_stack_test.notification_SNS_topic)
    #     self.assertIsNotNone(ec2_isolate_stack_test.notification_SNS_topic.subscriptions)
    #     self.assertEqual(len(ec2_isolate_stack_test.notification_SNS_topic.subscriptions), 1)
        
    #     subscription = ec2_isolate_stack_test.notification_SNS_topic.subscriptions[0]
    #     self.assertIsInstance(subscription, subscriptions.EmailSubscription)
    #     self.assertEqual(subscription.endpoint, "bhavith.sai.poola@op.fi")
    # def test_sns_topic_subscription(self):
    #     ec2_isolate_stack_test = IsolateEc2Stack(app, "IsolateEc2Stack",env=cdk.Environment(account="317623606131", region="eu-central-1"), vpc_id=VPC_ID)
    
    #     # Get the SNS topic ARN from the stack
    #     topic_arn = ec2_isolate_stack_test.notification_SNS_topic_arn
    
    #     # Assert that the SNS topic ARN is not None
    #     self.assertIsNotNone(topic_arn)
        
    #     # Get the SNS topic from the ARN
    #     topic = sns.Topic.from_topic_arn(self, "SNS topic", topic_arn)
    
    #     # Add any additional assertions as needed
    #     self.assertEqual(topic.topic_name, "teamC-topic")
    
    #     # Get the subscriptions of the SNS topic
    #     subscriptions = topic.subscriptions
    
    #     # Assert that there is at least one subscription
    #     self.assertGreater(len(subscriptions), 0)
    
    #     # Iterate over the subscriptions and check if there is an email subscription
    #     email_subscription_found = False
    #     for subscription in subscriptions:
    #         if isinstance(subscription, subscriptions.EmailSubscription):
    #             # Assert the email address
    #             self.assertEqual(subscription.endpoint, "bhavith.sai.poola@op.fi")
    #             email_subscription_found = True
    #             break
    
    #     # Assert that an email subscription was found
    #     self.assertTrue(email_subscription_found)