SRC = plates
TEST = tests

.PHONY: tests reports

all:
	make format
	flake8
	make typecheck
	pytest $(TEST)/test_*.py

tests:
	pytest -v $(TEST)/test_*.py

format:
	black $(SRC)
	black $(TEST)

check-format:
	flake8 $(SRC)
	flake8 $(TEST)

typecheck:
	mypy $(SRC)/*.py --strict
