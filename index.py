from typing import Union

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import csv
import json
import aiofiles
import os

current_dir = os.getcwd()+'/api'


# Move this function to utils.py

def get_postal_code_data (postal_code):
  print('current_dir', current_dir)
  with open(current_dir+'/db.json') as json_file:
    data = json.load(json_file)
    return data[postal_code]

def validate(postal_code):
  if len(postal_code) != 5:
    return False
  return True

# Move this function to utils.py

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def make_json(csvFilePath, jsonFilePath):
     
    # create a dictionary
    data = {}
     
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='latin-1') as csvf:
        fields = ['d_codigo', 'd_asenta', 'd_estado', 'd_ciudad',  'c_estado', 'D_mnpio']
        csvReader = csv.DictReader(csvf, delimiter='|', fieldnames=fields )
         
        # Convert each row into a dictionary 
        # and add it to data
        for rows in csvReader:
            newRow = {}

            for key in rows.keys():
              print('key', key)
              try:
                #use try to prevent errors and script stopping
                newKey = key.replace('d_codigo', 'codigo').replace('D_mnpio', 'municipio').replace('d_asenta', 'asentamiento').replace('c_', '').replace('d_', '').lower()
                newRow[newKey] = rows[key]
                print(newRow)
              except:
                print('error')
                pass

            # Assuming a column named 'No' to
            # be the primary key
            key = rows['d_codigo']
            data[key] = newRow
 
    # Open a json writer, and use the json.dumps() 
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=2))

@app.get("/api/healthchecker")
def healthchecker():
    return {"status": "success", "message": "Integrate FastAPI Framework with Next.js"}

         
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/update/")
async def create_upload_file(file: UploadFile):
  print(file.filename)
  async with aiofiles.open('db.csv', 'wb') as out_file:
      while content := await file.read(1024):  # async read chunk
          await out_file.write(content)  # async write chunk
  
  make_json('db.csv', 'db.json')
    # return {"filename": file.filename}
  return {"filename": file.filename}



@app.get("/postcodes/{postcode}")
def read_root(postcode: str):
  isValid = validate(postcode)

  if not isValid:
    return {
      "error": "Invalid postal code"
    }
  
  postal_code_data = get_postal_code_data(postcode)
  return postal_code_data
  
  # return {
  #   "postal_code":postcode,
  #   "country_code":"MX",
  #   "city":"Edgewater",
  #   "state":"New Jersey",
  #   "state_code":"NJ",
  #   "province":"Bergen",
  #   "province_code":"003"
  # },


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}