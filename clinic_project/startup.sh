# Clinic Appointment System - Startup Script

pipenv run python clinic_project/manage.py runserver
npm run watch:css

echo "Server started at http://localhost:8000"
echo "CSS watcher started"

# Keep the script running to prevent the container from exiting
while true; do
    sleep 1
done