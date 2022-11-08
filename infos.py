from pyobigram.utils import sizeof_fmt,nice_time
import datetime
import time
import os

def text_progres(index,max):
	try:
		if max<1:
			max += 1
		porcent = index / max
		porcent *= 100
		porcent = round(porcent)
		make_text = ''
		index_make = 1
		make_text += '\n['
		while(index_make<21):
			if porcent >= index_make * 5: make_text+='█'
			else: make_text+='░'
			index_make+=1
		make_text += ']\n'
		return make_text
	except Exception as ex:
			return ''

def porcent(index,max):
    porcent = index / max
    porcent *= 100
    porcent = round(porcent)
    return porcent

def createDownloading(filename,totalBits,currentBits,speed,time,tid=''):
    msg = '📥𝕯𝖊𝖘𝖈𝖆𝖗𝖌𝖆𝖓𝖉𝖔... \n\n'
    msg+= '🔖𝕹𝖔𝖒𝖇𝖗𝖊: ' + str(filename)+'\n'
    msg+= '🗂𝕿𝖆𝖒𝖆ñ𝖔 𝕿𝖔𝖙𝖆𝖑: ' + str(sizeof_fmt(totalBits))+'\n'
    msg+= '🗂𝕯𝖊𝖘𝖈𝖆𝖗𝖌𝖆𝖉𝖔: ' + str(sizeof_fmt(currentBits))+'\n'
    msg+= '📶𝖛𝖊𝖑𝖔𝖈𝖎𝖉𝖆𝖉: ' + str(sizeof_fmt(speed))+'/s\n'
    msg+= '🕐𝕿𝖎𝖊𝖒𝖕𝖔: ' + str(datetime.timedelta(seconds=int(time))) +'\n\n'

    msg = '📥 𝕯𝖊𝖘𝖈𝖆𝖗𝖌𝖆𝖓𝖉𝖔 𝕬𝖗𝖈𝖍𝖎𝖛𝖔....\n\n'
    msg += '🔛 𝕬𝖗𝖈𝖍𝖎𝖛𝖔: '+filename+'\n'
    msg += text_progres(currentBits,totalBits)+'\n'
    msg += '🔛 𝕻𝖔𝖗𝖈𝖊𝖓𝖙𝖆𝖏𝖊: '+str(porcent(currentBits,totalBits))+'%\n\n'
    msg += '🔛 𝕿𝖔𝖙𝖆𝖑: '+sizeof_fmt(totalBits)+'\n\n'
    msg += '🔛 𝕯𝖊𝖘𝖈𝖆𝖗𝖌𝖆𝖉𝖔: '+sizeof_fmt(currentBits)+'\n\n'
    msg += '🔛 𝖛𝖊𝖑𝖔𝖈𝖎𝖉𝖆𝖉: '+sizeof_fmt(speed)+'/s\n\n'
    msg += '🔛 𝕿𝖎𝖊𝖒𝖕𝖔 𝖉𝖊 𝕯𝖊𝖘𝖈𝖆𝖗𝖌𝖆: '+str(datetime.timedelta(seconds=int(time)))+'s\n\n'

    if tid!='':
        msg+= '/cancel_' + tid
    return msg
