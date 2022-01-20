import requests


def run(source_uri=None):

    params = {'key': ''}
    tokenUrl = "https://styx.neurology.emory.edu/girder/api/v1/api_key/token"

    token = requests.post(tokenUrl, params=params).json()["authToken"]["token"]

    headers = {'girder-token': token}

    r = requests.get(source_uri, headers=headers)

    if r.status_code == 200:
        with open("test.tif", "wb") as f:
            f.write(r.content)

    # data = r.json()
    # vandy_dict = {
    # "name" : data['name'],
    # "size" : data["size"],
    # "meta":{
    #     "updated" : data["updated"],
    #     "DSAGroupSet" : data["meta"]["DSAGroupSet"],
    #     "htanMeta" : data["meta"]["htanMeta"],
    #     "ioparams" : data["meta"]["ioparams"],
    #     "omeSceneDescription" : data["meta"]["omeSceneDescription"],
    # }
    # }
# add dict to meta field on model
# upload to s3
# add uri to s3 field to model


run("https://styx.neurology.emory.edu/girder/api/v1/file/60e84a1868f4fe34fc7eef72/download")
