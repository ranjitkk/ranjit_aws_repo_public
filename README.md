# Public AWS Repo created by ranjit kalidasan for AWS Code Snippets
## Splunk-GuardDuty-CWLogs_Processor.py
### This lambda function is used as pre-processor function in Kinesis Data Firehose to send GuardDuty Findings into Splunk. This updated code takes the input records for GD findings and parse the content to generate appropriate detective urls as additional fields into Splunk. Sample URLs are shown as below:
```
  "detectiveUrls": {
     awsAccount: https://console.aws.amazon.com/detective/home?region=us-east-1#entities/AwsAccount/647604195155?scopeStart=1624674429&scopeEnd=1626473483
     ec2Instance: https://console.aws.amazon.com/detective/home?region=us-east-1#entities/Ec2Instance/i-0149bf6226265a155?scopeStart=1624674429&scopeEnd=1626473483
     externalIpAddress1: https://console.aws.amazon.com/detective/home?region=us-east-1#entities/IpAddress/170.106.176.49?scopeStart=1624674429&scopeEnd=1626473483
     externalIpAddress2: https://console.aws.amazon.com/detective/home?region=us-east-1#entities/IpAddress/185.180.143.148?scopeStart=1624674429&scopeEnd=1626473483
     guardDutyFindings: https://console.aws.amazon.com/detective/home?region=us-east-1#findings/GuardDuty/e6bd2314fee874a9d9490d7ebc2b42d8?scopeStart=1624674429&scopeEnd=1626473483
     privateIpAddress: https://console.aws.amazon.com/detective/home?region=us-east-1#entities/IpAddress/10.10.1.112?scopeStart=1624674429&scopeEnd=1626473483
     publicIpAddress: https://console.aws.amazon.com/detective/home?region=us-east-1#entities/IpAddress/54.82.24.215?scopeStart=1624674429&scopeEnd=1626473483
   }
 ```

