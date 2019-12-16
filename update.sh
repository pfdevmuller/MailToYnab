rm mailtoynab_lambda.zip

cd src

zip -r ../mailtoynab_lambda.zip .

cd ..

aws lambda update-function-code --function-name MailToYnab --zip-file fileb://mailtoynab_lambda.zip

aws lambda update-function-configuration --function-name MailToYnab --handler mail_to_ynab.lambda_handler

aws lambda invoke --function-name MailToYnab --log-type Tail /tmp/lambda_out |jq -r '.LogResult' | base64 --decode
