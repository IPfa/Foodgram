FROM python:3.8.5
RUN mkdir /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY foodgram/ /app 
WORKDIR app/
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]

