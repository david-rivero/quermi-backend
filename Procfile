release: cd quermi_project && \
         python manage.py migrate --run-syncdb && \
         echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@admin.com', 'admin1234')" | python manage.py shell
web: cd quermi_project && gunicorn quermi_project.wsgi