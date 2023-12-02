import os
import json
import time

from localstack_client.session import Session as local_boto3

sqs = local_boto3(localstack_host='localstack').resource("sqs")

queue = sqs.Queue(os.getenv('COPILOT_QUEUE_URI'))

if __name__ == "__main__":
    time.sleep(5)
    while True:
        print('escutando...')
        messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=int(os.getenv('MAX_NUMBER_OF_MESSAGES')),
            WaitTimeSeconds=int(os.getenv('WAIT_TIME_SECONDS'))
        )
        for msg in messages:
            parse_message = json.loads(msg.body)
            
            message = json.loads(parse_message['Message'])['message']
            
            print(f"Mensagem recebida: {message}")
            msg.delete()
