# Rotina Animal - Configuração Local

Passo a passo rápido para rodar o projeto na sua máquina com PostgreSQL.

### 1. Banco de Dados e Ambiente

1. Abra o pgAdmin, clique com o botão direito em **Databases** > **Create** > **Database...** e crie um banco chamado `rotina_animal_db`.
2. Na raiz do projeto, crie um arquivo chamado `.env` e cole a estrutura abaixo (ajuste a senha se a sua for diferente):

```.env
SECRET_KEY=django-insecure-nd=6v)mxrks26uxee!!@hhvqfm-1*))-kzpa!wtq=!2wp0zyhx
DB_NAME=rotina_animal_db
DB_USER=postgres
DB_PASSWORD='sua_senha'
DB_HOST=localhost
DB_PORT=5432
```


### 2. Configurar o Django
Execute os comandos abaixo no terminal, um por um, para gerar os arquivos de migração, criar a estrutura das tabelas no banco e criar a sua conta de administrador:

```
python manage.py makemigrations core
python manage.py migrate
python manage.py createsuperuser
```

### 3. Rodar o Projeto
Inicie o servidor local:

```
python manage.py runserver
```

Acesso ao sistema: http://127.0.0.1:8000/

Painel de Administração (Django Admin): http://127.0.0.1:8000/admin/ (use o superusuário que você criou no passo anterior).
