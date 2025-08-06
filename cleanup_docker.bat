@echo off
echo Cleaning up all Docker resources...

echo.
echo Stopping all running containers...
docker stop $(docker ps -q) 2>nul

echo.
echo Removing all containers...
docker rm $(docker ps -aq) 2>nul

echo.
echo Stopping Docker Compose services...
docker-compose down 2>nul

echo.
echo Removing all unused Docker resources (images, networks, volumes)...
docker system prune -a --volumes -f

echo.
echo Checking remaining containers...
docker ps -a

echo.
echo Checking remaining images...
docker images

echo.
echo Docker cleanup complete!
pause
