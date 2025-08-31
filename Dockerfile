FROM python:3.10-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do app
COPY . .

# Criar diretório persistente do cache
RUN mkdir -p /data/cache && chmod -R 777 /data

# Definir variáveis de ambiente
ENV PORT=7860
ENV HF_HOME=/data

# Comando de inicialização
CMD ["python", "app.py"]