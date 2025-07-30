# 🚀 Desafio Técnico UOL - API Flask

API desenvolvida para processar dados de usuários do UOL a partir de arquivos texto, aplicando filtros por faixa de mensagens, pasta `INBOX` e username.


## 🚀 Como rodar com Docker Compose

### Pré-requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Clone o projeto:

```bash
git clone https://github.com/seu_usuario/desafio-uol.git
cd desafio-uol

docker-compose up --build
docker-compose up -d
http://localhost:8001
```
## 📂 Upload de Arquivo

**Endpoint:** `PUT /upload`  
**Descrição:** Envia um arquivo `.txt` ou `.sh` para a pasta de dados.  
**Parâmetros:**  
- Enviar no `form-data` o campo:  
  - `file`: (arquivo a ser enviado)

**Exemplo no Insomnia ou Postman:**
PUT http://localhost:8001/upload
Body: Multipart Form
Campo: file | arquivo.txt



---

## 📊 Rota de Consulta por Faixa de Mensagens

**Endpoint:** `GET /usuarios_por_mensagens`  
**Parâmetros:**
- `nome_arquivo` (obrigatório): nome do arquivo dentro da pasta `data/`
- `min` (opcional): número mínimo de mensagens
- `max` (opcional): número máximo de mensagens
- `username` (opcional): filtro por parte do e-mail
- `page` (opcional): número da página para paginação (default 1)
- `limit` (opcional): quantidade por página (default 10)

**Exemplos:**

1. Todos usuários entre 1000 e 5000 mensagens:
GET http://localhost:8001/usuarios_por_mensagens?nome_arquivo=input&min=1000&max=5000


2. Buscar por username específico:
GET http://localhost:8001/usuarios_por_mensagens?nome_arquivo=input&username=_tojnel@uol.com.br


3. Paginar resultados:
GET http://localhost:8001/usuarios_por_mensagens?nome_arquivo=input&page=2&limit=10


---

## ⚙️ Estrutura esperada dos dados
O arquivo deve conter linhas no seguinte formato:
email@uol.com.br inbox 001234567 size 012345678


A API filtra apenas linhas com `inbox` e que estejam dentro da faixa de mensagens especificada.

---

## 🧪 Testes

- Utilize `Insomnia` ou `Postman` para testar upload e chamadas.
- Certifique-se que os arquivos estejam dentro da pasta `data/`.

---

## 🧑‍💻 Autor

Desenvolvido por Jonathan Souza para o desafio técnico da UOL.
