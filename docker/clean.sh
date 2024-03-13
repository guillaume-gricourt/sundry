#!/bin/bash

docker rm $(docker ps -aq --no-trunc)
docker rmi $(docker images | grep '^<none>' | awk '{print $3}')
