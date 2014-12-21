import mysql.connector
import pickle
from bs4 import BeautifulSoup
import urllib2

connection = mysql.connector.connect(user='ron', 
                                    database='onelivi2_efcdb', 
                                    passwd='27352Ide')
cursor = connection.cursor()

query = """
            SELECT sermontitle, sermonpassage, sermonblogid, 
            sermondate, sermonauthor, seriesid, sermonAudioUrl FROM sermons
        """
#WHERE seriesid = 12
cursor.execute(query)

sermons = []
for (title, passage, blogid, date, author, series, audiourl) in cursor:
    url = "http://www.onelivinghope.wordpress.com/?p=%s" % str(blogid)
    try:
        html = urllib2.urlopen(url).read()
    except:
        print blogid
        continue
    if blogid != 0:
        soup = BeautifulSoup(html)
        #word press parsing
        entry_inner = soup.select('.entry-inner')
        paragraphs = entry_inner[0].find_all('p')
        transcript_list = ['<p>']
        for p in paragraphs:
            transcript_list.append(p.text)
            transcript_list.append('</p>')
            transcript_list.append('<p>')
        #get rid of last hanging <p>
        transcript = ''.join(transcript_list[:-1])
    else:
        print '%s no transcript' % title
        transcript = ''

    sermon_info = {'title':title, 'passage':passage,
                   'blogid':blogid, 'date':date, 'author':author,
                   'series':series, 'transcript':transcript,
                   'audiourl':audiourl}
    sermons.append(sermon_info)
    
f = open('D:/dropbox/django/livinghope_proj/old_site_data.pickle', 'wb')
pickle.dump(sermons, f)
f.close()