FROM python

ENV SCRIPT_NAME=CheapPriceNotifier.py

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD python3 ${SCRIPT_NAME}
