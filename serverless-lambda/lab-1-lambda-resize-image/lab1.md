# Lab 1: Lambda Resize Image

## Overview
This lab demonstrates how to create a Lambda function that automatically resizes images uploaded to S3. The function uses the Pillow library to create multiple thumbnail sizes.

## Step 1: Create S3 Bucket

Create an S3 bucket that will trigger the Lambda function when images are uploaded.

## Step 2: Prepare Lambda Layer with Pillow Library

**IMPORTANT:** The Pillow library must be built for Amazon Linux 2 (the Lambda runtime environment), not Windows. Using the wrong platform will cause the error:
```
[ERROR] Runtime.ImportModuleError: Unable to import module 'lambda_function': 
cannot import name '_imaging' from 'PIL'
```

### Create python directory
```bash
mkdir python
```

### Install Pillow with correct platform

**For Bash/Git Bash/WSL (single line command):**
```bash
pip install Pillow --platform manylinux2014_x86_64 --target python --implementation cp --python-version 3.12 --only-binary=:all: --no-deps --upgrade
```

**For PowerShell (multi-line command):**
```powershell
pip install Pillow `
    --platform manylinux2014_x86_64 `
    --target python `
    --implementation cp `
    --python-version 3.12 `
    --only-binary=:all: `
    --no-deps `
    --upgrade
```

### Create the zip file

Zip `python` folder to `python.zip`

### Upload Layer to AWS
1. Go to AWS Lambda Console → Layers → Create Layer
2. Name: `python-pillow-layer`
3. Upload `python.zip`
4. Compatible architectures: `x86_64`
5. Compatible runtimes: `Python 3.12`
6. Click "Create"

## Step 3: Create Lambda Function

1. Go to AWS Lambda Console → Create Function
2. Function name: `resize-image-lambda`
3. Runtime: `Python 3.12`
4. Architecture: `x86_64`
5. Create function

## Step 4: Add Layer to Lambda Function

1. In your Lambda function, scroll down to "Layers"
2. Click "Add a layer"
3. Choose "Custom layers"
4. Select `python-pillow-layer`
5. Click "Add"

## Step 5: Configure Lambda Function

1. Upload the `resize-image-lambda.py` code
2. Set timeout to at least 30 seconds (Configuration → General configuration → Edit)
3. Increase memory to at least 512 MB for faster image processing

## Step 6: Configure S3 Trigger

1. Click "Add trigger"
2. Select "S3"
3. Choose your bucket
4. Event type: "All object create events"
5. Prefix: `images/`
6. Suffix (optional): `.jpg` (to only trigger on JPG files)
7. Acknowledge the recursive invocation warning
8. Click "Add"

## Step 7: Test the Function

1. Upload a `.jpg` image to your S3 bucket. *Image name must not contain special character!*
2. Check the Lambda function logs in CloudWatch
3. Verify that resized images appear in the folders: `resized_100/`, `resized_200/`, `resized_500/`, `resized_1000/`

## Troubleshooting

### Error: "cannot import name '_imaging' from 'PIL'"
**Cause:** The layer was built on Windows instead of for Amazon Linux 2.  
**Solution:** Rebuild the layer using the scripts provided (`build-layer.ps1` or `build-layer.sh`) which use the `--platform manylinux2014_x86_64` flag.

### Error: "Task timed out"
**Cause:** Lambda timeout is too short for large images.  
**Solution:** Increase the timeout in Configuration → General configuration → Edit (recommended: 30-60 seconds).

### Error: "Memory limit exceeded"
**Cause:** Not enough memory allocated for image processing.  
**Solution:** Increase memory to at least 512 MB in Configuration → General configuration → Edit.
