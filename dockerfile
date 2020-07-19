FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY . /build

WORKDIR /build

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]
