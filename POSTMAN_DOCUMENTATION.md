# Documentação Postman - CineReserve API

Documentação completa da API CineReserve para uso no Postman.

## Importação para Postman

### 1. Importar Collection e Environment

1. Abra o Postman
2. Clique em **Import** (Ctrl+O)
3. Selecione os dois arquivos:
   - `CineReserve.postman_collection.json` - Requisições da API
   - `CineReserve.postman_environment.json` - Variáveis de ambiente

### 2. Ativar o Environment

1. No canto superior direito, clique no dropdown de ambiente
2. Selecione **CineReserve Development**

## Fluxo de Autenticação

### Passo 1: Registrar um Novo Usuário

**Requisição**: `POST /api/auth/register/`

```json
{
  "username": "seu_usuario",
  "email": "seu_email@example.com",
  "password": "sua_senha_segura"
}
```

**Resposta**: 201 Created
```json
{
  "id": 2,
  "username": "seu_usuario",
  "email": "seu_email@example.com"
}
```

### Passo 2: Fazer Login e Obter Token

**Requisição**: `POST /api/auth/login/`

```json
{
  "username": "seu_usuario",
  "password": "sua_senha_segura"
}
```

**Resposta**: 200 OK
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

⚠️ **IMPORTANTE**: Copie o valor de `access` e salve na variável `{{access_token}}` do seu environment

**Para salvar automaticamente no Postman** (versão melhorada):

Na aba **Tests** da requisição de login, adicione:

```javascript
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.access);
    pm.environment.set("refresh_token", jsonData.refresh);
}
```

### Passo 3: Usar o Token em Requisições

Todas as requisições que requerem autenticação usam automaticamente a variável `{{access_token}}` via Bearer Token configurado no environment.

### Renovar Token (quando expirar)

**Requisição**: `POST /api/auth/refresh/`

```json
{
  "refresh": "{{refresh_token}}"
}
```

**Resposta**: 200 OK
```json
{
  "access": "novo_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Seções da API

### 1. Autenticação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/auth/register/` | Registrar novo usuário |
| POST | `/api/auth/login/` | Fazer login (obter tokens JWT) |
| POST | `/api/auth/refresh/` | Renovar access token |

**Permissões**: 
- Register: Sem autenticação (AllowAny)
- Login: Sem autenticação (AllowAny)  
- Refresh: Sem autenticação (AllowAny)

### 2. Filmes 🎬

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/api/filmes/` | Listar todos | Não |
| POST | `/api/filmes/` | Criar novo | Staff only |
| GET | `/api/filmes/{id}/` | Detalhes | Não |
| PATCH | `/api/filmes/{id}/` | Atualizar | Staff only |
| DELETE | `/api/filmes/{id}/` | Deletar | Staff only |

**Exemplo de Criação**:
```json
{
  "titulo": "Avatar 3",
  "duracao": 180,
  "em_cartaz": true
}
```

### 3. Salas 🎪

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/api/salas/` | Listar todas | Não |
| POST | `/api/salas/` | Criar nova | Staff only |
| GET | `/api/salas/{id}/` | Detalhes | Não |
| PATCH | `/api/salas/{id}/` | Atualizar | Staff only |
| DELETE | `/api/salas/{id}/` | Deletar | Staff only |

**Exemplo de Criação**:
```json
{
  "nome": "Sala IMAX 1",
  "colunas": 15,
  "fileiras": 12
}
```

**Limites**:
- Colunas: Máximo 99 (assentos por fileira)
- Fileiras: Máximo 26 (validados como A-Z)
- Padrão: 10x10

