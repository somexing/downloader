#coding:utf8
import  sys,re

SITE = 'CaoL2' #you ma
 
TOPIC_URL_prefix = 'http://cl2.hydz.info/'
TOPIC_URL_postfix = ''
#PAGE_URL_FIRST =  TOPIC_URL_prefix +'thread0806.php?fid=15&search=&page=1'
#PAGE_URL_prefix = TOPIC_URL_prefix +'thread0806.php?fid=15&search=&page='
PAGE_URL_postfix = ''

PAGE_URL_FIRST =  TOPIC_URL_prefix +'thread0806.php?fid=2&search=&page=1'  #no mask
PAGE_URL_prefix = TOPIC_URL_prefix +'thread0806.php?fid=2&search=&page='


urllist = [PAGE_URL_FIRST, PAGE_URL_prefix, PAGE_URL_postfix, TOPIC_URL_prefix, TOPIC_URL_postfix]
#每页列表的标题匹配
str_topic_re = r'<a href="(.*?)" target="_blank" id="">(.*?)</a>'
#每个帖子内容列表匹配
 
#str_content_re = r'<div class="t t2" style="border-top:0">.*?<div class="tpc_content do_not_catch">(.*?)</div>.*?(Posted.*?)<'

xpathstr_content_re = '//*[@id="main"]/div[3]/table/tbody/tr[1]/th[2]/table/tbody/tr/td/div[4]'
str_content_re = r'(http://www.rmdown.com/.*?)</a>'
str_cleanhtml_re =  r'<[^>]+>|(\\r)|(\\n)'

re_strlist = [str_topic_re, str_content_re, str_cleanhtml_re]

#最大页码
MAX_PAGE_IDX = 5



if __name__ == '__main__':

    sys.path.append("../mymodule")
    import   bbs 
    
    filename= SITE + "_result.htm"
    fp = open(filename,'w')
    re1 = re.compile( str_topic_re )
    re2 = re.compile( str_content_re, re.S )
    #re2 =   str_content_re 
    re3 = re.compile( str_cleanhtml_re )
    relist = [re1, re2, re3]
    
    bbs = bbs.FixPageBBSCrawl()
    bbs.init_argv(urllist,  relist,  fp, MAX_PAGE_IDX )
    bbs.setOutPutPathFileName(u"D:\\Python27\\mysource\\bbs\\cl\\"+SITE) #will add .htm
    
    bbs.OpenBBS()

    fp.flush()
    fp.close() 
