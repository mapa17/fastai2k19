from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse, PlainTextResponse
from fastai import *
from fastai.vision import *

from pudb import set_trace as st

TRAINED_MODEL = './export.pkl'

app = Starlette()

defaults.device = torch.device('cpu')
print('Loading trained model [%s] ... ' % TRAINED_MODEL)
try:
    learner = load_learner(path=os.path.dirname(TRAINED_MODEL), file=os.path.basename(TRAINED_MODEL))
except Exception as e:
    print("Loading model failed!")
    print(e)


def predict_image_as_bytes(image):
    img = open_image(BytesIO(image))

    _, class_, losses = learner.predict(img)
    return JSONResponse({
        "prediction": learner.data.classes[class_.item()],
        "scores": sorted(
            zip(learner.data.classes, map(float, losses)),
            key=lambda p: p[1],
            reverse=True
        )
    })

@app.route("/classify-url", methods=["GET"])
async def classify_url(request):
    bytes = await get_bytes(request.query_params["url"])
    predict_image_as_bytes(bytes)


@app.route("/upload", methods=["POST"])
async def upload(request):
    data = await request.form()
    bytes = await (data["file"].read())
    return predict_image_as_bytes(bytes)


@app.route("/")
def form(request):
    return HTMLResponse("""
        <h3>This app will classify Dance styles using images<h3>
        <form action="/upload" method="post" enctype="multipart/form-data">
            Select image to upload:
            <input type="file" name="file">
            <input type="submit" value="Upload Image">
        </form>
        Or submit a URL:
        <form action="/classify-url" method="get">
            <input type="url" name="url">
            <input type="submit" value="Fetch and analyze image">
        </form>
    """)


