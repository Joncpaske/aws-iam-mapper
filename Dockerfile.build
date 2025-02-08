FROM python:3.13-alpine3.21 AS builder

# dummy creds needed for pytests
ENV AWS_ACCESS_KEY_ID dummy
ENV AWS_SECRET_ACCESS_KEY dummy

# install poetry
RUN apk add curl \
    && curl -fsSL https://install.python-poetry.org | python -
ENV PATH "/root/.local/bin:$PATH"


WORKDIR /app


# requirements-dev.txt generated from poetry export hook
# run manually by with:
# poetry export --with=dev --format=requirements.txt --output=./requirements-dev.txt
COPY requirements-dev.txt .
RUN python -m pip install -r requirements-dev.txt

COPY . .

# test / static code analysis
RUN pytest tests \ 
    && black . \
    && pylint .

RUN poetry build

FROM python:3.13-alpine3.21

COPY --from=builder /app/dist/*.whl .
RUN python -m pip install awsiammapper*.whl \
    && rm *.whl

# non-root user
RUN adduser awsiammapper -D -u 1000
USER awsiammapper

ENTRYPOINT [ "python3", "-m", "awsiammapper" ]
CMD ["-h"]