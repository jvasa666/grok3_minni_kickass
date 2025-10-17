# Basic multi-stage example; edit for repo language
FROM alpine:3.18 AS base
WORKDIR /app
COPY . .
CMD ["/bin/sh"]
