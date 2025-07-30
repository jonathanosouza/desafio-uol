# 🚀 Desafio Técnico UOL - API Flask

API desenvolvida para processar dados de usuários do UOL a partir de arquivos texto, aplicando filtros por faixa de mensagens, pasta `INBOX` e username.

---

## 🚀 Como rodar com Docker Compose

### Pré-requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Clone o projeto

```bash
git clone https://github.com/seu_usuario/desafio-uol.git
cd desafio-uol
```

### Suba o container

```bash
docker-compose up --build
# Ou em segundo plano
docker-compose up -d
```

Acesse: [http://localhost:8001](http://localhost:8001)

---

## 📂 Upload de Arquivo

**Endpoint:** `PUT /upload`  
**Descrição:** Envia um arquivo `.txt` ou `.sh` para a pasta de dados.

**Exemplo no Insomnia/Postman:**

```
PUT http://localhost:8001/upload
Body: Multipart Form
Campo: file | arquivo.txt
```

---

## 📚 Listar Arquivos

**Endpoint:** `GET /listar_arquivos`  
**Descrição:** Retorna a lista de arquivos disponíveis na pasta `data/`.

**Exemplo:**

```
GET http://localhost:8001/listar_arquivos
```

---

## 📏 Listar Tamanho de Arquivos de um Usuário

**Endpoint:** `GET /size`  
**Descrição:** Lista as mensagens e tamanhos de arquivos filtrando por usuário.

**Parâmetros:**

| Parâmetro | Tipo    | Obrigatório | Descrição                       |
|-----------|---------|-------------|---------------------------------|
| filename  | string  | ✅ Sim       | Nome do arquivo em `data/`      |
| username  | string  | ✅ Sim       | Parte ou nome completo do e-mail |
| mode      | string  | ❌ Não       | `"min"` para menor arquivo       |

**Exemplos:**

```
GET http://localhost:8001/size?filename=input&username=joao@uol.com.br
GET http://localhost:8001/size?filename=input&username=joao@uol.com.br&mode=min
```

---

## 📊 Listar Usuários Por Mensagem

**Endpoint:** `GET /usuarios_por_mensagens`

### Parâmetros:

| Parâmetro     | Obrigatório | Tipo     | Descrição                                                      |
|---------------|-------------|----------|----------------------------------------------------------------|
| nome_arquivo  | ✅ Sim      | string   | Nome do arquivo dentro da pasta `data/`                        |
| min           | ❌ Não      | inteiro  | Número mínimo de mensagens                                     |
| max           | ❌ Não      | inteiro  | Número máximo de mensagens                                     |
| username      | ❌ Não      | string   | Filtro por parte do e-mail                                     |
| page          | ❌ Não      | inteiro  | Número da página (default: 1)                                  |
| limit         | ❌ Não      | inteiro  | Resultados por página (default: 10)                            |

**Exemplos:**

```
GET http://localhost:8001/usuarios_por_mensagens?nome_arquivo=input&min=1000&max=5000
GET http://localhost:8001/usuarios_por_mensagens?nome_arquivo=input&username=ana@uol.com.br
GET http://localhost:8001/usuarios_por_mensagens?nome_arquivo=input&page=2&limit=20
```

---

## 🔢 Listar Usuários Ordenados por Mensagens

**Endpoint:** `GET /ordenar_usuarios`  
**Descrição:** Lista os usuários ordenados por número de mensagens de forma decrescente.

**Parâmetros:**

| Parâmetro     | Obrigatório | Tipo     | Descrição                               |
|---------------|-------------|----------|-----------------------------------------|
| nome_arquivo  | ✅ Sim      | string   | Nome do arquivo dentro da pasta `data/` |

**Exemplo:**

```
GET http://localhost:8001/ordenar_usuarios?nome_arquivo=input
```

---

## ⚙️ Estrutura esperada dos dados

O arquivo `.txt` enviado deve conter linhas no seguinte formato:

```
email@uol.com.br inbox 001234567 size 012345678
```

- A API filtra apenas linhas com a pasta `inbox`
- E com o número de mensagens dentro da faixa especificada (`min`, `max`)

---

## 🧪 Testes

- Utilize `Insomnia` ou `Postman` para testar upload e chamadas
- Certifique-se de que os arquivos estejam na pasta `data/` após o upload

---

## 🧑‍💻 Autor

Desenvolvido por **Jonathan Souza**  
📧 jonathanosouza@uol.com.br  
🧪 Desafio Técnico UOL - 2025
