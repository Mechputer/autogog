docker stop input 2>/dev/null || true
docker rm -f input 2>/dev/null || true
docker image rm -f input 2>/dev/null || true
docker build --rm -t input:latest .
docker run --name input --memory=8g --cpus=4 -d -p 5000:5000 input:latest
docker container prune -f
docker image prune -f
docker images
docker ps -a
