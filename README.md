# Infrastructure-Drift-Detection-Auto-Remediation

step 1: 
1. Infrastructure Provisioning Using Terraform

creted instance
security group 
s3 bucket

![](./images/Screenshot%202026-04-05%20081903.png)

![](./images/Screenshot%202026-04-05%20081916.png)

![](./images/Screenshot%202026-04-05%20081952.png)

step 2 :
2. Simulate Drift
Manually modify:
Security group rule
EC2 tag
 
![](./images/Screenshot%202026-04-05%20082050.png)

step 3:

3. Drift Detection
Implement:
 	Scheduled Terraform plan

![](./images/Screenshot%202026-04-05%20082136.png)

step 4:

4. Auto Remediation
Create Lambda function that:
Detects drift
Re-applies Terraform

![](./images/Screenshot%202026-04-05%20082223.png)

created one directory inside project 
called terraform-lambda 

![](./images/Screenshot%202026-04-05%20083035.png)

stored files inside directory

and created zipfile to upload on lambda

![](./images/Screenshot%202026-04-05%20085205.png)

attached i am role to lambda function

![](./images/Screenshot%202026-04-05%20084940.png)

uploded lambda-package.zip file in lambda function

![](./images/Screenshot%202026-04-05%20083317.png)

![](./images/Screenshot%202026-04-05%20083341.png)

![](./images/Screenshot%202026-04-05%20083400.png)

## eventbridge setup

⚙️ How It Works
EventBridge runs on a fixed schedule (cron or rate)
It triggers the Lambda function
Lambda executes:
terraform init
terraform plan
If drift detected → terraform apply
Logs are stored in CloudWatch Logs

🎯 Rule Configuration
Rule Name: terraform-drift-auto-fix
Event Bus: default
Type: Scheduled Rule
Target: Lambda Function (terraform-drift-remediation)
Status: Enabled

![](./images/Screenshot%202026-04-05%20083643.png)

## 🏗️ Architecture Flow

EventBridge (Schedule)
        ↓
Lambda Function
        ↓
Terraform (init → plan → apply)
        ↓
AWS Infrastructure (EC2, S3, SG, etc.)
        ↓
CloudWatch Logs


## project output:

manually changed on aws console

changed security group rule
deleted ssh
added 443

changed instance name with my-ec2

![](./images/Screenshot%202026-04-05%20094752.png)

![](./images/Screenshot%202026-04-05%20094814.png)

If we manually change something in the AWS Console:

👉 Terraform detects it as drift

Your actual AWS resources no longer match your Terraform code

👉 What your system does next:

⏰ Amazon EventBridge triggers your Lambda automatically
⚙️ AWS Lambda runs terraform plan
🔍 Drift is detected
🔧 Lambda runs terraform apply to fix it

👉 Final result:

Your infrastructure is restored back to the original Terraform configuration ✅

![](./images/Screenshot%202026-04-05%20095612.png)

![](./images/Screenshot%202026-04-05%20095630.png)

step 5:

5. Logging
Store events in:
CloudWatch Logs 

![](./images/Screenshot%202026-04-05%20100000.png)


✅ Conclusion

This project builds a self-healing infrastructure system using Terraform and AWS services like AWS Lambda and Amazon EventBridge. It automatically detects and fixes infrastructure drift, ensuring consistency, reducing manual effort, and improving reliability of cloud resources. 🚀


