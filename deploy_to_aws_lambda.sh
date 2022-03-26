# Parse config and set on lambda:
configvars="$(PYTHONPATH=./dependencies/ynab-v1/ python3 ./src/mail_to_ynab.py dump-config)"
echo "$configvars"
aws lambda update-function-configuration --function-name MailToYnab --environment "$configvars"

# Set entry point:
aws lambda update-function-configuration --function-name MailToYnab --handler mail_to_ynab.lambda_handler

# Create build folder:
rm -rf ./build
mkdir ./build

# Copy source:
cp ./src/*.py ./build/

# Copy Generated Swagger Client:
cp -R ./dependencies/ynab-v1/swagger_client ./build

# Install Dependencies:
pip install certifi -t ./build
pip install imapclient -t ./build
pip install beautifulsoup4 -t ./build

# Zip it up:
rm ./mailtoynab_lambda.zip
cd build
zip -r ../mailtoynab_lambda.zip .
cd ..

# Upload to Lambda:
aws lambda update-function-code --function-name MailToYnab --zip-file fileb://mailtoynab_lambda.zip

# Try it:
aws lambda invoke --function-name MailToYnab --log-type Tail /tmp/lambda_out |jq -r '.LogResult' | base64 --decode
