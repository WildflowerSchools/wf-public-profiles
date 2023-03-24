build:
    poetry build

publish: build
    poetry publish

format:
    black wf_public_profiles

lint:
    pylint wf_public_profiles

test:
    pytest tests/

version:
    poetry version