### 4. Sessões 🎞️

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/api/sessoes/` | Listar todas | Não |
| GET | `/api/filmes/{id}/sessoes/` | Listar sessões de um filme | Não |
| POST | `/api/sessoes/` | Criar nova | Staff only |
| GET | `/api/sessoes/{id}/` | Detalhes | Não |
| GET | `/api/sessoes/{id}/assentos_ocupados/` | Assentos ocupados | Não |
| PATCH | `/api/sessoes/{id}/` | Atualizar | Staff only |
| DELETE | `/api/sessoes/{id}/` | Deletar | Staff only |

**Filtro por filme específico**:
- `GET /api/sessoes/?filme=1`
- Retorna somente sessões do filme informado.

**Endpoint direto por filme específico**:
- `GET /api/filmes/1/sessoes/`
- Retorna todas as sessões do filme informado (ordenadas por `horario_inicio`).

**Exemplo de resposta do endpoint direto**:
```json
[
  {
    "id": 3,
    "sala": 3,
    "sala_nome": "Sala IMAX 1",
    "filme": 2,
    "filme_titulo": "Avatar 3",
    "assentos_disponiveis": 180,
    "horario_inicio": "2026-03-22T19:00:00Z"
  },
  {
    "id": 4,
    "sala": 3,
    "sala_nome": "Sala IMAX 1",
    "filme": 2,
    "filme_titulo": "Avatar 3",
    "assentos_disponiveis": 180,
    "horario_inicio": "2026-03-22T21:00:00Z"
  }
]
```

**Exemplo de Criação**:
```json
{
  "filme": 1,
  "sala": 1,
  "horario_inicio": "2026-03-25T19:30:00Z"
}
```

**Resposta com Assentos Ocupados**:
```json
{
  "sessao": 1,
  "assentos_ocupados": [
    {"fileira": "A", "coluna": 1},
    {"fileira": "A", "coluna": 2}
  ],
  "total_ocupados": 2
}
```

**Propriedade Automática**: 
- `assentos_disponiveis`: Calculado como (capacidade_sala - reservas_confirmadas)

### 5. Reservas de Assentos 🎫

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/api/reservas/` | Minhas reservas | Sim (JWT) |
| POST | `/api/reservas/` | Criar nova | Sim (JWT) |
| GET | `/api/reservas/{id}/` | Detalhes | Sim (JWT) |
| PATCH | `/api/reservas/{id}/` | Atualizar status | Sim (JWT) |
| DELETE | `/api/reservas/{id}/` | Cancelar | Sim (JWT) |

**Exemplo de Criação**:
```json
{
  "sessao": 1,
  "fileira": "A",
  "coluna": 5
}
```

**Validações Automáticas**:
- ✅ Assento não pode estar duplicado (unique constraint)
- ✅ Fileira deve ser letra A-Z
- ✅ Coluna deve estar dentro do range da sala (1 a N)
- ✅ Fileira deve estar dentro do range da sala (A a X)

**Erros Comuns**:

```json
// Erro: Assento já reservado
{
  "non_field_errors": ["Este assento já foi reservado."]
}

// Erro: Coluna inválida
{
  "coluna": ["Coluna deve estar entre 1 e 15"]
}

// Erro: Fileira inválida
{
  "fileira": ["Fileira informada está fora do limite da sala"]
}
```

**Status de Reserva**:
- `R` = Reservado (padrão)
- `P` = Presente (usado no cinema)

**Setor de Usuário vs Staff**:
- **Usuários comuns**: Veem apenas suas próprias reservas via GET `/api/reservas/`
- **Staff**: Veem todas as reservas de todos os usuários

## Exemplos de Fluxo Completo

### Fluxo 1: Usuário Comum Fazendo Reserva

```
1. POST /api/auth/register/
   {username, email, password}
   → Obtém id do usuário

2. POST /api/auth/login/
   {username, password}
   → Obtém access_token, refresh_token

3. GET /api/filmes/
   → Lista filmes disponíveis

4. GET /api/salas/
   → Lista salas disponíveis

5. POST /api/sessoes/
   (staff cria sessão de filme em sala)
   → Obtém sessao_id

6. GET /api/sessoes/{id}/assentos_ocupados/
   → Vê qual assento está livre

7. POST /api/reservas/
   {sessao: 1, fileira: "A", coluna: 5}
   → Reserva criada com sucesso!

8. GET /api/reservas/
   → Vê todas suas reservas
```

