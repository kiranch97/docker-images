# Object Detection Kit - ODK stack

* FastAPI API - handles stream of scans via websockets
* RabbitMQ - mesage broker
* Vue JS clients
  - Dashboard
  - Streaming App (Client)

# Developer guide

Install python requirements in your virtaulenv

	python -m pip -r requirements.txt

Run websocket API

	python main.py

Run Mlworker

	cd odklib
	python MlWorker.py

Run frontend Clients

	# Dashboard
	cd odk-dash
	npm install
	npm run serve

	# Streaming App (Client)
	cd odk-client
	npm install
	npm run serve


<!-- # Developement guide

does not work yet.

	docker-compose pull
	docker-compose up -->
