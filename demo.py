import asyncio

from async_bing_client import Bing_Client,ConversationStyle
# 本地启动http代理,vscode 直接运行,观察控制台的输出即可查看到结果
# 如果后续demo无法正常启动,要么代理有问题,要么cookie问题,要么代码已经过时了,适应不了当前的bing
# client = Bing_Client(cookie="cookie.json", proxy="socks5://127.0.0.1:4781")
client = Bing_Client(cookie="cookie.json", proxy="http://127.0.0.1:4780")
# client = Bing_Client(cookie="cookie.json")

async def main():
    await client.init()
    chat = await client.create_chat()
    async for text in client.ask_stream("根据收到的图像描述,推理图图中包含的商品信息,商品品牌,商品卖点,目标人群对象,并用json对象返回,需要能被golang等语言正确解析",image="./tmp/bg.jpeg", chat=chat,
                                    yield_search=False,
                                    conversation_style=ConversationStyle.Creative):
        print(text, end="")


if __name__ == '__main__':
    asyncio.run(main())
