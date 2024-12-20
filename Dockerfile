FROM python:3.12

# RUN mkdir /Base_app_dir

WORKDIR /Base_app_dir

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /Base_app_dir

RUN chmod a+x /Base_app_dir/docker/*.sh

# CMD ["gunicorn", "app.app_main.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]