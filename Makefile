.PHONY: backend-dev frontend-dev test format

backend-dev:
uvicorn backend.main:app --reload

frontend-dev:
cd frontend && npm run dev

test:
pytest backend/tests

format:
echo "Add formatters (black/isort/prettier) as needed"
