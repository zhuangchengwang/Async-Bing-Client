import asyncio

from async_bing_client import Bing_Client,ConversationStyle
# 本地启动http代理,vscode 直接运行,观察控制台的输出即可查看到结果
# 如果后续demo无法正常启动,要么代理有问题,要么cookie问题,要么代码已经过时了,适应不了当前的bing
# client = Bing_Client(cookie="cookie.json", proxy="socks5://127.0.0.1:4781")
client = Bing_Client(cookie="cookie.json", proxy="http://127.0.0.1:7890")
# client = Bing_Client(cookie="cookie.json")

async def main():
    await client.init()
    chat = await client.create_chat()
    images = await client.draw("创造一辆火车,卡通,富有儿童感")
    print(images)

if __name__ == '__main__':
    asyncio.run(main())
