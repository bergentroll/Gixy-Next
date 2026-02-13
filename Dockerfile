FROM python:alpine

WORKDIR /src

COPY setup.py ./
COPY gixy/ ./gixy/

RUN pip install --upgrade pip setuptools wheel
RUN pip install .

CMD ["gixy"]
