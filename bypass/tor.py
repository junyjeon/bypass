from torrequest import TorRequest

# TorRequest 인스턴스 생성
tr = TorRequest(password='8642')

# 현재 IP 주소 확인
import requests
response = requests.get('https://icanhazip.com')
print("My Original IP Address:", response.text)

# Tor를 통해 요청 보내기
tr.reset_identity()  # Tor 리셋
response = tr.get('https://icanhazip.com')
print("New Ip Address", response.text)