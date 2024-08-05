from django import template
from django.contrib.auth import get_user_model

from django.utils import timezone

register = template.Library()

@register.filter(name = 'intdivide')
def  intdivide(value,div) :
    try :
        return int(value)//int(div)
    except (ValueError,ZeroDivisionError) : 
        return None


@register.filter
def beginswith(text,test) :
    try :
        if str(text.__str__()).startswith(str(test)) :
            return True
        else : return False
    except :
        return False

@register.filter
def if_empty(text,default) :
    try : 
        if len(str(text)) < 1 or text == "None" or not text :
            return default
        else : return text 
    except : return default 

@register.filter
def readtime(text) :

    try :
        read_speed = 150
        count = len(str(text.split()))
        time = count//read_speed
        if time < 1 :
            time = 1
        return time 
    except ValueError :
        return None 

@register.filter
def filetype(file,check_type) :
    try :
        ext_dict = {'video':['mp4','avi','3gp'],'picture' : ['jpg','jpeg','png']}
        file_ext = str(file).split('.')[1]
        avail_ext = ext_dict.get(str(check_type),None)
        if avail_ext : #if noe was returned it means we dont expect the type
            if file_ext in avail_ext :
                return True
        return False
    except :
        return False            


@register.filter
def readable(text) :
    try :
        text = str(text)
        text = text.split('_') 
        text = ' '.join(text) 
        return text  

    except ValueError :
        return None  

@register.filter
def higher(text) :
    try :
       
        return str(text).upper()  

    except ValueError :
        return None  


@register.filter
def firstcap(text) :
    try :
       
        return str(text).capitalize()  

    except ValueError :
        return None          


@register.filter
def timepublished(date) :
    
    
    current = timezone.now()
    diff = current - date
    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60 :
        seconds = diff.seconds

        if seconds == 1  :
            return str(seconds) + " s"
        else : return str(seconds) +  " s"

    if diff.days == 0 and diff.seconds >= 60 and diff.seconds  < 3600 :
        if diff.seconds < 120 :
            return str(diff.seconds//60) + " m "
        else : return str(diff.seconds//60) + " m "

    if diff.days == 0 and diff.seconds >= 3600  and diff.seconds < 86400 :
        if diff.seconds < 7200 :
            return str(diff.seconds//3600) + " h "
        else : return str(diff.seconds//3600) + " h "

    if diff.days >=  1 and diff.days < 30 :
        if diff.days < 2 : return  str(1) + " d "
        else : return str(diff.days) + " d "

    if diff.days >= 30 and diff.days < 365 :
        if diff.days < 60 :
            return str(diff.days//30) + " m " 
        else : return str(diff.days//30) + " m "

    if diff.days >= 365 :
        if diff.days < 730 :
            return  str(diff.days//365) + " y "
        else : return str(diff.days//365) + " y "               


@register.filter
def frontspace(txt) :
    try : return str(txt) + "    ."
    except ValueError : return None

@register.filter
def backspace(txt) :
    try : return "  " + str(txt) 
    except ValueError : return None   

@register.filter
def fewwords(txt,words) :
    try :
        words = int(words)
        text = list(txt)
        texts = text[words]
        texts = " ".join(texts)  
        texts = texts + "..."
        return str(texts) 
    except ValueError : return None  

@register.filter
def dictValue(dict,key) :
    try :
        return dict[key]
    except ValueError : return None 

@register.filter
def getBlogArticleCategoryModCount(value) :
    from blog.models import Article
    return len(Article.objects.filter(category=str(value)))

@register.filter
def boldmentions(text) :
    try :
        new_text = list()
        text = text.split() 
        for text in text : 
            if text.startswith('@') :
                if text.strip('@').find('@') > 0 :
                    text = text.strip('@').split('@')
                    for text in text :
                        text = "@{}".format(text)
                        new_text.append("<a style='color:black' href = '/gk/{}/'><strong>{}</strong></a>".format(str(text.strip('@')),text))#login is test later change to profile view
                else : new_text.append("<a style='color:black' href = '/gk/{}/'><strong>{}</strong></a>".format(text.strip('@'),text))
            else : new_text.append(text) 
        return " ".join(new_text)         
    except TypeError : 
        return None
    

@register.filter
def boldtags(text) :
    try :
        new_text = list()
        text = text.split()
        for text in text :
            if text.startswith('#') :
                if text.strip('#').find('#') > 0 :    #making sure there are no more than one comjoined tags
                    text = text.strip('#').split('#')
                    for text in text :
                       text = "#{}".format(text)      #put back the # for display
                       new_text.append("<a href = '/socials/tag/explore-tag/{}' style ='color:black'><strong>{}</strong></a>".format(text.strip('#'),text)) 
                else : new_text.append("<a href = '/socials/tag/explore-tag/{}' style ='color:black'><strong>{}</strong></a>".format(text.strip('#'),text))
            else : new_text.append(text) 
        return " ".join(new_text) 
    except TypeError :
        return None 


@register.filter
def contains(text,word) :
    try : 
        if word in  text :
            return True
        else : return False
    except :
        return None

@register.filter
def subtract(num) :
    try : return int(num) - 1
    except : return num    

   

                

                    


            
        






