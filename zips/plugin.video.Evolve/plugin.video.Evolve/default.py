#V 2.0.6
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,requests,urllib,urllib2,json,os,re,sys,datetime,urlresolver,random,liveresolver,base64,pyxbmct
from resources.lib.common_addon import Addon
from HTMLParser import HTMLParser
from metahandler import metahandlers
import nanscrapers


addon_id        = 'plugin.video.Evolve'
addon           = Addon(addon_id, sys.argv)
selfAddon       = xbmcaddon.Addon(id=addon_id)
addonInfo       = xbmcaddon.Addon().getAddonInfo
fanart          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.png'))
fanarts         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.png'))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
nextpage        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/art', 'next.png'))
rd              = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources','rd.txt'))
baseurl         = 'http://evolverepo.net/anewEvolvemenu/EvolveMainMenu.xml'
baseurl2        = 'http://evolverepo.net/Evolvemasterlist/'
adultpass       = selfAddon.getSetting('password')
metaset         = selfAddon.getSetting('enable_meta')
messagetext     = 'http://evolverepo.net/anewEvolvemenu/info.txt'#+'?%d=%s' % (random.randint(1, 10000), random.randint(1, 10000))
userdata        = xbmc.translatePath('special://home/userdata/addon_data/' + addon_id)
favs            = xbmc.translatePath(os.path.join('special://home/userdata/Database', 'Evolve.db'))
favsdb = open(favs,'a')
favsdb.close()

