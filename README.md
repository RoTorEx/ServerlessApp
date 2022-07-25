# Serverless application on Python using AWS

## Authentication & API

For all APIs, except for auth API, it is necessary to pass in the __Headers__ request *authorizationToken* in *key* and the *generated token* in *value* field.

Each generated JWT token lives for `one minute`. Token encode & decode with secret key, which created using the current date and time.

API endpoint to generate JWT token:

- [auth](https://yvqhf40uva.execute-api.us-east-1.amazonaws.com/prod/auth) - `GET & POST` methods. In the body of the request, pass the *username* to the *name* field and return the generated JWT token.

The following API endpoints are implemented with API Gateway Authorizers:

- [home](https://yvqhf40uva.execute-api.us-east-1.amazonaws.com/prod/home) - only `GET` method, return hello-string.

- [customers](https://yvqhf40uva.execute-api.us-east-1.amazonaws.com/prod/customers) - only `GET` method, return list of all customers.

- [customer](https://yvqhf40uva.execute-api.us-east-1.amazonaws.com/prod/customer) - `GET, POST, PATCH & DELETE` methods, return customer.
