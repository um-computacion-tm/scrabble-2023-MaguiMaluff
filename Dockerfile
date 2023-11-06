FROM python:3-alpine

WORKDIR /scrabble-2023-MaguiMaluff

RUN apk update

RUN apk add git

RUN git clone https://github.com/um-computacion-tm/scrabble-2023-MaguiMaluff.git

WORKDIR /scrabble-2023-MaguiMaluff

COPY . .

RUN pip install -r requirements.txt

CMD [ "sh", "-c", "coverage run -m unittest && coverage report -m && python3 -m scrabble-2023-MaguiMaluff.scrabble_main" ]