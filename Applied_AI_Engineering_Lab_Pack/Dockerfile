FROM python:3.12-slim
WORKDIR /app
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt
RUN useradd --create-home course
COPY --chown=course:course solutions ./solutions
COPY --chown=course:course integrations ./integrations
USER course
ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "exec python -m uvicorn integrations.api_app:app --host 0.0.0.0 --port ${PORT:-8000}"]
