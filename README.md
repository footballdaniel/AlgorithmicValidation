# AlgorithmicValidation
Validation for Algorithmic gaze analysis

## Streamlit
[The app is hosted here](https://share.streamlit.io/footballdaniel/algorithmicvalidation/main/validation.py)

## Dockerfile
I used the procedure from [here](https://www.databentobox.com/2020/10/08/python-apps-with-docker/) to run the streamlit app in a docker container.
The docker container was built with `docker build -f Dockerfile -t algorithmicvalidation:latest .`  and exposed `Port 8000`. The resulting container can be run with `docker run -p 8000:8000 algorithmicvalidation` 

## Push dockerfile to github package
I used the procedure from [here](https://docs.github.com/en/free-pro-team@latest/actions/guides/publishing-docker-images). The v2 of the build-push-action did not work properly.
I then used the manual approach to uploading a docker image to the github container repository ([source](https://docs.github.com/en/free-pro-team@latest/packages/managing-container-images-with-github-container-registry/pushing-and-pulling-docker-images)). I had to create a personal access token (`PAT`) for the container repository ([source](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)). I saved it as `CR_PAT`, an Ubuntu environment variable.
After login, I had to take the existing image (`algorithmicvalidation`) and give it a new tag: `docker tag algorithmicvalidation ghcr.io/footballdaniel/algorithmicvalidation`


