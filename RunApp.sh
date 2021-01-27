echo Running DOCKER in web browser
echo Requires DOCKER to be installed

docker pull ghcr.io/footballdaniel/algorithmicvalidation:latest

# Run in detached mode (when shell exits, will still run)
# docker container create --pid ghcr.io/footballdaniel/algorithmicvalidation:latest
docker run --publish 8501:8501 --name algo -it ghcr.io/footballdaniel/algorithmicvalidation:latest &

# SHOULD WAIT FOR PORT TO OPEN. ITS NOT WORKING YET SO I COMMAND IT TO SLEEP
# Linux wait for port responding
# while ! echo exit | nc localhost 8501; do sleep 10; done
# Windows wait for port responding
# while ! timeout 1 bash -c "echo > /dev/tcp/localhost:8501"; do sleep 1; done

sleep 3

# Run in explorer
case "$OSTYPE" in
  solaris*) echo "SOLARIS not implemented" ;;
  darwin*)  open http://localhost:8501/ ;; 
  linux*)   xdg-open http://localhost:8501/ ;;
  bsd*)     echo "BSD not implemented" ;;
  msys*)    start http://localhost:8501/ ;;
  *)        echo "unknown: $OSTYPE" ;;
esac


# To view output:
# $SHELL
