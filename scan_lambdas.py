class LambdaScanner():
    def __init__(self, lambda_client):
        self.lambda_client = lambda_client
        self.over_memory = ""
        self.over_conc = ""

    def scan_lambdas(self):
        count = 0
        
        try:
            response = self.lambda_client.list_functions()
            functions = response["Functions"]
            
            if not functions:
                return "No Lambda functions found"

            for func in functions:
                func_name = functions[count]["FunctionName"]
                count = count + 1
                
                func_memory = self.lambda_client.get_function(FunctionName=func_name).get("Configuration").get("MemorySize")

                func_conc = self.lambda_client.get_function_concurrency(FunctionName=func_name).get("ReservedConcurrentExecutions")

                if func_conc is not None:
                    if func_conc > 5:
                        self.over_conc += func_name + "\n"

                if func_memory > 512:
                    self.over_memory += func_name + "\n"

            return self.over_conc, self.over_memory
            
        except Exception as e:
            print(f"Lambda scanning function failed with the following error: {e}")
            raise Exception(f"Lambda scanning function failed with the following error: {e}")