FROM python:3.13.7-slim

# Avoid interactive tzdata prompts, speed up apt
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHERUSAGESTATS=false

WORKDIR /app

RUN apt-get update && apt-get install -y \
   build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

ENV FOLDER="project_aiai18h"
COPY ${FOLDER}/ ./${FOLDER}/
COPY streamtex_package/ ./streamtex_package/

WORKDIR /app/${FOLDER}

ENV PORT=8501
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "book.py", "--server.port=8501", "--server.address=0.0.0.0"]
