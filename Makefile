.PHONY: run score

run:
	uv run -m app.main

score:
	uv run -m app_scorer.main

