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
#VPC_ID =  'vpc-0bd4b61810acf1bbe'
app = cdk.App()

class IsolateEc2Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        #create SNS topic
        notification_SNS_topic = sns.Topic(self, "SNS topic", topic_name="teamC-topic")
        notification_SNS_topic.add_subscription(
            subscriptions.EmailSubscription("bhavith.sai.poola@op.fi")
        )
        
        #instance metadata collection
        instance_metadata = tasks.CallAwsService(self, "instance Metadata", 
            service = "ec2",
            action = "describeInstances",
            parameters = {
                "InstanceIds" : sfn.JsonPath.string_at("States.Array($.InstanceId)")
            },
            iam_resources = ["*"],
            result_path = sfn.JsonPath.string_at("$.InstanceDescription"),
        )
        
        # Check tag value quarantined
        instance_tags_check = tasks.CallAwsService(self, "check quarantined tags",
            service = "ec2",
            action = "describeTags",
            parameters = {
                "Filters" : [
                     {
                        "Name" : "resource-id",
                        "Values" : sfn.JsonPath.string_at("States.Array($.InstanceId)")
                    },
        
                    {
                        "Name" : "value",
                        "Values" : [
                            "Quarantined"
                            ]
                    } 
                    ]   
                },
            
            iam_resources = ["*"],
            result_path = sfn.JsonPath.string_at("$.InstanceTags"),
        )
        
        #create isolation SG
        self.vpc = ec2.Vpc.from_lookup(self,"VPC",vpc_id = vpc_id)
        self.isolation_sg = ec2.SecurityGroup(
            self, "EC2IsolationSecurityGroup",vpc=self.vpc)

        self.isolation_sg.add_ingress_rule(
        peer = ec2.Peer.ipv4("10.241.7.231/32"),
        connection = ec2.Port.tcp(22),
        description = "Allow my IP"
        )
        
        #Enable termination protection
        EC2_termination_protection = tasks.CallAwsService(self, "Enable termination protection",
            service = "ec2",
            action = "modifyInstanceAttribute",
            parameters = {
                "InstanceId" : sfn.JsonPath.string_at("$.InstanceDescription.Reservations[0].Instances[0].InstanceId"),
                    "DisableApiTermination" : {
                        "Value" : "true"
                    }
            },
            iam_resources = ["*"],
            result_path = sfn.JsonPath.string_at("$.EnableTermination"),
        )
        
        #Check auto scaling group info
        auto_scaling_info = tasks.CallAwsService(self, "Get Autosacling Group Info",
            service = "autoscaling",
            action = "describeAutoScalingInstances",
            parameters = {
                "InstanceIds" : sfn.JsonPath.string_at("States.Array($.InstanceId)")
            },
            iam_resources = ["*"],
            result_path = sfn.JsonPath.string_at("$.AutoScalingResult")
        )
        
        #Detach EC2 from auto scaling group
        detach_ec2_from_asg =  tasks.CallAwsService(self, "Detch EC2 from ASG",
            service = "autoscaling",
            action = "detachInstances",
            parameters = {
                "AutoScalingGroupName" :  sfn.JsonPath.string_at("$.AutoScalingResult.AutoScalingInstances[0].AutoScalingGroupName"),
                "ShouldDecrementDesiredCapacity": "false",
                 "InstanceIds" : sfn.JsonPath.string_at("States.Array($.InstanceId)")
            },
            iam_resources = ["*"],
            result_path = sfn.JsonPath.string_at("$.DetachInstance")
        )
        
        #Create snapshot from isolated instance
        create_snapshot =  tasks.CallAwsService(self, "Create Snapshot from Isolated Instance",
            service = "ec2",
            action = "createSnapshot",
            parameters = {
                "VolumeId": sfn.JsonPath.string_at("$.InstanceDescription.Reservations[0].Instances[0].BlockDeviceMappings[0].Ebs.VolumeId")
            },
            iam_resources = ["*"],
            result_path = sfn.JsonPath.string_at("$.SnapshotId")
        )
        
        #create forensic instance
        create_forensic_instance = tasks.CallAwsService(self, " Forensics Instance",
            service = "ec2",
            action = "runInstances",
            parameters = {
                "MaxCount": 1,
                "MinCount": 1,
                "InstanceType": sfn.JsonPath.string_at("$.InstanceDescription.Reservations[0].Instances[0].InstanceType"),
                "ImageId": sfn.JsonPath.string_at("$.InstanceDescription.Reservations[0].Instances[0].ImageId"),
                "SubnetId": sfn.JsonPath.string_at("$.InstanceDescription.Reservations[0].Instances[0].NetworkInterfaces[0].SubnetId"),
                "SecurityGroupIds": [
                    self.isolation_sg.security_group_id
                ]
            },
            iam_resources=["*"],
            result_selector={
                "ForensicInstanceId": sfn.JsonPath.string_at("$.Instances[0].InstanceId")
            }
        )
        
        #verify snapshot creating snapshot
        get_snapshot_status = tasks.CallAwsService(self, "Get Snapshot status",
            service = "ec2",
            action = "describeSnapshots",
            parameters = {
              "SnapshotIds" : sfn.JsonPath.string_at("States.Array($.SnapshotId.SnapshotId)")
            },
            iam_resources = ["*"],
            result_path = sfn.JsonPath.string_at("$.SnapshotStatus"),
            result_selector = {
                "SnapshotState": sfn.JsonPath.string_at("$.Snapshots.[0].State")
            }
        )
        
        #Send Email about SnapshotID
        ###################################
        send_email_about_snapshotId = tasks.CallAwsService(self, "Send Email about SnapshotID",
            service = "sns",
            action = "publish",
            parameters = {
                "TopicArn" : notification_SNS_topic.topic_arn,
                "Message" : "Snapshot created"
            },
            iam_resources = ["*"]
        )
        
        #create EBS volume from Snapshot
        EBS_volume_from_snapshot =  tasks.CallAwsService(self, "Create EBS Volume from Snapshot",
            service = "ec2",
            action = "createVolume",
            parameters = {
                 "AvailabilityZone": sfn.JsonPath.string_at("$.InstanceDescription.Reservations[0].Instances[0].Placement.AvailabilityZone"),
                 "SnapshotId": sfn.JsonPath.string_at("$.SnapshotId.SnapshotId")
            },
             iam_resources = ["*"],
             result_path = sfn.JsonPath.string_at("$.Volumes")
        )
        
        #Check EBS volume creation
        ebs_volume_status_check = tasks.CallAwsService(self, "Get EBS Volume Status",
            service="ec2",
            action="describeVolumes",
            parameters = {
                "VolumeIds": sfn.JsonPath.string_at("States.Array($.Volumes.VolumeId)")
            },
            iam_resources = ["*"],
            result_path = sfn.JsonPath.string_at("$.VolumeDescription")
        )
        
        #attach volume to forensic instance
        attach_volume =  tasks.CallAwsService(self, "Attach Volume",
            service="ec2",
            action="attachVolume",
            parameters={
                "Device": "/dev/sdf",
                "InstanceId": sfn.JsonPath.string_at("$[0].ForensicInstanceId"),
                "VolumeId": sfn.JsonPath.string_at("$[1].Volumes.VolumeId")
            },
            iam_resources = ["*"],
            result_path = sfn.JsonPath.DISCARD
        )
                
        #attach isolation security group to instance - 
        modify_forencis_instance_sg = tasks.CallAwsService(self, "modify Instance SG",
            service = "ec2",
            action = "authorizeSecurityGroupIngress",
            parameters = {
                #"GroupId": sfn.JsonPath.string_at("$[1].InstanceDescription.Reservations[0].Instances[0].SecurityGroups[0].GroupId"),
                "GroupId": sfn.JsonPath.string_at("$[1].InstanceDescription.Reservations[0].Instances[0].NetworkInterfaces[0].Groups[0].GroupId"),
                #"GroupId" : self.isolation_sg.security_group_name,
                "IpPermissions": [
                    {
                        "IpProtocol": "-1",
                        "FromPort": -1,
                        "UserIdGroupPairs": [
                            {
                                "GroupId": self.isolation_sg.security_group_id
                            }
                        ]
                    }
                ]
            },
            iam_resources = ["*"],
            result_path = sfn.JsonPath.DISCARD
        )
        
        #tag forensic instance with tag quarantine
        tag_instance = tasks.CallAwsService(self, "Tag Instance as Quarntine",
            service="ec2",
            action="createTags",
            parameters={
                "Resources":  sfn.JsonPath.string_at("States.Array($[1].InstanceId)"),
                "Tags": [
                    {
                        "Key": "Status",
                        "Value": "Quarantined"
                    }
                ]
            },
        #    result_path=sfn.JsonPath.string_at("$.InstanceTags"),
            iam_resources = ["*"]
        )
        #Send Email about tags
        ###################################
        send_email_with_tags = tasks.CallAwsService(self, "Send Email about instance tags",
            service = "sns",
            action = "publish",
            parameters = {
                "TopicArn" : notification_SNS_topic.topic_arn,
                "Message" : "Instance tags updated with status Quarantine"
            },
            iam_resources = ["*"]
        )
        
        #Send Email that Instance is already in Quarantine state
        ###################################
        send_email_already_Quarantine = tasks.CallAwsService(self, "Email Instance already Quarantined ",
            service = "sns",
            action = "publish",
            parameters = {
                "TopicArn" : notification_SNS_topic.topic_arn,
                "Message" : "Instance is already Quarantined"
            },
            iam_resources = ["*"]
        )
     
        
        has_quarantine_tags_choice = sfn.Choice(self, " Quarantine Tag present ? ")

        yes_instance_tag_con = sfn.Condition.is_present(variable="$.InstanceTags.Tags[0].Value")
        # #Build state machine state: Choice, Condition, Pass, Wait
        # has_quarantine_tags_choice = sfn.Choice(self, "Is Instance Quarantined?")
        # #yes_instance_tag_con = sfn.Condition.string_equals(variable=,value="Quarantined")
        # yes_instance_tag_con = sfn.Condition.string_equals(variable="$.States.Array($[1].InstanceId)",value="Quarantined")
        
        has_asg_choice = sfn.Choice(self, "Has ASG?")
        
        yes_asg_con = sfn.Condition.is_present(variable="$.AutoScalingResult.AutoScalingInstances[0].AutoScalingGroupName")
        
        is_snapshot_complete_choice = sfn.Choice(self, "Is Snapshot Complete?")
        
        yes_snapshot_complete_con = sfn.Condition.string_equals(variable="$.SnapshotStatus.SnapshotState",value="completed")
        
        is_ebs_volume_available_choice = sfn.Choice(self, "Is EBS Volume Available?")
        
        no_ebs_volume_available_con = sfn.Condition.not_(sfn.Condition.string_equals(variable="$.VolumeDescription.Volumes[0].State",value="available"))
        
        volume_creation_complete_wait = sfn.Wait(self, "Wait for Volume Creation", time=sfn.WaitTime.duration(Duration.seconds(15)))
        
        snapshot_creation_complete_wait = sfn.Wait(self, "Wait for Snapshot Creation", time=sfn.WaitTime.duration(Duration.seconds(15)))
        
        volume_create_complete_pass = sfn.Pass(self, "Volume Creation Complete")
        
        parallel_create = sfn.Parallel(self, "Create Forensic Instance, Snapshots, Volume")
        
        parallel_create.branch(create_forensic_instance)
        
        parallel_create.branch(create_snapshot.next(get_snapshot_status).next(is_snapshot_complete_choice.when(
                yes_snapshot_complete_con, EBS_volume_from_snapshot.next(ebs_volume_status_check).next(is_ebs_volume_available_choice.when(
                        no_ebs_volume_available_con, volume_creation_complete_wait.next(ebs_volume_status_check)
                    ).otherwise(volume_create_complete_pass))
            ).otherwise(snapshot_creation_complete_wait.next(get_snapshot_status))))
            
        # Build the state machine definition
        chain = sfn.Chain.start(instance_metadata).next(instance_tags_check).next(has_quarantine_tags_choice.when
                    (
                        yes_instance_tag_con, send_email_already_Quarantine
                        ).otherwise(EC2_termination_protection.next(auto_scaling_info).next(has_asg_choice.when
                  (
                      yes_asg_con, detach_ec2_from_asg
                  ).afterwards(include_otherwise=True)
                    ).next(parallel_create).next(attach_volume).next(modify_forencis_instance_sg).next(tag_instance).next(send_email_with_tags).next(send_email_about_snapshotId)))
        # State machine      
        sm = sfn.StateMachine(self, "StateMachine",
            definition=chain
        )

        CfnOutput(self, "StepFunctionArn", description="Step function ARN",
            value=sm.state_machine_arn       
        )

        CfnOutput(self, "StpFunctionURL", description="Step Function URL",
            value=Fn.sub("https://${AWS::Region}.console.aws.amazon.com/states/home?region=${AWS::Region}#/statemachines/view/${EC2IsolationStateMachine}",
               {"EC2IsolationStateMachine": sm.state_machine_arn}
            )       
        )