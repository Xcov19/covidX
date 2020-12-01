#!/bin/bash

touch .env
export SECRET_KEY=$(gcloud secrets versions access latest --secret="SECRET_KEY")
echo "DB_PORT=5432" > .env
echo "" >> .env
echo "SOCIAL_AUTH_TRAILING_SLASH=False  # Remove trailing slash from routes" >> .env
echo "" >> .env
echo "SOCIAL_AUTH_AUTH0_DOMAIN=$(gcloud secrets versions access latest --secret='SOCIAL_AUTH_AUTH0_DOMAIN')" >> .env
echo "" >> .env
echo "SOCIAL_AUTH_AUTH0_KEY=$(gcloud secrets versions access latest --secret='SOCIAL_AUTH_AUTH0_KEY')" >> .env
echo "" >> .env
echo "SOCIAL_AUTH_AUTH0_SECRET=$(gcloud secrets versions access latest --secret='SOCIAL_AUTH_AUTH0_SECRET')" >> .env
echo "" >> .env
echo "ACCESS_TOKEN_METHOD=POST" >> .env
echo "" >> .env
echo "JWT_AUDIENCE=$(gcloud secrets versions access latest --secret='JWT_AUDIENCE')" >> .env
echo "" >> .env
echo "ALGOLIA_API_KEY=$(gcloud secrets versions access latest --secret='ALGOLIA_API_KEY')" >> .env
echo "" >> .env
echo "ALGOLIA_APPLICATION_ID=$(gcloud secrets versions access latest --secret='ALGOLIA_APPLICATION_ID')" >> .env
