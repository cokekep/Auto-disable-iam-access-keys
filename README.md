# Overview
The lambda function deployed using this repository is used to 

* disable the Access Keys older than 180 days for IAM Users in the Central AWS Access Account.
* delete the Access Keys older than 180 days for IAM Users in the Central AWS Access Account.

The function can be depoyed using serverless framework.

# Instructions
* The retention can be controlled using the `DAYS_RETENTION` environment variable. The default value is 180 days.

* The default Status of access key checked by the function is `Active` and it can be controlled using the varibale `STATUS_FILTER`.

## Deploying the functions
The function can be deployed using `serverless` framework.

### Deploying the function

Deploy command (**access-account** example):
```bash
aws lambda create-function --function-name disableAccessKeys --runtime python3.8 \
--zip-file fileb://disableAccessKeys.zip --handler handler.lambda_handler \
--role arn:aws:iam::xxxxxxxxxxxx:role/temp-lambda-disableAccessKeys \
--environment "Variables={DAYS_RETENTION=180,STATUS_FILTER='Active'}"
```

### Update function code
```bash
aws lambda update-function-code --function-name disableAccessKeys  --zip-file fileb://disableAccessKeys.zip
```

# References

* https://serverless.com/framework/docs/getting-started/