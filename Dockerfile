FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN git clone https://github.com/um-computacion-tm/scrabble-2023-MaguiMaluff.git

COPY . .

RUN coverage run -m unittest && coverage report -m

CMD ["python3", "scrabble_main.py"]
