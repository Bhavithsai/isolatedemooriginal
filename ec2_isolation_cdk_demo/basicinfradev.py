from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_sns as sns,
    aws_lambda as _lambda,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancing  as elb,
    aws_sns_subscriptions as subs
)
import boto3
import aws_cdk as core

app = core.App()

class Ec2IsolationCdkDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,vpc_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = ec2.Vpc.from_lookup(self,"VPC",vpc_id = vpc_id)
        # vpc = app.node.try_get_context("VPC-ID")
        instance = ec2.Instance(
            self,
            "myinfradevec2instance-alpha",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=self.vpc
        )
        # if not  instance.instance.instance_initiated_shutdown_behavior:
        #     instance_shutdown_behavior = ec2.InstanceInitiatedShutdownBehavior.STOP
        #     print("Termination protection enabled for the instance.")
        # else:
        #     print("Termination protection is already enabled for the instance.")
        # isolation_sg = ec2.SecurityGroup(
        #         self, 'IsolationSecurityGroup-alpha',
        #         vpc=vpc,
        #         description='Isolation Security Group team dev'
        #     )
        # isolation_sg.add_ingress_rule(
        # ec2.Peer.any_ipv4(), ec2.Port.tcp(22))
        
        auto_scaling_group = autoscaling.AutoScalingGroup(
            self,
            "MyAutoScalingGroup-gama",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image=ec2.AmazonLinuxImage(),
            desired_capacity=2,
            vpc=self.vpc,
            min_capacity=2,
            max_capacity=3
        )  
        Isolate_loadbalancing = elb.LoadBalancer(self, "Isolate_loadbalancing",
        vpc=self.vpc,
        subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC), 
        #internet_facing=True,
        health_check=elb.HealthCheck(port=80)
        )
        #Isolate_Instance_LB.add_target(elb.InstanceTarget(Isolate_Instance))
        Isolate_loadbalancing.add_target(auto_scaling_group)
        Isolate_loadbalancing.add_listener(external_port=80)