FROM python:alpine

WORKDIR /src

COPY setup.py MANIFEST.in ./
COPY gixy/ ./gixy/

RUN pip install --upgrade pip setuptools wheel
RUN pip install .

CMD ["gixy"]
