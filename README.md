# aws-service-scan
Simple CF template and Lambda functions for scanning a few AWS services for specific config info.

Changed some identifyng lines for my AWS account but should work fine.

* Would probably be a good idea to create the bucket first and upload Lambda code since the CF template uses a .zip file for the lambdas; or use SAM to package and deploy at the same time
