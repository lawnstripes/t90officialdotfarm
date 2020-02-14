docker build -t farm_bot:rpi -f Dockerfile.pi-prod .
docker tag farm_bot:rpi 398080897724.dkr.ecr.us-east-1.amazonaws.com/farm_bot:rpi
docker build -t farm_bot -f Dockerfile.prod .
docker tag farm_bot:latest 398080897724.dkr.ecr.us-east-1.amazonaws.com/farm_bot:latest