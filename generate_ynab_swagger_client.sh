# The below uses swagger-codegen version 3.0.18, which can be acquired on OSX using `brew install swagger-codegen`
swagger-codegen generate -i https://api.youneedabudget.com/papi/spec-v1-swagger.json -l python -o ./dependencies/ynab_v1
