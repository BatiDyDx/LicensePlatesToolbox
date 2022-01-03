SRC = plates
TEST = tests

.PHONY: tests reports

all:
	make format
	make check-format
	make typecheck
	pytest $(TEST)/test_*.py

tests:
	pytest -v $(TEST)/test_*.py

format:
	black $(SRC)
	black $(TEST)

check-format:
	flake8 $(SRC) --exclude=__init__.py
	flake8 $(TEST) --ignore=F403,F405

typecheck:
	mypy $(SRC)/*.py --strict