def createUploading(filename,totalBits,currentBits,speed,time,originalname=''):
    msg = '⏫𝕾𝖚𝖇𝖎𝖊𝖓𝖉𝖔 𝕬 𝕷𝖆 𝕹𝖚𝖇𝖊☁... \n\n'
    msg+= '🔖𝕹𝖔𝖒𝖇𝖗𝖊: ' + str(filename)+'\n'
    if originalname!='':
        msg = str(msg).replace(filename,originalname)
        msg+= '⏫𝕾𝖚𝖇𝖎𝖊𝖓𝖉𝖔: ' + str(filename)+'\n'
    msg+= '🗂𝕿𝖆𝖒𝖆ñ𝖔 𝕿𝖔𝖙𝖆𝖑: ' + str(sizeof_fmt(totalBits))+'\n'
    msg+= '🗂𝕾𝖚𝖇𝖎𝖉𝖔: ' + str(sizeof_fmt(currentBits))+'\n'
    msg+= '📶𝖛𝖊𝖑𝖔𝖈𝖎𝖉𝖆𝖉: ' + str(sizeof_fmt(speed))+'/s\n'
    msg+= '🕐𝕿𝖎𝖊𝖒𝖕𝖔: ' + str(datetime.timedelta(seconds=int(time))) +'\n'

    msg = '⏫ 𝕾𝖚𝖇𝖎𝖊𝖓𝖉𝖔 𝕬 𝕷𝖆 𝕹𝖚𝖇𝖊☁...\n\n'
    msg += '🔛 𝕹𝖔𝖒𝖇𝖗𝖊: '+filename+'\n'
    if originalname!='':
        msg = str(msg).replace(filename,originalname)
        msg+= '🔛 𝕹𝖔𝖒𝖇𝖗𝖊: ' + str(filename)+'\n'
    msg += text_progres(currentBits,totalBits)+'\n'
    msg += '🔛 𝕻𝖔𝖗𝖈𝖊𝖓𝖙𝖆𝖏𝖊: '+str(porcent(currentBits,totalBits))+'%\n\n'
    msg += '🔛 𝕿𝖔𝖙𝖆𝖑: '+sizeof_fmt(totalBits)+'\n\n'
    msg += '🔛 𝕯𝖊𝖘𝖈𝖆𝖗𝖌𝖆𝖉𝖔: '+sizeof_fmt(currentBits)+'\n\n'
    msg += '🔛 𝖛𝖊𝖑𝖔𝖈𝖎𝖉𝖆𝖉: '+sizeof_fmt(speed)+'/s\n\n'
    msg += '🔛 𝕿𝖎𝖊𝖒𝖕𝖔 𝖉𝖊 𝕯𝖊𝖘𝖈𝖆𝖗𝖌𝖆: '+str(datetime.timedelta(seconds=int(time)))+'s\n\n'

    return msg
def createCompresing(filename,filesize,splitsize):
    msg = '📚𝕮𝖔𝖒𝖕𝖗𝖎𝖒𝖎𝖊𝖓𝖉𝖔... \n\n'
    msg+= '🔖𝕹𝖔𝖒𝖇𝖗𝖊: ' + str(filename)+'\n'
    msg+= '🗂𝕿𝖆𝖒𝖆ñ𝖔 𝕿𝖔𝖙𝖆𝖑: ' + str(sizeof_fmt(filesize))+'\n'
    msg+= '📂𝕿𝖆𝖒𝖆ñ𝖔 𝕻𝖆𝖗𝖙𝖊𝖘: ' + str(sizeof_fmt(splitsize))+'\n'
    msg+= '💾𝕮𝖆𝖓𝖙𝖎𝖉𝖆𝖉 𝕻𝖆𝖗𝖙𝖊𝖘: ' + str(round(int(filesize/splitsize)+1,1))+'\n\n'
    return msg
def createFinishUploading(filename,filesize,split_size,current,count,findex):
    msg = '⚜️𝕻𝖗𝖔𝖈𝖊𝖘𝖔 𝕱𝖎𝖓𝖆𝖑𝖎𝖟𝖆𝖉𝖔⚜️\n\n'
    msg+= '🔖𝕹𝖔𝖒𝖇𝖗𝖊: ' + str(filename)+'\n'
    msg+= '🗂𝕿𝖆𝖒𝖆ñ𝖔 𝕿𝖔𝖙𝖆𝖑: ' + str(sizeof_fmt(filesize))+'\n'
    msg+= '📂𝕿𝖆𝖒𝖆ñ𝖔 𝕻𝖆𝖗𝖙𝖊𝖘: ' + str(sizeof_fmt(split_size))+'\n'
    msg+= '📤𝕻𝖆𝖗𝖙𝖊𝖘 𝕾𝖚𝖇𝖎𝖉𝖆𝖘: ' + str(current) + '/' + str(count) +'\n\n'
    msg+= '🗑𝕭𝖔𝖗𝖗𝖆𝖗 𝕬𝖗𝖈𝖍𝖎𝖛𝖔: ' + '/del_'+str(findex)
    return msg

