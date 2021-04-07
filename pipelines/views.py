from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests

url = "https://circleci.com/api/v2/project/gh/15five/qa_e2e_test/pipeline"

def home(request):
    return render(request, 'home.html')

@login_required
def runAll(request):
    if request.method == 'GET':
        payload='{"branch": "cci_test",\n    \"parameters\": {\n        \"workingdir\": \"feedback\"\n    }\n}'
        headers = {
            'Circle-Token': '5d007a30d834984bff7eea585cc3eabe543856d3',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

        return render(request, 'runAll.html')
    elif request.POST['cciToken']:
        payload={
            "branch": "cci_test",
            "parameters":
                {"workingdir": "feedback"
                 }
        }
        headers = {
        'Circle-Token': '5d007a30d834984bff7eea585cc3eabe543856d3',
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        return redirect('home')
