# AlgorithmicValidation
Validation for Algorithmic gaze analysis

## Streamlit
[The app is hosted here](https://share.streamlit.io/footballdaniel/algorithmicvalidation/main/validation.py)

## Dockerfile
I used the procedure from [here](https://www.databentobox.com/2020/10/08/python-apps-with-docker/) to run the streamlit app in a docker container.
The docker container was built with `docker build -f Dockerfile -t algorithmicvalidation:latest .`  and exposed `Port 8000`. The resulting container can be run with `docker run -p 8000:8000 algorithmicvalidation` 

## Push dockerfile to github package
I used the procedure from [here](https://docs.github.com/en/free-pro-team@latest/actions/guides/publishing-docker-images)