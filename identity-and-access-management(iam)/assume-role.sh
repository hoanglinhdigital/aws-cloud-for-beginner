#Assume role cli:
aws sts assume-role --role-arn <role-arn> --role-session-name <session-name> 

#Example
aws sts assume-role --role-arn arn:aws:iam::430950558682:role/udemy-test-power-user-role --role-session-name udemy-test-assume 
