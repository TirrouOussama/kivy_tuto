

import requests
import re


start_lon = 3.006193661499026
start_lat = 36.59308912856339

end_lon = 2.999173625182806
end_lat = 36.61426132068456


body = {"coordinates":[[start_lon,start_lat],[end_lon,end_lat]]}

headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': '5b3ce3597851110001cf6248e32f3f787ba541e8b3d916f4681b9340',
    'Content-Type': 'application/json; charset=utf-8'
}
call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/gpx', json=body, headers=headers)


string_res = call.text

print(string_res)

tag = 'rtept'
reg_str = '</' + tag + '>(.*?)' + '>'
res = re.findall(reg_str, string_res)
print(res)
print('_____________________________________')
string1 = str(res)
tag1 = '"'
reg_str1 = '"' + '(.*?)' + '"'
res1 = re.findall(reg_str1, string1)
print(res1)
