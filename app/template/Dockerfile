FROM alpine
FROM club9822/scientific-libs:latest
FROM club9822/ta-lib:latest
ENV TZ=Asia/Tehran
WORKDIR /
COPY . /

RUN pip install -r /requirements.txt

EXPOSE 7000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000"]