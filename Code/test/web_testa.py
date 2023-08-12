import requests


sample_data =[
  {"age": 56, "job": "housemaid", "marital": "married", "education": "basic.4y", "default": "no", "housing": "no", "loan": "no", "contact": "telephone", "duration": 261, "campaign": 1, "pdays": 999, "previous": 0, "poutcome": "nonexistent", "emp.var.rate": 1.1, "cons.price.idx": 93.994, "cons.conf.idx": -36.4, "euribor3m": 4.857, "nr.employed": 5191.0, "id": "3ad93d85-2390-11ee-83b8-e7e9bcdc248d"}
, {"age": 57, "job": "services", "marital": "married", "education": "high.school", "default": "unknown", "housing": "no", "loan": "no", "contact": "telephone", "duration": 149, "campaign": 1, "pdays": 999, "previous": 0, "poutcome": "nonexistent", "emp.var.rate": 1.1, "cons.price.idx": 93.994, "cons.conf.idx": -36.4, "euribor3m": 4.857, "nr.employed": 5191.0, "id": "3ad93d86-2390-11ee-bd5e-e7e9bcdc248d"}
, {"age": 37, "job": "services", "marital": "married", "education": "high.school", "default": "no", "housing": "yes", "loan": "no", "contact": "telephone", "duration": 226, "campaign": 1, "pdays": 999, "previous": 0, "poutcome": "nonexistent", "emp.var.rate": 1.1, "cons.price.idx": 93.994, "cons.conf.idx": -36.4, "euribor3m": 4.857, "nr.employed": 5191.0, "id": "3ad93d87-2390-11ee-8a78-e7e9bcdc248d"}
, {"age": 40, "job": "admin.", "marital": "married", "education": "basic.6y", "default": "no", "housing": "no", "loan": "no", "contact": "telephone", "duration": 151, "campaign": 1, "pdays": 999, "previous": 0, "poutcome": "nonexistent", "emp.var.rate": 1.1, "cons.price.idx": 93.994, "cons.conf.idx": -36.4, "euribor3m": 4.857, "nr.employed": 5191.0, "id": "3ad93d88-2390-11ee-b81f-e7e9bcdc248d"}
, {"age": 56, "job": "services", "marital": "married", "education": "high.school", "default": "no", "housing": "no", "loan": "yes", "contact": "telephone", "duration": 307, "campaign": 1, "pdays": 999, "previous": 0, "poutcome": "nonexistent", "emp.var.rate": 1.1, "cons.price.idx": 93.994, "cons.conf.idx": -36.4, "euribor3m": 4.857, "nr.employed": 5191.0, "id": "3ad93d89-2390-11ee-a395-e7e9bcdc248d"}
]

url = 'http://127.0.0.1:9696/predict'
result=  requests.post(url,json=sample_data)

assert result.status_code == 200
print(result.status_code)
print(result.json())