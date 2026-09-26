# 📅 MVP2 — Scheduling Backend

Backend REST responsável pelo **gerenciamento de consultas** do sistema de gestão de saúde.

Este serviço faz parte de uma arquitetura composta por:

* [**Frontend** — interface web (docker-composer)](https://github.com/maloisio/mvp2-healthcare-frontend)
* [**BFF (Backend for Frontend)** — API GraphQL que centraliza as requisições do frontend](https://github.com/maloisio/mvp2-bff)
* [**Patient Backend** — gerenciamento de pacientes](https://github.com/maloisio/mvp2-patient-backend)
* [**Scheduling Backend** — gerenciamento de consultas](https://github.com/maloisio/mvp2-scheduling-backend)


---

## 📌 Responsabilidade

O Scheduling Backend é responsável pelos dados relacionados às consultas.

Suas principais funcionalidades são:

* Cadastrar consultas
* Consultar consultas de um paciente
* Consultar consultas de vários pacientes
* Remover uma consulta
* Remover todas as consultas de um paciente
* Validar a existência de pacientes através do Patient Backend











# ️ 🚀 Como executar

### As instruções de como executar estão no diretório do projeto mvp2-healthcare-frontend
a
 🏗️ Arquitetura

```text
┌─────────────────────┐
│      Frontend       │
│   HTML / CSS / JS   │
└──────────┬──────────┘
           │
           │ GraphQL
           ▼
┌─────────────────────┐ REST  ┌─────────┐    
│         BFF         │◄─────►│  ViaCEP │ 
│ Flask + Ariadne     │       │         │ 
└──────────┬──────────┘       └─────────┘
           │
           ├──────────────────────────┐
           │                          │
           │ REST                     │ REST
           ▼                          ▼
┌─────────────────────┐      ┌─────────────────────┐
│   Patient Backend   │◄────►│ Scheduling Backend  │
│      Flask          │      │       Flask         │
└─────────────────────┘      └─────────────────────┘
           │                          │
           ▼                          ▼

```

O frontend **não acessa diretamente os backends REST**.

A comunicação principal da aplicação ocorre da seguinte maneira:



```text
Frontend
   │
   │ GraphQL
   ▼
 BFF
   │
   ├── REST ──► Patient Backend
   │
   └── REST ──► Scheduling Backend
```
---

# 🔄 Comunicação com o BFF

O BFF possui um serviço responsável por consumir os endpoints do Scheduling Backend:

```text
BFF
 │
 │ scheduling_service.py
 │
 ├── GET /appointments/patient/{patient_id}
 ├── GET /appointments/batch
 ├── POST /appointment
 └── DELETE /appointment/{appointment_id}
```

O BFF possui um `schedulling_service.py` responsável por realizar essas chamadas.

Exemplo:

```python
response = requests.get(
    f"{SCHEDULING_BACKEND_URL}/appointments/patient/{patient_id}",
    timeout=5
)
```



---

# 👤 Comunicação com o Patient Backend

O Scheduling Backend também precisa consultar o Patient Backend.

Isso acontece principalmente quando uma consulta é criada.

Antes de criar uma consulta, o serviço verifica se o paciente informado existe.

```text
Frontend
   │
   ▼
BFF
   │
   ▼
Scheduling Backend
   │
   │ GET /patient/{patient_id}
   ▼
Patient Backend
   │
   ├── Paciente existe
   │       │
   │       ▼
   │   cria consulta
   │
   └── Paciente não existe
           │
           ▼
       retorna erro
```

# 🐳 Execução com Docker

A aplicação também possui um `Dockerfile`.

A imagem pode ser construída com:

```bash
docker build -t schedulling-backend .
```

##  Entretanto, no ambiente completo do projeto, o serviço é executado pelo `docker-compose.yml` localizado no repositório principal do [frontend](https://github.com/maloisio/mvp2-healthcare-frontend).
# 📖 OpenAPI

A API possui documentação automática através do Flask-OpenAPI3.

Com o serviço local:

```text
http://localhost:5001/openapi
```

A documentação permite testar os endpoints diretamente pelo navegador.


---

# 🛠️ Tecnologias

* Python
* Flask
* Flask-OpenAPI3
* Pydantic
* Requests
* SQLAlchemy
* Docker

---