### Fluxo 2: Admin Criando Setup Inicial

```
1. Login como staff (admin/Admin@12345)
   POST /api/auth/login/

2. Criar Filmes
   POST /api/filmes/
   {titulo: "Avatar 3", duracao: 180, em_cartaz: true}

3. Criar Salas
   POST /api/salas/
   {nome: "Sala 1", colunas: 15, fileiras: 10}

4. Criar Sessões
   POST /api/sessoes/
   {filme: 1, sala: 1, horario_inicio: "2026-03-25T19:30:00Z"}

5. Gerenciar Reservas (view all)
   GET /api/reservas/

6. Atualizar Status (marcar como presente)
   PATCH /api/reservas/1/
   {status: "P"}
```

## Superusuário Padrão

**Credenciais para desenvolvimento**:
- Username: `admin`
- Senha: `Admin@12345`

Use essas credenciais para fazer login e acessar a interface admin em `/admin/`

## Tratamento de Erros

### Autenticação

```json
// 401 Unauthorized - Token inválido ou expirado
{
  "detail": "Invalid token."
}

// 403 Forbidden - Sem permissão suficiente
{
  "detail": "You do not have permission to perform this action."
}
```

### Validação

```json
// 400 Bad Request - Dados inválidos
{
  "campo": ["Descrição do erro"]
}
```

### Não encontrado

```json
// 404 Not Found - Recurso não existe
{
  "detail": "Not found."
}
```

## Dicas de Uso

### 1. Organizar Requisições no Postman

Use as pastas já organizadas:
- `Autenticação` - Login, registro, refresh
- `Filmes` - CRUD de filmes
- `Salas` - CRUD de salas  
- `Sessões` - CRUD de sessões
- `Reservas` - CRUD de reservas

### 2. Usar Variáveis de Ambiente

Você pode criar variáveis adicionais para testes:

```
{{base_url}} - URL base da API (padrão: http://127.0.0.1:8000)
{{access_token}} - Token JWT do usuário autenticado
{{refresh_token}} - Token para renovação
```

### 3. Testar Casos de Erro

Teste situações que geram erros 400:
- Criar assento duplicado
- Coluna fora do range
- Fileira inválida (não é letra de A-Z)

### 4. Monitor e Automação

Use a aba **Tests** para:
- Validar respostas esperadas
- Salvar tokens automaticamente após login
- Executar testes em sequência com **Collection Runner**

## Documentação Adicional

### Modelo de Dados

**Filme**
- `id` (int): ID único
- `titulo` (string): Nome do filme
- `duracao` (int): Minutos
- `em_cartaz` (bool): Ativo ou não

**Sala**
- `id` (int): ID único
- `nome` (string): Nome da sala
- `colunas` (int): Assentos horizontais
- `fileiras` (int): Assentos verticais

**Sessão**
- `id` (int): ID único
- `filme` (int): ID do filme FK
- `sala` (int): ID da sala FK
- `horario_inicio` (datetime): ISO 8601 UTC
- `assentos_disponiveis` (int): Calculado automaticamente

**Reserva**
- `id` (int): ID único
- `usuario` (int): ID do usuário FK
- `sessao` (int): ID da sessão FK
- `fileira` (string): A-Z
- `coluna` (int): 1-N
- `status` (string): R (Reservado) ou P (Presente)
- `data_reserva` (datetime): Auto-preenchido

### Paginação

O Postman normalmente retorna respostas paginadas para listas:

```json
{
  "count": 10,
  "next": "http://127.0.0.1:8000/api/filmes/?page=2",
  "previous": null,
  "results": [...]
}
```

Use `?page=N` para ir para outra página.

---

**Última atualização**: Março 22, 2026
