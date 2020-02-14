#!/bin/bash
$(aws ecr get-login --no-include-email --region us-east-1)
#
docker push 398080897724.dkr.ecr.us-east-1.amazonaws.com/farm_bot:rpi
docker push 398080897724.dkr.ecr.us-east-1.amazonaws.com/farm_bot:latest