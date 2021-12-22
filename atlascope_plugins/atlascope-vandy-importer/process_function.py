import json

def vandy_processor(data):

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

    # f = open("atlascope/core/management/dataloader/dataset.json", "w")
    # json.dump(vandy_dict, f)

    return ()
