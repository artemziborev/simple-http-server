APP_NAME=simple_http_server
IMAGE_NAME=$(APP_NAME):latest
CONTAINER_NAME=$(APP_NAME)-container

.PHONY: build run stop logs lint test clean rebuild

build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME) .

run:
	@echo "Running server..."
	docker run -d -p 8080:8080 --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	@echo "Stopping server..."
	docker stop $(CONTAINER_NAME) && docker rm $(CONTAINER_NAME)

logs:
	docker logs -f $(CONTAINER_NAME)

lint:
	flake8 httpd.py core/ utils/ tests/
	mypy httpd.py core/ utils/

test:
	pytest tests/

clean:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME) || true
	rm -rf __pycache__

rebuild: clean build
