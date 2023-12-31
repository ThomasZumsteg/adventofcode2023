run: day*.py
	for file in $^; do \
		echo $$file; \
		python $$file; \
	done

setup:
	pip install -r requirements.txt

clean:
	rm -rf .AoC-*.tmp .*.sw?

flake: day*.py
	flake8 $^

freeze: requirements.txt

requirements.txt:
	pip freeze > requirements.txt

test: day*.py
	pytest $^
