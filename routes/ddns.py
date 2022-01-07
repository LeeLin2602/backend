from flask import Response, request
from __main__ import app, g, users, dns
from controllers.users import OperationError
from controllers.dns import DNSError

@app.route("/ddns/<path:domain>/records/<string:type_>/<string:value>", methods=['POST'])
def addRecord(domain, type_, value):
    if not g.user:
        return {"message": "Unauth."}, 401

    user = users.getUser(g.user['uid'])
    domain = domain.strip('/').split('/')
    domainName = '.'.join(reversed(domain))

    req = request.json
    ttl = 5
    
    if req and 'ttl' in req:
        ttl = int(req[ttl])

    try:
        if not users.authorize(user, "MODIFY", domain):
            return {"errorType": "PermissionDenied", "msg": ""}, 403
        dns.addRecord(user['uid'], domainName, type_, value, ttl)
    except OperationError as e:
        return {"errorType": e.typ, "msg": e.msg}, 403
    except DNSError as e:
        return {"errorType": e.typ, "msg": e.msg}, 403

    return {"msg":"ok"}

@app.route("/ddns/<path:domain>/records/<string:type_>/<string:value>", methods=['DELETE'])
def delRecord(domain, type_, value):
    if not g.user:
        return {"message": "Unauth."}, 401

    user = users.getUser(g.user['uid'])
    domain = domain.strip('/').split('/')
    domainName = '.'.join(reversed(domain))

    try:
        if not users.authorize(user, "MODIFY", domain):
            return {"errorType": "PermissionDenied", "msg": ""}, 403
        dns.delRecord(user['uid'], domainName, type_, value)
    except OperationError as e:
        return {"errorType": e.typ, "msg": e.msg}, 403
    except DNSError as e:
        return {"errorType": e.typ, "msg": e.msg}, 403

    return {"msg":"ok"}
