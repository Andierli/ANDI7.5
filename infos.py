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
			if porcent >= index_make * 5: make_text+='β'
			else: make_text+='β'
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
    msg = 'π₯π―ππππππππππ... \n\n'
    msg+= 'ππΉπππππ: ' + str(filename)+'\n'
    msg+= 'ππΏπππΓ±π πΏππππ: ' + str(sizeof_fmt(totalBits))+'\n'
    msg+= 'ππ―πππππππππ: ' + str(sizeof_fmt(currentBits))+'\n'
    msg+= 'πΆπππππππππ: ' + str(sizeof_fmt(speed))+'/s\n'
    msg+= 'ππΏπππππ: ' + str(datetime.timedelta(seconds=int(time))) +'\n\n'

    msg = 'π₯ π―ππππππππππ π¬ππππππ....\n\n'
    msg += 'π π¬ππππππ: '+filename+'\n'
    msg += text_progres(currentBits,totalBits)+'\n'
    msg += 'π π»πππππππππ: '+str(porcent(currentBits,totalBits))+'%\n\n'
    msg += 'π πΏππππ: '+sizeof_fmt(totalBits)+'\n\n'
    msg += 'π π―πππππππππ: '+sizeof_fmt(currentBits)+'\n\n'
    msg += 'π πππππππππ: '+sizeof_fmt(speed)+'/s\n\n'
    msg += 'π πΏπππππ ππ π―πππππππ: '+str(datetime.timedelta(seconds=int(time)))+'s\n\n'

    if tid!='':
        msg+= '/cancel_' + tid
    return msg
def createUploading(filename,totalBits,currentBits,speed,time,originalname=''):
    msg = 'β«πΎπππππππ π¬ π·π πΉπππβ... \n\n'
    msg+= 'ππΉπππππ: ' + str(filename)+'\n'
    if originalname!='':
        msg = str(msg).replace(filename,originalname)
        msg+= 'β«πΎπππππππ: ' + str(filename)+'\n'
    msg+= 'ππΏπππΓ±π πΏππππ: ' + str(sizeof_fmt(totalBits))+'\n'
    msg+= 'ππΎπππππ: ' + str(sizeof_fmt(currentBits))+'\n'
    msg+= 'πΆπππππππππ: ' + str(sizeof_fmt(speed))+'/s\n'
    msg+= 'ππΏπππππ: ' + str(datetime.timedelta(seconds=int(time))) +'\n'

    msg = 'β« πΎπππππππ π¬ π·π πΉπππβ...\n\n'
    msg += 'π πΉπππππ: '+filename+'\n'
    if originalname!='':
        msg = str(msg).replace(filename,originalname)
        msg+= 'π πΉπππππ: ' + str(filename)+'\n'
    msg += text_progres(currentBits,totalBits)+'\n'
    msg += 'π π»πππππππππ: '+str(porcent(currentBits,totalBits))+'%\n\n'
    msg += 'π πΏππππ: '+sizeof_fmt(totalBits)+'\n\n'
    msg += 'π π―πππππππππ: '+sizeof_fmt(currentBits)+'\n\n'
    msg += 'π πππππππππ: '+sizeof_fmt(speed)+'/s\n\n'
    msg += 'π πΏπππππ ππ π―πππππππ: '+str(datetime.timedelta(seconds=int(time)))+'s\n\n'

    return msg
def createCompresing(filename,filesize,splitsize):
    msg = 'ππ?πππππππππππ... \n\n'
    msg+= 'ππΉπππππ: ' + str(filename)+'\n'
    msg+= 'ππΏπππΓ±π πΏππππ: ' + str(sizeof_fmt(filesize))+'\n'
    msg+= 'ππΏπππΓ±π π»πππππ: ' + str(sizeof_fmt(splitsize))+'\n'
    msg+= 'πΎπ?πππππππ π»πππππ: ' + str(round(int(filesize/splitsize)+1,1))+'\n\n'
    return msg
def createFinishUploading(filename,filesize,split_size,current,count,findex):
    msg = 'βοΈπ»ππππππ π±πππππππππβοΈ\n\n'
    msg+= 'ππΉπππππ: ' + str(filename)+'\n'
    msg+= 'ππΏπππΓ±π πΏππππ: ' + str(sizeof_fmt(filesize))+'\n'
    msg+= 'ππΏπππΓ±π π»πππππ: ' + str(sizeof_fmt(split_size))+'\n'
    msg+= 'π€π»πππππ πΎππππππ: ' + str(current) + '/' + str(count) +'\n\n'
    msg+= 'ππ­πππππ π¬ππππππ: ' + '/del_'+str(findex)
    return msg

def createFileMsg(filename,files):
    import urllib
    if len(files)>0:
        msg= '<b>πEnlacesπ</b>\n'
        for f in files:
            url = urllib.parse.unquote(f['directurl'],encoding='utf-8', errors='replace')
            #msg+= '<a href="'+f['url']+'">π' + f['name'] + 'π</a>'
            msg+= "<a href='"+url+"'>π"+f['name']+'π</a>\n'
        return msg
    return ''

def createFilesMsg(evfiles):
    msg = 'ππ¬πππππππ ('+str(len(evfiles))+')π\n\n'
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
    msg = 'βοΈπ?ππππππππππππππ π―π πππππππβοΈ\n\n'
    msg+= 'ππΉπππππ: @' + str(username)+'\n'
    msg+= 'πππππ: ' + str(userdata['moodle_user'])+'\n'
    msg+= 'π³π»πππππππ: ' + str(userdata['moodle_password'])+'\n'
    msg+= 'π‘π³πππ: ' + str(userdata['moodle_host'])+'\n'
    if userdata['cloudtype'] == 'moodle':
        msg+= 'π·π½ππππ΄π―: ' + str(userdata['moodle_repo_id'])+'\n'
    msg+= 'π·π?πππππΏπππ: ' + str(userdata['cloudtype'])+'\n'
    msg+= 'πππtyππ: ' + str(userdata['uploadtype'])+'\n'
    if userdata['cloudtype'] == 'cloud':
        msg+= 'ππ―ππ: /' + str(userdata['dir'])+'\n'
    msg+= 'ππΏπππΓ±π ππ ππππ : ' + sizeof_fmt(userdata['zips']*1024*1024) + '\n\n'
    msgAdmin = 'πΉπ'
    if isadmin:
        msgAdmin = 'πΎπ'
    msg+= 'π¦Ύπ¬ππππ : ' + msgAdmin + '\n'
    proxy = 'πΉπΊ'
    if userdata['proxy'] !='':
       proxy = 'πΎπ'
    tokenize = 'πΉπΊ'
    if userdata['tokenize']!=0:
       tokenize = 'πΎπ'
    msg+= 'ππππππ : ' + proxy + '\n'
    msg+= 'π?πΏπππππππ : ' + tokenize + '\n\n'
    msg+= 'βοΈπ?πππππππππ πΈπππππβοΈ\nπ€π°ππππππ /ππππ πππππ://ππππ.ππ.ππ/π'
    return msg