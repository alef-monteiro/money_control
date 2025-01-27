# MoneyControl

**MoneyControl** é uma plataforma de controle financeiro pessoal, desenvolvida com Django e Angular, utilizando Tailwind CSS para o design. A aplicação permite aos usuários registrar seus gastos, criar um perfil e gerenciar suas finanças.

## Tecnologias Utilizadas

- **Backend**: Django, Postgres
- **Frontend**: Angular, Tailwind CSS

## Links dos Repositórios

- [Backend - MoneyControl](https://github.com/alef-monteiro/money_control/)
- [Frontend - MoneyControl](https://github.com/alef-monteiro/front-money-control)

---

## Como Usar o Backend

1. **Configuração do Banco de Dados**
   - Consulte o arquivo `.config` e crie um banco de dados com as credenciais especificadas.
   - Devido a problemas com a biblioteca `psycopg`, o acesso ao banco de dados não é automático. Recomenda-se criar um arquivo Docker para substituir essa configuração.
   
2. **Migrations**
   - Execute `makemigrations` e `migrate` para aplicar as migrações do banco de dados.
   
3. **Criar Superusuário**
   - No terminal, crie um superusuário utilizando o comando:
     ```bash
     python manage.py createsuperuser
     ```
   - Sem um superusuário, o backend não funcionará corretamente. No entanto, é possível contornar isso criando um modelo de controle de usuários ou algo similar.

4. **Acessando o Backend**
   - Acesse o backend localmente em `http://localhost:8000`.
   - Faça login no painel administrativo do Django (`/admin`) com as credenciais do superusuário.
   - Você pode acessar os dados da API em `http://localhost:8000/api`.

**Observação:** A funcionalidade de exibir os gastos mensais não foi implementada devido a restrições de tempo e orçamento. Isso exigiria a utilização de várias bibliotecas em conjunto.

---

## Como Usar o Frontend

1. **Instalar as Dependências**
   - Instale as bibliotecas necessárias com o comando:
     ```bash
     npm install
     ```
   
2. **Rodar o Projeto**
   - Execute o projeto com o comando:
     ```bash
     ng serve
     ```
   - O frontend será acessível em `http://localhost:4200`.

3. **Cadastro e Login**
   - Teste o processo de cadastro e login utilizando os formulários disponibilizados.
   - A plataforma permite adicionar gastos e realizar outras ações relacionadas ao controle financeiro.

**Problemas Conhecidos**:
- Os formulários não possuem alertas visuais para a quantidade de caracteres. Isso pode ser facilmente implementado utilizando `@if` no HTML de cada componente, associando critérios de validação nos `FormBuilder` correspondentes.

**Componentes Necessários**:
- Login
- Register
- Wallet-register
- Card-register
- Card-update
- Profile-update

**Observação:** Por falta de tempo, a implementação do interceptor não foi realizada. Essa funcionalidade necessitaria de mais tempo e um orçamento maior.

---

## Contribuindo

Se você deseja contribuir para o projeto, sinta-se à vontade para enviar pull requests! Para garantir que seu código seja aceito, por favor, siga as boas práticas de codificação e escreva testes, se necessário.

---

**Obrigado por usar o MoneyControl!**
