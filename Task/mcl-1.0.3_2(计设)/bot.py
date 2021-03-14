import os
from graia.broadcast import Broadcast
import urllib.request
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.application import Image
from graia.application.message.elements.internal import Plain
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.event.messages import GroupMessage
from aip import AipImageProcess
import os,base64

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080", # 填入 httpapi 服务运行的地址
        authKey="tanleiddtanleidd", # 填入 authKey
        account=2027063275, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)
@bcc.receiver("GroupMessage")
async def group_message_reword( 
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group,
    member: Member,):
        list1=["航航","人了","人呢"]
        list2=["sb","nt","傻","弱智","fw","滚","SB","敢不敢","tm","nm","透","nb","日","wc","草","操","TM","他妈","屁","sy","智障","sg","尼玛","你妈","去你"]
        list3=["勇士"]
        for x in list1:
                if message.asDisplay().find(x)!=-1:
                        await app.sendGroupMessage(group, MessageChain.create([Plain("找你爹干嘛呀了")]))
                        break;
        for y in list2:
                if message.asDisplay().find(y)!=-1:
                        await app.sendGroupMessage(group, MessageChain.create([Plain("小孩子你讲nmd脏话呢！")]))
                        break
        for z in list3:
                if message.asDisplay().find(z)!=-1:
                        await app.sendGroupMessage(group, MessageChain.create([Plain("总冠军！")]))
                        break
        if '无损放大' in message.asDisplay():
                if message.has(Image):
                        await app.sendGroupMessage(group,MessageChain.create([Plain(text='图片处理中')]))
                        print((message.get(Image))[0].url)
                        skin_Img = (message.get(Image))[0].url
                        skin_file = '1.jpg'
                        request = urllib.request.Request(skin_Img)
                        response = urllib.request.urlopen(request)
                        get_img = response.read()
                        with open(skin_file, 'wb') as fb:
                                fb.write(get_img)
                        """ 读取图片 """
                        def get_file_content(filePath):
                                with open(filePath, 'rb') as fp:
                                        return fp.read()
                        image = get_file_content('1.jpg')
                        """ 调用图像无损放大 """
                        images=client.imageQualityEnhance(image)
                        imgdata=base64.b64decode(images["image"])
                        file=open('2.jpg','wb')
                        file.write(imgdata)
                        file.close()
                        await app.sendGroupMessage(group, MessageChain.create([
                                Image.fromLocalFile("2.jpg")
                        ]))
app.launch_blocking()

