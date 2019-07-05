FROM python:3.6
WORKDIR /tailssubmission
COPY . /tailssubmission
EXPOSE 5000
ENV POSTCODE_API=https://api.postcodes.io/postcodes
ENV HOST_IP=0.0.0.0

RUN pip install -r requirements.txt
RUN python -m unittest

ENTRYPOINT ["python","app.py"]