def MAINMENU():
        if not os.path.exists(userdata):
                os.mkdir(userdata)
        popup(messagetext,'GlobalCompare')
        addDir('[B][COLOR royalblue]F[/COLOR][COLOR white]avs[/COLOR][/B]','url',22,'http://i.imgur.com/Fi18HDV.png',fanarts)
        addDir('[B][COLOR red]M[/COLOR][COLOR white]ovies[/COLOR][/B]','http://evolverepo.net/EvolveMenus/Movies/Mainmenu.xml',26,'http://i.imgur.com/x6BAZUe.png',fanarts)
        addDir('[B][COLOR blue]TV[/COLOR]  [COLOR blue]S[/COLOR][COLOR white]hows[/COLOR][/B]','http://evolverepo.net/EvolveMenus/TvShows/Mainmenu.xml',27,'http://i.imgur.com/SLdxQL6.png',fanarts)
        link=open_url(baseurl)
        match= re.compile('<item>(.+?)</item>').findall(link)
        for item in match:
                data=re.compile('<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                for name,url,iconimage,fanart in data:
                        addDir(name,url,1,iconimage,fanart)
        addDir('[B][COLOR chartreuse]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR chartreuse]E[/COLOR][COLOR white]volve[/COLOR][/B]','url',5,'http://i.imgur.com/oHqT3bb.png',fanarts)
        xbmc.executebuiltin('Container.SetViewMode(500)')

def MOVIEMENU(name,url,iconimage,fanart):
        addDir('[B][COLOR red]MOVIE SEARCH[/COLOR][/B]','http://evolverepo.net/EvolveMenus/Movies/Search/Search.txt',5,'http://i.imgur.com/Qlc3Efe.png',fanarts)
        addDir('[B][COLOR yellow]UK CINEMA RELEASE DATES[/COLOR][/B]','http://www.empireonline.com/movies/features/upcoming-movies/',34,'http://i.imgur.com/1ImmOS4.png',fanarts)
        prettyname=removetags(name)
        selfAddon.setSetting('movie',prettyname)
        link=open_url(url)
        match= re.compile('<item>(.+?)</item>').findall(link)
        for item in match:
                data=re.compile('<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                for name,url,iconimage,fanart in data:
                    ACTION(name,url,iconimage,fanart,item)
                
def TVSHOWMENU(name,url,iconimage,fanarts):
        addDir('[B][COLOR blue]TV SEARCH[/COLOR][/B]','http://evolverepo.net/anewEvolvemenu/search.xml',33,'http://i.imgur.com/gLWo9QO.png',fanarts)
        addDir('[B][COLOR yellow]TV SCHEDULE[/COLOR][/B]','http://www.tvwise.co.uk/uk-premiere-dates/',32,'http://i.imgur.com/Pq53Nxh.png',fanarts)
        addDir('[B][COLOR blue]Latest[/COLOR] [COLOR white]Episodes[/COLOR][/B]','http://www.watchepisodes4.com',28,'http://i.imgur.com/PmLtUtH.png',fanarts)
        addDir('[B][COLOR blue]Popular[/COLOR] [COLOR white]Shows[/COLOR][/B]','http://www.watchepisodes4.com/home/popular-series',29,'http://i.imgur.com/SHXfj1a.png',fanarts)
        addDir('[B][COLOR blue]New[/COLOR] [COLOR white]Shows[/COLOR][/B]','http://www.watchepisodes4.com/home/new-series',30,'http://i.imgur.com/roVYGM8.png',fanarts)
        prettyname=removetags(name)
        selfAddon.setSetting('tv',prettyname)
        link=open_url(url)
        match= re.compile('<item>(.+?)</item>').findall(link)
        for item in match:
                data=re.compile('<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                for name,url,iconimage,fanart in data:
                    ACTION(name,url,iconimage,fanart,item)

def RUNNER(name,url,iconimage,fanart):
        prettyname=removetags(name)
        selfAddon.setSetting('tv',prettyname)
        link=open_url(url)
        view(link)
        if '<message>' in link:
                messagetext = re.compile('<message>(.+?)</message>').findall(link)[0]
                popup(messagetext,prettyname)
        if '<intro>' in link:
                intro = re.compile('<intro>(.+?)</intro>').findall(link)[0]
                INTROPLAY(intro)      
        if 'XXX>yes</XXX' in link: ADULT_CHECK(link)
        match= re.compile('<item>(.+?)</item>').findall(link)
        for item in match:
                ACTION(name,url,iconimage,fanart,item)

def ACTION(name,url,iconimage,fanart,item):
        try:
                if '<sportsdevil>' in item: SPORTS_DEVIL(name,url,iconimage,fanart,item)
                elif '<iplayer>' in item: IPLAYER(name,url,iconimage,fanart,item)
                elif '<folder>'in item: FOLDER(name,url,iconimage,fanart,item)
                elif '<iptv>'in item: IPTV(name,url,iconimage,fanart,item)
                elif '<image>'in item: IMAGE(name,url,iconimage,fanart,item)
                elif '<text>'in item: TEXT(name,url,iconimage,fanart,item)
                elif '<scraper>' in item: SCRAPER(name,url,iconimage,fanart,item)
                elif '<lbscraper>' in item: LBSCRAPER(name,url,iconimage,fanart,item)
                elif '<redirect>' in item: REDIRECT(name,url,iconimage,fanart,item)
                elif '<oktitle>' in item: OK(name,url,iconimage,fanart,item)
                elif '<nan>' in item: NAN(name,url,iconimage,fanart,item)
                else:GETCONTENT(name,url,iconimage,fanart,item)
        except:pass

def IPLAYER(name,url,iconimage,fanart,item):
        url=re.compile('<iplayer>(.+?)</iplayer>').findall(item)[0]
        name=re.compile('<title>(.+?)</title>').findall(item)[0]
        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
        url='plugin://plugin.video.iplayerwww/?url=%s&mode=202&name=%s&iconimage=%s&description=&subtitles_url=&logged_in=False'%(url,name,iconimage)
        addLinkNoDialog(name,url,16,iconimage,fanart)

def NAN(name,url,iconimage,fanart,item):
        name=re.compile('<title>(.+?)</title>').findall(item)[0]
        meta=re.compile('<meta>(.+?)</meta>').findall(item)[0]
        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
        stype=re.compile('<nan>(.+?)</nan>').findall(item)[0]
        imdb=re.compile('<imdb>(.+?)</imdb>').findall(item)[0]            
        if stype=='movie':
                imdb=imdb+'<>movie'
        elif stype=='tvshow':
                showname=re.compile('<showname>(.+?)</showname>').findall(item)[0] 
                season=re.compile('<season>(.+?)</season>').findall(item)[0]            
                episode=re.compile('<episode>(.+?)</episode>').findall(item)[0]
                showyear=re.compile('<showyear>(.+?)</showyear>').findall(item)[0]
                episodeyear=re.compile('<episodeyear>(.+?)</episodeyear>').findall(item)[0]
                imdb=imdb+'<>'+showname+'<>'+season+'<>'+episode+'<>'+showyear+'<>'+episodeyear
                stype = "tvep"
        addLinkMeta(name, imdb,19,iconimage, 1, stype, isFolder=True)

def DONAN(name,imdb,iconimage,fanart):
        rd=''
        title=name
        prettyname=removetags(name)
        selfAddon.setSetting('tv',prettyname)
        if 'movie' in imdb:
                imdb=imdb.split('<>')[0]
                streamurl=[]
                streamname=[]
                splitName=name.partition('(')
                nanname=splitName[0]
                nanname=removetags(nanname)
                nanyear=splitName[2].partition(')')[0]
                scrape = nanscrapers.scrape_movie(nanname, nanyear, imdb, timeout=800)
        else:
                showname=imdb.split('<>')[1]
                imdbnum=imdb.split('<>')[0]
                season=imdb.split('<>')[2]
                episode=imdb.split('<>')[3]
                showyear=imdb.split('<>')[4]
                episodeyear=imdb.split('<>')[5]
                scrape=nanscrapers.scrape_episode(showname, showyear, episodeyear, season, episode, imdbnum, None)
        i=1
        for results in list(scrape()):
                for result in results:
                        if urlresolver.HostedMediaFile(result['url']).valid_url():
                                rd=RDCHECK(result['url'])
                                name="Link "+str(i)+ ' | ' +  result['source']+rd
                                i=i+1
                                addLink(name,result['url'],2,iconimage,fanart,description=selfAddon.getSetting('tv'))
   
def SCRAPER(name,url,iconimage,fanart,item):
        name=re.compile('<title>(.+?)</title>').findall(item)[0]
        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
        url=re.compile('<scraper>(.+?)</scraper>').findall(item)[0]
        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
        addDir(name,url,18,iconimage,fanart)

def DOSCRAPER(name,url,iconimage,fanart):
        scraper=url
        if scraper=='latestmovies':
                smode=15
                itemlist=MOVIESINDEXER()
                items=re.compile('<item>(.+?)</item>').findall(itemlist)
                for item in items:
                        data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                        count = len(items)
                        for name,url,iconimage,fanart in data:
                                if '<meta>' in item:
                                        metatype=re.compile('<meta>(.+?)</meta>').findall(item)[0]
                                        addLinkMeta(name,url,smode,iconimage,count,metatype,isFolder=False)
                                else:addLink(name,url,15,iconimage,fanart)

##################################################  TV
def GET_LATESTEPISODES(name,url,iconimage,fanarts):
    link=open_url3('http://www.watchepisodes4.com')
    content=re.compile('<a title=".+?" .+? style="background-image: url(.+?)"></a>.+?<div class="hb-right">.+?<a title=".+?" href="(.+?)" class="episode">(.+?)</a>',re.DOTALL).findall(link)
    for iconimage,url,name in content:
        iconimage=iconimage.replace("('","").replace("')","")
        name=name.replace("&#39;","'").replace('&amp;',' & ')
        name=name.split('  ')[0]
        addDir(name,url,24,iconimage,iconimage)

def GET_NEWSERIESCONTENT(name,url,iconimage,fanart):
    link=open_url3(url)
    content=re.compile('<div class="cb-first">.+?<a href="(.+?)" class="c-image"><img alt=".+?" title="(.+?)" src="(.+?)"></a>',re.DOTALL).findall(link)
    for url,name,iconimage in content:
        name=name.replace("&#39;","'").replace('&amp;',' & ')
        addDir(name,url,31,iconimage,iconimage)

def GET_POPULARSERIESCONTENT(name,url,iconimage,fanart):
    link=open_url3(url)
    content=re.compile('<div class="cb-first">.+?<a href="(.+?)" class="c-image"><img alt=".+?" title="(.+?)" src="(.+?)"></a>',re.DOTALL).findall(link)
    for url,name,iconimage in content:
        name=name.replace("&#39;","'").replace('&amp;',' & ')
        addDir(name,url,31,iconimage,iconimage)

def LIST_SEASONS(name,url,iconimage,fanart):
        link=open_url2(url)
        sname=re.compile('<div class="std-cts">.+?<div class="sdt-content tnContent">.+?<h2>(.+?)</h2>',re.DOTALL).findall(link)[0].replace(' Episodes','').replace("&#39;","'").replace('&amp;',' & ')
        match=re.compile('<a title=".+?" href="(.+?)">.+?<div class="season">(.+?) </div>.+?<div class="episode">(.+?)</div>.+?<div class="e-name">(.+?)</div>',re.DOTALL).findall(link)
        for url,season,episode,ename in match:
            ename=ename.replace("&#39;","'").replace('&amp;',' & ')
            if '</div>' in name:name = 'TBA'
            addDir('%s '%sname + '(%s '%season  + '%s)'%episode,url,24,iconimage,iconimage)

def GET_LATESTTVLINKS(name,url,iconimage,fanart):
        title=name
        link=open_url2(url)
        hostlist=re.compile('<a target="_blank" href=".+?" data-episodeid=".+?" data-linkid=".+?" data-hostname=".+?" class="watch-button" data-actuallink="(.+?)">Watch Now!</a>').findall(link)
        i=1
        streamurl=[]
        streamname=[]
        for host in hostlist:
                rd=RDCHECK(host)
                if 'http' in host:hostname=host.split('/')[2].split('.')[0]
                else: hostname=host
                name="Link "+str(i)+ ' | ' +hostname+rd
                if hostname != 'www':
                        addLink(hostname,host,2,iconimage,fanart,description='')

def GET_TVSCHEDULE(name,url,iconimage,fanart):
    link=open_url2(url)
    content=re.compile('<td height="20">(.+?)</td>.+?<td>(.+?)</td>.+?<td><a href=".+?">(.+?)</a></td>.+?<td><a href=".+?">(.+?)</a></td>.+?</tr>',re.DOTALL).findall(link)
    for channel,name,date,time in content:
        name=name.replace("&#8217;","'").replace('&amp;',' & ')
        addDir('[COLOR yellow]%s[/COLOR] - '%date + '[COLOR blue]%s[/COLOR] '%name + '- [COLOR white]%s[/COLOR]'%channel,url,28,iconimage,fanart)

def TVSEARCH(url):
    searchterm =''
    keyboard = xbmc.Keyboard(searchterm, '[B][COLOR red]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B]')
    keyboard.doModal()
    if keyboard.isConfirmed():
        searchterm = keyboard.getText().replace(' ','+').replace('+and+','+%26+')
    if len(searchterm)>1:
        url = 'http://www.watchepisodes4.com/search/ajax_search?q='+ searchterm
        link=open_url2(url)
        data = json.loads(link)
        data=data['series']
        for item in data:
            name=item['value']
            movurl=item['seo']
            url='http://www.watchepisodes4.com/'+movurl
            iconimage='http://www.watchepisodes4.com/movie_images/'+movurl+'.jpg'
            addDir(name,url,31,iconimage,fanart)      
        searchterm=searchterm[:-1]
        link=open_url('http://evolverepo.net/anewEvolvemenu/search.xml')
	slist=re.compile('<link>(.+?)</link>').findall(link)
	for url in slist:
                try:
                        link=open_url(url)
                        entries= re.compile('<item>(.+?)</item>').findall(link)
                        for item in entries:
                                match=re.compile('<title>(.+?)</title>').findall(item)
                                for title in match:
                                        title=removetags(title.upper())
                                        searchterm=searchterm.upper()
                                        if searchterm in title:
                                            ACTION(name,url,iconimage,fanart,item)
                except:pass
                                    
##################################################  MOVIES
def GET_MOVIESCHEDULE(name,url,iconimage,fanart):
    link=open_url2(url)
    content=re.compile('<h2 id=".+?">(.+?)</h2>.+?<p><span class="article__image article__image--undefined"><img src="(.+?)" alt=".+?"></span> </p>.+?<p><strong>(.+?)</strong>(.+?)<',re.DOTALL).findall(link)
    for title,iconimage,due,date in content:
        name=name.replace("&#8217;","'").replace('&amp;',' & ')
        addDir('[COLOR yellow]%s [/COLOR] '%title + '[COLOR red]%s[/COLOR]'%due + '[COLOR white]%s[/COLOR]'%date,url,35,iconimage,fanart)
def GET_LATESTMOVIECONTENT(name,url,iconimage,fanart):
    link=open_url('http://evolverepo.net/EvolveMenus/Movies/EvolveLatest/mainmenu.xml')
    content=re.compile('<item>(.+?)</item>').findall(link)
    for item in content:
        ACTION(name,url,iconimage,fanart,item)
##################################################  MOVIES

def LBSCRAPER(name,url,iconimage,fanart,item):
        name=re.compile('<title>(.+?)</title>').findall(item)[0]
        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
        url=re.compile('<lbscraper>(.+?)</lbscraper>').findall(item)[0]
        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
        addDir(name,url,10,iconimage,fanart)
        
def DOLBSCRAPER(name,url,iconimage,fanart):
        scrape=DOLB(name,url,iconimage)
        match= re.compile('<item>(.+?)</item>',re.DOTALL).findall(scrape)
        for item in match:
                ACTION(name,url,iconimage,fanart,item)
        
def DOLB(name,url,iconimage):
        scraper=url
        string=''
        if url=='mamahd':
                link=open_url3("http://mamahd.com").replace('\n','').replace('\t','')
                livegame=re.compile('<a href="(.+?)">.+?<img src="(.+?)"></div>.+?<div class="home cell">.+?<span>(.+?)</span>.+?<span>(.+?)</span>.+?</a>').findall(link)
                for url,iconimage,home,away in livegame:
                    string=string+'<item>\n<title>%s vs %s</title>\n<sportsdevil>%s</sportsdevil>\n<thumbnail>%s</thumbnail>\n<fanart>fanart</fanart>\n</item>\n\n'%(home,away,url,iconimage)
                return string
        
        elif url=='cricfree': 
                link=open_url3("http://cricfree.sc/football-live-stream")
                events=re.compile('<td><span class="sport-icon(.+?)</tr>',re.DOTALL).findall(link)
                for event in events:
                        cal=re.compile('<td>(.+?)<br(.+?)</td>').findall(event)
                        for day,date in cal:
                                day='[COLOR red]'+day+'[/COLOR]'
                                date=date.replace('>','')   
                        time=re.compile('<td class="matchtime" style="color:#545454;font-weight:bold;font-size: 9px">(.+?)</td>').findall(event)[0]
                        time='[COLOR white]('+time+')[/COLOR]'
                        naurl=re.compile('<a style="text-decoration:none !important;color:#545454;" href="(.+?)" target="_blank">(.+?)</a></td>').findall(event)
                        for url,progname in naurl:
                                url=url
                                progname=progname
                        string=string+'\n<item>\n<title>%s</title>\n<sportsdevil>%s</sportsdevil>\n'%(day+' '+time+' - '+progname,url)
                        string=string+'<thumbnail>iconimage</thumbnail>\n<fanart>fanart</fanart>\n</item>\n'
                return string
        
        elif url=='bigsports':  
                link=open_url3("http://www.bigsports.me/cat/4/football-live-stream.html")
                livegame=re.compile('<td>.+?<td>(.+?)\-(.+?)\-(.+?)</td>.+?<td>(.+?)\:(.+?)</td>.+?<td>Football</td>.+?<td><strong>(.+?)</strong></td>.+?<a target=.+? href=(.+?) class=.+?',re.DOTALL).findall(link)
                for day,month,year,hour,mins,name,url in livegame:
                        if not '</td>' in day:
                                url=url.replace('"','')
                                date=day+' '+month+' '+year
                                time=hour+':'+mins
                                date='[COLOR red]'+date+'[/COLOR]'
                                time='[COLOR white]('+time+')[/COLOR]'
                                string=string+'\n<item>\n<title>%s</title>\n<sportsdevil>%s</sportsdevil>\n'%(date+' '+time+' '+name,url)
                                string=string+'<thumbnail>iconimage</thumbnail>\n<fanart>fanart</fanart>\n</item>\n'
                return string

def OK(name,url,iconimage,fanart,item):
        name=re.compile('<title>(.+?)</title>').findall(item)[0]
        oktitle=re.compile('<oktitle>(.+?)</oktitle>').findall(item)[0]
        line1=re.compile('<line1>(.+?)</line1>').findall(item)[0]
        line2=re.compile('<line2>(.+?)</line2>').findall(item)[0]
        line3=re.compile('<line3>(.+?)</line3>').findall(item)[0]
        text='##'+oktitle+'#'+line1+'#'+line2+'#'+line3+'##'
        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
        addLinkNoDialog(name,text,17,iconimage,fanart)

def DOOK(name,url):
        lines=re.compile('##(.+?)##').findall(url)[0].split('#')
        dialog = xbmcgui.Dialog()
        dialog.ok(lines[0],lines[1],lines[2],lines[3])
        
def REDIRECT(name,url,iconimage,fanart,item):
        url=re.compile('<redirect>(.+?)</redirect>').findall(item)[0]
        RUNNER('name',url,'iconimage','fanart')
                                                            
def TEXT(name,url,iconimage,fanart,item):
        name=re.compile('<title>(.+?)</title>').findall(item)[0]
        text=re.compile('<text>(.+?)</text>').findall(item)[0]
        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
        addLinkNoDialog(name,text,9,iconimage,fanart)

def DOTEXTBOX(name,url):
        textfile=open_url2(url)
        showText(name, textfile)
       
def IMAGE(name,url,iconimage,fanart,item):
        images=re.compile('<image>(.+?)</image>').findall(item)
        if len(images)==1:
                name=re.compile('<title>(.+?)</title>').findall(item)[0]
                iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                image=re.compile('<image>(.+?)</image>').findall(item)[0]
                fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                addLinkNoDialog(name,image,7,iconimage,fanart)
        elif len(images)>1:
                name=re.compile('<title>(.+?)</title>').findall(item)[0]
                iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                store=''
                for image in images:store=store+'<image>'+image+'</image>'
                path = userdata
                name=removetags(name) 
                comparefile = os.path.join(os.path.join(path,''), name+'.txt')
                if not os.path.exists(comparefile):file(comparefile, 'w').close()
                text_file = open(comparefile, "w")
                text_file.write(store)
                text_file.close()
                addLinkNoDialog(name,'image',8,iconimage,fanart)
                  
def IPTV(name,url,iconimage,fanart,item):
        name=re.compile('<title>(.+?)</title>').findall(item)[0]
        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
        url=re.compile('<iptv>(.+?)</iptv>').findall(item)[0]
        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
        addDir(name,url,6,iconimage,fanart)

def GETIPTV(url,iconimage):
	link=open_url2(url)
	matches=re.compile('^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$',re.I+re.M+re.U+re.S).findall(link)
	li = []
	for params, name, url in matches:
		item_data = {"params": params, "name": name, "url": url}
		li.append(item_data)
	list = []
	for channel in li:
		item_data = {"name": channel["name"], "url": channel["url"]}
		matches=re.compile(' (.+?)="(.+?)"',re.I+re.M+re.U+re.S).findall(channel["params"])
		for field, value in matches:
			item_data[field.strip().lower().replace('-', '_')] = value.strip()
		list.append(item_data)
        for channel in list:
                if '.ts' in channel["url"]:addLinkNoDialog(channel["name"],channel["url"],2,iconimage,fanart)      
                else:addLink(channel["name"],channel["url"],2,iconimage,fanart)
        
def GETCONTENT(name,url,iconimage,fanart,item):
        rd=''
        links=re.compile('<link>(.+?)</link>').findall(item)
        data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
        for name,url2,iconimage,fanart in data:
                if 'youtube.com/playlist?' in url2:
                        searchterm = url2.split('list=')[1]
                        addDir(name,url2,mode,iconimage,fanart,description=searchterm)
        if len(links)==1:
                data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                for name,url,iconimage,fanart in data:
                        try:
                                rd=RDCHECK(url)
                                domain=url.split('/')[2].replace('www.','')
                                if 'SportsDevil' in url: domain=''
                        except:pass
                        if '.ts' in url:addLink(name,url,16,iconimage,fanart,description='')      
                        if '<meta>' in item:
                                metatype=re.compile('<meta>(.+?)</meta>').findall(item)[0]
                                addLinkMeta(name+rd,url,2,iconimage,10,metatype,isFolder=False)
                        else:
                                addLink(name+rd,url,2,iconimage,fanart)
        elif len(links)>1:
                name=re.compile('<title>(.+?)</title>').findall(item)[0]
                iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                if '.ts' in url:addLink(name,url,16,iconimage,fanart,description='')
                if '<meta>' in item:
                        metatype = re.compile('<meta>(.+?)</meta>').findall(item)[0]
                        addLinkMeta(name,url,3,iconimage,len(links), metatype, isFolder=True)
                else:
                        addDir(name,url,3,iconimage,fanart)

                             
def SPORTS_DEVIL(name,url,iconimage,fanart,item):
        links=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(item)
        links2=re.compile('<link>(.+?)</link>').findall(item)
        if len(links)+len(links2)==1:
                name=re.compile('<title>(.+?)</title>').findall(item)[0]
                iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                url=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(item)[0]
                url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +url
                addLinkNoDialog(name,url,16,iconimage,fanart)   
        elif len(links)+len(links2)>1:
                name=re.compile('<title>(.+?)</title>').findall(item)[0]
                iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                addDir(name,url,3,iconimage,fanart)
        
def ADULT_CHECK(link):
	if adultpass == '':
		dialog = xbmcgui.Dialog()
		ret = dialog.yesno('Adult Content', 'You have found the goodies ;)','','Please set a password to prevent accidental access','Cancel','OK')
		if ret == 1:
                        keyb = xbmc.Keyboard('', 'Set Password')
			keyb.doModal()
			if (keyb.isConfirmed()):
			    passw = keyb.getText()
			    selfAddon.setSetting('password',passw)
                else:quit()
	elif adultpass <> '':
		dialog = xbmcgui.Dialog()
		ret = dialog.yesno('Adult Content', 'Please enter the password you set!','to continue','dirty git','Cancel','OK')
		if ret == 1:    
			keyb = xbmc.Keyboard('', 'Enter Password')
			keyb.doModal()
			if (keyb.isConfirmed()):
				passw = keyb.getText()
			if passw <> adultpass:
				quit()
		else:quit()
		                    		
def GETMULTI(name,url,iconimage):
        caption=''
        prettyname=removetags(name)
        selfAddon.setSetting('tv',prettyname)
        link=open_url(url)
        urls=re.compile('<title>.*?'+re.escape(name)+'.*?</title>(.+?)</item>',re.DOTALL).findall(link)[0]
        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(urls)[0]
        links=[]
        if '<link>' in urls:
                nlinks=re.compile('<link>(.+?)</link>').findall(urls)
                for nlink in nlinks:
                        links.append(nlink)
        if '<sportsdevil>' in urls:
                slinks=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(urls)
                for slink in slinks:
                        slink='plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +slink
                        links.append(slink)
        i=1
        for link in links:
                if '(' in link:
                        link=link.split('(')
                        caption=link[1].replace(')','')
                        link=link[0]
                rd=RDCHECK(link)
                domain=link.split('/')[2].replace('www.','')
                if caption<>'':name="Link "+str(i)+ ' | ' +  caption+rd
                else:name="Link "+str(i)+ ' | ' +  domain+rd
                i=i+1
                addLinkMeta(name,link,2,iconimage,10,'',isFolder=False,description=selfAddon.getSetting('tv'))

def FOLDER(name,url,iconimage,fanart,item):
        data=re.compile('<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
        for name,url,iconimage,fanart in data:
                if 'youtube.com/channel/' in url:
                        searchterm = url.split('channel/')[1]
                        addDir(name,url,mode,iconimage,fanart,description=searchterm)
                elif 'youtube.com/user/' in url:
                        searchterm = url.split('user/')[1]
                        addDir(name,url,mode,iconimage,fanart,description=searchterm)
                elif 'youtube.com/playlist?' in url:
                        searchterm = url.split('list=')[1]
                        addDir(name,url,mode,iconimage,fanart,description=searchterm)
                elif 'plugin://' in url:
                        htmlp = HTMLParser()
                        url=htmlp.unescape(url)
                        addDir(name,url,mode,iconimage,fanart)
                else:
                        addDir(name,url,1,iconimage,fanart)

def SEARCH():
	keyb = xbmc.Keyboard('', '[B][COLOR red]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B]')
	keyb.doModal()
	if (keyb.isConfirmed()):
		searchterm=keyb.getText()
		searchterm=searchterm.upper()
	else:quit()
	link=open_url('http://evolverepo.net/anewEvolvemenu/search.xml')
	slist=re.compile('<link>(.+?)</link>').findall(link)
	for url in slist:
                try:
                        link=open_url(url)
                        entries= re.compile('<item>(.+?)</item>').findall(link)
                        for item in entries:
                                match=re.compile('<title>(.+?)</title>').findall(item)
                                for title in match:
                                        title=title.upper()
                                        if searchterm in title:
                                            ACTION(name,url,iconimage,fanart,item)
                except:pass
                        
def SHOWIMAGE(url):
    string = "ShowPicture(%s)" %url
    xbmc.executebuiltin(string)
        
def LINKTEST(name,url,iconimage,description):
        if description:name=description
        try:
                if 'plugin://plugin.video.SportsDevil/' in url:
                        PLAYLINKNODIALOG(name,url,iconimage)      
                elif '.ts'in url:
                        url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name='+name+'&amp;url='+url
                        url=url.replace('|','')
                        PLAYLINKNODIALOG(name,url,iconimage)
                elif urlresolver.HostedMediaFile(url).valid_url():
                        url = urlresolver.HostedMediaFile(url).resolve()
                        PLAYLINK(name,url,iconimage)
                elif liveresolver.isValid(url)==True:
                        url=liveresolver.resolve(url)
                        PLAYLINK(name,url,iconimage)
                else:PLAYLINK(name,url,iconimage)
        except:
                notification(addtags('Evolve'),'Stream Unavailable', '3000', icon)
        
def INTROPLAY(url):
        if urlresolver.HostedMediaFile(url).valid_url():
                url = urlresolver.HostedMediaFile(url).resolve()     
        xbmc.Player ().play(url)
        
def PLAYLINK(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

def PLAYLINKNODIALOG(name,url,iconimage):
        xbmc.executebuiltin('Dialog.Close(all,True)')
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player ().play(url, liz, False)
        
def TRAILER(url):
        xbmc.executebuiltin("PlayMedia(%s)"%url)
                
def open_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'mat')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=link.replace('<fanart></fanart>','<fanart>x</fanart>').replace('<thumbnail></thumbnail>','<thumbnail>x</thumbnail>').replace('<utube>','<link>https://www.youtube.com/watch?v=').replace('</utube>','</link>')#.replace('></','>x</')
        if '{'in link:
                string=link[::-1]
                string=string.replace('}','').replace('{','').replace(',','').replace(']','').replace('[','')  
                string=string+'=='
                link=string.decode('base64')
        if url <> messagetext: link=link.replace('\n','').replace('\r','')
        print link
        return link

def open_url2(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'mat')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def open_url3(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=link.replace('\n','').replace('\r','')
        return link

 
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]                    
        return param

def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")
    
def removetags(string):
        tags=re.compile('(\[.+?\])').findall(string)
        for tag in tags:string=string.replace(tag,'')
        return string

def addtags(string):
        string=string.split(' ')
        final=''
        for segment in string:
            formatted='[B][COLOR red]'+segment[0].upper()+'[/COLOR][COLOR white]'+segment[1:]+'[/COLOR][/B] '
            final=final+formatted
        return final
        
def addLinkMeta(name,url,mode,iconimage,itemcount,metatype,isFolder=False,description=''):
        if isFolder == True: selfAddon.setSetting('favtype','folder')
        else:selfAddon.setSetting('favtype','link')
        if metaset=='true':
                origname = name
                name=removetags(name)
                simplename=""
                simpleyear=""
                contextMenuItems = []
                mg = eval(base64.b64decode('bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ=='))
                meta = {}
                if metatype=='movie':
                        splitName=name.partition('(')
                        if len(splitName)>0:
                                simplename=splitName[0]
                                simpleyear=splitName[2].partition(')')
                        if len(simpleyear)>0:
                                simpleyear=simpleyear[0]
                        meta = mg.get_meta('movie', name=simplename ,year=simpleyear)
                        if not meta['trailer']=='':contextMenuItems.append((addtags('Play Trailer'), 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 11, 'url':meta['trailer']})))
                elif metatype=='tvep':
                        title=selfAddon.getSetting('tv')
                        if '<>' in url:
                                print url
                                imdbnum=url.split('<>')[0]
                                showname=url.split('<>')[1]
                                season=url.split('<>')[2]
                                episode=url.split('<>')[3]
                                showyear=url.split('<>')[4]
                                episodeyear=url.split('<>')[5]
                                meta = mg.get_episode_meta(showname, imdb_id=imdbnum, season=season, episode=episode, air_date='', episode_title='', overlay='')
                        else:    
                                seep=re.compile('Season (.+?) Episode (.+?)\)').findall(name)
                                for sea,epi in seep:
                                        meta = mg.get_episode_meta(title, imdb_id='', season=sea, episode=epi, air_date='', episode_title='', overlay='')
                try:
                        if meta['cover_url'] == '':iconimage=iconimage
                        else: iconimage=meta['cover_url']
                except:pass
                u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)
                ok=True
                liz=xbmcgui.ListItem(origname, iconImage=iconimage, thumbnailImage=iconimage)
                liz.setInfo( type="Video", infoLabels= meta)
                liz.setProperty("IsPlayable","true")
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
                if not meta.get('backdrop_url','') == '': liz.setProperty('fanart_image', meta['backdrop_url'])
                else: liz.setProperty('fanart_image', fanart)
                favlist=selfAddon.getSetting('favlist')
                cmenu=[]
                cmenu.append((addtags('Stream Information'), 'XBMC.Action(Info)'))
                if favlist == 'yes':cmenu.append(('[COLOR white]Remove from Evolve Favourites[/COLOR]','XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],name,url,iconimage)))
                else:cmenu.append(('[COLOR white]Add to Evolve Favourites[/COLOR]','XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],name,url,iconimage)))
                liz.addContextMenuItems(cmenu, replaceItems=False) 
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
                return ok
        else:
                if isFolder:
                        addDir(name,url,mode,iconimage,fanart,description='')
                else:
                        addLink(name,url,mode,iconimage,fanart,description='')
	
def addDir(name,url,mode,iconimage,fanart,description=''):
        selfAddon.setSetting('favtype','folder')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart) 
        if 'youtube.com/channel/' in url:
		u = 'plugin://plugin.video.youtube/channel/'+description+'/'
	if 'youtube.com/user/' in url:
		u = 'plugin://plugin.video.youtube/user/'+description+'/'
        if 'youtube.com/playlist?' in url:
                u = 'plugin://plugin.video.youtube/playlist/'+description+'/'
        if 'plugin://' in url:
                u=url
        cmenu=[]
        favlist=selfAddon.getSetting('favlist')
        if favlist == 'yes':cmenu.append(('[COLOR white]Remove from Evolve Favourites[/COLOR]','XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],name,url,iconimage)))
        else:cmenu.append(('[COLOR white]Add to Evolve Favourites[/COLOR]','XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],name,url,iconimage)))
        liz.addContextMenuItems(cmenu, replaceItems=False) 
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLinkNoDialog(name,url,mode,iconimage,fanart,description=''):
        selfAddon.setSetting('favtype','link')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        cmenu=[]
        favlist=selfAddon.getSetting('favlist')
        if favlist == 'yes':cmenu.append(('[COLOR white]Remove from Evolve Favourites[/COLOR]','XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],name,url,iconimage)))
        else:cmenu.append(('[COLOR white]Add to Evolve Favourites[/COLOR]','XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],name,url,iconimage)))
        liz.addContextMenuItems(cmenu, replaceItems=False) 
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        selfAddon.setSetting('favtype','link')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        cmenu=[]
        favlist=selfAddon.getSetting('favlist')
        if favlist == 'yes':cmenu.append(('[COLOR white]Remove from Evolve Favourites[/COLOR]','XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],name,url,iconimage)))
        else:cmenu.append(('[COLOR white]Add to Evolve Favourites[/COLOR]','XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],name,url,iconimage)))
        liz.addContextMenuItems(cmenu, replaceItems=False) 
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def popup(url,name):
        message=open_url2(url)
        if len(message)>1:
                path = userdata
                comparefile = os.path.join(os.path.join(path,''), name+'.txt')
                if not os.path.exists(comparefile):
                    file(comparefile, 'w').close()
                r = open(comparefile)
                compfile = r.read()       
                if compfile == message:pass
                else:
                        showText('[B][COLOR red]E[/COLOR][COLOR white]volve[/COLOR][/B] [B][COLOR red]I[/COLOR][COLOR white]nformation[/COLOR][/B]', message)
                        text_file = open(comparefile, "w")
                        text_file.write(message)
                        text_file.close()
  
def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(500)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
	try:
	    xbmc.sleep(10)
	    retry -= 1
	    win.getControl(1).setLabel(heading)
	    win.getControl(5).setText(text)
	    return
	except:
	    pass

def SHOWMULTIPLEIMAGES(name):
        global Icon
        global Next
        global Previous
        global window
        global Quit
        global images
        comparefile = os.path.join(os.path.join(userdata,''), name+'.txt')
        r = open(comparefile)
        compfile = r.read()
        images=re.compile('<image>(.+?)</image>').findall(compfile)
        selfAddon.setSetting('pos','0')
	window= pyxbmct.AddonDialogWindow('')
        artpath = '/resources/art'
        next_focus = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + artpath, 'next_focus.png'))
        next_no_focus = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + artpath, 'next1.png'))
        prev_focus = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + artpath, 'previous_focus.png'))
        prev_no_focus = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + artpath, 'previous.png'))
        close_focus = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + artpath, 'close_focus.png'))
        close_no_focus = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + artpath, 'close.png'))
        bg = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + artpath, 'main-bg1.png'))
        window.setGeometry(1300, 720, 100, 50)
        background=pyxbmct.Image(bg)
        window.placeControl(background, -10, -10, 130, 70)
        text = '0xFF000000'
	Previous = pyxbmct.Button('',focusTexture=prev_focus,noFocusTexture=prev_no_focus,textColor=text,focusedColor=text)
	Next = pyxbmct.Button('',focusTexture=next_focus,noFocusTexture=next_no_focus,textColor=text,focusedColor=text)
	Quit = pyxbmct.Button('',focusTexture=close_focus,noFocusTexture=close_no_focus,textColor=text,focusedColor=text)
	Icon=pyxbmct.Image(images[0], aspectRatio=2)
	window.placeControl(Previous ,102, 1,  10, 10)
	window.placeControl(Next ,102, 40, 10, 10)
	window.placeControl(Quit ,102, 21, 10, 10)
	window.placeControl(Icon, 0, 0, 100, 50)
	Previous.controlRight(Next)
	Previous.controlUp(Quit)
	window.connect(Previous,PREVIOUSPAGE)
	window.connect(Next,NEXTPAGE)   
	Previous.setVisible(False)
        window.setFocus(Quit)
        Previous.controlRight(Quit)
        Quit.controlLeft(Previous)
        Quit.controlRight(Next)
        Next.controlLeft(Quit)
	window.connect(Quit, window.close)
	window.doModal()
	del window
        
def NEXTPAGE():
        currentpos=int(selfAddon.getSetting('pos'))
        nextpos=int(currentpos)+1
        selfAddon.setSetting('pos',str(nextpos))
        imagecount=len(images)
        Icon.setImage(images[int(nextpos)])
        Previous.setVisible(True)
        if int(nextpos) ==int(imagecount)-1:
                Next.setVisible(False)
       
def PREVIOUSPAGE():
        currentpos=int(selfAddon.getSetting('pos'))
        prevpos=int(currentpos)-1
        selfAddon.setSetting('pos',str(prevpos))
        Icon.setImage(images[int(prevpos)])
        Next.setVisible(True)
        if int(prevpos) ==0:
                Previous.setVisible(False)

def GETFAVS(url,fanart):
        selfAddon.setSetting('favlist','yes')
        filedata = None
	file = open(favs, 'r')
	filedata = file.read().replace('\n','').replace('\r','')
	match=re.compile("<item>(.+?)</item>",re.DOTALL).findall(filedata)
	for item in match:
                ACTION(name,url,icon,fanart,item)
        selfAddon.setSetting('favlist','no')
                                    
def ADDTOFAVS(name,url,iconimage,fanart):
        favtype=selfAddon.getSetting('favtype')
	url=url.replace(' ','%20')
	iconimage=iconimage.replace(' ','%20')
        if '<>' in url:
                imdbnum=url.split('<>')[0]
                season=url.split('<>')[1]
                episode=url.split('<>')[2]
                showyear=url.split('<>')[3]
                episodeyear=url.split('<>')[4]
                string='<FAV><item>\n<title>'+name+'</title>\n<meta>tvep</meta>\n<nan>tvshow</nan>\n<showyear>'+showyear+'</showyear>\n<imdb>'+imdbnum+'</imdb>\n<season>'+season+'</season>\n<episode>'+episode+'</episode>\n<episodeyear>'+episodeyear+'</episodeyear>\n<thumbnail>'+iconimage+'</thumbnail>\n<fanart>'+fanart+'</fanart></item></FAV>\n'
        elif len(url)==9:
                string='<FAV><item>\n<title>'+name+'</title>\n<meta>movie</meta>\n<nan>movie</nan>\n<imdb>'+url+'</imdb>\n'+'<thumbnail>'+iconimage+'</thumbnail>\n<fanart>'+fanart+'</fanart></item></FAV>\n'       
        else:
                string='<FAV><item>\n<title>'+name+'</title>\n<'+favtype+'>'+url+'</'+favtype+'>\n'+'<thumbnail>'+iconimage+'</thumbnail>\n<fanart>'+fanart+'</fanart></item></FAV>\n'         
	favsdb = open(favs,'a')
	favsdb.write(string)
	favsdb.close()
	
def REMFAVS(name,url,iconimage):
        print name
	filedata = None
	file = open(favs, 'r')
	filedata = file.read()
	newlist=''
	match=re.compile('<item>(.+?)</item>',re.DOTALL).findall(filedata)
	for data in match:
		string='\n<FAV><item>\n'+data+'</item>\n'
		if name in data:
                        print 'xxxxxxxxxxxxxxxxx'
			string=string.replace('item',' ')
		newlist=newlist+string
	file = open(favs, 'w')
	file.truncate()
	file.write(newlist)
	file.close()
	xbmc.executebuiltin('Container.Refresh')

def RDCHECK(url):
        try:
                domain=url.split('/')[2].replace('www.','')
                file = open(rd, 'r')
                rdhost = file.read()
                if domain in rdhost: return '[COLOR springgreen] (RD)[/COLOR]'
                else: return ''
        except:return ''

def OPENNANSCRAPERSETTINGS():
        xbmcaddon.Addon('script.module.nanscrapers').openSettings()

def OPENURLRESOLVERSETTINGS():
        xbmcaddon.Addon('script.module.urlresolver').openSettings()

def OPENMETASETTINGS():
        xbmcaddon.Addon('script.module.metahandler').openSettings()

def view(link):
        try:
                layout= re.compile('<layouttype>(.+?)</layouttype>').findall(link)[0]
                if layout=='thumbnail': xbmc.executebuiltin('Container.SetViewMode(500)')              
                else:xbmc.executebuiltin('Container.SetViewMode(50)')  
        except:pass
        

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None; description=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass
try: description=str(params["description"])
except: pass

if mode==None or url==None or len(url)<1: MAINMENU()
elif mode==1:RUNNER(name,url,iconimage,fanart)
elif mode==2:LINKTEST(name,url,iconimage,description)
elif mode==3:GETMULTI(name,url,iconimage)
elif mode==4:PLAYLINK(name,url,iconimage)
elif mode==5:SEARCH()
elif mode==6:GETIPTV(url,iconimage)
elif mode==7:SHOWIMAGE(url)
elif mode==8:SHOWMULTIPLEIMAGES(name)
elif mode==9:DOTEXTBOX(name,url)
elif mode==10:DOLBSCRAPER(name,url,iconimage,fanart)
elif mode==11:TRAILER(url)
elif mode==12:OPENURLRESOLVERSETTINGS()
elif mode==13:OPENMETASETTINGS()
elif mode==15:SCRAPEMOVIE(name,url,iconimage)
elif mode==16:PLAYLINKNODIALOG(name,url,iconimage)
elif mode==17:DOOK(name,url)
elif mode==18:DOSCRAPER(name,url,iconimage,fanart)
elif mode==19:DONAN(name,url,iconimage,fanart)

elif mode==20:ADDTOFAVS(name,url,iconimage,fanart)
elif mode==21:REMFAVS(name,url,iconimage)
elif mode==22:GETFAVS(url,fanart)
elif mode==23:DOIPLAYER(name,url,iconimage,fanart)
elif mode==24:GET_LATESTTVLINKS(name,url,iconimage,fanart)
elif mode==25:OPENNANSCRAPERSETTINGS()

elif mode==26:MOVIEMENU(name,url,iconimage,fanart)
elif mode==27:TVSHOWMENU(name,url,iconimage,fanart)
elif mode==28:GET_LATESTEPISODES(name,url,iconimage,fanart)
elif mode==29:GET_POPULARSERIESCONTENT(name,url,iconimage,fanart)
elif mode==30:GET_NEWSERIESCONTENT(name,url,iconimage,fanart)
elif mode==31:LIST_SEASONS(name,url,iconimage,fanart)
elif mode==32:GET_TVSCHEDULE(name,url,iconimage,fanart)
elif mode==33:TVSEARCH(url)
elif mode==34:GET_MOVIESCHEDULE(name,url,iconimage,fanart)
elif mode==35:GET_LATESTMOVIECONTENT(name,url,iconimage,fanart)







xbmcplugin.endOfDirectory(int(sys.argv[1]))
