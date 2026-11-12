SHELL := /bin/bash
PYTHON ?= python3
AWS_REGION ?= us-east-1
TF_DIR := terraform

.PHONY: up down lint test train deploy drift-demo tf-init tf-plan tf-apply tf-destroy

up: tf-init tf-plan
	@echo "Infrastructure plan created. Review before applying."

down: tf-destroy

lint:
	pre-commit run --all-files

test:
	pytest -q

train:
	$(PYTHON) -m src.fetch_data --output data/raw/iris.csv
	$(PYTHON) -m src.data_validation --input data/raw/iris.csv --output data/processed/iris_validated.csv
	$(PYTHON) -m src.training --input data/processed/iris_validated.csv --model-output models/model.joblib

deploy:
	kubectl apply -f k8s/

drift-demo:
	$(PYTHON) -m src.drift_check --baseline data/processed/iris_validated.csv --current data/processed/iris_validated.csv --threshold 0.2

tf-init:
	cd $(TF_DIR) && terraform init

tf-plan:
	cd $(TF_DIR) && terraform plan -out=tfplan

tf-apply:
	cd $(TF_DIR) && terraform apply tfplan

tf-destroy:
	cd $(TF_DIR) && terraform destroy -auto-approve
