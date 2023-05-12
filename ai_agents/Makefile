
install:
	python -m pip install -r requirements.txt

site:
	streamlit run Home.py

search:
	python scripts/search.py

docker-network:
	docker network create ai_agents

mysql:
	docker run --name mysql -d \
		--network ai_agents \
		-p 3306:3306 \
		-e MYSQL_ROOT_PASSWORD=admin123 \
		-v $(PWD)/setup:/docker-entrypoint-initdb.d \
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