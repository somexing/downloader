#coding:utf-8  #must be line 1
#  2016/12 python2
# 多线程发送 ajax 搜索到10个视频 token和vid
#每个视频发送getMore Ajax请求媒体的tag（137）和扩展名。根据v，t，tag计算link
# cookie需要当日从浏览器访问该网站更新一下，否则会返回204 508。。。。
#文件名vtitle含有gb2312无法编码的，18030才能编码的，显示是？，但是无法被替换，就忽略掉才能对比
#文件名"|!:改为_ ?去掉空格比较文件名。下载的url转义过的文件名写文件中是这样的
#制定下载22tag是带音频的，文件名带720P。137只是1080p视频

import requests
import sys,urllib,re,threading , Queue ,time, json, os
reload(sys) 
sys.setdefaultencoding('gb18030') #for UnicodeDecodeError: 'ascii' codec can't decode byte 0xa1 in position 0: ordinal not in range(128)

USE_PROXY = 0     #home use   


CHECK_FILE_EXIST_FLAG = True  # 检查文件是否已经在目录和目录列表（下面定义）
OTHER_DOWN_FILE_DIR = ["H:\\youtube\\"]  #other for check
#host = "www.converdio.com"
#host = 'downloads99.com'
#host = "loreleikoren.com"
#host = "mvlse.org"

host = 'mp3alpha.com'
host = 'mytubeconverter.com'
host = "mytube.az"
host = "mp3play.org"

 
#keyWord="Apple (UCE_M8A5yxnLfW0KghEeajjw)"
 

 
DOWN_FILE_DIR = "H:\youtube"
#0 不指定下载格式,默认按后面顺序/137 1080p光视频 /136 720光视频/22下载720p视频音频/
itagToDOWN = 0  #不指定0的情况下，如果指定格式没找到，才会返回第一个数字的mp4
DROP_LOW_RES = True  # 是否丢弃低于720p

strMonDate = time.strftime("%m%d",time.localtime())
LINK_FILE_NAME =  keyWord +"_"+ host+strMonDate+"_link.txt"
 
 
#corp use
#DOWN_FILE_DIR = "f:/Download" #for judge if file existed
#USE_PROXY = 1     #是否使用代理

USE_PROXYFILE = 0  #是否使用代理列表文件读出多个代理扫描
PROXY_SERVER = {"http":" : "} #固定代理 ，USE_PROXYFILE =0启用
bRunMT = True  #false sing thread run
MAXTHREADS_NUM = 10

MAX_TRYCONNECT_NUM = 15  #重新请求网络次数 request max times
TIME_OUT_VALUE     = 20  #网络超时时间
FILE_EXIST_FLAG ="!!!"   # 在 DOWN_FILE_DIR找到同名文件则前面加上这个标志记录


URL  = "http://"+ host
Request_URL =  URL +"/ajax"	
keyWordURL = URL +'/'+ urllib.quote(keyWord)
PageNum  = 0 


#unit test define
UNIT_TEST = 0  #1will test
test_keyWord='x' 
test_id= "szKxAdvlCCM"
test_title= "21 Savage & Metro Boomin - X ft Future (Official Audio)"
test_token="FABE-B0E5-B09D-51B2-4931-F938-B117-8CF0"
test_downloadlink ="http://youtubemp3.scriptscraft.com/download/FABEB0E5-B09D51B2-4931F938-B1178CF0-737A4B78-4164766C-43434D00-00000089/21+Savage+%26+Metro+Boomin+-+X+ft+Future+(Official+Audio)%20-%20(youtubemp3.scriptscraft.com)%201080p.mp4"

linesWrited = 0

RequestDefaulHeader = {                
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip,deflate', #Exception :'utf8' codec can't decode byte 0x8b in position 1: invalid start byte
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection':'keep-alive',
       	'Host':host,
        'Origin':URL,
        'Cookie':'PHPSESSID=2uahdsiq1hd10k5r3p7bfbuo73; __atuvc=1%7C32%2C1%7C33; __atuvs=57b807c13331561e000; _ga=GA1.2.2099785564.1471678404; noadvtday=0;'+
                 "searchTerm="+urllib.quote(keyWord),
   	    'X-Requested-With':'XMLHttpRequest',
        'Refer':keyWordURL
        }


