include MakeEnv.mk
# include .env

install:
	python -m pip install -r requirements.txt

site:
	streamlit run Home.py

search:
	python scripts/search.py

docker-network:
	docker network create ai_agents

mysql-run:
	docker run --name mysql -d \
		--network ai_agents \
		-p 3306:3306 \
		-e MYSQL_ROOT_PASSWORD=admin123 \
		-v $(PWD)/setup/mysqlsampledatabase.sql:/docker-entrypoint-initdb.d/mysql.sql \
		mysql:8

mysql-rm:
	docker stop mysql
	docker rm mysql

mysql-cli:
	docker run -it --rm \
		--network ai_agents \
		-v $(PWD)/setup:/setup \
		mysql:8 \
		mysql -h mysql -u root -p

#### Build Docker Image ####

agents-build:
	docker build -f setup/Dockerfile -t $(IMAGE_NAME):$(IMAGE_VERSION) .

agents-rmi:
	docker rmi $(IMAGE_NAME):$(IMAGE_VERSION)

agents-run:
	docker run --name ai_agents -d \
		--network ai_agents \
		-p 8501:8501 \
		-v $(PWD)/.env.docker:/app/.env \
		$(IMAGE_NAME):$(IMAGE_VERSION)

agents-rm:
	docker stop ai_agents
	docker rm ai_agents

agents-push:
	docker push $(IMAGE_NAME):$(IMAGE_VERSION)

mysql-build:
	docker build -f setup/Dockerfile_mysql -t $(IMAGE_NAME_MYSQL):$(IMAGE_VERSION_MYSQL) .

mysql-rmi:
	docker rmi $(IMAGE_NAME_MYSQL):$(IMAGE_VERSION_MYSQL)

mysql-push:
	docker push $(IMAGE_NAME_MYSQL):$(IMAGE_VERSION_MYSQL)

### Docker Compose ####

stack-up:
	docker-compose -f setup/stack.yml --project-name stack up -d

stack-down:
	docker-compose -f setup/stack.yml --project-name stack  down