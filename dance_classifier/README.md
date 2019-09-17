# Dance Classifier
A simple image classifier that can distinguish between Bachata, Salsa, Zouk, and Kizomba
images of people dancing.

## Running it
It uses [Scarlette](https://www.starlette.io) and [uvicorn](https://www.uvicorn.org/) in order to provide a web interface to the classifier.

It can be run by calling something like in the main directory

```bash
gunicorn -w 2 -k uvicorn.workers.UvicornWorker --log-level warning webserve:app
```

Than open your browser and go to [localhost:8000](localhost:8000)

## Data set
The images to train the classifier have been extracted from teaching videos using ffmpeg
by running something like

```bash
for i in *.mp4; do ffmpeg -i "$i" -vf scale=212:212,fps=1 "${i%.*}_foto%04d.jpg" ; done
```

The extracted images are extracted at 1 fps and scaled to 212x212 pixels.
