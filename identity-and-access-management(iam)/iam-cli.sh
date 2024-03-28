#Test credential
aws sts get-caller-identity

#List all s3 bucket
aws s3 ls

#Download file
aws s3 cp <s3 uri> <local destination>

#Upload file
aws s3 cp <local destination> <s3 uri> 

#Lisst file
aws s3 ls <s3://path>

#Using cli with MFA
#Step 1 issue temporary token
aws sts get-session-token --serial-number arn:aws:iam::123456789012:mfa/developer-01-iphone --token-code 123456

#Step 2: config credential file.
"C:\Users\<your user name>\.aws\credentials"
#--------------------
[udemy-mfa]
aws_access_key_id = ASIAWIVVHVPNI6WO5AOW
aws_secret_access_key = KKqlnJn6XT2RQWeNwuxQvhOWAjVbvSCbkRMEny9f
aws_session_token = IQoJb3JpZ2luX2VjEK///////////wEaDmFwLXNvdXRoZWFzdC0xIkgwRgIhAO1Z8dMTyKyyDIcJBSSPBtnAUHpMUpQ3+mCeTyDpiK5PAiEAujswq262YxMSuHSmzU+1ZzoUqQfuZ19/Ut4NXqHgPfQq+AEIqP//////////ARAAGgw0MzA5NTA1NTg2ODIiDMkOIirsIpfYG0BbTirMAWDz7GCM632sxd6mGDY4ZfBmfBZuaVSm55P0ECkKt2qijTx8HsnijcOlwcnrXBjCdKwp126YaU6INtpecdCAYJGL4GH9enkwn+zQdT7eYN+io0Y8ciHMnA9MPPRAE8rJCAjA+FHVBZEY0zDqjGQQTr/BgWNiCR/e43orrikVXX+w3SfVRriTVsyma05A6o7bz1J0uz5mqG+AIHazGmr8Mek8fybV1t9YQDGmPxeYGfyausSOquitvJhJCocASWYUkSPCu12PMd9j4MdWYDCg0IqiBjqXAVLYQ7FVcMujq99V4azMjIDpIzLyasX9W/0J/VUIrxekFzdQE1SEfBNxInYgV8ER1TJ2WltKPmVH4rRb8n6Abtc4C40f1WDjDCcAqYdsrLQtk9hdKgSFD2pvnKK+vxvm8Wpexw6oVX4t77tncXAhqPAnQ8RnNcFSwtynszgIRZUqhGcapaEHQlrQ/4JKB0kXaxv8DlsiSF0=
#-------------

#Step 3: specify --profile when run command.
aws s3 ls --profile udemy-mfa
aws s3 ls s3://<your-bucket-name>/ --profile udemy-mfa





