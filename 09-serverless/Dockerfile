FROM agrigorev/model-2025-hairstyle:v1

# instalar dependências
RUN pip install --no-cache-dir numpy pillow onnxruntime

# copiar o código do lambda
COPY lambda_function.py .

# apontar o handler do lambda
CMD ["lambda_function.lambda_handler"]
