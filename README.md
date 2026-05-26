# 💰 Financial App (Desktop)

## 🇧🇷 Português

### 📌 Sobre o projeto

Aplicação desktop para controle financeiro desenvolvida com **Python + PyQt6 + PostgreSQL**.

O sistema permite gerenciar transações financeiras com operações completas de CRUD, incluindo filtros dinâmicos para consulta de dados.

---

### 🚀 Tecnologias utilizadas

* Python
* PyQt6
* PostgreSQL
* psycopg
* dotenv
* Git / GitHub

---

### 📊 Funcionalidades

#### Categorias

* Criar categoria
* Listar categorias
* Atualizar categoria
* Deletar categoria

#### Transações

* Criar transação
* Buscar transações com filtros:

  * Descrição
  * Categoria
  * Tipo (income/expense)
  * Status
  * Intervalo de datas
  * Valor mínimo e máximo
* Atualizar transação
* Deletar transação

---

### 🧠 Conceitos aplicados

* CRUD completo
* Conexão com banco de dados (PostgreSQL)
* Queries dinâmicas com filtros
* Uso de `.env` para variáveis sensíveis
* Separação de telas (arquitetura por janelas)
* Manipulação de dados com PyQt (QTableWidget, QComboBox, QDateEdit)

---

### ⚙️ Configuração do ambiente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repo.git
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` com:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

4. Execute o projeto:

```bash
python main.py
```

---

### 📌 Próximos passos

* Melhorias na UI/UX
* Validação de inputs
* Dashboard com gráficos
* Sistema de autenticação
* Separação em camadas (services/repositories)

---

---

## 🇺🇸 English

### 📌 About the project

Desktop financial management application built with **Python + PyQt6 + PostgreSQL**.

The system allows full CRUD operations for financial transactions, including dynamic filters for data querying.

---

### 🚀 Technologies

* Python
* PyQt6
* PostgreSQL
* psycopg
* dotenv
* Git / GitHub

---

### 📊 Features

#### Categories

* Create category
* List categories
* Update category
* Delete category

#### Transactions

* Create transaction
* Search transactions with filters:

  * Description
  * Category
  * Type (income/expense)
  * Status
  * Date range
  * Min and max amount
* Update transaction
* Delete transaction

---

### 🧠 Concepts applied

* Full CRUD operations
* Database integration (PostgreSQL)
* Dynamic SQL queries with filters
* Environment variables with `.env`
* Multi-window UI architecture
* PyQt widgets (QTableWidget, QComboBox, QDateEdit)

---

### ⚙️ Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repo.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
```

4. Run the application:

```bash
python main.py
```

---

### 📌 Next steps

* UI/UX improvements
* Input validation
* Dashboard with charts
* Authentication system
* Layered architecture (services/repositories)

---
