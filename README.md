# claim-process-payment-service

| Service name      | claim-process-payment-service |
|-------------------|-------------------------------|
| Language/Framework| Python/FastApi                |
| Database          | sqlite                        |

## Problem Statement: 
to create a **_dockerized_** service, **claim_process**  to process claims. 

## Requirements
1. **claim_process** transforms a JSON payload representing a single claim input with multiple lines and stores it into a RDB.
   - An example input (in CSV format) - *claim_1234.csv* is provided. Note that the names are not consistent in capitalization.
2. **claim_process** generates a unique id per claim.
3. **claim_process** computes the *“net fee”* as a result per the formula below.
*“net fee” = “provider fees” + “member coinsurance” + “member copay” - “Allowed fees”* (note again that the names are not consistent in capitalization).
4. A downstream service, **payments**, will consume *“net fee”* computed by **claim_process**.
5. Implement an endpoint that returns the top 10 provider_npis by net fees generated. The endpoint should be optimized for performance, and the you should explain the data structure and algorithm used to compute the top 10 provider_npis. It would be good to have a rate limiter to this api probably 10 req/min.

## Local Setup
1. Clone the repository
   ```git clone https://github.com/Niwedita17/claim-process-payment-service.git```
   
2. Create Virtual Environment in the project root
   ```python3 -m venv .venv```
3. Activate the Virtual Environment
   ```source .venv/bin/activate```

4. Create .env from sample.env

5. Install all dependencies
   ```pip3 install -r requirements.txt```

6. Run Server
    ```uvicorn src.main:app --reload```

7. Visit the docs panel http://127.0.0.1:8000/docs/
   The application will be available at http://localhost:8000.

8. Visit the graphql UI for query and mutation http://127.0.0.1:8000/graphql

## EndPoints
# POST /claims
This endpoint creates a new claim.

- Request Body
   - {
         "service_date": "string",
         "submitted_procedure": "string",
         "quadrant": "string",
         "plan_group_number": "string",
         "subscriber_number": "string",
         "provider_npi": "5555555555",
         "provider_fees": 10,
         "allowed_fees": 10,
         "member_coinsurance": 20,
         "member_copay": 20
      }

- Response
   - net_fee (float): The net fee for the claim

# GET /claims/{id}
This endpoint retrieves a specific claim by its unique ID.

- Parameters
   - id (int): The ID of the claim to retrieve.

- Response
   - claim

# GET /claims
This endpoint retrieves a list of all claims.

- Parameters

   - skip (int): The number of items to skip.
   - limit (int): The maximum number of items to retrieve.
- Response
   - [claims]


# GET /providers
This endpoint retrieves the top 10 provider_npis by net fees generated.

- Response
   - [provider_npi]


# Handling Multiple instances
If multiple instances of either service are running concurrently to handle a large volume of claims, care must be taken to ensure that each instance is processing unique claims and that there are no database conflicts.

To deal with this, the Claim Process service can employ a distributed lock to ensure that only one instance is processing a given claim at any given time. This can be done with a library such as redis-py or python-etcd.

Similarly, the Payments service can use a distributed lock to ensure that only one instance of a payment is processing it at any given time.

# Handling rate limiter for 5th requirement
We include a rate limiter by utilizing the FastAPILimiter and RateLimiter classes from the fastapi-limiter library. The key_func argument specifies a function that generates a unique key for each client request, which is used to track the rate limit for that client. In this example, we'll use the client's IP address as the key.

The limiter.limit decorator is used to apply the rate limiter to the endpoint, with a limit of 10 requests per minute. If a client exceeds this limit, a 429 Too Many Requests response will be returned.


# Failure handling
If either service fails, steps will be taken to reverse the process. For example, if the Claim Process service or payment service fails, the partially processed claim is rolled back and the database is left in its previous state. 

To handle communication failures between services, the Claim Process service can retry the request a set number of times before giving up. If it continues to fail, it can log the error and notify an administrator, as well as take other corrective actions.
