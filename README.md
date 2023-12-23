## Application requirements
1. Python 3.11+
2. Virtualenv
3. Redis
4. graphql

## Running application
In the first step you need to create virtualenv.
```shell
python -m venv venv
```

Then enable the virtualenv.
```shell
source venv/bin/activate
```

Now we have to run the migrations and gather static files.
```shell
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

After that we need some data to test the api. Some test data is added to the assessment so you can easily add the data 
with the below command
```shell
python manage.py import_shipments initial_data.csv
```

The las step is to add env variables. you have to add `.env` file like below
```shell
OPEN_WEATHER_MAP_API_KEY=somapikey
REDIS_HOST=127.0.0.1 # Or your redis ip
REDIS_PASSWORD=redispassword
REDIS_PORT=6379 #Or your redis port
```

Now we enabled virtualenv and test data. We can run the api with the following command
```shell
#Local system
python manage.py runserver

#In production
gunicorn --bind 0.0.0.0:8000 parstech_ai_task.asgi -w 4 --worker-class uvicorn.workers.UvicornWorker
```


To test the api you can go to `127.0.0.1/graphql` and run the below query to see the result:
```gql
query shipmentQuery{
  shipment(carrier: "GLS", trackingNumber: "TN12345682") {
    id
    receiverAddress
    articles {
      name
      quantity
      price
      SKU
    }
    weather {
      description
      feelsLike
      maxTemp
      temp
      minTemp
    }
  }
}
```


## Project Explanation
In the first step I check if `trackingnumber` exists, then fetch the data from the database the get the destination city
from `reciever_address` and check if weather data is saved in redis or not. The key is city name and value is weather 
info in json format. If weather exist for the city I get the existing data from data else fetch data from openmap api 
and save it in redis. Weather data exists for 2h then we have to fetch new data again.


## Answer for Assessment's Question
1. What were the important design choices and trade-offs you made?
Using setx for data saved in redis, provide graphql, so consumers can easily take whatever they want. Use redis for 
caching.
2. What would be required to deploy this application to production?
We can deploy it as system service so we need gunicorn else we can deploy it via docker. Dockerfile is also provided but 
not tested.
3. What would be required to scale this application to handle 1000 requests per second?
There are multiple ways: We can add more worker to gunicorn or load balance between multiple number of running images
of the application. And if we use another database(like postgresql or mysql) we should use master/slave way. master node
is just for writing data and slave node is for reading.  

