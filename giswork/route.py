#curl 'https://www.strava.com/frontend/routemaster/bulk_route'   -H 'authority: www.strava.com'  -H 'accept: application/json'   -H 'content-type: application/json;charset=UTF-8'   -H 'x-csrf-token: 6A27m/946XEbnsr0fLymJzk3gMTb5zlqZFUQ0PmIXrJAs8b8PeU47QWoejNyUI5wBCFSzaby7DEsfPVjLiRdkg=='         -H 'cookie: _strava4_session=ggt6un0df2t24q23dl0na9sboloa9fie; CloudFront-Key-Pair-Id=APKAIDPUN4QMG7VUQPSA; _sp_ses.047d=*; '   --data-raw '{"sets":[{"elements":[{"element_type":1,"waypoint":{"point":{"lat":42.36250167231222,"lng":-71.10958420020755}}},{"element_type":1,"waypoint":{"point":{"lat":42.37465244020785,"lng":-71.11358751166367}}}],"preferences":{"popularity":1.0,"elevation":0,"route_type":1,"route_sub_type":5,"straight_line":false}}]}' 

import requests
url = 'https://www.strava.com/frontend/routemaster/bulk_route'  
headers = { 
 'authority': 'www.strava.com',
 'accept': 'application/json',   
 'content-type': 'application/json;charset=UTF-8',   
 'x-csrf-token': '6A27m/946XEbnsr0fLymJzk3gMTb5zlqZFUQ0PmIXrJAs8b8PeU47QWoejNyUI5wBCFSzaby7DEsfPVjLiRdkg==',         
 'cookie': '_strava4_session=ggt6un0df2t24q23dl0na9sboloa9fie; CloudFront-Key-Pair-Id=APKAIDPUN4QMG7VUQPSA; _sp_ses.047d=*; ',
}

r = requests.post(url, headers=headers, data='{"sets":[{"elements":[{"element_type":1,"waypoint":{"point":{"lat":42.36250167231222,"lng":-71.10958420020755}}},{"element_type":1,"waypoint":{"point":{"lat":42.37465244020785,"lng":-71.11358751166367}}}],"preferences":{"popularity":1.0,"elevation":0,"route_type":1,"route_sub_type":5,"straight_line":false}}]}')


print(r.text)
