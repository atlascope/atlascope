import requests
from process_function import vandy_processor


# def run(source_uri=None):
#     print(f"Congratulations! You have imported {source_uri} from vandy.")

def run(source_uri=None):

    headers = {'Girder-Token': ''}

    r = requests.get(source_uri, headers = headers)

    data = r.json()


    vandy_dict = {

    "name" : data['name'],
    "size" : data["size"],
    "meta":{
        "updated" : data["updated"],
        "DSAGroupSet" : data["meta"]["DSAGroupSet"],
        "htanMeta" : data["meta"]["htanMeta"],
        "ioparams" : data["meta"]["ioparams"],
        "omeSceneDescription" : data["meta"]["omeSceneDescription"],
    }
    }
# add dict to meta field on model
# upload to s3
# add uri to s3 field to model
