import time

from fastapi import FastAPI, Request, Response, Form

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from furl import furl

from pydantic import BaseModel

import validators

import score_lists
import tools
import youtube_id
import config


class URLQuery(BaseModel):
    url: str
    method: str = None
    srcip: str = None


debug = int(config.BaseConfig.DEBUG)

application = FastAPI()


def jsonify_response(msg, code):
    status_code = code
    success = False
    response = {
        'success': success,
        'error': {
            'code': code,
            'message': msg
        }
    }

    return jsonable_encoder(response), status_code


def invalid_url_jsonify_response():
    return jsonify_response("Bad input: url must be a valid url!", 400)


@application.get("/")
def read_root():
    return {"Hello": "World"}


@application.post("/api/v1/checkurl/form")
async def check_form(response: Response, request: Request, url: str = Form(...), method: str = Form(...)):
    query = URLQuery
    query.url = url
    query.method = method
    return check_query(query, response, request)


@application.post("/api/v1/checkurl/json")
async def check_json(query: URLQuery, response: Response, request: Request):
    return check_query(query, response, request)


@application.get("/api/v1/checkurl/")
async def check_get(response: Response, request: Request, url: str = None, method: str = None):
    query = URLQuery
    query.url = url
    if tools.is_string(method):
        query.method = method
    else:
        query.method = "unknown"
    return check_query(query, response, request)


def check_query(query, response, request):
    details = dict()
    details["url"] = query.url
    if tools.is_string(query.method):
        details["method"] = query.method
    else:
        details["method"] = "unknown"

    if debug >0:
        print("Request details:", details)

    invalid_url = False
    if isinstance(details.get("url"), type(None)) or details.get("url") == "":
        invalid_url = True
    if invalid_url is not True and validators.url(details.get("url")) is False:
        invalid_url = True
    if tools.is_string(details.get("url")) and len(details.get("url")) < 4:
        invalid_url = True

    if invalid_url:
        json_response, status_code = invalid_url_jsonify_response()
        return JSONResponse(content=json_response, status_code=status_code)

    response_data, headers = check_url(details.get("url"), details.get("method"))

    if debug >0:
        print("check_url response:", response_data, headers)

    json_response = jsonable_encoder(response_data)

    # response.headers = headers
    # response.body = response_data
    return JSONResponse(content=json_response, headers=headers, status_code=200)


def check_url(request_url, method):
    start = time.process_time()

    response = dict()

    headers = {'Content-Type': 'application/json'}

    try:
        f = furl(request_url)
        headers["X-URL-Parsed-OK"] = "1"
    except Exception as e:
        print("X-URL-Parsed-OK:", e)
        response["tlsbump"] = 1000

    if not tools.is_valid_hostname(f.host):
        headers["X-Invalid-Hostname"] = "1"
        response["tlsbump"] = 1000
        response["invalid"] = 1000

        return response, headers

    if tools.is_valid_ip_address(f.host):
        headers["X-URL-Hostname-Is-IP"] = "1"
    else:
        headers["X-URL-Hostname-Is-IP"] = "0"

    yt_vid = youtube_id.get_yt_vid(request_url)
    if yt_vid is not None:
        headers['X-Vid-Check'] = "1"
        # matched_lists = score_lists.check_score(yt_vid)
        matched_lists = score_lists.check_score(yt_vid)
        if debug > 0:
            print("check_score res:", matched_lists)
        if len(matched_lists) > 0:
            for key in matched_lists:
                response[key] = matched_lists[key]

    headers["X-Query-Duration"] = str(time.process_time() - start)

    if debug > 0:
        print(response)
    return response, headers
