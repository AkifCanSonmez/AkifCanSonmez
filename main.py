from starlette.staticfiles import StaticFiles
import fastapi
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Depends, File, UploadFile, HTTPException, APIRouter, Request, Form
import urllib.parse
import time
import base64
import numpy as np
import cv2


templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret_key")
app.mount("/static", StaticFiles(directory="static"), name="static")

'''@app.get("/home/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})'''

@app.get("/login/")
async def get_html(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/home")
async def login(request:Request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "admin":
        response = templates.TemplateResponse("home.html", {"request": request})
    else:
        response = RedirectResponse(url="/login/", status_code=303)
    return response

@app.post("/newmeal/")
async def new_meal(request: Request):
    data = await request.form()
    btn_name = data.get("btn_name")
    print(btn_name)
    if btn_name == "newMeal":
        return templates.TemplateResponse("photo_options.html", {"request": request})
    else:
        return templates.TemplateResponse("photo_options.html", {"request": request})

@app.post("/foods/")
async def open_camera(request: Request):
    data = await request.form()
    btn_name = data.get("btn_name")
    if btn_name == "cameraBtn":
        response = templates.TemplateResponse("camera.html", {"request": request})
    elif btn_name == "selectBtn":
        food_image = data.get("food_image").file
        image = cv2.imdecode(np.frombuffer(food_image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        #objects = model.predict(image) # Assuming that model.predict(image) returns the detected objects
        objects = ["selectimage","elma","armut"]
        request.session["objects"] = objects
        response = RedirectResponse(url="/objects/display", status_code=302)
    elif btn_name == "typeBtn":
        response = templates.TemplateResponse("textfoods.html", {"request": request})
    
    return response


@app.post("/objects")
async def objects_post(request: Request, image: UploadFile):
    image_bytes = await image.read()
    np_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
    # Pass the image to your YOLO model for prediction
    # objects = model.predict(image)
    #objects = def method that for yolo
    detected_foods = ["elma","armut","kelmahmut"]
    request.session["objects"] = detected_foods
    return {"message": "Objects received"}

@app.get("/objects/display")
async def objects_get(request: Request):
    objects = request.session.get("objects")
    return templates.TemplateResponse("objects.html", {"request": request, "objects": objects})

@app.post("/parameters")
async def parameters_post(request: Request):
    data = await request.json()
    objects = data["objects"]
    objects = ["akif","can"]
    request.session["objects"] = objects
    return {"message": "Objects received"}

@app.get("/parameters/display")
async def parameters_get(request: Request):
    objects = request.session.get("objects")
    #other_parameters = 
    if not objects:
        return HTMLResponse(status_code=404, content={"error": "Objects not found"})
    return templates.TemplateResponse("parameters.html", {"request": request, "objects": objects})


#bunu düzelt yarın, foodları yazıyla düzeltme, sonra bunu /foods'taki elif'e bağla
@app.post("/text")
async def get_text(request:Request):
    # Get the request body as a list of dictionaries, where each dictionary
    # represents a text bar
    data = await request.json()
    objects = data.get("input_values")
    # Extract the text values from the dictionaries
    request.session["objects"] = objects
    # Return the text values as a response
    return {"text_values": objects}

@app.post("/pstrsql")
async def pstrsql_post(request: Request):
    # Do something with input_values
    # ...
    data = await request.json()
    params = data.get('input_values')
    request.session["params"] = params
    return {"message": "Success"}

@app.get("/pstrsql/display")
async def pstrsql_get(request: Request):
    objects = request.session["params"]
    print(objects)
    liste = []
    for i in objects:
        liste.append(i["value"])
    return templates.TemplateResponse("final.html", {"request": request, "objects": liste})


#yolo model predict yaz image'i objectslere çeviren

# parametres.html'e buton ekle, bu buton tüm parametreleri gönderip sql işlemi yapsın, dönen verilerle yeni html sayfası yap







    


'''
    
@app.post("/server")
async def amount_inputs():
     Bu miktarlar girildikten kişi onaylarsa  sql serverına tokluk şeker girilir, daha sonra
        belirlenen algoritmaya göre belirlenen miktarda veri çekilir. Kişiye sunulur, daha
        sonra kişi home'a döner veya çıkış yapar.

'''






'''@app.post("/login")
async def login():
    js_file = open("static/js/login.js", "r").read()
    return HTMLResponse(content=f"<script>{js_file}</script>", media_type="text/html")

'''

'''

@app.post("/predict")
async def predict(image: bytes = File(...)):
    # Perform object detection on the image here
    result = model.predict(image)
    
@app.get("/")
def get_html(request: Request):
    return RedirectResponse(url='/result/')
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/result/")
def get_any():
    return {"asd":"asdf"}

@app.get("/static/js/{file_path:path}")
async def serve_js(file_path: str):
    return File(f"static/js/{file_path}")

@app.post("/predict")
async def predict(file: bytes = File(...)):
    # Here you can use the model.predict(...) function with the image file
    print("asdfa")
    # and return the result to the client
    return {"prediction": model.predict(file)}

@app.get("/new_meal")
def get_img()'''
