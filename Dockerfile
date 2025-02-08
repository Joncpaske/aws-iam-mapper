FROM python:3.13-alpine3.21

COPY dist/*.whl .
RUN python -m pip install awsiammapper*.whl \
    && rm *.whl

# non-root user
RUN adduser awsiammapper -D -u 1000
USER awsiammapper

ENTRYPOINT [ "python3", "-m", "awsiammapper" ]
CMD ["-h"]