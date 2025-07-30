FROM python:3.10-slim

# Instala bash e ferramentas essenciais
RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

# Cria a pasta /app e define como diretório de trabalho
WORKDIR /app

# Copia todos os arquivos da pasta local para dentro da imagem
COPY app/ app/
COPY data/ data/       
COPY requirements.txt .

# Instala dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta onde o Flask vai rodar
EXPOSE 8001

# Comando para rodar a aplicação Flask
CMD ["python", "app/main.py"]
