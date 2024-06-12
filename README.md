
# transfeera-challenge

Este projeto é uma aplicação desenvolvida utilizando conceitos de Domain-Driven Design (DDD), onde a estrutura é dividida em camadas de domínio, aplicação e infraestrutura para garantir um alto nível de desacoplamento.
 
## Estrutura do Projeto

-  **Domínio**: Esta camada contém as entidades de negócio e as regras de domínio da aplicação.
-  **Aplicação**: Aqui estão os serviços de aplicação que orquestram as operações de negócio, utilizando os elementos do domínio.
-  **Infraestrutura**: Responsável por integrar a aplicação com recursos externos, como bancos de dados, além de também disponibilizar os endereços para afetuar as requisições.

## Tecnologias Utilizadas
A linguagem de programação utilizada foi o Python, na sua versão 3.12. Além disso, foram utilizadas as seguintes tecnologias.

-  **Django-Ninja**: Framework para construção de APIs RESTful em Python, que permite desenvolver APIs de forma rápida e eficiente. [link](https://github.com/vitalik/django-ninja).
-  **PostgreSQL**: Banco de dados relacional utilizado para armazenar os dados da aplicação.
-  **Docker e Docker Compose**: Utilizados para containerizar a aplicação e seus serviços, garantindo um ambiente de desenvolvimento consistente e portátil.

## Como Executar

Para executar a aplicação via Docker, siga os passos abaixo:
1. Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.
2. Clone este repositório em sua máquina local.
3. Navegue até o diretório raiz do projeto.
4. Execute o comando abaixo para construir e iniciar os contêineres Docker:
```
docker-compose up --build
```
ou
```
./run-containers.sh
```
5. Aguarde até que todos os serviços sejam inicializados. Após a conclusão, a aplicação estará disponível e pronta para uso. OBS: O banco de dados será pré-populado com 30 registros de teste, além disso, para fins de teste, é possível popular com diferentes valores, isso através do comando (para rodar esse comando, certifique-se de ter configurando o ambiente local, [conforme explicado na seção de execução dos testes](#executando-testes):
```
python manage.py pre_populate_receivers -n <quantidade de registros desejado>
```
6. Acesse a aplicação em [http://localhost:8000](http://localhost:8000) e comece a explorar suas funcionalidades.

## Executando Testes
Este projeto possui uma cobertura abrangente de testes, incluindo testes de unidade e testes de integração, para garantir o correto funcionamento das funcionalidades implementadas.
Para executar os testes da aplicação utilizando o Pytest, siga os passos abaixo:

### 1. Configurando o Ambiente de Desenvolvimento Local

Certifique-se de ter o Python instalado em sua máquina (foi utilizado o Python na versão 3.12 nesse projeto). Em seguida, siga os passos abaixo para configurar o ambiente de desenvolvimento:
 
#### Criando e Ativando um Ambiente Virtual
 
```bash
python3.12  -m  venv  venv
source  venv/bin/activate
```

#### Instalando as Dependências de Desenvolvimento
 
```bash
pip  install  -r  src/dev_requirements.txt
```
### 2 Configurando as Variáveis de Ambiente
Crie o arquivo `.env`. Existe o arquivo modelo chamado `.env_template` na raiz do projeto para referência. Segue exemplo para melhor entendimento:
```
SECRET_KEY=<random key>
NAME_DB=receiver_app
USER_DB=admin
PASSWORD_DB=1234
ALLOWED_HOSTS=*
```

### 3. Configurando o Banco de Dados
Certifique-se de que o banco de dados PostgreSQL está configurado e em execução conforme as configurações especificadas no arquivo `docker-compose.yaml`. Além disso, também é necessário rodar as migrações caso não tenha rodado:
```bash
python src/manage.py migrate
```
### 4. Executando os Testes
Com o ambiente de desenvolvimento configurado e o banco de dados em execução, execute o seguinte comando para rodar os testes com o Pytest:
```bash
pytest
```
Isso executará todos os testes no diretório atual e subdiretórios, exibindo os resultados no terminal.
Se desejar executar testes específicos ou personalizar a execução dos testes, consulte a [documentação do Pytest](https://docs.pytest.org/en/stable/contents.html) para obter mais informações.

## Documentação da API

A API possui uma documentação Swagger, onde é possível visualizar e interagir com os endpoints disponíveis. A documentação pode ser acessada através do seguinte endereço:
[http://localhost:8000/api/docs](http://localhost:8000/api/docs)
