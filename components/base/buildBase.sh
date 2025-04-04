docker stop base 2>/dev/null || true
docker rm -f base 2>/dev/null || true
docker build --rm -t base:latest .
docker container prune -f
docker image prune -f
docker images
docker ps -a
