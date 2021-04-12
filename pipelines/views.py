import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import accounts.models

url = "https://circleci.com/api/v2/project/gh/15five/qa_e2e_test/pipeline"
gh_branch = "https://api.github.com/repos/15five/qa_e2e_test/branches"
e2e_path = "https://api.github.com/repos/15five/qa_e2e_test/contents/test/specs"
ios_path = "https://api.github.com/repos/15five/qa_e2e_test/contents/test/specsMobile"

def home(request):
    return render(request, 'home.html')

def payload(sta = 'false', pro = 'false', ios = 'false'):
    payload='{"branch": "cci_test", "parameters": {"workingdir": "feedback", "run_smoke_custom": false, "run_smoke_ios_staging": '+ios+', "run_smoke_production": '+pro+', "run_smoke_staging": '+sta+'}}'
    return payload

def payload_custom(env, dir, branch="cci_test"):
    payload_custom = {
        "branch": branch,
        "parameters": {
            "workingdir": dir,
            "run_smoke_custom": True,
            "run_smoke_ios_staging": False,
            "run_smoke_production": False,
            "run_smoke_staging": False,
            "working_env": env}}
    payload_json = json.dumps(payload_custom)
    return payload_json

@login_required
def runAll(request):
    token = (accounts.models.Accounts.objects.filter(user=request.user).values_list('token'))[0]
    headers = {
        'Circle-Token': token[0],
        'Content-Type': 'application/json'
    }
    print(list(request.POST.items()))
    if request.method == 'GET':
        print(token[0])
        return render(request, 'runAll.html')
    elif 'staging' in request.POST:
        print(payload(sta='true'))
        response = requests.request("POST", url, headers=headers, data=payload(sta='true'))
        print(response.text)
        return redirect('home')
    elif 'production' in request.POST:
        response = requests.request("POST", url, headers=headers, data=payload(pro='true'))
        print(response.text)
        return redirect('home')
    elif 'ios' in request.POST:
        response = requests.request("POST", url, headers=headers, data=payload(ios='true'))
        print(response.text)
        return redirect('home')

@login_required
def runCustom(request):
    token = (accounts.models.Accounts.objects.filter(user=request.user).values_list('token'))[0]
    gh_token = (accounts.models.Accounts.objects.filter(user=request.user).values_list('gh_token'))[0]
    headers = {
        'Circle-Token': token[0],
        'Content-Type': 'application/json'
    }
    gh_headers = {
        'Authorization': f'token {gh_token[0]}'
    }
    if request.method == 'GET':
        # print(token[0])
        # print(gh_token[0])
        response = requests.request("GET", gh_branch, headers=gh_headers, data={})
        branches = response.json()
        response = requests.request("GET", e2e_path, headers=gh_headers, data={})
        e2e = response.json()
        response = requests.request("GET", ios_path, headers=gh_headers, data={})
        ios = response.json()
        return render(request, 'runCustom.html', {'branches': branches, "e2e": e2e, "ios": ios})
    else:
        print(list(request.POST.items()))
        print(payload_custom(request.POST['webenv'], request.POST['webdir'], request.POST['branch']))
        response = requests.request("POST", url, headers=headers, data=payload_custom(request.POST['webenv'], request.POST['webdir'], request.POST['branch']))
        print(response.text)
        return redirect('home')

@login_required
def history(request):
    return render(request, 'history.html')