def sendSearchAjax(directAction):
    global PageNum  
    PageNum = PageNum + 1   
    print("search %s %s-%s\n "%(keyWordURL, PageNum*10-9,  PageNum*10 ))
    thisHeader =  RequestDefaulHeader
    #thisHeader['Refer'] = keyWordURL
    if (directAction is None):
      thisData = {"query":keyWord,  "purpose":"search"}
    else  :
      thisData = {"query":directAction,  "purpose":"search"}
    thisHeader['Content-Length'] = str(len(thisData))
    for i in range( MAX_TRYCONNECT_NUM ):                   
      try:      
          if USE_PROXY == 1:
            r = requests.post(Request_URL, proxies = PROXY_SERVER, timeout=TIME_OUT_VALUE , headers= thisHeader, data=thisData)    
            # thisHeader['Proxy-Connection'] = 'keep-alive '
          else:
            r =  requests.post(Request_URL,timeout=TIME_OUT_VALUE , headers= thisHeader, data=thisData)                      
          if r.status_code != 200 : #and resp.status != 302:           
            print ("status_code:%s   pageNum %s, return value:"%( r.status_code,   PageNum))  
     
            continue
          ##print(r.text)
          jsn = json.loads(r.text) 

          return jsn
      except Exception, e:       
          print (" sendSearchAjax Exception :%s PageNum %s , try times %s"%(str(e), PageNum, i+1))                         
          continue 
    print (" sendSearchAjax Failed :  PageNum %s , try times %s"%(   PageNum, MAX_TRYCONNECT_NUM))                         
    return None


def sendgetMoreAjax(v, t):
    
    thisHeader =  RequestDefaulHeader
    #thisHeader['Refer'] = keyWordURL
   
    thisData = {"v":v, "t":t,  "purpose":"getMore"}
    thisHeader['Content-Length'] = str(len(thisData)) 
    for i in range( MAX_TRYCONNECT_NUM ):                   
        try:      
          if USE_PROXY == 1:
            r = requests.post(Request_URL, proxies = PROXY_SERVER, timeout=TIME_OUT_VALUE , headers= thisHeader, data=thisData)   
            # thisHeader['Proxy-Connection'] = 'keep-alive '
          else:
            r =  requests.post(Request_URL,timeout=TIME_OUT_VALUE , headers= thisHeader, data=thisData)                      
          if r.status_code != 200 : #and resp.status != 302:           
            print ("status_code:%s    v %s , retrun value:"%( r.status_code,   v))  
            return None
          ##print(r.text)
          jsn = json.loads(r.text) 

          #print jsn
          return jsn    
        except Exception, e:       
          print ("sendgetMoreAjax Exception :%s v: %s . try times %s"%(str(e), v, i+1))                         
          continue
    print ("sendgetMoreAjax Failed :  v: %s . try times %s"%(  v, MAX_TRYCONNECT_NUM))  
    return None
           

def getMediaInfo(v, t):
    jsn = sendgetMoreAjax(v, t)
    if (jsn is None ):
       return ["",0]
    try: 
        if (jsn["status"] is False ):
           print("getMediaInfo get json  status is False") 
           print jsn
           return ["",0]   
    except Exception, e:       
        print ("getMediaInfo Exception :%s v %s, print json object:  "%(str(e), v))  
        print jsn           

    try: 
        itagFound = 0
        extension =  ""
        for eachLink in jsn["links"]:
           extension = eachLink["extension"]
           if (cmp(extension, "mp4") !=0):
             continue;
           vtype = eachLink["type"]
           if (cmp(vtype, "video") !=0):
             continue;
           itag = eachLink["itag"]
           if (itagFound ==  0 and itag > 0):
              itagFound = itag
           if (itagToDOWN != 0 ):  # indicate to down video with sound (22)
              if (itag != itagToDOWN ):
                 continue
           return [extension,  itag ] #found mp4 video        
    except Exception, e:       
        print ("getMediaInfo Exception :%s v %s, print json object:  "%(str(e), v))  
        print jsn
    #if itagToDOWN  not indicate, found the first video type tag returned
    if (itagToDOWN == 0 and itagFound > 0  and extension != ""): 
       return [extension,  itagFound ]

    return ["",0] 
    


    
