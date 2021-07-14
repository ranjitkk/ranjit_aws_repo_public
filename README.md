# Public AWS Repo created by ranjit kalidasan for AWS Code Snippets
## Splunk-GuardDuty-CWLogs_Processor.py
### This lambda function is used as pre-processor function in Kinesis Data Firehose to send GuardDuty Findings into Splunk. This updated code takes the input records for GD findings and parse the content to generate appropriate detective urls as additional fields into Splunk. Sample URLs are shown as below:
```
  "detectiveUrls": {
    "guardDutyFindings": "https://console.aws.amazon.com/detective/home?region=us-east-1#findings/GuardDuty/20bd4db52394c7660dcd5e3be6024cc1",
    "ec2Instance": "https://console.aws.amazon.com/detective/home?region=us-east-1#entities/Ec2Instance/i-99999999",
    "externalIpAddress1": "https://console.aws.amazon.com/detective/home?region=us-east-1#entities/IpAddress/198.51.100.0",
    "externalIpAddress2": "https://console.aws.amazon.com/detective/home?region=us-east-1#entities/IpAddress/10.0.0.23",
    "awsAccount": "https://console.aws.amazon.com/detective/home?region=us-east-1#entities/AwsAccount/647604195155",
    "publicIpAddress": "https://console.aws.amazon.com/detective/home?region=us-east-1#entities/IpAddress/198.51.100.0",
    "privateIpAddress": "https://console.aws.amazon.com/detective/home?region=us-east-1#entities/IpAddress/10.0.0.1"
  }
 ```

