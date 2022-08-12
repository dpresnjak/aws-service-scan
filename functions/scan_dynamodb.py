class DynamoDBScanner:
    def __init__(self, ddb_client):
        self.ddb_client = ddb_client
        self.over_cu = ""

    def scan_tables(self):
        try:
            response = self.ddb_client.list_tables()
            tables = response.get("TableNames", [])
            if not tables:
                return "No tables found."

            for table in tables:
                table_desc = self.ddb_client.describe_table(TableName=table)

                if table_desc.get("Table") is None:
                    raise Exception(f"Failed fetching {table} DDB table's description")

                provisioned_throughput = table_desc['Table'].get("ProvisionedThroughput")  

                if provisioned_throughput is not None:
                    rcu = provisioned_throughput["ReadCapacityUnits"]
                    wcu = provisioned_throughput["WriteCapacityUnits"]

                    if rcu > 5 or wcu > 5:
                        self.over_cu += table + "\n"

            return self.over_cu
        except Exception as e:
            print(f"Table scanning function failed with the following error: {e}")
            raise Exception(f"Table scanning function failed with the following error: {e}")