def createFileMsg(filename,files):
    import urllib
    if len(files)>0:
        msg= '<b>🖇Enlaces🖇</b>\n'
        for f in files:
            url = urllib.parse.unquote(f['directurl'],encoding='utf-8', errors='replace')
            #msg+= '<a href="'+f['url']+'">🔗' + f['name'] + '🔗</a>'
            msg+= "<a href='"+url+"'>🔗"+f['name']+'🔗</a>\n'
        return msg
    return ''

def createFilesMsg(evfiles):
    msg = '📑𝕬𝖗𝖈𝖍𝖎𝖛𝖔𝖘 ('+str(len(evfiles))+')📑\n\n'
    i = 0
    for f in evfiles:
            try:
                fextarray = str(f['files'][0]['name']).split('.')
                fext = ''
                if len(fextarray)>=3:
                    fext = '.'+fextarray[-2]
                else:
                    fext = '.'+fextarray[-1]
                fname = f['name'] + fext
                msg+= '/txt_'+ str(i) + ' /del_'+ str(i) + '\n' + fname +'\n\n'
                i+=1
            except:pass
    return msg
def createStat(username,userdata,isadmin):
    from pyobigram.utils import sizeof_fmt
    msg = '⚙️𝕮𝖔𝖓𝖉𝖎𝖌𝖚𝖗𝖆𝖈𝖎𝖔𝖓𝖊𝖘 𝕯𝖊 𝖀𝖘𝖚𝖆𝖗𝖎𝖔⚙️\n\n'
    msg+= '🔖𝕹𝖔𝖒𝖇𝖗𝖊: @' + str(username)+'\n'
    msg+= '📑𝖀𝖘𝖊𝖗: ' + str(userdata['moodle_user'])+'\n'
    msg+= '🗳𝕻𝖆𝖘𝖘𝖜𝖔𝖗𝖉: ' + str(userdata['moodle_password'])+'\n'
    msg+= '📡𝕳𝖔𝖘𝖙: ' + str(userdata['moodle_host'])+'\n'
    if userdata['cloudtype'] == 'moodle':
        msg+= '🏷𝕽𝖊𝖕𝖔𝕴𝕯: ' + str(userdata['moodle_repo_id'])+'\n'
    msg+= '🏷𝕮𝖑𝖔𝖚𝖉𝕿𝖞𝖕𝖊: ' + str(userdata['cloudtype'])+'\n'
    msg+= '📟𝖀𝖕ty𝖕𝖊: ' + str(userdata['uploadtype'])+'\n'
    if userdata['cloudtype'] == 'cloud':
        msg+= '🗂𝕯𝖎𝖗: /' + str(userdata['dir'])+'\n'
    msg+= '📚𝕿𝖆𝖒𝖆ñ𝖔 𝖉𝖊 𝖅𝖎𝖕𝖘 : ' + sizeof_fmt(userdata['zips']*1024*1024) + '\n\n'
    msgAdmin = '𝕹𝖔'
    if isadmin:
        msgAdmin = '𝕾𝖎'
    msg+= '🦾𝕬𝖉𝖒𝖎𝖓 : ' + msgAdmin + '\n'
    proxy = '𝕹𝕺'
    if userdata['proxy'] !='':
       proxy = '𝕾𝖎'
    tokenize = '𝕹𝕺'
    if userdata['tokenize']!=0:
       tokenize = '𝕾𝖎'
    msg+= '🔌𝖕𝖗𝖔𝖝𝔂 : ' + proxy + '\n'
    msg+= '🔮𝕿𝖔𝖐𝖊𝖓𝖎𝖟𝖊 : ' + tokenize + '\n\n'
    msg+= '⚙️𝕮𝖔𝖓𝖋𝖎𝖌𝖚𝖗𝖆𝖗 𝕸𝖔𝖔𝖉𝖑𝖊⚙️\n🤜𝕰𝖏𝖊𝖒𝖕𝖑𝖔 /𝖍𝖔𝖘𝖙 𝖍𝖙𝖙𝖕𝖘://𝖊𝖛𝖊𝖆.𝖚𝖍.𝖈𝖚/👀'
    return msg