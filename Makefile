clean_pytest:
	rm -rf .pytest_cache .coverage htmlcov .tox

generate_requirements:
	pip-compile --output-file=requirements.txt requirements.in
	pip-compile --output-file=requirements-dev.txt requirements-dev.in

generate_requirements_with_poetry:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	poetry export -f requirements.txt --output requirements-dev.txt --without-hashes --dev



activate_virtualenv_poetry:
	poetry shell

activate_virtualenv:
	source .venv/bin/activate

run_tests:
	pytest -v --cov=tests --cov-report=term-missing --cov-fail-under=100 --cov-report=html

start:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers --reload

install-precommit:
	pre-commit install