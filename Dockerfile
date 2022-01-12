# https://playwright.dev/python/docs/docker
# https://github.com/microsoft/playwright/blob/main/utils/docker/Dockerfile.bionic
FROM mcr.microsoft.com/playwright:focal

WORKDIR /app

ADD hashotter/ /app/hashotter
ADD requirements.txt /app
ADD app.py /app

RUN pip install -r requirements.txt
RUN playwright install

EXPOSE 80

CMD ["python", "app.py"]
