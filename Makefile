SRC = plates
TEST = tests

.PHONY: tests format all

all:
	make format
	flake8
	mypy $(SRC)
	pytest $(TEST)

tests:
	pytest -v $(TEST)

format:
	black $(TEST) $(SRC)
