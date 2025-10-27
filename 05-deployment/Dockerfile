FROM agrigorev/zoomcamp-model:2025

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/* \
 && curl -LsSf https://astral.sh/uv/install.sh | sh \
 && ln -s /root/.local/bin/uv /usr/local/bin/uv

COPY pyproject.toml ./
# sem --frozen (deixa o uv resolver e criar o lock durante o build)
RUN uv sync --no-dev

COPY app.py ./app.py
COPY pipeline_v1.bin ./pipeline_v1.bin

EXPOSE 9696
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9696"]
