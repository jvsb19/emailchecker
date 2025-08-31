FROM python:3.10-slim

WORKDIR /app

# Instalar dependências do sistema (ex: para pdf, etc.)
RUN apt-get update && apt-get install -y \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do app
COPY . .

# Definir variável de ambiente
ENV PORT=7860

# Comando de inicialização
CMD ["python", "app.py"]
ENV TRANSFORMERS_CACHE=/app/cache
