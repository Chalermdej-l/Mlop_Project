import code.predict as predict
import json
def test_convert_data():
    with open('test/sample_data.json','r') as f:
        sample_data = [json.load(f)]

    convert_data= predict.convertdata(sample_data)

    expected_output = [{'age': 4, 'job': 'housemaid', 'marital': 'married', 'education': 'basic.4y', 'default': 'no', 'housing': 'no', 'loan': 'no', 'contact': 'telephone', 'duration': 6, 'campaign': 1, 'pdays': 999, 'previous': 0, 'poutcome': 'nonexistent', 'emp.var.rate': 1.1, 'cons.price.idx': 93.994, 'cons.conf.idx': -36.4, 'euribor3m': 4.857, 'nr.employed': 5191.0, 'id': '3ad93d85-2390-11ee-83b8-e7e9bcdc248d'}]
    assert  convert_data == expected_output

