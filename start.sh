gunicorn DocWise.wsgi:application --log-file - &

# Start Daphne
daphne -b 0.0.0.0 -p 8001 DocWise.asgi:application