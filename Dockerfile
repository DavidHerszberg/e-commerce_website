FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get install libmagic1
RUN pip install -r requirements.txt
COPY . /code/
ENV PORT=8000
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]