.PHONY: setup check test first reader full docker
setup:
	python tools/bootstrap.py --profile core
check:
	uv run --no-sync python course.py verify --profile core
test:
	uv run --no-sync python course.py test --profile core --output my_work/tests_$(shell date +%Y%m%d_%H%M%S)
first:
	uv run --no-sync python course.py run --stage 0 --output my_work/stage00_$(shell date +%Y%m%d_%H%M%S)
reader:
	uv run --no-sync python course.py serve
full:
	python tools/bootstrap.py --profile full
	uv run --no-sync python course.py run --all --output my_work/full_$(shell date +%Y%m%d_%H%M%S)
docker:
	python tools/docker_verify.py --profile core
