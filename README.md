# 📁 File Organizer and analyzer API

API REST para organização e análise de arquivos com múltiplos filtros e categorização automática.

API desenvolvida com **FastAPI** para organizar, analisar e filtrar arquivos de um diretório.

---

## 🚀 Funcionalidades

* 📂 Listar arquivos e pastas
* 🔍 Filtrar por:

  * nome
  * extensão
  * data (dia, mês, ano)
  * tamanho mínimo
* 📊 Estatísticas de arquivos
* 🗂️ Organização automática por categoria
* 🕒 Listagem de arquivos mais recentes
* 📦 Listagem dos maiores arquivos
* 📁 Categoria automática **"outros"** para arquivos não identificados

---

## 🛠️ Tecnologias

* Python
* FastAPI
* Uvicorn

---

## ▶️ Como rodar o projeto

```bash
git clone https://github.com/davizeds/file-organizer-analyzer-api.git
cd file-organizer-analyzer-api

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Acesse a documentação automática:

```
http://127.0.0.1:8000/docs
```

---

## 📌 Endpoints

### 🔹 GET `/files`

Lista arquivos e pastas com filtros opcionais.

**Parâmetros:**

* `caminho` (obrigatório)
* `nome`
* `extensao`
* `dia`, `mes`, `ano`
* `tamanho_minimo`

**Exemplo:**

```
/files?caminho=C:/Users/Usuario/Downloads&nome=relatorio
```

---

### 🔹 POST `/organize/preview`

Mostra como os arquivos serão organizados.

**Body:**

```json
{
  "caminho": "C:/Users/Usuario/Downloads"
}
```

---

### 🔹 POST `/organize/run`

Cria pastas e move os arquivos automaticamente.

---

### 🔹 GET `/stats`

Retorna estatísticas dos arquivos por categoria.

---

### 🔹 GET `/recent`

Lista arquivos mais recentes.

**Parâmetros:**

* `caminho`
* `limite`

---

### 🔹 GET `/largest`

Lista os maiores arquivos.

**Parâmetros:**

* `caminho`
* `limite`

---

## 📂 Estrutura do projeto

```
app/
├── main.py
├── routers/
├── services/
├── core/
```

---

## 💡 Objetivo do projeto

Este projeto foi desenvolvido com o objetivo de praticar conceitos de backend com Python, incluindo:

* criação de APIs com FastAPI
* organização de código em módulos
* manipulação de arquivos
* construção de lógica de negócio reutilizável

---

## 📌 Observações

* Funciona com caminhos locais do sistema operacional
* Ideal para fins de estudo e portfólio

---

## 👨‍💻 Autor

Desenvolvido por Davi Felipe Nasario🚀
