import boto3

lamb = boto3.client("lambda")

class scan_lambdas():
    response = lamb.list_functions()
    funcs = response["Functions"]
    
    count = 0
    over_memory = ""
    over_conc = ""
    
    for i in funcs:
        func_name = funcs[count]["FunctionName"]
        count = count +1
    
        get_func = lamb.get_function(FunctionName=func_name)
        func_mem = get_func["Configuration"]["MemorySize"]
    
        get_func_conc = lamb.get_function_concurrency(FunctionName=func_name)
        func_conc = 0
    
        try:
            func_conc = get_func_conc["ReservedConcurrentExecutions"]
        except KeyError:
            pass
    
        if func_conc > 5:
            over_conc += func_name + "\n"
        else:
            pass
    
        if func_mem > 512:
            over_memory += func_name + "\n"
        else:
            pass
