#!/bin/bash
docker build -t farm_app -f ./farm_app/Dockerfile.prod ./farm_app/.
docker tag farm_app:latest 398080897724.dkr.ecr.us-east-1.amazonaws.com/farm_app:latest
docker build -t nginx-proxy -f ./nginx/Dockerfile ./nginx/.
docker tag nginx-proxy:latest 398080897724.dkr.ecr.us-east-1.amazonaws.com/nginx-proxy:latest