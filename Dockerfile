FROM python:3.11.4
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh","./entrypoint.sh"]