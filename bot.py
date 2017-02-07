#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import ConfigParser
import json
import time


class MyWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)

        self.tuling_key = ""
        self.robot_switch = False
        self.masterstatus = u"工作中"
        self.autorelpy = u""
        self.talkdic = {'test':time.time()}

        try:
            cf = ConfigParser.ConfigParser()
            cf.read('conf.ini')
            self.tuling_key = cf.get('main', 'key')
        except Exception:
            pass

        print 'tuling_key:', self.tuling_key
        self.masterstatus_update()

    def masterstatus_update(self):
        try:
            cf = ConfigParser.ConfigParser()
            cf.read('conf.ini')
            mastername = cf.get('master','name')
            mastertel = cf.get('master','tel')
            self.autorelpy = u"%s在%s，有事请留言，和我聊天请回复#1。\n急事请电话联系：%s" %(mastername,self.masterstatus,mastertel)
        except Exception:
            print 'get master status error'
            pass

    def tuling_auto_reply(self, uid, msg):
        if self.tuling_key:
            url = "http://www.tuling123.com/openapi/api"
            user_id = uid.replace('@', '')[:30]
            body = {'key': self.tuling_key, 'info': msg.encode('utf8'), 'userid': user_id}
            r = requests.post(url, data=body)
            respond = json.loads(r.text)
            result = ''
            if respond['code'] == 100000:
                result = respond['text'].replace('<br>', '  ')
                result = result.replace(u'\xa0', u' ')
            elif respond['code'] == 200000:
                result = respond['url']
            elif respond['code'] == 302000:
                for k in respond['list']:
                    result = result + u"【" + k['source'] + u"】 " +\
                        k['article'] + "\t" + k['detailurl'] + "\n"
            else:
                result = respond['text'].replace('<br>', '  ')
                result = result.replace(u'\xa0', u' ')

            print '    ROBOT:', result
            return result
        else:
            return u"知道啦"

    def auto_switch(self, msg):
        msg_data = msg['content']['data']
        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开']
        #start_cmd = [u'出来', u'启动', u'工作',u'开启']
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[Mobot]' + u'机器人已关闭！', msg['to_user_id'])

            if msg_data[:2] == u"@去":
                self.masterstatus = msg_data[msg_data.find(u"@去")+2:]+u"中"
                self.masterstatus_update()
                self.robot_switch = True
                self.send_msg_by_uid(u'主人当前状态：'+ self.masterstatus, msg['to_user_id'])

        else:
            #for i in start_cmd:
                #if msg_data.find(i) != -1:
                    if msg_data[:2] == u"@去":
                        self.masterstatus = msg_data[msg_data.find(u"@去")+2:]+u"中"
                        self.masterstatus_update()
                        self.robot_switch = True
                        self.send_msg_by_uid(u'[Mobot]' + u'机器人已启动！\n主人当前状态：'+ self.masterstatus, msg['to_user_id'])

    def handle_msg_all(self, msg):
        if not self.robot_switch and msg['msg_type_id'] != 1:
            return
        if msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # reply to self
            self.auto_switch(msg)
            #self.send_msg_by_uid(self.autorelpy,msg['user']['id'])
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 0:  # text message from contact
            if msg['content']['data'] == u"#1":
                self.updatetalktime(msg['user']['id'])
                self.send_msg_by_uid(u"说点什么呢[微笑]",msg['user']['id'])
            else:
                if self.is_tulingtalk(msg['user']['id']):
                    self.send_msg_by_uid(self.tuling_auto_reply(msg['user']['id'], msg['content']['data']), msg['user']['id'])
                else:
                    self.send_msg_by_uid(self.autorelpy,msg['user']['id'])
        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:  # group text message
            if 'detail' in msg['content']:
                my_names = self.get_group_member_name(msg['user']['id'], self.my_account['UserName'])
                if my_names is None:
                    my_names = {}
                if 'NickName' in self.my_account and self.my_account['NickName']:
                    my_names['nickname2'] = self.my_account['NickName']
                if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
                    my_names['remark_name2'] = self.my_account['RemarkName']

                is_at_me = False
                for detail in msg['content']['detail']:
                    if detail['type'] == 'at':
                        for k in my_names:
                            if my_names[k] and my_names[k] == detail['value']:
                                is_at_me = True
                                break
                if is_at_me:
                    src_name = msg['content']['user']['name']
                    reply = 'to ' + src_name + ': '
                    if msg['content']['type'] == 0:  # text message
                        #reply += self.tuling_auto_reply(msg['content']['user']['id'], msg['content']['desc'])
                        reply += self.autorelpy
                    else:
                        reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
                    self.send_msg_by_uid(reply, msg['user']['id'])

    def is_tulingtalk(self,uid):
        lasttalktime = self.talkdic.get(uid,0)
        if lasttalktime == 0:
            return False
        elif time.time() - lasttalktime > 60:
            return False
        else:
            self.updatetalktime(uid)
            return True


    def updatetalktime(self,uid):
        self.talkdic[uid] = time.time()

def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'

    bot.run()


if __name__ == '__main__':
    main()

