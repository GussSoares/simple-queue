# Simple Queue

Este projeto consiste em uma implementação simples apresenta o funcionamento de dois serviços.

- [Producer](/producer.py)
- [Consumer](/consumer.py)

## Como funciona?

Inicialmente cada serviço roda de forma independente. É criada uma fila SQS e um tópico SNS que se inscreve na fila

```python
sns_sqs_list = ['simple-queue']
sns = local_boto3(localstack_host='localstack').resource("sns")
sqs = local_boto3(localstack_host='localstack').resource("sqs")
sns_client = local_boto3(localstack_host='localstack').client('sns')
for sns_sqs in sns_sqs_list:
    sns.create_topic(Name=sns_sqs)
    sqs.create_queue(QueueName=sns_sqs)
    sns_client.subscribe(
        TopicArn=f'arn:aws:sns:us-east-1:000000000000:{sns_sqs}',
        Protocol='sqs',
        Endpoint=f'arn:aws:sqs:us-east-1:000000000000:{sns_sqs}')
```

### Producer
O Producer se conecta ao SNS

```python
sns = boto3.client('sns')
topic = json.loads(os.environ.get('COPILOT_SNS_TOPIC_ARNS'))
```

e publica uma mensagem no tópico que está inscrito na fila ao qual deseja enviar a mensagem.

```python
message = {"message": f'Eu sou o produtor! Esta é a mensagem {uuid.uuid4()}!'}
response = sns.publish(
    TopicArn=topic.get('simple_queue'),
    Message=json.dumps(message)
)
```

### Consumer

O Consumer se conecta a fila ao qual deseja receber a mensagem fica coletando mensagens da fila e apresentando no terminal.

```python
sqs = local_boto3(localstack_host='localstack').resource("sqs")

queue = sqs.Queue(os.getenv('COPILOT_QUEUE_URI'))
```

Em seguida entra em loop para obter sequencialmente cada mensagem presente na fila para processá-la.

```python
messages = queue.receive_messages(
    MessageAttributeNames=['All'],
    MaxNumberOfMessages=int(os.getenv('MAX_NUMBER_OF_MESSAGES')),
    WaitTimeSeconds=int(os.getenv('WAIT_TIME_SECONDS'))
)

for msg in messages:
    parse_message = json.loads(msg.body)
    message = json.loads(parse_message['Message'])['message']
```

Após processar a mensagem ela deve ser apagada para que não seja consumida novamente.

```python
msg.delete()
```
