# CineReserve 🎬

Um sistema completo de reserva de ingressos para cinemas, desenvolvido com Django REST Framework no backend.

## 📋 Descrição do Projeto

**CineReserve** é uma plataforma que permite aos usuários:
- 🔐 Registrar-se e fazer login
- 🎥 Navegar por filmes disponíveis
- 🕐 Visualizar sessões (horários) de cada filme
- 🪑 Reservar assentos específicos em uma sala
- 📅 Acompanhar histórico de reservas

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.14+** - Linguagem de programação
- **Django 6.0.3** - Framework web Python
- **PostgreSQL** - Banco de dados

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- [Python 3.14+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [PostgreSQL 12+](https://www.postgresql.org/download/)
- [Poetry](https://python-poetry.org/docs/#installation) (para gerenciar dependências Python)

## 🚀 Instalação e Configuração

### 1. Configurar o Banco de Dados PostgreSQL

Abra o psql ou seu cliente PostgreSQL e execute:

```sql
CREATE DATABASE cinereserve;
CREATE USER postgres WITH PASSWORD '1234';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET default_transaction_deferrable TO off;
ALTER ROLE postgres SET default_transaction_read_only TO off;
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE cinereserve TO postgres;
```

### 2. Configurar o Backend (Django)

```bash
# Navegue até a pasta do backend
cd CineReserve

# Instale as dependências com Poetry
poetry install

# Crie um arquivo .env na raiz do projeto (ou atualize-o)
# Conteúdo do .env:
NAME=cinereserve
USER=postgres
PASSWORD=senha
HOST=localhost
PORT=5432

# Rode as migrações do banco de dados
poetry run python manage.py migrate

# Crie um superusuário (para acessar o painel admin)
poetry run python manage.py createsuperuser

# Inicie o servidor de desenvolvimento
poetry run python manage.py runserver
```

O backend estará disponível em **http://localhost:8000**

### 3. Configurar o Frontend (React)

```bash
# Navegue até a pasta do frontend
cd Front/fronend-cinema

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em **http://localhost:5173** (ou a porta indicada no terminal)

## 📱 Como Executar o Projeto

### Opção 1: Execução Manual

Abra **dois terminais** diferentes:

**Terminal 1 - Backend:**
```bash
cd CineReserve
poetry run python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd Front/fronend-cinema
npm run dev
```

Após iniciar ambos, acesse o frontend em **http://localhost:5173**


## 🔌 Endpoints da API

### Autenticação
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/auth/register/` | Registrar novo usuário |
| POST | `/api/auth/login/` | Fazer login (retorna tokens JWT) |
| POST | `/api/auth/refresh/` | Renovar token de acesso |

### Filmes
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/filmes/` | Listar todos os filmes | ❌ |
| POST | `/api/filmes/` | Criar novo filme | ✅ (Staff) |
| GET | `/api/filmes/{id}/` | Detalhes de um filme | ❌ |
| GET | `/api/filmes/{id}/sessoes/` | Sessões de um filme | ❌ |

### Salas
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/salas/` | Listar todas as salas | ❌ |
| POST | `/api/salas/` | Criar nova sala | ✅ (Staff) |

### Sessões
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/sessoes/` | Listar todas as sessões | ❌ |
| GET | `/api/sessoes/?filme={id}` | Filtrar por filme | ❌ |
| GET | `/api/sessoes/{id}/assentos_ocupados/` | Assentos ocupados | ❌ |
| POST | `/api/sessoes/` | Criar nova sessão | ✅ (Staff) |

### Reservas
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/reservas/` | Criar reserva | ✅ |
| GET | `/api/reservas/` | Minhas reservas | ✅ |
| PATCH | `/api/reservas/{id}/` | Atualizar reserva | ✅ |

