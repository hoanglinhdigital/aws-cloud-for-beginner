# AWS KMS CLI demo

Simple demo showing how to create a customer master key (CMK / KMS key), encrypt a small file, and decrypt it using the AWS CLI.

Prerequisites
- AWS CLI configured with credentials and region (`aws configure`).
- IAM user/role with kms:CreateKey, kms:CreateAlias, kms:Encrypt, kms:Decrypt, kms:DescribeKey.

1) Create a KMS key
```bash
aws kms create-key \
    --description "demo key for local testing" \
    --tags TagKey=project,TagValue=kms-demo
# note: response contains KeyMetadata.KeyId and KeyMetadata.Arn
```
Save the KeyId or ARN returned (example: `1234abcd-12ab-34cd-56ef-1234567890ab`).

2) (Optional) Create a friendly alias
```bash
aws kms create-alias --alias-name alias/demo-key --target-key-id <KeyId-or-ARN>
```

3) Encrypt a plaintext file
```bash
# write plaintext
echo "Welcome to AWS Cloud for beginner" > secret.txt

# encrypt with the key or alias
aws kms encrypt \
    --key-id alias/demo-key \
    --plaintext fileb://secret.txt \
    --output text \
    --query CiphertextBlob > secret.encrypted.b64

# secret.encrypted is binary ciphertext
```

4) Decrypt the ciphertext
```bash
# First convert base64 to binary
base64 -d secret.encrypted.b64 > secret.encrypted.bin

# Then decrypt
aws kms decrypt \
    --ciphertext-blob fileb://secret.encrypted.bin \
    --output text \
    --query Plaintext \
    | base64 -d > secret-decrypted.txt

5) Cleanup (remove alias then key)
```bash
aws kms delete-alias --alias-name alias/demo-key
aws kms schedule-key-deletion --key-id <KeyId-or-ARN> --pending-window-in-days 7
aws kms schedule-key-deletion --key-id arn:aws:kms:ap-northeast-1:586098608758:key/fa39ce04-bdcb-4f0d-bc9c-c0a2374fe9b6 --pending-window-in-days 7
# KMS keys cannot be immediately destroyed; schedule deletion window is required.
```