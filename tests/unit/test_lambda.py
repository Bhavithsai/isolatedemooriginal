#Isolate_ec2_stack
import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_ec2 as ec2,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    )
from aws_cdk import (Fn, CfnOutput,Duration)
#from .basic_infra_dev_stack import BasicInfraDevStack
VPC_ID =  'vpc-0e38d2'
# IsolateEc2Stack(app, "IsolateEc2Stack", env=cdk.Environment(account="3171", region="eu-cl-1"), vpc_id=VPC_ID)
app = cdk.App()
# accountid = app.node.try_get_context("accountid")
# region = app.node.try_get_context("region")
# vpc_id = app.node.try_get_context("VPC-ID")

env_EU = cdk.Environment(account="131", region="eu-central-1")

import unittest
from ec2_isolation_cdk_demo.ec2_isolate import IsolateEc2Stack

class TestIsolateEc2Stack(unittest.TestCase):

    def test_sns_topic_created(self):
        app = cdk.App()
        stack = IsolateEc2Stack(app, "IsolateEc2Stack",env=env_EU,vpc_id=VPC_ID)
        
        # Assertions
        self.assertIsNotNone(stack.notification_SNS_topic)
        self.assertEqual(stack.notification_SNS_topic.topic_name, "teamC-topic")
        self.assertEqual(len(stack.notification_SNS_topic.subscriptions), 1)
        self.assertEqual(stack.notification_SNS_topic.subscriptions[0].endpoint, "bhavith.sai.poola@op.fi")
    
    def test_isolation_security_group_created(self):
        app = cdk.App()
        stack =IsolateEc2Stack(app, "IsolateEc2Stack",env=env_EU,vpc_id=VPC_ID)
        

    #     # Assertions
        security_group_rules = stack.isolation_sg.connections.allow_from_any_ipv4(
        port_range=ec2.Port.tcp(22)
        )

    # # Assertions
    #     self.assertIsNotNone(stack.isolation_sg)
    #     self.assertEqual(len(security_group_rules), 1)
    #     self.assertEqual(security_group_rules[0].port, 22)
    #     self.assertEqual(security_group_rules[0].description, "10.241.7.231/32")
        self.assertIsNotNone(stack.isolation_sg)
        # self.assertEqual(stack.isolation_sg.connections.allow_from_any_ipv4[0].port, 22)
        self.assertEqual(stack.isolation_sg.connections.allow_from_any_ipv4[0].description, "10.241.7.231/32")
    
    def test_termination_protection_enabled(self):
        app = cdk.App()
        stack = IsolateEc2Stack(app, "IsolateEc2Stack",env=env_EU,vpc_id=VPC_ID)
        
        # Assertions
        self.assertIsNotNone(stack.EC2_termination_protection)
        self.assertEqual(stack.EC2_termination_protection.service, "ec2")
        self.assertEqual(stack.EC2_termination_protection.action, "modifyInstanceAttribute")
        self.assertEqual(stack.EC2_termination_protection.parameters["DisableApiTermination"]["Value"], "true")
    
    # Add more test cases for other components and functionality
    
if __name__ == '__main__':
    unittest.main()
