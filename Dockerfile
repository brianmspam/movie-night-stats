FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

<<<<<<< HEAD
CMD ["python", "run.py"]
=======
CMD ["python", "run.py"]
>>>>>>> 6d933837d92ba68fa3cee8f3d2ca522aec7c11b2
