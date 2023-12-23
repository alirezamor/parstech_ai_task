python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py import_shipments initial_data.csv
gunicorn --bind 0.0.0.0:8000 parstech_ai_task.asgi -w 4 --worker-class uvicorn.workers.UvicornWorker


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