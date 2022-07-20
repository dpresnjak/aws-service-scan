import boto3

glue = boto3.client("glue")

class scan_glue():
    response = glue.list_jobs()
    jobs = response["JobNames"]

    count  = 0
    max_cap  = 0
    num_of_work = 0
    over_max = ""

    for i in jobs:
        job_name = jobs[count]
        job_desc = glue.get_job(JobName=jobs[count])

        try:        
            max_cap = job_desc["Job"]["MaxCapacity"]
        except KeyError:
            max_cap = 0

        try:
            num_of_work = job_desc["Job"]["NumberOfWorkers"]
        except KeyError:
            num_of_work = 0

        count = count + 1

        if max_cap > 10 or num_of_work > 10:
            over_max += job_name + "\n"