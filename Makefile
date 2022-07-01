MAKEFLAGS  	+= --silent
SHELL      	 = /bin/bash

install-libs:
	@echo "Installing..."
	cd ./monitor && \
	source venv/bin/activate && \
	pip install -r requirements.txt
	@echo "Installed"

run:
	@echo "Running..."
	cd ./monitor && \
	source venv/bin/activate && \
	python3 monitor.py
	@echo "Done."

freeze:
	@echo "Freezing..."
	cd ./monitor && \
	source venv/bin/activate && \
	pip freeze > requirements.txt
	@echo "Done."

docker:
	@echo "Building docker image..."
	cd ./monitor && \
	docker build -t monitor .
	@echo "Done."

run-docker:
	@echo "Running docker image..."
	cd ./monitor && \
	docker run --rm -it \
	--network monitoring-mysql_monitor-net \
	-e DB_HOST=mysql \
	-p 8000:8000 monitor
	@echo "Done."
