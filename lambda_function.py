import boto3
from scan_dynamodb import scan_dynamodb
from scan_glue import scan_glue
from scan_lambdas import scan_lambdas

sns = boto3.client("sns")


def lambda_handler(event, context):
    scan_lambdas()
    scan_dynamodb()
    scan_glue()

    sns.publish(
        TopicArn="arn:aws:sns:us-east-1:176984903748:ScanTopic",
        Subject="iOLAP Academy service scan",
        Message=f"Lambda functions over the 256MB limit:\n{scan_lambdas.over_memory}\
                \nLambda functions over the 5 concurrency limit: \n{scan_lambdas.over_conc}\
                \nDynamoDB tables over the 5 RCU/WCU: \n{scan_dynamodb.over_cu}\
                \nGlue jobs over limits (Workers and capacity): \n{scan_glue.over_max}"
    )
