#!/bin/bash

touch .env
export SECRET_KEY=$(SECRET_KEY)
echo "DB_PORT=5432" > .env
echo "SOCIAL_AUTH_TRAILING_SLASH=False  # Remove trailing slash from routes" >> .env
echo "SOCIAL_AUTH_AUTH0_DOMAIN=$(SOCIAL_AUTH_AUTH0_DOMAIN)" >> .env
echo "SOCIAL_AUTH_AUTH0_KEY=$(SOCIAL_AUTH_AUTH0_KEY)" >> .env
echo "SOCIAL_AUTH_AUTH0_SECRET=$(SOCIAL_AUTH_AUTH0_SECRET)" >> .env
echo "ACCESS_TOKEN_METHOD=POST" >> .env
