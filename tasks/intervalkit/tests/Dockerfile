# Verifier image (separate mode). Runs the hidden suite against /app/intervalkit.
FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm

COPY . /tests/
RUN mkdir -p /app && chmod 0755 /tests/test.sh
