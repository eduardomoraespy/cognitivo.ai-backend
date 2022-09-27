# cognitivo.ai-backend

Acesso Servidor web: https://cognitivo-ai.herokuapp.com/swagger/


https://cognitivo-ai.herokuapp.com/redoc/


Tecnologias Usadas:
  - Linguagem: Python
  - FrameWork: Django e Django RestFramework
  - Bibliotecas mais relevantes: Pandas, tweepy

## Descrevendo mais a solução
A resolução do projeto consistiu em atender o problema de negócio que a empresa tem. A necessidade de automação e criação de relatórios em csv, json e guardar as informações no banco de dados. Com isso a solução criada para atende o problema de negócio foi feito da seguinte forma:


  - No DataSet disponibilizado foi feito análise exploratória (ETL) e foi isolado o principal canal de comunicação que é o Twitter e os top 10 apps sobre música e livros.  


  - Criação de api para comunicar com o twitter para obter informações sobre assuntos mais falados referente a músicas e livros determinados no dataset.


- Resposta no navegador das informações buscadas no twitter, com o dia e hora do registro criado, caso exista a necessidade de rápida visualização.


Execução do Projeto:
1º clone projeto: git clone https://github.com/eduardomoraespy/cognitivo.ai-backend.git


2º Criar ambiente virtual: virtualenv env


3º Ativar ambiente virtual: env\Scripts\activate


4º instalar bibliotecas e módulos - pip install -r requirements.txt


5º Realizar migrações: python manage.py migrate


6º Executar servidor local do projeto: python manage.py runserver
