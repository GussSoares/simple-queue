"""Producer file
"""

import json
import os
import time
import uuid

from localstack_client.session import Session as local_boto3

boto3 = local_boto3(localstack_host='localstack')


def create_queue():
    """Create initial sns topic and sqs queue 
    """
    sns_sqs_list = [
        'simple-queue',
    ]
    _sns = local_boto3(localstack_host='localstack').resource("sns")
    _sqs = local_boto3(localstack_host='localstack').resource("sqs")
    sns_client = local_boto3(localstack_host='localstack').client('sns')
    for sns_sqs in sns_sqs_list:
        _sns.create_topic(Name=sns_sqs)
        _sqs.create_queue(QueueName=sns_sqs)
        sns_client.subscribe(
            TopicArn=f'arn:aws:sns:us-east-1:000000000000:{sns_sqs}',
            Protocol='sqs',
            Endpoint=f'arn:aws:sqs:us-east-1:000000000000:{sns_sqs}')


if __name__ == "__main__":
    create_queue()

    while True:
        sns = boto3.client('sns')
        topic = json.loads(os.environ.get('COPILOT_SNS_TOPIC_ARNS'))

        message = {"message": f'Eu sou o produtor! Esta é a mensagem {uuid.uuid4()}!'}
        response = sns.publish(
            TopicArn=topic.get('simple_queue'),
            Message=json.dumps(message)
        )
        print(f'mensagem enviada: {message["message"]}')
        time.sleep(3)
