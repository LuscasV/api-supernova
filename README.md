# 🛒 Ecommerce API (Django + PostgreSQL)

API RESTful para um sistema de e-commerce desenvolvida com Django e Django Rest Framework.

---

## 🚀 Tecnologias

- Python
- Django
- Django Rest Framework
- PostgreSQL
- JWT (SimpleJWT)
- SMTP (envio de emails)

---

## 📦 Funcionalidades

### 👤 Autenticação & Usuário
- Cadastro de usuário
- Verificação de email
- Reenvio de email de confirmação
- Login com JWT
- Alteração de senha via token enviado por email
- Perfil de usuário

---

### 🛍️ Produtos
- Cadastro de produtos
- Listagem de produtos
- Filtro de produtos via query params  
  Ex: `?gender=feminino&category=vestidos`
- Produtos em destaque

---

### ❤️ Wishlist
- Adicionar produtos à wishlist
- Remover produtos da wishlist
- Listar wishlist do usuário

---

### 🛒 Carrinho
- Adicionar produtos ao carrinho
- Remover produtos do carrinho
- Listar itens do carrinho

---

### 📦 Pedidos (Orders)
- Criar pedido
- Finalizar compra
- Cancelar pedido
- Listar pedidos do usuário

---

### 📉 Controle de Estoque
- Ao finalizar uma compra:
  - O estoque do produto é automaticamente reduzido

---

### 📍 Endereços
- Cadastrar endereço de entrega
- Listar endereços
- Selecionar endereço no checkout

---

## 📡 Endpoints

| Método | Endpoint        | Descrição            |
|--------|---------------|---------------------|
| POST   | /api/accounts/login  | Login do usuário     |
| POST   | api/accounts/register | Cadastro de usuário |
| POST   | /api/accounts/resend-verification/ | Reenvio de confirmação |
| GET    | /products/ | Listar produtos |
| GET    | /products/?gender=&category= | Filtrar produtos |
| GET    | /cart/ | Listar carrinho |
| POST   | /cart/ | Adicionar item |
| DELETE | /cart/{id}/ | Remover item |
| POST   | /orders/ | Criar pedido |
| GET    | /orders/ | Listar pedidos |
| POST   | /orders/{id}/cancel/ | Cancelar pedido |
---

## 🔐 Autenticação

A API utiliza JWT (JSON Web Token).

### Login:
```http
POST /auth/login/
```
Resposta:
{
  "access": "token",
  "refresh": "token"
}

Use o token no header:

Authorization: Bearer seu_token

---

## ⚙ Instalação

### 1. Clone seu projeto

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2. Crie e ative o ambiente virtual

```bash
- python -m venv env
```

Windows:

```bash
env\Scripts\activate
```

### 3. Instale as dependências

```
pip install -r requirements.txt
```

### 4. Configure o arquivo .env
### Crie um arquivo .env na raiz do projeto:
```bash
SECRET_KEY=sua_chave
DEBUG=True

DB_NAME=seu_banco
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=seu_email
EMAIL_HOST_PASSWORD=sua_senha_email
```

### 5. Rode as migrations

```bash
python manage.py migrate
```

### 5. Crie um super usuário

```bash
python manage.py createsuperuser
```

### 6. Rode o servidor

```bash
python manage.py runserver
```

Acesse:

```bash
http://127.0.0.1:8000/
```

## Envio de emails

A API utiliza SMTP (Gmail) para:

- Verificação de email
- Reset de senha
- Reenvio de confirmação de conta

## Estrutura do Projeto

```
accounts/   -> autenticação e usuários
products/   -> produtos
orders/     -> pedidos
cart/       -> carrinho
```
