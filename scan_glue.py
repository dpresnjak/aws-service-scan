class GlueScanner:
    def __init__(self, glue_client):
        self.glue_client = glue_client
        self.over_max = ""
        self.over_timeout = ""

    def scan_jobs(self):
        try:
            response = self.glue_client.list_jobs()
            jobs = response.get("JobNames", [])
    
            for job in jobs:
                job_desc = self.glue_client.get_job(JobName=job)
    
                if job_desc.get("Job") is None:
                    raise Exception(f"Failed fetching {job} job description.")
                
                job_details = job_desc["Job"]
                timeout = job_details["Timeout"]
    
                try:
                    max_cap = job_details["MaxCapacity"]
                except KeyError:
                    max_cap = 0
    
                try:
                    num_of_work = job_details["NumberOfWorkers"]
                except KeyError:
                    num_of_work = 0
    
                if max_cap > 10 or num_of_work > 10:
                    self.over_max += job + "\n"
    
                if timeout > 480:
                    self.over_timeout += job + "\n"

            return self.over_timeout, self.over_max

        except Exception as e:
            print(f"Glue jobs scan failed with the following error: {e}")
            raise Exception(f"Glue jobs scan failed with the following error: {e}")