import requests

response = requests.get('https://blog.naver.com/dlfauddl/223290805815')

print(response.status_code)