# กำหนด Python image
FROM python:3.11-slim

# ตั้ง working directory
WORKDIR /app

# copy requirements ก่อน (เพื่อ cache)
COPY requirements.txt .

# install dependency
RUN pip install --no-cache-dir -r requirements.txt

# copy code
COPY . .

# expose port
EXPOSE 8000

# run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]