# 🚀 Desafio Pipeline BRT  

## 📌 Sobre o Projeto  
Este projeto consiste em um pipeline de dados para coletar, armazenar e transformar informações de GPS dos ônibus do BRT do Rio de Janeiro. Utilizei **Prefect** para orquestração, **PostgreSQL** para armazenamento, **DBT** para transformação dos dados e **Docker** para subir o banco postgres.  
 
![Pipeline BRT](https://raw.githubusercontent.com/Danielllira/desafio-pipeline-brt/main/img_readme/pipeline_excalidraw.jpg)

## 🚀 Como Rodar o Projeto  

### 1️⃣ Pré-requisitos  
Antes de começar, instale Docker na sua maquina:  
- **Docker** → [Instalar Docker](https://docs.docker.com/get-docker/)  


### 2️⃣ Subir o Banco de Dados  
Clone o repositório e execute:  

```bash
docker-compose up -d
```

### 3️⃣ Criar um Ambiente Virtual

Com o repositório clonado, execute

```bash
python3 -m venv venv
```
Para ativar
```
source venv/bin/activate
```

No Windows use
```
venv\Scripts\activate
```

### 4️⃣ Configurar o Caminho do DBT

No arquivo flows.py, altere a variável DBT_PROJECT_PATH para o caminho correto no seu sistema:
```
DBT_PROJECT_PATH = '/seu/caminho/aqui/dbt/brt_data_pipeline'
```
Para descobrir o camininho use 
```
pwd 
```

### 5️⃣ Criar as Tabelas no PostgreSQL
Você pode criar as tabelas manualmente usando DBeaver, pgAdmin ou diretamente no CLI do PostgreSQL. O arquivo sql está na pasta scripts/


### 6️⃣ Instalar libs necessarias
E claro, não podemos esquecer de rodar o comando
```
pip install -r requirements.txt
```

### 7️⃣ Rodar o Pipeline
Agora, basta executar o main.py:
```
python main.py
```

## ❓ Dúvidas?

Me encontre em:

📩 Email: danielllira@icloud.com

💼 [Linkedin](https://www.linkedin.com/in/1danielllira/)




