#!usr/bin/ven python
# -*- coding:utf-8 -*-

import itchat
from itchat.content import *
import global_list

itchat.auto_login(hotReload=True)
sfs = itchat.search_friends()
my = sfs


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO])
def text_reply(msg):
    if msg['FromUserName'] == my['UserName']:
        if msg['Text'] == u'开启群聊':
            global_list.flag_i_group = 1
            global_list.flag_i = 1
        elif msg['Text'] == u'关闭群聊':
            global_list.flag_i_group = 0
            global_list.flag_i = 1
        elif msg['Text'] == u'开启私聊':
            global_list.flag_i_it = 1
            global_list.flag_i = 1
        elif msg['Text'] == u'关闭私聊':
            global_list.flag_i_it = 0
            global_list.flag_i = 1
        elif msg['Text'] == u'好友群发':
            global_list.flag_i_it_to_all = 1
            global_list.flag_set_it = 1
        elif msg['Text'] == u'群友群发':
            global_list.flag_i_group_to_all = 1
            global_list.flag_set_group = 1
        elif msg['Text'] == u'关闭群发':
            global_list.flag_i_it_to_all = 0
            global_list.flag_i_group_to_all = 0
        elif msg['Text'] == u'帮助':
            itchat.send(u'开启群聊:关闭群聊:开启私聊:开启私聊:好友群发:群友群发:复位(关闭所有功能)', msg['FromUserName'])


        elif msg['Text'] == u'复位':
            global_list.flag_i = 0
            global_list.flag_i_it_to_all = 0
            global_list.flag_i_group_to_all = 0
            itchat.send('%s, %s' % (u'感谢使用', u'复位成功'), msg['FromUserName'])

        if global_list.flag_i_it_to_all == 1 and global_list.flag_set_it != 1:
            print u'好友群发'
            myt = itchat.get_friends(update=True)
            for myi in range(len(myt)):
                itchat.send('%s(%s), %s' % (myt[myi].get('NickName'),
                                            myt[myi].get('RemarkName'), msg['Text']), myt[myi].get('UserName'))

        if global_list.flag_i_group_to_all == 1 and global_list.flag_set_group != 1:
            print u'群友群发'
            chatrooms = itchat.get_chatrooms(update=True)
            for cr in range(len(chatrooms)):
                print cr, 'saiun', chatrooms[cr]['NickName'].encode("utf-8"), chatrooms[cr]['UserName'].encode("utf-8")
                itchat.send(u'@%s\u2005的群友们: %s' % (chatrooms[cr]['NickName'], msg['Text']), chatrooms[cr]['UserName'])

        global_list.flag_set_it = 0  # 防止第一次开启命令被群发出去
        global_list.flag_set_group = 0  # 防止第一次开启命令被群发出去

    rn = itchat.search_friends(userName=msg['FromUserName']).get('RemarkName')
    nn = itchat.search_friends(userName=msg['FromUserName']).get('NickName')

    if global_list.flag_i_it == 1 and global_list.flag_i == 1:
        if msg['Type'] in [PICTURE, RECORDING, ATTACHMENT, VIDEO]:
            msg['Text'](msg['FileName'])
            return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])
        else:
            itchat.send('%s(%s), %s' % (nn, rn, msg['Text']), msg['FromUserName'])


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO],
                     isGroupChat=True)
def text_reply(msg):
    if global_list.flag_i_group == 1 and global_list.flag_i == 1:
        if msg['Type'] in [PICTURE, RECORDING, ATTACHMENT, VIDEO]:
            msg['Text'](msg['FileName'])
            return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])
        else:
            itchat.send(u'%s, %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])

itchat.run()