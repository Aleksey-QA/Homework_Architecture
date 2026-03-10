import json

import requests

url = "http://localhost:8000/boards/"

payload = json.dumps({
  "title": "23e4r5t",
  "description": "At quisquam distinctio magnam consequatur odit facilis animi reprehenderit. Voluptatem architecto doloremque in recusandae nostrum rerum atque minima. Similique ipsum vitae magnam ut nobis. Ipsa soluta minus repellendus repellat id quas vel velit suscipit. A alias commodi omnis sed dolor ipsam beatae.",
  "public": False
})
headers = {
  # 'Authorization': f'Bearer {res_json["access_token"]}',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)