import aws_cdk as core
import aws_cdk.assertions as assertions
from ec2_isolation_cdk_demo.ec2_isolation_cdk_demo_stack import Ec2IsolationCdkDemoStack


def test_sqs_queue_created():
    app = core.App()
    stack = Ec2IsolationCdkDemoStack(app, "ec2-isolation-cdk-demo")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created():
    app = core.App()
    stack = Ec2IsolationCdkDemoStack(app, "ec2-isolation-cdk-demo")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::SNS::Topic", 1)
