# the base image: Python 3.12 on a stripped-down Debian. Small, standard.
FROM python:3.12-slim
# every later command runs from this folder inside the image
WORKDIR /app
# dependencies first — this is the cache lesson from Theory 2
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# now the code — the layer that changes every session goes last
COPY . .
# the program (fixed) + its default arguments (replaceable) — Theory 3
ENTRYPOINT ["python", "ingest.py"]
CMD ["--help"]
 