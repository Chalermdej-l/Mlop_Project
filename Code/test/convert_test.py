from predict import convertdata,preparerespond
import datetime

def test_convert_data():
    sample_data = [{"age": 56, "job": "housemaid", "marital": "married", "education": "basic.4y", "default": "no", "housing": "no", "loan": "no", "contact": "telephone", "duration": 261, "campaign": 1, "pdays": 999, "previous": 0, "poutcome": "nonexistent", "emp.var.rate": 1.1, "cons.price.idx": 93.994, "cons.conf.idx": -36.4, "euribor3m": 4.857, "nr.employed": 5191.0, "id": "3ad93d85-2390-11ee-83b8-e7e9bcdc248d"}]
    convert_data= convertdata(sample_data)
    expected_output = [{'age': 4, 'job': 'housemaid', 'marital': 'married', 'education': 'basic.4y', 'default': 'no', 'housing': 'no', 'loan': 'no', 'contact': 'telephone', 'duration': 6, 'campaign': 1, 'pdays': 999, 'previous': 0, 'poutcome': 'nonexistent', 'emp.var.rate': 1.1, 'cons.price.idx': 93.994, 'cons.conf.idx': -36.4, 'euribor3m': 4.857, 'nr.employed': 5191.0, 'id': '3ad93d85-2390-11ee-83b8-e7e9bcdc248d'}]
    assert  convert_data == expected_output
    return expected_output

def test_respond():
    sample_predict = [1,0,0]
    sample_data = [{'id': '3ad93d85-2390-11ee-83b8-e7e9bcdc248d'},{'id': '5cc93d85-2390-11ee-83b8-e7e9bcdc60c'},{'id': '9cv93d98-2390-11ee-83b8-e7e9bcdc90d'}]
    sample_respond = preparerespond(sample_predict,sample_data,1)

    date = datetime.datetime.now().strftime('%Y-%m-%d')
    expected_respond = {'date': date, 'model_version': 1, 'result': [('3ad93d85-2390-11ee-83b8-e7e9bcdc248d', 1), ('5cc93d85-2390-11ee-83b8-e7e9bcdc60c', 0), ('9cv93d98-2390-11ee-83b8-e7e9bcdc90d', 0)]}
    assert  sample_respond == expected_respond

def mock_model(data):
    i
def test_predict():
    moc
