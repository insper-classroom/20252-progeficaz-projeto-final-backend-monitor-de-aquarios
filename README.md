# API de Monitoramento de Aquários

**Link do back-end:** [52.87.254.97](http://52.87.254.97)  
**Documentação completa:** [Google Docs](https://docs.google.com/document/d/1l-EYmFpR5xTyNQxth-VJdnYsd4AgUx7_Ao2qCU-txK0/edit?usp=sharing)

---

## 📖 Descrição

Este repositório contém a **API back-end** do projeto de **monitoramento e ocupação dos aquários do Insper**, desenvolvida para facilitar o uso dos espaços de estudo coletivo.  
A API é responsável por **gerenciar os dados dos aquários**, **autenticar usuários** e **atualizar o status de ocupação** em tempo real.

O sistema se comunica com o front-end (em React) e com o banco de dados MongoDB, permitindo que usuários consultem, filtrem e ocupem aquários de forma simples e eficiente.

---

## 🚀 Funcionalidades

- Retorna informações de todos os aquários ou de um aquário específico.  
- Filtra aquários por prédio, andar, capacidade e disponibilidade.  
- Permite login e registro de usuários.  
- Atualiza o estado de ocupação dos aquários (ocupar/desocupar).  
- Envia e-mails para aviso de liberação de aquário.  

---

## 🧩 Arquitetura

A API foi construída em **Python com Flask**, e utiliza o **MongoDB** como banco de dados não relacional.  
Ela expõe endpoints RESTful consumidos pela aplicação front-end em React.

```
Frontend (React) ⇄ API (Flask) ⇄ Banco de Dados (MongoDB)
```

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python  
- **Framework:** Flask  
- **Banco de Dados:** MongoDB  

- **Bibliotecas Principais:**
  - `flask` — criação das rotas da API  
  - `flask_cors` — habilitação de requisições entre domínios (front/back)  
  - `flask_jwt_extended` — gerenciamento de autenticação via tokens JWT  
  - `flask_bcrypt` — criptografia de senhas  
  - `pymongo` — integração com o banco de dados MongoDB  
  - `dotenv` — gerenciamento de variáveis de ambiente  
  - `requests` — comunicação com APIs externas  
  - `pytest` — testes automatizados  

- **API Externa:**
  - `Twilio` — utilizada para envio automatizado de e-mails de verificação e notificação de liberação de aquários.

---


## 📡 Endpoints Principais

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/aquarios` | Retorna todos os aquários |
| `GET` | `/aquario/<id>` | Retorna dados de um aquário específico |
| `PUT` | `/aquario/<id>` | Atualiza o status de ocupação (ocupar/desocupar) |
| `GET` | `/filter` | Retorna aquários filtrados (por prédio, andar, tipo, etc.) |
| `POST` | `/register` | Cria um novo usuário |
| `POST` | `/login` | Realiza autenticação de usuário |

---

## 👥 Autores

- Léo Montefusco Maximiano  
- Arthur Belei Zilio Goes  
- Arthur Sampaio Bernardes  
- Guilherme Kenzo Taba Nakamura  
- Giovanna Barros Scalco  
- Lucas Grohmann Haro  
- Victor de Almeida Cunha  

---

## 🌐 Links Importantes

- 🔗 **Back-end:** [52.87.254.97](http://52.87.254.97)  
- 📄 **Documentação completa:** [Google Docs](https://docs.google.com/document/d/1l-EYmFpR5xTyNQxth-VJdnYsd4AgUx7_Ao2qCU-txK0/edit?usp=sharing)
