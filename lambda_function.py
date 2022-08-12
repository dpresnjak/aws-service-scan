import boto3
from scan_dynamodb import DynamoDBScanner
from scan_glue import GlueScanner
from scan_lambdas import LambdaScanner

sns = boto3.client("sns")
ddb_client = boto3.client("dynamodb")
glue_client = boto3.client("glue")
lambda_client = boto3.client("lambda")


def lambda_handler(event, context):
    lambda_scanner = LambdaScanner(lambda_client)
    glue_scanner = GlueScanner(glue_client)
    ddb_scanner = DynamoDBScanner(ddb_client)
    
    over_timeout, over_max = glue_scanner.scan_jobs()
    over_conc, over_memory = lambda_scanner.scan_lambdas()
    
    sns.publish(
        TopicArn="arn:aws:sns:us-east-1:176984903748:AcademyScanTopic",
        Subject="iOLAP Academy service scan",
        Message=f"Lambda functions over the 512MB limit:\n{over_memory}\
                \nLambda functions over the 5 concurrency limit: \n{over_conc}\
                \nDynamoDB tables over the 5 RCU/WCU: \n{ddb_scanner.scan_tables()}\
                \nGlue jobs over limits (Workers and/or capacity): \n{over_max}\
                \nGlue jobs over timeout limit (480min, Default=2880min): \n{over_timeout}"
    )