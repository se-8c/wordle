
def resp_ok_code(code,data):
    return {
        "code": code,
        "msg": "success",
        "data": data
    }

def resp_ok(data):
    return {
        "code": 1,
        "msg": "success",
        "data": data
    }

def resp_err(code, msg):
    return {
        "code": code,
        "msg": msg
    }