SRC = plates
TEST = tests

.PHONY: tests reports

all:
	make format
	make check-format
	make typecheck
	pytest $(TEST)/test_*.py -v

tests:
	pytest $(TEST)/test_*.py

format:
	black $(SRC)
	black $(TEST)

check-format:
	flake8 $(SRC) --exclude=__init__.py

typecheck:
	mypy $(SRC)/*.py --strict

reports:
	mypy $(SRC)/*.py --html-report reports/typecheck
	pytest $(TEST)/test_*.py -v --html=reports/testing/index.html
