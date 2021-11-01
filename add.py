from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random
import re
import os, sys
import configparser
re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

class main():

    def banner():
        
        print(gr+f"""                
              KÉO MEMBER VÀO NHÓM TELEGRAM
            """+gr)



cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)

except KeyError:
    os.system('clear')
    main.banner()
    print(re+"[!] run python3 setup.py first !!\n")
    sys.exit(1)


SLEEP_TIME = 30



client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Nhập code: '))

def add_users_to_group():
    os.system('clear')
    main.banner()
    input_file = sys.argv[1]
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            try:
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
            except:
                ahssj=0
            users.append(user)

    random.shuffle(users)
    chats = []
    last_date = None
    chunk_size = 10
    groups=[]

    result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup== True: # CONDITION TO ONLY LIST MEGA GROUPS.
                groups.append(chat)
        except:
            continue
    main.banner()
    print('Chọn nhóm thêm member:')
    i=0
    for group in groups:
        print(str(i) + '- ' + group.title)
        i+=1

    g_index = input("Nhập lựa chọn: ")
    target_group=groups[int(g_index)]
    print('\n\nGroup tăng member:\t' + groups[int(g_index)].title)

    target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
    
    mode = int(input("Nhập 1 để thêm theo tên người dùng hoặc 2 để thêm theo ID: "))

    error_count = 0
    Flood_Error=0
    m=1
    main.banner()
    for user in users:
        try:
            print ("Thêm {}".format(user['username']))
            if mode == 1:
                if user['username'] == "":
                    continue
                user_to_add = client.get_input_entity(user['username'])
            elif mode == 2:
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                sys.exit("Đã chọn chế độ không hợp lệ. Vui lòng thử lại.")
            client(InviteToChannelRequest(target_group_entity,[user_to_add]))
            print("Số thành viên đã thêm:",m)
            m+=1
            print("Chờ 10 đến 15 giây...")
            time.sleep(random.randrange(10, 15))
        except PeerFloodError:
             Flood_Error += 1
             print("Nhận lỗi lũ lụt từ điện tín.")
             if Flood_Error > 6:
                 sys.exit('Nhận lỗi lũ lụt từ điện tín. Tập lệnh hiện đang dừng. Vui lòng thử lại sau 1 ngày.')
        except UserPrivacyRestrictedError:
            print("Cài đặt quyền riêng tư của người dùng không cho phép bạn làm điều này. Bỏ qua.")
        except:
            traceback.print_exc()
            print("Unexpected Error")
            error_count += 1
            if error_count > 10:
                sys.exit('too many errors')
            continue


def list_users_in_group():
    os.system('clear')
    main.banner()
    chats = []
    last_date = None
    chunk_size = 200
    groups=[]
    
    result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            ))
    chats.extend(result.chats)
    
    for chat in chats:
        try:           
            if chat.megagroup== True:
                 groups.append(chat)
        except:
            continue
    
    print('Chọn một nhóm để loại bỏ các thành viên:')
    i=0
    for g in groups:
        print(str(i) + '- ' + g.title)
        i+=1
    
    g_index = input("Nhập lựa chọn: ")
    target_group=groups[int(g_index)]

    print('\n\nGroup :\t' + groups[int(g_index)].title)
    
    print('Tìm nạp thành viên...')
    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=True)
    
    print('Đang lưu trong tệp...')
    with open("members.csv","w",encoding='UTF-8') as f :
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
        for user in all_participants:
            if user.username:
                username= user.username
            else:
                continue
                
            if user.first_name:
                first_name= user.first_name
            else:
                first_name= ""
            if user.last_name:
                last_name= user.last_name
            else:
                last_name= ""
            name= (first_name + ' ' + last_name).strip()
            writer.writerow([username])      
    print('Thành viên đã được loại bỏ thành công.')



    

def printCSV():
    os.system('clear')
    main.banner()
    input_file = sys.argv[1]
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['id'] = int(row[1])
            user['access_hash'] = int(row[2])
            users.append(user)
            print(row)
            print(user)
    sys.exit('FINITO')

    
def send_sms():

        os.system('clear')
        main.banner()
        input_file = sys.argv[1]
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)
        print(gr+"[1] gửi sms bằng ID người dùng\n[2] gửi sms bằng tên người dùng")
        mode = int(input(gr+"Input : "+re))
         
        message = input(gr+"[+] Nhập tin nhắn của bạn : "+re)
        for user in users:
            if mode == 2:
                if user['username'] == "":
                    continue
                receiver = client.get_input_entity(user['username'])
            elif mode == 1:
                receiver = InputPeerUser(user['id'],user['access_hash'])
            else:
                print(re+"[!] Chế độ không hợp lệ. Đang thoát.")
                client.disconnect()
                sys.exit()
            try:
                print(gr+"[+] Gửi tin nhắn tới:", user['name'])
                client.send_message(receiver, message.format(user['name']))
                print( "Chờ 40 giây")
                time.sleep(random.randrange(30, 45))
#                time.sleep(SLEEP_TIME)
            except PeerFloodError:
                print(re+"[!] Nhận lỗi lũ lụt từ điện tín. \n[!] Tập lệnh hiện đang dừng. \n[!] Vui lòng thử lại sau một thời gian.")
                client.disconnect()
                sys.exit()
            except Exception as e:
                print(re+"[!] Error:", e)
                print(re+"[!] Đang cố gắng tiếp tục...")
                continue
        client.disconnect()
        print("Xong. Đã gửi tin nhắn cho tất cả người dùng.")




print('Tìm nạp thành viên ...')
# all_participants = []
# all_participants = client.get_participants(target_group, aggressive=True)
print('Bạn muốn làm gì:')
mode = int(input("Enter \n1-Liệt kê người dùng trong một nhóm \n2-Thêm người dùng từ CSV vào Nhóm (CSV phải được chuyển làm tham số cho tập lệnh\n3-Show CSV\n4-Gửi tin nhắn hàng loạt\n\nTùy chọn của bạn: "))

if mode == 1:
    list_users_in_group()
elif mode == 2:
    add_users_to_group()
elif mode == 3:
    printCSV()
elif mode == 4:
    send_sms()
