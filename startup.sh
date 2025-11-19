# Startup Script

pipenv run python clinic_project/manage.py runserver
echo "Server started at http://127.0.0.1:8000"

# Keep the script running to prevent the container from exiting
while true; do
    sleep 1
done