#!/usr/bin/env python3

import aws_cdk as cdk

from ec2_isolation_cdk_demo.ec2_isolate import IsolateEc2Stack
from ec2_isolation_cdk_demo.basicinfradev import Ec2IsolationCdkDemoStack
#from ec2_isolation_cdk_demo.ec2_isolation_cdk_demo_stack import Ec2IsolationCdkDemoStack
#from ec2_isolation_cdk_demo.pipeline_stack import PipelineStack
#INSTANCE_ID = 'i-02794c41318d77d39'
# VPC_ID =  'vpc-03941e18a3dde38d2'
app = cdk.App()

accountid = app.node.try_get_context("accountid")
region = app.node.try_get_context("region")
vpc_id = app.node.try_get_context("VPC-ID")

env_EU = cdk.Environment(account=accountid, region=region)

IsolateEc2Stack(app, "IsolateEc2Stack",env=env_EU,vpc_id=vpc_id)
Ec2IsolationCdkDemoStack(app, "ec2-isolation-cdk-demo",env=env_EU,vpc_id=vpc_id)

# IsolateEc2Stack(app, "IsolateEc2Stack", env=cdk.Environment(account="317623606131", region="eu-central-1"), vpc_id=VPC_ID)
# Ec2IsolationCdkDemoStack(app, "ec2-isolation-cdk-demo",env=cdk.Environment(account="317623606131", region="eu-central-1"), vpc_id=VPC_ID)
app.synth()
