FROM registry.tc.egov.local/library/python:3.12.4-alpine

WORKDIR /app

COPY clean-empty-dirs-s3.py /app/
COPY boto3/*.whl /app/

RUN addgroup -g 1000 appgroup && adduser -u 1000 -G appgroup -D appuser && \
    chown -R appuser:appgroup /app

RUN python -m pip install /app/*.whl

USER appuser

CMD ["python", "/app/clean-empty-dirs-s3.py"]
