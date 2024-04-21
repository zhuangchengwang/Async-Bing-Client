import http.client
import json
conn = http.client.HTTPSConnection("127.0.0.1", 7890)
conn.set_tunnel("chat.openai.com")
# conn = http.client.HTTPSConnection("chat.openai.com")
payload = json.dumps({
   "action": "next",
   "messages": [
      {
         "id": "aaa2e1a9-5b40-4fe0-b2e4-f4dc2d3a793c",
         "author": {
            "role": "user"
         },
         "content": {
            "content_type": "text",
            "parts": [
               "你好"
            ]
         },
         "metadata": {}
      }
   ],
   "parent_message_id": "aaa18b55-72d4-4326-965a-c7b43a5b9bfd",
   "model": "text-davinci-002-render-sha",
   "timezone_offset_min": -480,
   "suggestions": [
      "Tell me a random fun fact about the Golden State Warriors",
      "Can you explain the concept of \"nostalgia\" to a kindergartener?",
      "Compare shifting business strategies from budget to luxury and luxury to budget, using a brief table to outline different aspects",
      "I have a photoshoot tomorrow. Can you recommend me some colors and outfit options that will look good on camera?"
   ],
   "history_and_training_disabled": False,
   "conversation_mode": {
      "kind": "primary_assistant"
   },
   "force_paragen": False,
   "force_paragen_model_slug": "",
   "force_nulligen": False,
   "force_rate_limit": False,
   "websocket_request_id": "2fdf53df-de01-4d27-8c2e-9c263585e85c"
})
headers = {
   'authority': 'chat.openai.com',
   'accept': 'text/event-stream',
   'accept-language': 'zh-CN,zh;q=0.9',
   'cache-control': 'no-cache',
   'oai-device-id': 'e23c8cf6-297c-4857-b92d-86af5dd7bf02',
   'oai-language': 'en-US',
   'openai-sentinel-chat-requirements-token': 'gAAAAABmDfUQTzWioJfSnMUuNxPlSnxWVTCIfKlBETm02NiLh1RoybP36dwKtpgGB-rsZ06QFBVbU9UrNgn_TtaxNVb7Sg8Wsy3glv0dOD_DV_UYyo_yrTdq1ZgCz18en-95OKcjEMadWH61i0zCtrB2W0kXWlhv2IvPtpEpox1rXU_AH-Olsl8ESgLeLSzsTJQAYUqR2MTxxqkbYoksJJ42BWpM08Hf_NLpgl3tloE1O3ULrJNQMjh70l6_-qvHkXierYdhfTJY-8vTsqX6YsiNTYEF3-tOVPwMN-Y2LrSXOGDjikP_mig=',
   'origin': 'https://chat.openai.com',
   'pragma': 'no-cache',
   'referer': 'https://chat.openai.com/',
   'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"macOS"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-origin',
   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
   'Cookie': '_ga=GA1.2.73326254.1680240055; oai-did=e23c8cf6-297c-4857-b92d-86af5dd7bf02; __Host-next-auth.csrf-token=1a07d6c56ed3143005d06930170e7f6fbe2d7d6daa7a3fa42fd5420357ef3e4c%7C5df5a9e4f520e79fd3073de48c7fff7c7d15d8b7f458d6b0d9c621ecbe505536; __cflb=0H28vVfF4aAyg2hkHFTZ1MVfKmWgNcKF72gDgAFPhWm; __cf_bm=XR1NvtvB.AYqMCYFJSmUDJ3M_EdR8Wvjvk466oLTwWw-1712190720-1.0.1.1-J30MKJrEwxq43dT7Cz5Pe22uXjNWkS9IB3Nh6GnxOmWJOjEfu61xxa7By9oLkiERb1UvoVInQTaIg9x73STD6g; _cfuvid=p_Ed.wayBgmyayFBc8z9KIhlGGuMfgBBd3jamLZ.HHI-1712190720925-0.0.1.1-604800000; cf_clearance=c2PNyjt8NYndRMxKM6yST19fePXEPhFHWjgJj78Rn_U-1712190723-1.0.1.1-qb3UKaplmAbaResBshx1Y6Kie2Y5jX8GKrEZ_nNFmkWFMzVbgPk.E07LCHY3oUOXXuc.WFQDZZU8EL2FEtZ9VA; __Secure-next-auth.callback-url=https%3A%2F%2Fchat.openai.com; _dd_s=rum',
   'content-type': 'application/json'
}
conn.request("POST", "/backend-anon/conversation", payload, headers)
res = conn.getresponse()

# 读取 SSE 事件流
for line in res:
    print(line.decode("utf-8"))
data = res.read()
print(data.decode("utf-8"))