def getDownLink(video, vToken,   vTitle ,vExtension, mediaTAG):
    #print(video, vToken,   vTitle,vExtension, mediaTAG)
    vToken = vToken.replace('-', '')
    try: 
      #vTitle = vTitle.replace('/', '')
      vTitle = vTitle.encode('gb2312', 'ignore');#UnicodeEncodeError: 'gbk' codec can't encode character u'\u30fb' in position    
      #downloadName = urllib.quote_plus(vTitle.encode('gb18030'))      #encodeURIComponent    
      downloadName = urllib.quote_plus(vTitle)      #encodeURIComponent    
      #downloadName = downloadName.replace("%20", '+')   #%20 will stop xunlei download
    except  Exception, e:       
        print ("getDownLink quote_plus Exception :%s vTitle %s    "%(str(e), vTitle))  
    
    if (mediaTAG == 137):
      tagName = '+1080p'   # 1080p=137 720p=136 space to + xunlei will ignore the blank
    elif (mediaTAG == 136):  
      tagName = '+720p'    # 1080p=137 720p=136 only video streams
    elif (mediaTAG == 22):  
      tagName = '+720P'    #   720p=136 videos
    else:
      tagName = '+lowP'  

    #downloadName += ' - (' + host + ')' +tagName+'.' + vExtension           
    #downloadName += tagName+'.' + vExtension       

    #itagHEX = hex(mediaTAG)[2:];
    #itagHEX = new Array((4 - itagHEX.length) + 1).join('0') + itagHEX; #js code
    #if (mediaTAG == 137):   
    #   itagHEX = "0089"  #4 bit, to Hex
    #elif (mediaTAG == 136):
    #   itagHEX = "0088"  #4 bit, to Hex
    itagHEX = "00"+hex(mediaTAG)[2:]  #int -> hex -> string 89,88,16(22)

    #downloadToken = (vToken + library.asciiHEX(video + '\x00\x00\x00') + itagHEX).match(/.{8}/g).join('-'); #js code
    videoASCIItoHEX = "".join("{:02X}".format(ord(c)) for c in video)
    downloadToken = vToken + videoASCIItoHEX +"000000"+ itagHEX
    b=re.findall(r'.{8}',downloadToken) 
    c='-'.join(b)            
    downloadLink = URL + '/download/' + c + '/' + downloadName+ tagName+'.' + vExtension     

    if (not CHECK_FILE_EXIST_FLAG):
        return downloadLink
     
    #vTitle = vTitle[:len(vTitle)-6]  #ignore right 6 char for ?,中文
    errorchar=['*','!','"',':','|','/']  
    for thechar in errorchar:
       vTitle = vTitle.replace(thechar, '_')
    vTitle = vTitle.replace('?', '') #ending
    vTitle = vTitle.strip()
    #for the downloaded filename replace ! with _

   
    
    fileList = os.listdir(DOWN_FILE_DIR)
    for file in fileList:
      if (vTitle in file):        
        print("!!!   file existed !!! %s\n"% (vTitle.encode("gb18030")))
        return None #FILE_EXIST_FLAG + downloadLink

   
 
    for other_DIR in OTHER_DOWN_FILE_DIR:
      fileList_ = os.listdir(other_DIR)
      for file in fileList_:
        if (vTitle in file):
          print("!!!   file existed !!! %s\n"% (vTitle.encode("gb18030")))
          return None #FILE_EXIST_FLAG + downloadLink
    	  
  
    return downloadLink


   
class MT(object):
    def __init__(self, func, argsVector, MAXTHREADS, queue_results=True):
                self._func = func
                self._lock = threading.Lock()
                #self._Arg0 = arg0
                self._nextArgs = iter(argsVector).next

                self._threadPool = [ threading.Thread(target = self._doFunc) for i in range (MAXTHREADS)]
                
                if queue_results:
                   self._queue = Queue.Queue()
                else:
                   self._queue = None
                 
 
 
                   
    def _doFunc(self):          #find one pwd
                while (True):                
                 
                    #get next passwd for crack   
                     self._lock.acquire()
                     try:
                          try:
                               arg = self._nextArgs()                    
                          except StopIteration:
                               break
                     finally:
                          self._lock.release()   
                   
                     returnValue = self._func(arg)

                     if (returnValue is not None):     # 记录结果到queue                 
                           if self._queue is not None :
                             self._queue.put(  returnValue )                                                  

    def start(self):
                for thread in self._threadPool:
                    time.sleep(0)  #give chance to other threads
                    thread.start()
                
    def join(self, timeout = None):
                for thread in self._threadPool:
                    thread.join(timeout)

                  
             
               
    def get(self, *a, **kw):
                if self._queue is not None:
                    return self._queue.get(*a, **kw)
                else:
                    raise ValueError, 'Not queueing results'
                    
    def quewrite(self, fpresult):     
               counter = 0
               while not self._queue.empty():                  
                  rt = self._queue.get() #returnValue is a list, see getDownLinkFunc  
                  counter+= writeResult(fpresult, rt)                                            
               #fpresult.flush()
               return counter

