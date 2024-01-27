## Start with `Docker`

> 👉 **Step 1** - Download the code from the GH repository (using `GIT`) 

```bash
$ git clone https://github.com/tdggalvao/modeloPreditivo.git
$ cd modeloPreditivo
```

<br />

> 👉 **Step 2** - Start the APP in `Docker`

```bash
$ chmod +x entrypoint.sh
$ docker-compose up --build 
```

Visit `http://localhost:5085` in your browser. The app should be up & running.

<br />


## Manual Build

> Download the code 

```bash
$ git clone https://github.com/tdggalvao/modeloPreditivo.git
$ cd modeloPreditivo
```

<br />

### 👉 Set Up for `Unix`, `MacOS` 

> Install modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> Generate API

```bash
$ python manage.py generate-api -f
```

<br />

> Start the APP

```bash
$ python manage.py createsuperuser # create the admin
$ python manage.py runserver       # start the project
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />

### 👉 Set Up for `Windows` 

> Install modules via `VENV` (windows) 

```
$ virtualenv env
$ .\env\Scripts\activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> Start the APP

```bash
$ python manage.py createsuperuser # create the admin
$ python manage.py runserver       # start the project
```


At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />

<br />

## Sitema Web Django

<br />

O sistema Web possui autenticação de usuário (login e registro)
Inicia com uma tela demonstrativa ilustrativa de um modelo (ARIMA) - NÂO REAL.
<br />
No menu lateral:
Dashboard.
Dynamic Tables - Onde apresenta os dados do banco de dados, com opção de baixar em pdf e em excel.
<br />
Dynamic tables (http://127.0.0.1:8000/tables/) deve ser adicionado um arquivo csv como base de dados. Após isso deve ser passado na url padrão (http://127.0.0.1:8000/) 
<br />
Generated API - Onde apresenta os dados em .json.
Authentication - Para registro de usuário e posterior login.
<br />
Nesse sistema há a possibilidade de geral o modelo SARIMAX por meio da URL:
Argumentos no formato '<str:nome_do_produto>/<int:Numero_de_meses>'
<br />
Exemplo: http://127.0.0.1:8000/Newell%20322/12 ----> "predição do produto Newell 20322 para 12 meses.
Pode ser usado o argumento ALL para analise de todos os produtos
Exemplo: http://127.0.0.1:8000/ALL/12

127.0.0.1:8000/ALL/12 - Aqui apresenta a predição de 12 meses para todos os produtos.

Também há possibilidade de fazer a predição para um produto individual e para uma quantidade de meses desejada, exemplo:

127.0.0.1:8000/mouse/4 - Nesse caso colocar o nome do produto (item do banco de dados) seguido do número de meses de predição.

<br />

## Codebase Structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |-- core/                            
   |    |-- settings.py                   # Project Configuration  
   |    |-- urls.py                       # Project Routing
   |
   |-- home/
   |    |-- views.py                      # APP Views 
   |    |-- urls.py                       # APP Routing
   |    |-- models.py                     # APP Models 
   |    |-- tests.py                      # Tests  
   |    |-- templates/                    # Theme Customisation 
   |         |-- pages                    # 
   |              |-- custom-index.py     # Custom Dashboard      
   |
   |-- requirements.txt                   # Project Dependencies
   |
   |-- env.sample                         # ENV Configuration (default values)
   |-- manage.py                          # Start the app - Django default start script
   |
   |-- ************************************************************************
```
