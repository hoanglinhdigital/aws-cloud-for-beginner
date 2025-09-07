#Check role by simple command:
aws s3 ls
aws sts get-caller-identity


#Create a role with name "udemy-test-power-user-role" then allow user "developer-01" to assume role.
#See file "iam-trust-policy.json"

#Assume role cli:
aws sts assume-role --role-arn <role-arn> --role-session-name <session-name> 

#Example
aws sts assume-role --role-arn arn:aws:iam::799227077423:role/MyPowerRole --role-session-name udemy-test-assume 

#Test command
aws s3 ls --profile test-assume

aws s3 ls s3://udemy-bucket-linh --recursive --profile test-assume