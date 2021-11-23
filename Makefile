test:
	pytest src/test_*.py

format:
	black src/license_plates
	black tests

check-format:
	flake8 src/license_plates
	flake8 tests

typecheck:
	mypy src/lic_plates.py --strict

make-reports:
	mypy src/lic_plates.py --html-report reports/typecheck;
	pytest src/test_lic_plates.py --html=reports/testing/index.html
