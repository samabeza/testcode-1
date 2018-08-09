from datetime import datetime as dt
import requests
import json
from requests.auth import HTTPBasicAuth
import jsonpath
def log_tool_usage(tool_id, automation_exec_time_mins, used_by ):
    print('log_tool_usage request==> {},{},{}'.format(tool_id,automation_exec_time_mins,used_by))
    url = 'http://10.53.32.117:8000/QEAnalytics/default/api/tool_usage.json'
    headers = {'Content-type': 'application/json'}
    curr_time= dt.now().strftime('%Y-%m-%d %H:%M:%S')
    print(curr_time)
    data = {'tool_id':tool_id, 
            'automation_exec_time_mins':automation_exec_time_mins, 
            'creation_date': curr_time,
            'created_by': ''+used_by
            }
    #data_json = json.dumps(data)
    myResponse = requests.post(url=url, data=data)
    # For successful API call, response code will be 200 (OK)
    if(myResponse.ok):
        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        jData = json.loads(myResponse.content)
        match = jsonpath.jsonpath(jData,'$.errors')
        print(match)
        return match[0]
    else:
      # If response code is not ok (200), print the resulting http error code with description
      print('{}'.format(myResponse))
      return myResponse.raise_for_status()
