from pyobigram.utils import sizeof_fmt,get_file_size,createID,nice_time
from pyobigram.client import ObigramClient,inlineQueryResultArticle
from MoodleClient import MoodleClient

from JDatabase import JsonDatabase
import zipfile
import os
import infos
import xdlink
import mediafire
#from megacli.mega import Mega
#import megacli.megafolder as megaf
#import megacli.mega
import datetime
import time
import youtube
import NexCloudClient

from pydownloader.downloader import Downloader
from ProxyCloud import ProxyCloud
import ProxyCloud
import socket
import S5Crypto



def downloadFile(downloader,filename,currentBits,totalBits,speed,time,args):
    try:
        bot = args[0]
        message = args[1]
        thread = args[2]
        if thread.getStore('stop'):
            downloader.stop()
        downloadingInfo = infos.createDownloading(filename,totalBits,currentBits,speed,time,tid=thread.id)
        bot.editMessageText(message,downloadingInfo)
    except Exception as ex: print(str(ex))
    pass

def uploadFile(filename,currentBits,totalBits,speed,time,args):
    try:
        bot = args[0]
        message = args[1]
        originalfile = args[2]
        thread = args[3]
        downloadingInfo = infos.createUploading(filename,totalBits,currentBits,speed,time,originalfile)
        bot.editMessageText(message,downloadingInfo)
    except Exception as ex: print(str(ex))
    pass

def processUploadFiles(filename,filesize,files,update,bot,message,thread=None,jdb=None):
    try:
        bot.editMessageText(message,'🔝𝕻𝖗𝖊𝖕𝖆𝖗𝖆𝖓𝖉𝖔 𝕻𝖆𝖗𝖆 𝕾𝖚𝖇𝖎𝖗☁...')
        evidence = None
        fileid = None
        user_info = jdb.get_user(update.message.sender.username)
        cloudtype = user_info['cloudtype']
        proxy = ProxyCloud.parse(user_info['proxy'])
        if cloudtype == 'moodle':
            client = MoodleClient(user_info['moodle_user'],
                                  user_info['moodle_password'],
                                  user_info['moodle_host'],
                                  user_info['moodle_repo_id'],
                                  proxy=proxy)
            loged = client.login()
            itererr = 0
            if loged:
                if user_info['uploadtype'] == 'evidence':
                    evidences = client.getEvidences()
                    evidname = str(filename).split('.')[0]
                    for evid in evidences:
                        if evid['name'] == evidname:
                            evidence = evid
                            break
                    if evidence is None:
                        evidence = client.createEvidence(evidname)

                originalfile = ''
                if len(files)>1:
                    originalfile = filename
                draftlist = []
                for f in files:
                    f_size = get_file_size(f)
                    resp = None
                    iter = 0
                    tokenize = False
                    if user_info['tokenize']!=0:
                       tokenize = True
                    while resp is None:
                          if user_info['uploadtype'] == 'evidence':
                             fileid,resp = client.upload_file(f,evidence,fileid,progressfunc=uploadFile,args=(bot,message,originalfile,thread),tokenize=tokenize)
                             draftlist.append(resp)
                          if user_info['uploadtype'] == 'draft':
                             fileid,resp = client.upload_file_draft(f,progressfunc=uploadFile,args=(bot,message,originalfile,thread),tokenize=tokenize)
                             draftlist.append(resp)
                          if user_info['uploadtype'] == 'blog':
                             fileid,resp = client.upload_file_blog(f,progressfunc=uploadFile,args=(bot,message,originalfile,thread),tokenize=tokenize)
                             draftlist.append(resp)
                          if user_info['uploadtype'] == 'calendario':
                             fileid,resp = client.upload_file_calendar(f,progressfunc=uploadFile,args=(bot,message,originalfile,thread),tokenize=tokenize)
                             draftlist.append(resp)
                          iter += 1
                          if iter>=10:
                              break
                    os.unlink(f)
                if user_info['uploadtype'] == 'evidence':
                    try:
                        client.saveEvidence(evidence)
                    except:pass
                return draftlist
            else:
                bot.editMessageText(message,'❌F error❌')
        elif cloudtype == 'cloud':
            tokenize = False
            if user_info['tokenize']!=0:
               tokenize = True
            bot.editMessageText(message,'🔝𝕾𝖚𝖇𝖎𝖊𝖓𝖉𝖔 ☁ 𝕰𝖘𝖕𝖊𝖗𝖊... 😄')
            host = user_info['moodle_host']
            user = user_info['moodle_user']
            passw = user_info['moodle_password']
            remotepath = user_info['dir']
            client = NexCloudClient.NexCloudClient(user,passw,host,proxy=proxy)
            loged = client.login()
            if loged:
               originalfile = ''
               if len(files)>1:
                    originalfile = filename
               filesdata = []
               for f in files:
                   data = client.upload_file(f,path=remotepath,progressfunc=uploadFile,args=(bot,message,originalfile,thread),tokenize=tokenize)
                   filesdata.append(data)
                   os.unlink(f)
               return filesdata
        return None
    except Exception as ex:
        bot.editMessageText(message,'❌𝕰𝖗𝖗𝖔𝖗❌\n' + str(ex))
        return None


