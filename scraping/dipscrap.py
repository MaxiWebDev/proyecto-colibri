# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.diputado import Diputado, Asiento
from models.partido import Partido, Grupo
from mongoengine import connect
import re
from settings import DIPUTADOS_URL, DATABASE
from scraper import create_curl
from bs4 import BeautifulSoup

def get_urls():
    url = DIPUTADOS_URL
    has_next = True
    url_fichas = []

    while(has_next):
        curl_request = create_curl(url)
        curl_request.perform()
        html_doc = curl_request.body.getvalue()
        curl_request.close()
        soup = BeautifulSoup(html_doc)
        list_dip = soup.findAll(lambda tag: tag.name == 'a' and tag.parent.name == 'li' and tag.has_key('class'), "")
        for dip in list_dip:
            url_fichas.append(dip.attrs['href'].__str__())

        paginacion = soup.find(lambda tag: tag.name == 'a' and tag.parent.name == 'ul' and tag.has_key('class'), "", text='Página Siguiente')
        if not paginacion:
            has_next = False
        else:
            url = paginacion.attrs['href'].__str__()

        #has_next = False

    return url_fichas

def get_dips(url_fichas):
    m = []
    for url in url_fichas:
        curl = create_curl(url)
        curl.perform()
        curl.http_code = curl.getinfo(curl.HTTP_CODE)
        m.append(curl)
        curl.close()

    return m

def parser_dip(m):
    connection = connect(DATABASE)
    # get result
    for c in m:
        print "%-53s http_code %3d" % (c.url, c.http_code)

        html_doc = c.body.getvalue()
        soup = BeautifulSoup(html_doc)
        exist_dip = Diputado.objects(ficha=c.url)
        if exist_dip:
            dip_instance = exist_dip[0]
        else:
            dip_instance = Diputado()
        
        if c.http_code == 200:
            #get name
            nombre_soup = soup.find(id='curriculum').find('div', 'nombre_dip')
            if nombre_soup:
                dip_instance.nombre = nombre_soup.text.split(',')[1].strip().encode('utf8')
                dip_instance.apellidos = nombre_soup.text.split(',')[0].strip().encode('utf8')
            
            #get url
            dip_instance.ficha = c.url
    
            #get email
            correo_soup = soup.find(id='curriculum').find(lambda tag: tag.name == 'a' and tag.parent.name == 'div' and tag.has_key('title'), text=re.compile("([a-zA-Z0-9]*[\.])*@congreso.es"))
            if correo_soup:
                dip_instance.correo = correo_soup.text.split()[0].encode('utf8')
            #get web
            web_soup = soup.find(id='curriculum').find(lambda tag: tag.name == 'a' and tag.parent.name == 'div' and tag.has_key('title'), text=re.compile("https?:\/\/"))
            if web_soup:
                dip_instance.web = web_soup.attrs['href'].encode('utf8')
            #get twitter
            twitter_soup = soup.find(id='curriculum').findAll(lambda tag: tag.name == 'img' and tag.parent.name == 'a',src=re.compile("codigoTipoDireccion=tw"))
            if twitter_soup:
                dip_instance.twitter = twitter_soup[0].parent.attrs['href'].encode('utf8')

            circuns_soup = soup.find(id='curriculum').find('div', 'dip_rojo', text=re.compile("Diputad[ao] por [a-zA-Z]?"))
            if circuns_soup:
                circuns_soup = re.sub(r'Diputad[ao] por ', '' ,circuns_soup.text).strip()
                circuns_soup = re.sub(r'\.$', '' ,circuns_soup)
                dip_instance.circunscripcion = circuns_soup.encode('utf8')

            
            dip_instance.save()
    
            print "**********", dip_instance.nombre, "**********"
            print "************************************************************************************************"

    connection.disconnect()

#Get urls
url_fichas = get_urls()

#Get dips
if len(url_fichas) > 0:
    m = get_dips(url_fichas)
    parser_dip(m)
