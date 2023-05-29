#!/usr/bin/env python3

import aws_cdk as cdk

from ec2_isolation_cdk_demo.ec2_isolation_cdk_demo_stack import Ec2IsolationCdkDemoStack


app = cdk.App()
Ec2IsolationCdkDemoStack(app, "ec2-isolation-cdk-demo")

app.synth()