def processFile(update,bot,message,file,thread=None,jdb=None):
    file_size = get_file_size(file)
    getUser = jdb.get_user(update.message.sender.username)
    max_file_size = 1024 * 1024 * getUser['zips']
    file_upload_count = 0
    client = None
    findex = 0
    if file_size > max_file_size:
        compresingInfo = infos.createCompresing(file,file_size,max_file_size)
        bot.editMessageText(message,compresingInfo)
        zipname = str(file).split('.')[0] + createID()
        mult_file = zipfile.MultiFile(zipname,max_file_size)
        zip = zipfile.ZipFile(mult_file,  mode='w', compression=zipfile.ZIP_DEFLATED)
        zip.write(file)
        zip.close()
        mult_file.close()
        client = processUploadFiles(file,file_size,mult_file.files,update,bot,message,jdb=jdb)
        try:
            os.unlink(file)
        except:pass
        file_upload_count = len(zipfile.files)
    else:
        client = processUploadFiles(file,file_size,[file],update,bot,message,jdb=jdb)
        file_upload_count = 1
    bot.editMessageText(message,'🗃𝕻𝖗𝖊𝖕𝖆𝖗𝖆𝖓𝖉𝖔 𝕬𝖗𝖈𝖍𝖎𝖛𝖔📂...')
    evidname = ''
    files = []
    if client:
        if getUser['cloudtype'] == 'moodle':
            if getUser['uploadtype'] == 'evidence':
                try:
                    evidname = str(file).split('.')[0]
                    txtname = evidname + '.txt'
                    evidences = client.getEvidences()
                    for ev in evidences:
                        if ev['name'] == evidname:
                           files = ev['files']
                           break
                        if len(ev['files'])>0:
                           findex+=1
                    client.logout()
                except:pass
            if getUser['uploadtype'] == 'draft' or getUser['uploadtype'] == 'blog' or getUser['uploadtype']=='calendario':
               for draft in client:
                   files.append({'name':draft['file'],'directurl':draft['url']})
        else:
            for data in client:
                files.append({'name':data['name'],'directurl':data['url']})
        bot.deleteMessage(message.chat.id,message.message_id)
        finishInfo = infos.createFinishUploading(file,file_size,max_file_size,file_upload_count,file_upload_count,findex)
        filesInfo = infos.createFileMsg(file,files)
        bot.sendMessage(message.chat.id,finishInfo+'\n'+filesInfo,parse_mode='html')
        if len(files)>0:
            txtname = str(file).split('/')[-1].split('.')[0] + '.txt'
            sendTxt(txtname,files,update,bot)

def ddl(update,bot,message,url,file_name='',thread=None,jdb=None):
    downloader = Downloader()
    file = downloader.download_url(url,progressfunc=downloadFile,args=(bot,message,thread))
    if not downloader.stoping:
        if file:
            processFile(update,bot,message,file,jdb=jdb)
        else:
            megadl(update,bot,message,url,file_name,thread,jdb=jdb)

def megadl(update,bot,message,megaurl,file_name='',thread=None,jdb=None):
    megadl = megacli.mega.Mega({'verbose': True})
    megadl.login()
    try:
        info = megadl.get_public_url_info(megaurl)
        file_name = info['name']
        megadl.download_url(megaurl,dest_path=None,dest_filename=file_name,progressfunc=downloadFile,args=(bot,message,thread))
        if not megadl.stoping:
            processFile(update,bot,message,file_name,thread=thread)
    except:
        files = megaf.get_files_from_folder(megaurl)
        for f in files:
            file_name = f['name']
            megadl._download_file(f['handle'],f['key'],dest_path=None,dest_filename=file_name,is_public=False,progressfunc=downloadFile,args=(bot,message,thread),f_data=f['data'])
            if not megadl.stoping:
                processFile(update,bot,message,file_name,thread=thread)
        pass
    pass

