from g4f.client import Client
## 速度太慢了, 不管有没有接代理
client = Client(proxies="http://10.254.32.104:7890")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
   
)
print(response.choices[0].message.content)

# response = client.images.generate(
#     model="dall-e-3",
#     prompt="a white siamese cat",
# )

# image_url = response.data[0].url