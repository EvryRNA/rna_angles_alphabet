# Path to check the code
export PATH_TO_CODE=src
# Path to the unit tests
export PATH_TO_UNIT_TESTS=tests/unit

# Score thresholds
export COVERAGE_SCORE=10
export COMPLEXITY_SCORE=2.7
export DOCUMENTATION_SCORE=5

# Max line length for black
MAX_LINE_LENGTH=99
export PYTHON?=python -m

# Path to the lintage directory
LINTAGE_DIR=script/lintage

# Convert the code to black format
format_code :
	$(PYTHON) black --line-length $(MAX_LINE_LENGTH) ${PATH_TO_CODE}

# Do all the static tests
test_static_all: format_code
	$(PYTHON) black --check --line-length $(MAX_LINE_LENGTH)  ${PATH_TO_CODE}
	$(PYTHON) isort --profile black ${PATH_TO_CODE}
	$(PYTHON) mypy ${PATH_TO_CODE} --ignore-missing-imports
	$(PYTHON) flake8 --exclude=tests --max-line-length $(MAX_LINE_LENGTH) ${PATH_TO_CODE}

# Unit tests
unit_test:
	$(PYTHON) pytest ${PATH_TO_UNIT_TESTS}

test_unit_coverage:
	${LINTAGE_DIR}/coverage.sh

test_complexity:
	${LINTAGE_DIR}/complexity.sh

test_documentation:
	${LINTAGE_DIR}/documentation.sh

all_tests: test_static_all test_complexity test_documentation test_unit_coverage

NAME="Clement"
run:
	$(PYTHON) src.return_hello --name=$(NAME)

test_angle:
	./src/c_code/angle -d example/training_set_ex/ -l example/training_ex.txt -o example/result_ex -R -p -f -t

angle:
	./src/c_code/angle -d data/training_set/ -l data/training.txt -o data/result -R -p -f -t
