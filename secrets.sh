#!/bin/bash

touch .env
export SECRET_KEY=$(gcloud secrets versions access latest --secret="SECRET_KEY")
echo "DB_PORT=5432" >> .env
echo "SOCIAL_AUTH_TRAILING_SLASH=False  # Remove trailing slash from routes" >> .env
echo "SOCIAL_AUTH_AUTH0_DOMAIN=$(gcloud secrets versions access latest --secret='SOCIAL_AUTH_AUTH0_DOMAIN')" >> .env
echo "SOCIAL_AUTH_AUTH0_KEY=$(gcloud secrets versions access latest --secret='SOCIAL_AUTH_AUTH0_KEY')" >> .env
echo "SOCIAL_AUTH_AUTH0_SECRET=$(gcloud secrets versions access latest --secret='SOCIAL_AUTH_AUTH0_SECRET')" >> .env
