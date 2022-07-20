import boto3

db = boto3.client("dynamodb")

class scan_dynamodb():
    response = db.list_tables()
    tables = response["TableNames"]

    count  = 0
    rcu  = 0
    wcu = 0
    over_cu = ""

    for i in tables:
        table_name = tables[count]
        table_desc = db.describe_table(TableName=tables[count])
        rcu = table_desc["Table"]["ProvisionedThroughput"]["ReadCapacityUnits"]
        wcu = table_desc["Table"]["ProvisionedThroughput"]["WriteCapacityUnits"]

        count = count + 1
        if rcu > 5 or wcu > 5:
            over_cu += table_name + "\n"
        else:
            pass