def sendTxt(name,files,update,bot):
                txt = open(name,'w')
                fi = 0
                for f in files:
                    separator = ''
                    if fi < len(files)-1:
                        separator += '\n'
                    txt.write(f['directurl']+separator)
                    fi += 1
                txt.close()
                bot.sendFile(update.message.chat.id,name)
                os.unlink(name)

def onmessage(update,bot:ObigramClient):
    try:
        thread = bot.this_thread
        username = update.message.sender.username
        tl_admin_user = os.environ.get('tl_admin_user'LizardAlex'Andi9919')

        #Descomentar debajo solo si se ba a poner el usuario admin de telegram manual
        #tl_admin_user = '*'

        jdb = JsonDatabase('database')
        jdb.check_create()
        jdb.load()

        user_info = jdb.get_user(username)

        if username == tl_admin_user or tl_admin_user=='*' or user_info :  # validate user
            if user_info is None:
                if username == tl_admin_user:
                    jdb.create_admin(username)
                else:
                    jdb.create_user(username)
                user_info = jdb.get_user(username)
                jdb.save()
        else:return


        msgText = ''
        try: msgText = update.message.text
        except:pass

        # comandos de admin
        if '/adduser' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    user = str(msgText).split(' ')[1]
                    jdb.create_user(user)
                    jdb.save()
                    msg = '😃𝕲𝖊𝖓𝖎𝖆𝖑 @'+user+' 𝖆𝖍𝖔𝖗𝖆 𝖙𝖎𝖊𝖓𝖊 𝖒𝖎 𝕮𝖔𝖓𝖙𝖗𝖔𝖑👍'
                    bot.sendMessage(update.message.chat.id,msg)
                except:
                    bot.sendMessage(update.message.chat.id,'❌𝕰𝖗𝖗𝖔𝖗 𝖊𝖓 𝖊𝖑 𝖈𝖔𝖒𝖆𝖓𝖉𝖔 /𝖆𝖉𝖉𝖚𝖘𝖊𝖗 𝖚𝖘𝖊𝖗𝖓𝖆𝖒𝖊❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌🆃🅴 🅵🅰🅻🆃🅰 🅲🅰🅻🅻🅴 🆅🅴🆃🅴❌')
            return
        if '/banuser' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    user = str(msgText).split(' ')[1]
                    if user == username:
                        bot.sendMessage(update.message.chat.id,'❌𝕹𝖔 𝕾𝖊 𝕻𝖚𝖊𝖉𝖊 𝕭𝖆𝖓𝖊𝖆𝖗 𝖀𝖘𝖙𝖊𝖉❌')
                        return
                    jdb.remove(user)
                    jdb.save()
                    msg = '🦶Fuera @'+user+' Baneado❌'
                    bot.sendMessage(update.message.chat.id,msg)
                except:
                    bot.sendMessage(update.message.chat.id,'❌𝕰𝖗𝖗𝖔𝖗 𝖊𝖓 𝖊𝖑 𝖈𝖔𝖒𝖆𝖓𝖉𝖔 /𝖇𝖆𝖓𝖚𝖘𝖊𝖗 𝖚𝖘𝖊𝖗𝖓𝖆𝖒𝖊❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌🆃🅴 🅵🅰🅻🆃🅰 🅲🅰🅻🅻🅴 🆅🅴🆃🅴❌')
            return
        if '/getdb' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                bot.sendMessage(update.message.chat.id,'Base De Datos👇')
                bot.sendFile(update.message.chat.id,'database.jdb')
            else:
                bot.sendMessage(update.message.chat.id,'❌🆃🅴 🅵🅰🅻🆃🅰 🅲🅰🅻🅻🅴 🆅🅴🆃🅴❌')
            return
        # end

        # comandos de usuario
        if '/tutorial' in msgText:
            tuto = open('tuto.txt','r')
            bot.sendMessage(update.message.chat.id,tuto.read())
            tuto.close()
            return
        if '/myuser' in msgText:
            getUser = user_info
            if getUser:
                statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                bot.sendMessage(update.message.chat.id,statInfo)
                return
        if '/zips' in msgText:
            getUser = user_info
            if getUser:
                try:
                   size = int(str(msgText).split(' ')[1])
                   getUser['zips'] = size
                   jdb.save_data_user(username,getUser)
                   jdb.save()
                   msg = '😃𝕲𝖊𝖓𝖎𝖆𝖑 𝖑𝖔𝖘 𝖟𝖎𝖕𝖘 𝖘𝖊𝖗𝖆𝖓 𝖉𝖊 '+ sizeof_fmt(size*1024*1024)+' 𝓵𝓪𝓼 𝓹𝓪𝓻𝓽𝓮𝓼👍'
                   bot.sendMessage(update.message.chat.id,msg)
                except:
                   bot.sendMessage(update.message.chat.id,'❌𝕰𝖗𝖗𝖔𝖗 𝖊𝖓 𝖊𝖑 𝖈𝖔𝖒𝖆𝖓𝖉𝖔 /𝖟𝖎𝖕𝖘 𝖘𝖎𝖟𝖊❌')
                return
        if '/account' in msgText:
            try:
                account = str(msgText).split(' ',2)[1].split(',')
                user = account[0]
                passw = account[1]
                getUser = user_info
                if getUser:
                    getUser['moodle_user'] = user
                    getUser['moodle_password'] = passw
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
            except:
                bot.sendMessage(update.message.chat.id,'❌𝕰𝖗𝖗𝖔𝖗 𝖊𝖓 𝖊𝖑 𝖈𝖔𝖒𝖆𝖓𝖉𝖔 /𝖆𝖈𝖈𝖔𝖚𝖓𝖙 𝖚𝖘𝖊𝖗,𝖕𝖆𝖘𝖘𝖜𝖔𝖗𝖉❌')
            return
        if '/host' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                host = cmd[1]
                getUser = user_info
                if getUser:
                    getUser['moodle_host'] = host
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
            except:
                bot.sendMessage(update.message.chat.id,'❌𝕰𝖗𝖗𝖔𝖗 𝖊𝖓 𝖊𝖑 𝖈𝖔𝖒𝖆𝖓𝖉𝖔 /𝖍𝖔𝖘𝖙 𝖒𝖔𝖔𝖉𝖑𝖊𝖍𝖔𝖘𝖙❌')
            return
        if '/repoid' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                repoid = int(cmd[1])
                getUser = user_info
                if getUser:
                    getUser['moodle_repo_id'] = repoid
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
            except:
                bot.sendMessage(update.message.chat.id,'❌𝕰𝖗𝖗𝖔𝖗 𝖊𝖓 𝖊𝖑 𝖈𝖔𝖒𝖆𝖓𝖉𝖔 /𝖗𝖊𝖕𝖔 𝖎𝖉❌')
            return
        if '/tokenize_on' in msgText:
            try:
                getUser = user_info
                if getUser:
                    getUser['tokenize'] = 1
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
            except:
                bot.sendMessage(update.message.chat.id,'❌𝕰𝖗𝖗𝖔𝖗 𝖊𝖓 𝖊𝖑 𝖈𝖔𝖒𝖆𝖓𝖉𝖔 /𝖙𝖔𝖐𝖊𝖓𝖎𝖟𝖊 𝖘𝖙𝖆𝖙𝖊❌')
            return
        if '/tokenize_off' in msgText:
            try:
                getUser = user_info
                if getUser:
                    getUser['tokenize'] = 0
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
            except:
                bot.sendMessage(update.message.chat.id,'❌𝕰𝖗𝖗𝖔𝖗 𝖊𝖓 𝖊𝖑 𝖈𝖔𝖒𝖆𝖓𝖉𝖔 /𝖙𝖔𝖐𝖊𝖓𝖎𝖟𝖊 𝖘𝖙𝖆𝖙𝖊❌')
            return
        if '/cloud' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                repoid = cmd[1]
                getUser = user_info
                if getUser:
                    getUser['cloudtype'] = repoid
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
            except:
                bot.sendMessage(update.message.chat.id,'❌𝕰𝖗𝖗𝖔𝖗 𝖊𝖓 𝖊𝖑 𝖈𝖔𝖒𝖆𝖓𝖉𝖔 /𝖈𝖑𝖔𝖚𝖉 (𝖒𝖔𝖔𝖉𝖑𝖊 𝖔𝖗 𝖈𝖑𝖔𝖚𝖉)❌')
            return
        if '/uptype' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                type = cmd[1]
                getUser = user_info
                if getUser:
                    getUser['uploadtype'] = type
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
            except:
                bot.sendMessage(update.message.chat.id,'❌𝕰𝖗𝖗𝖔𝖗 𝖊𝖓 𝖊𝖑 𝖈𝖔𝖒𝖆𝖓𝖉𝖔 /𝖚𝖕𝖙𝖞𝖕𝖊 (𝖙𝖞𝖕𝖔 𝖉𝖊 𝖘𝖚𝖇𝖎𝖉𝖆 (𝖊𝖛𝖎𝖉𝖊𝖓𝖈𝖊,𝖉𝖗𝖆𝖋𝖙,𝖇𝖑𝖔𝖌))❌')
            return
        if '/proxy' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                proxy = cmd[1]
                getUser = user_info
                if getUser:
                    getUser['proxy'] = proxy
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
            except:
                if user_info:
                    user_info['proxy'] = ''
                    statInfo = infos.createStat(username,user_info,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
            return
        if '/dir' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                repoid = cmd[1]
                getUser = user_info
                if getUser:
                    getUser['dir'] = repoid + '/'
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
            except:
                bot.sendMessage(update.message.chat.id,'❌𝕰𝖗𝖗𝖔𝖗 𝖊𝖓 𝖊𝖑 𝖈𝖔𝖒𝖆𝖓𝖉𝖔 /𝖉𝖎𝖗 𝖋𝖔𝖑𝖉𝖊𝖗❌')
            return
        if '/cancel_' in msgText:
            try:
                cmd = str(msgText).split('_',2)
                tid = cmd[1]
                tcancel = bot.threads[tid]
                msg = tcancel.getStore('msg')
                tcancel.store('stop',True)
                time.sleep(3)
                bot.editMessageText(msg,'❌𝕬𝖈𝖈𝖎𝖔𝖓 𝕮𝖆𝖓𝖈𝖊𝖑𝖆𝖉𝖆❌')
            except Exception as ex:
                print(str(ex))
            return
        #end

        message = bot.sendMessage(update.message.chat.id,'🕰𝕻𝖗𝖔𝖈𝖊𝖘𝖆𝖓𝖉𝖔🕰...')

        thread.store('msg',message)

        if '/start' in msgText:
            start_msg = 'Bot          : 𝕿𝕲𝖀𝖕𝖑𝖔𝖆𝖉𝖊𝖗𝕻𝖗𝖔 𝖛15.0 𝕱𝖎𝖝𝖊𝖉\n'
            start_msg+= 'Desarrollador: @𝓐𝓷𝓭𝓲9919\n'
            start_msg+= 'Api          : 𝓐𝓷𝓭𝓲\n'
            start_msg+= 'Uso          : 𝕭𝖚𝖊𝖓𝖔 𝖆 𝖑𝖔 𝖖𝖚𝖊 𝖛𝖎𝖓𝖎𝖒𝖔𝖘 🫡  , 𝖁𝖊𝖆 𝕰𝖑 /𝖙𝖚𝖙𝖔𝖗𝖎𝖆𝖑)\n'
            bot.editMessageText(message,start_msg)
        elif '/files' == msgText and user_info['cloudtype']=='moodle':
             proxy = ProxyCloud.parse(user_info['proxy'])
             client = MoodleClient(user_info['moodle_user'],
                                   user_info['moodle_password'],
                                   user_info['moodle_host'],
                                   user_info['moodle_repo_id'],proxy=proxy)
             loged = client.login()
             if loged:
                 files = client.getEvidences()
                 filesInfo = infos.createFilesMsg(files)
                 bot.editMessageText(message,filesInfo)
                 client.logout()
             else:
                bot.editMessageText(message,'❌𝕰𝖗𝖗𝖔𝖗 𝖞 𝕮𝖆𝖚𝖘𝖆𝖘🧐\n1-𝕽𝖊𝖛𝖎𝖘𝖊 𝖘𝖚 𝕮𝖚𝖊𝖓𝖙𝖆\n2-𝕾𝖊𝖗𝖛𝖎𝖉𝖔𝖗 𝕯𝖊𝖘𝖆𝖇𝖎𝖑𝖎𝖙𝖆𝖉𝖔: '+client.path)
        elif '/txt_' in msgText and user_info['cloudtype']=='moodle':
             findex = str(msgText).split('_')[1]
             findex = int(findex)
             proxy = ProxyCloud.parse(user_info['proxy'])
             client = MoodleClient(user_info['moodle_user'],
                                   user_info['moodle_password'],
                                   user_info['moodle_host'],
                                   user_info['moodle_repo_id'],proxy=proxy)
             loged = client.login()
             if loged:
                 evidences = client.getEvidences()
                 evindex = evidences[findex]
                 txtname = evindex['name']+'.txt'
                 sendTxt(txtname,evindex['files'],update,bot)
                 client.logout()
                 bot.editMessageText(message,'TxT Aqui👇')
             else:
                bot.editMessageText(message,'❌𝕰𝖗𝖗𝖔𝖗 𝖞 𝕮𝖆𝖚𝖘𝖆𝖘🧐\n1-𝕽𝖊𝖛𝖎𝖘𝖊 𝖘𝖚 𝕮𝖚𝖊𝖓𝖙𝖆\n2-𝕾𝖊𝖗𝖛𝖎𝖉𝖔𝖗 𝕯𝖊𝖘𝖆𝖇𝖎𝖑𝖎𝖙𝖆𝖉𝖔: '+client.path)
             pass
        elif '/del_' in msgText and user_info['cloudtype']=='moodle':
            findex = int(str(msgText).split('_')[1])
            proxy = ProxyCloud.parse(user_info['proxy'])
            client = MoodleClient(user_info['moodle_user'],
                                   user_info['moodle_password'],
                                   user_info['moodle_host'],
                                   user_info['moodle_repo_id'],
                                   proxy=proxy)
            loged = client.login()
            if loged:
                evfile = client.getEvidences()[findex]
                client.deleteEvidence(evfile)
                client.logout()
                bot.editMessageText(message,'𝕬𝖗𝖈𝖍𝖎𝖛𝖔 𝕭𝖔𝖗𝖗𝖆𝖉𝖔 🦶')
            else:
                bot.editMessageText(message,'❌𝕰𝖗𝖗𝖔𝖗 𝖞 𝕮𝖆𝖚𝖘𝖆𝖘🧐\n1-𝕽𝖊𝖛𝖎𝖘𝖊 𝖘𝖚 𝕮𝖚𝖊𝖓𝖙𝖆\n2-𝕾𝖊𝖗𝖛𝖎𝖉𝖔𝖗 𝕯𝖊𝖘𝖆𝖇𝖎𝖑𝖎𝖙𝖆𝖉𝖔: '+client.path)
        elif '/delall' in msgText and user_info['cloudtype']=='moodle':
            proxy = ProxyCloud.parse(user_info['proxy'])
            client = MoodleClient(user_info['moodle_user'],
                                   user_info['moodle_password'],
                                   user_info['moodle_host'],
                                   user_info['moodle_repo_id'],
                                   proxy=proxy)
            loged = client.login()
            if loged:
                evfiles = client.getEvidences()
                for item in evfiles:
                	client.deleteEvidence(item)
                client.logout()
                bot.editMessageText(message,'𝕬𝖗𝖈𝖍𝖎𝖛𝖔 𝕭𝖔𝖗𝖗𝖆𝖉𝖔 🦶')
            else:
                bot.editMessageText(message,'❌𝕰𝖗𝖗𝖔𝖗 𝖞 𝕮𝖆𝖚𝖘𝖆𝖘🧐\n1-𝕽𝖊𝖛𝖎𝖘𝖊 𝖘𝖚 𝕮𝖚𝖊𝖓𝖙𝖆\n2-𝕾𝖊𝖗𝖛𝖎𝖉𝖔𝖗 𝕯𝖊𝖘𝖆𝖇𝖎𝖑𝖎𝖙𝖆𝖉𝖔 '+client.path)       
        elif 'http' in msgText:
            url = msgText
            ddl(update,bot,message,url,file_name='',thread=thread,jdb=jdb)
        else:
            bot.editMessageText(message,'😵𝕴𝖓𝖛𝖆𝖑𝖎𝖉𝖔😵')
    except Exception as ex:
           print(str(ex))


def main():
    bot_token = os.environ.get('bot_token')

    #decomentar abajo y modificar solo si se va a poner el token del bot manual
    #bot_token = 'BOT TOKEN'

    bot = ObigramClient(bot_token)
    bot.onMessage(onmessage)
    bot.run()

if __name__ == '__main__':
    try:
        main()
    except:
        main()
