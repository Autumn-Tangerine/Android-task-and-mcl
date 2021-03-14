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
import requests
import random

""" 你的 APPID AK SK """
APP_ID = '23573192'
API_KEY = 'NHLYfsNBtOqn0EF3vhL6bO24'
SECRET_KEY = '2RTYIcI2RpehTKj4q97X8Elea3TbnjBf'

client = AipImageProcess(APP_ID, API_KEY, SECRET_KEY)
loop = asyncio.get_event_loop()
city='太原'
bot_id='S45369'

q=-1
jiance=-1
baidu=-1
recyle=-1
picture=-1

def gettoken():
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=VziVGFi9hxGgx2RN6vHqb9pj&client_secret=TjTGEO84Nx7ggwzR1Ym8ZGogc2b5LG6z'
        response = requests.post(host)
        if response:
                json_res = response.json()
                access_token = json_res['access_token']
        return access_token
def gettoken2():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=bcdKrKod45MqlFgkpHN4rzpL&client_secret=Fm6NpVFSlRvA1RtHQx1XhdF5lf8a9PS3'
    response = requests.post(host)
    if response:
        json_res = response.json()
        access_token = json_res['access_token']
        return access_token
acs_token = gettoken2()


#结构化数据写作
def ai_artic(access_token):
        host = 'https://aip.baidubce.com/rest/2.0/nlp/v1/gen_article?access_token=' + access_token
        Headers = {
        'Content-Type':'application/x-www-form-urlencoded'
        }
        data = {
        'project_id':'79304',
        'city':city  #或者其他城市
        }
        response = requests.post(host,headers=Headers,data=data)
        if response:
                json_res = response.json()
                contents = json_res['result']['texts'][0]
                print(contents)
        return contents


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
        global city
        global word
        global q
        global jiance
        global baidu
        global bot_id
        global recyle
        global picture
        list1=["航航","人了","人呢"]
        list2=["sb","nt","傻","弱智","fw","滚","SB","敢不敢","tm","nm","透","nb","日","wc","草","操","TM","他妈","屁","sy","智障","sg","尼玛","你妈","去你"]
        list3=["勇士"]
        if '关闭循环模式'in message.asDisplay():
                recyle=-1
                await app.sendGroupMessage(group, MessageChain.create([Plain("关闭成功")]))
        if recyle>0:
                if '脏话'in message.asDisplay():
                        await app.sendGroupMessage(group, MessageChain.create([Plain("nmb")]))        
        if '开启循环模式' in message.asDisplay():
                recyle=1
                await app.sendGroupMessage(group, MessageChain.create([Plain("开启成功")]))
        if '关闭检测模式'in message.asDisplay():
                jiance=-1
                await app.sendGroupMessage(group, MessageChain.create([Plain("关闭成功")]))
        if '关闭图片处理模式'in message.asDisplay():
                picture=-1
                await app.sendGroupMessage(group, MessageChain.create([Plain("关闭成功")]))
        if jiance >0:
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
        if '开启检测模式'in message.asDisplay():
                jiance=1
                await app.sendGroupMessage(group, MessageChain.create([Plain("开启成功")]))             
        if '开启图片处理模式' in message.asDisplay():
                picture=1
                await app.sendGroupMessage(group, MessageChain.create([Plain("开启成功")]))
        if picture>0:
                if message.has(Image):
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
                        if '无损放大'in message.asDisplay():
                                images=client.imageQualityEnhance(image)
                                await app.sendGroupMessage(group, MessageChain.create([Plain("图片处理中")]))
                        if '上色' in message.asDisplay():
                                images=client.colourize(image)
                                await app.sendGroupMessage(group, MessageChain.create([Plain("图片处理中")]))
                        if '清晰度增强' in message.asDisplay():
                                images=client.imageDefinitionEnhance(image)
                                await app.sendGroupMessage(group, MessageChain.create([Plain("图片处理中")]))
                        if '去雾' in message.asDisplay():
                                images=client.dehaze(image)
                                await app.sendGroupMessage(group, MessageChain.create([Plain("图片处理中")]))
                        if '对比度增强' in message.asDisplay():
                                images=client.contrastEnhance(image)
                                await app.sendGroupMessage(group, MessageChain.create([Plain("图片处理中")]))
                        if '拉伸恢复' in message.asDisplay():
                                images=client.stretchRestore(image)
                                await app.sendGroupMessage(group, MessageChain.create([Plain("图片处理中")]))
                        if '动漫化' in message.asDisplay():
                                images=client.selfieAnime(image)
                                await app.sendGroupMessage(group, MessageChain.create([Plain("图片处理中")]))
                        if '修复' in message.asDisplay():
                                images=client.inpaintingByMask(image)
                                await app.sendGroupMessage(group, MessageChain.create([Plain("图片处理中")]))
                        if '图画' in message.asDisplay():
                                options['option'] = "cartoon"
                                images=client.styleTrans(image,options)
                                await app.sendGroupMessage(group, MessageChain.create([Plain("图片处理中")]))
                        imgdata=base64.b64decode(images["image"])
                        file=open('2.jpg','wb')
                        file.write(imgdata)
                        file.close()
                        await app.sendGroupMessage(group, MessageChain.create([
                                Image.fromLocalFile("2.jpg")
                        ]))
        if '天气预报:' in message.asDisplay():
                await app.sendGroupMessage(group, MessageChain.create([Plain("急死啦，正在查询")]))
                city=message.asDisplay()[5:]
                print(city)
                access_token = gettoken()
                await app.sendGroupMessage(group,MessageChain.create([Plain(ai_artic(access_token))]))
        if '关闭UNIT模式' in message.asDisplay():
                q=-1;
                await app.sendGroupMessage(group, MessageChain.create([Plain("关闭成功")]))
        if '关闭Baidu模式'in message.asDisplay():
                q=-1
                bot_id='S45369'
                await app.sendGroupMessage(group, MessageChain.create([Plain("关闭成功")]))
        if '关闭Tra模式'in message.asDisplay():
                q=-1
                bot_id='S45369'
                await app.sendGroupMessage(group, MessageChain.create([Plain("关闭成功")]))
        if '关闭Con模式'in message.asDisplay():
                q=-1
                bot_id='S45369'
                await app.sendGroupMessage(group, MessageChain.create([Plain("关闭成功")]))
        if '关闭YQWD'in message.asDisplay():
                q=-1
                bot_id='S45369'
                await app.sendGroupMessage(group, MessageChain.create([Plain("关闭成功")]))
        if q>0:
                word=message.asDisplay()
                urll = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + str(acs_token)
                log_id ='7758521'
                user_id='fdec7267261b4f5c85299ca97d7d842a'
                s_id=bot_id
                post_data = "{\"log_id\":\""+log_id+"\",\"version\":\"2.0\",\"service_id\":\""+s_id+"\",\"session_id\":\"\",\"request\":{\"query\":\""+word+"\",\"user_id\":\""+user_id+"\"},\"dialog_state\":{\"contexts\":{\"SYS_REMEMBERED_SKILLS\":[\"1057\"]}}}"
                headers = {'Content-Type':'application/json'}
                r = requests.post(urll, data=post_data.encode('utf-8'), headers=headers)
                if r:
                        back = r.json()
                        b = back['result']['response_list'][0]['action_list']
                        c = random.randint(0,len(b))
                        d = len(back['result']['response_list'][0]['action_list'])
                        c = random.randint(0,len(b))
                        huida = b[random.randint(0,d-1)]['say']
                        await app.sendGroupMessage(group,MessageChain.create([Plain(huida)]))
        if '开启UNIT模式' in message.asDisplay():
                q=1
                await app.sendGroupMessage(group, MessageChain.create([Plain("开启成功")]))
        if '开启Baidu模式'in message.asDisplay():
                q=1
                bot_id='S45441'
                await app.sendGroupMessage(group, MessageChain.create([Plain("开启成功")]))
        if '开启Tra模式'in message.asDisplay():
                q=1
                bot_id='S48723'
                await app.sendGroupMessage(group, MessageChain.create([Plain("开启成功")]))
        if '开启Con模式'in message.asDisplay():
                q=1
                bot_id='S48721'
                await app.sendGroupMessage(group, MessageChain.create([Plain("开启成功")]))
        if '开启YQWD模式'in message.asDisplay():
                q=1
                bot_id='S48722'
                await app.sendGroupMessage(group, MessageChain.create([Plain("开启成功")]))
        
        
                
app.launch_blocking()

