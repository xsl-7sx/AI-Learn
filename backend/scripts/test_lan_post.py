import httpx

try:
    with httpx.Client(trust_env=False, timeout=10) as client:
        r = client.post('http://192.168.0.10:8000/api/v1/quiz/generate', json={'topic': '测试'})
        print(r.status_code)
        print(r.text)
except Exception as e:
    print('exception:', repr(e))
