import tk
import textwrap
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from PIL import Image, ImageDraw, ImageFont
from vk_api.upload import VkUpload

token = tk.token

vk=vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk)
botlongpoll = VkBotLongPoll(vk,tk.group_id)
vkupload=VkUpload(vk)

width=500
height=400
offset=20

def find_id_str(st):
    if (type(st)!=str):
        return 0
    res=''
    isFirst=False
    for char in st:
        if not(isFirst) or str.isdigit(char):
            if str.isdigit(char):
                res+=char
        else:
            break
    return int(res)

def write_msg(id, message, attachment, isChat):
    if isChat:
        vk.method('messages.send',{'chat_id':id, 'message':message, 'random_id':get_random_id(), 'attachment':attachment})
    else:
        vk.method('messages.send',{'user_id':id, 'message':message, 'random_id':get_random_id(), 'attachment':attachment})


def create_img(text,avatar='',name=''):

    print("img_func was called")
    lines=textwrap.wrap(text,width=50)

    print(len(text))

    img=Image.new(mode="RGB", size=(width,height))
    idraw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype("arial.ttf", size=18)
    text_off=offset
    font_header=ImageFont.truetype("arial.ttf", size=24)
    idraw.text((width/2-150,text_off),"Цитаты великих людей",font=font_header)
    text_off*=3

    for line in lines:
        idraw.text((30,text_off),line,font=font)
        text_off+=offset
    idraw.text((offset,height-2*offset),name,font=font_header)

    img.save('1.jpg')
    return img



# for event in longpoll.listen():
#    if event.type==VkEventType.MESSAGE_NEW:
#         text=event.message
#         #print(event.message)
#         if text!='' and text[0]=='/':
           
#             conv_msg_id=find_id_str(event.attachments.get('reply'))

#             text=vk.method('messages.getByConversationMessageId',{'peer_id':event.peer_id,'conversation_message_ids':conv_msg_id})['items'][0]['text']

#             create_img(text, 'you')

#             photo=vkupload.photo_messages('1.jpg',2000000001)
#             owner_id = photo[0]['owner_id']
#             photo_id = photo[0]['id']
#             access_key = photo[0]['access_key']
#             attachment = f'photo{owner_id}_{photo_id}_{access_key}'

#             write_msg(event.user_id,"",attachment, False)

for event in botlongpoll.listen():
    if event.type==VkBotEventType.MESSAGE_NEW:
        text=event.message.get('text')

        if text!='' and text[0]=='/' and len(text)==1:
            
            print(event)
            try:
                from_id=int(event.object['message']['reply_message']['from_id'])
                text=event.object['message']['reply_message']['text']
                user = vk.method("users.get", {"user_ids": from_id}) 
                fullname = user[0]['first_name'] +  ' ' + user[0]['last_name']
                create_img(text,'',fullname)
                photo=vkupload.photo_messages('1.jpg',2000000001)
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                write_msg(event.chat_id,"",attachment, True)
            except BaseException:
                 print('err')