def writeResult(fpresult, rt):  #returnValue is a list, see getDownLinkFunc
    if (rt is None):
      return 0
    try:  
       title1 = rt[2].encode('gb18030')    
       fpresult.write("%s %s %s %s %s\n" %(rt[0],rt[1],title1,rt[3],rt[4]))
       fpresult.write("%s\n"%rt[5])   
       fpresult.flush()            
       return 1
    except  Exception, e:       
        print ("writeResult  Exception :%s rt:    "%(str(e)))    
        print rt
    return 0

def getDownLinkFunc(eachV):

       vId = eachV[0]
       vToken = eachV[1]
       vTitle = eachV[2]
       vExtension,  vTag = getMediaInfo(vId, vToken)            #1080p=137 720p=136
       
       if (vTag != 136 and vTag != 137 and vTag !=22):         
         print ("extension:%s taH:%s .media resolution low !  "%(vExtension,  vTag)) 
         if (DROP_LOW_RES):
           print (" drop it !")
           return None
       #print  vExtension,  vTag  
       link = getDownLink(vId, vToken, vTitle, vExtension, vTag)
       #print(link)
       #if (link is None):
       #   return None;
       if (link is None):
          return None
       return [vId, vToken, vTitle, vExtension, vTag, link]


def getLink():
    global linesWrited
    jsn = sendSearchAjax(None)
    if os.path.isdir(DOWN_FILE_DIR) is False:
      os.mkdir(DOWN_FILE_DIR)
    f = open(DOWN_FILE_DIR+'\\'+LINK_FILE_NAME, 'w')
                                              
    while (jsn != None):    
         
         if (jsn["status"] is False):
            print("sendSearchAjax get json status is False") 
            print jsn
            break                                                                
         directAction = jsn['directAction']   
         if (directAction is False):
            print("sendSearchAjax get json directAction is False. perhaps over")   
            print jsn
            break
               
         #get vId_list, vToken, vTitle                  
         v_list = []   
         _counter = 0                                                                                         
         for eachV in jsn['videos']:              
           vId = eachV['id']                            
           vToken = eachV['token']                      
           vTitle = eachV['title']                      
           eachV2 = [vId, vToken, vTitle ]     
           if (bRunMT) :
              v_list.append(eachV2)   
           else:
              rt = getDownLinkFunc(eachV2)
              _counter+= writeResult(f, rt)
             
              
         if (bRunMT) :                                             
            mt = MT(getDownLinkFunc, v_list, MAXTHREADS_NUM)                        
            mt.start()                                     
            mt.join()                                      
            _counter+=mt.quewrite(f)                                 
         print("%s lines writed" % _counter)

         linesWrited += _counter
         jsn = sendSearchAjax(directAction)
    f.close() 



def  _getLinkST():  #single thread , slow
   
   jsn = sendSearchAjax(None)
   f = open(LINK_FILE_NAME, 'w')
   while (jsn != None):
      if (jsn["status"] is False):                        	
         print("sendSearchAjax get json status is False")    
         print jsn                                           
         break                                                                   
      directAction = jsn['directAction']                     
      if (directAction is False)    :                       
         print("sendSearchAjax get json directAction is False. perhaps over")    
         print jsn                                           
         break                                               
     
     #get vId_list, vToken, vTitle 
     
      for eachV in jsn['videos']:
                                                                   
           vId = eachV['id']                            
           vToken = eachV['token']                      
           vTitle = eachV['title']                      
           eachV2 = [vId, vToken, vTitle ]                                                               
                                                                                       

      jsn = sendSearchAjax(directAction)  

   f.close()  


def UnitTest():
  if (UNIT_TEST != 1) :
    return False 
  test_getlink = getDownLink(test_id, test_token,   test_title, "mp4", 137)
  if (cmp(test_getlink, test_downloadlink) != 0):
    print("test  get link failed!")
    print("get   link :", test_getlink)
    print("right link :", test_downloadlink)
    return False
  return True




if __name__ == '__main__':
  if (not bRunMT):
      print("run single thread !")
  if (itagToDOWN == 22):
      print("Only search 720P video with audio !")
  if (itagToDOWN == 137):
      print("Only search 1080p video stream , NO audio !")
  print ("result will store in the file folder named %s\%s"%(DOWN_FILE_DIR,LINK_FILE_NAME))

  #UnitTest()    
  getLink()
  print("ttl %s lines writed" % linesWrited)


 
 


	
	

