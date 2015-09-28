#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import lxml.html
import re

import sys
import codecs

import csv
import os.path

pref_id_dict = { 
        1: "Hokkaido",  2: "Aomori",    3: "Iwate",     4: "Miyagi",    5: "Akita", 6: "Yamagata",  7: "Fukushima",
        8: "Tochigi",   9: "Ibaraki",   10:"Gumma",    11:"Saitama",    12:"Chiba", 13:"Tokyo",     14:"Kanagawa",
        15:"Niigata",   16:"Toyama",    17:"Ishikawa",  18:"Fukui",     19:"Yamanashi", 20: "Nagano",  
        21:"Gifu",      22:"Sizuoka",   23:"Aichi",     24:"Mie",   
        25:"Shiga",     26:"Kyoto",     27:"Osaka",     28:"Hyogo",     29:"Nara",  30:"Wakayama",
        31:"Tottori",   32:"Shimane",   33:"Okayama",   34:"Hiroshima", 35:"Yamaguchi",
        36:"Tokushima", 37:"Kagawa",    38:"Ehime",     39:"Kochi",     
        40:"Fukuoka",   41:"Saga",      42:"Nagasaki",  43:"Kumamoto",  44:"Oita",  45:"Miyazaki",  46:"Kagoshima", 47:"Okinawa"
        }

#============================================================
# Parameters

#cache
load_list_cache = False
save_list_cache = False
load_storedetail_cache = True
save_storedetail_cache = True
savedir = "starbucks"

# list that contains the numbers of prefectures to survey
region  = range(1, 48)

# output filename
filename = "20150928.csv"

# Progress Output
verbose = False
#============================================================

def verbose_output(text):
    if verbose == True:
        sys.stderr.write(text)

def create_storedetail_filepath(storeid, directory):
    return "%s/store_%d.html" % (directory, storeid)

def create_storelist_filepath(prefid, directory):
    return "%s/list_%d.html" % (directory, prefid)

def fetch_detailpage(storeid):
    storeurl = "http://www.starbucks.co.jp/store/search/detail.php?id=%d" % storeid
    html = urllib2.urlopen(storeurl).read()
    return html

def parse_bzhour(text_contents):
    weekday = ""
    friday  = ""
    saturday= ""
    sunday  = ""
    cannot_parse = ""
    if len(text_contents) == 0:
        pass
    else:
        for i in text_contents:
            record = i.split(u"：")
            if len(record) == 1:
                weekday = friday = saturday = sunday = record[0].encode('utf-8')
            elif len(record) == 2:
                record[1] = record[1].replace('\r', '')
                if record[0] == u"月～木":
                    weekday = record[1].encode('utf-8')
                elif record[0] == u"月～金":
                    weekday = friday = record[1].encode('utf-8')
                elif record[0] == u"日祝" or record[0] == u"祝日":
                    sunday = record[1].encode('utf-8')
                elif record[0] == u"月～土":
                    saturday = friday = weekday = record[1].encode('utf-8')
                elif record[0] == u"金":
                    friday = record[1].encode('utf-8')
                elif record[0] == u"土":
                    saturday = record[1].encode('utf-8')
                elif record[0] == u"金土":
                    saturday = friday = record[1].encode('utf-8')
                elif record[0] == u"土日祝":
                    sunday = saturday = record[1].encode('utf-8')
                elif record[0] == u"金土日祝":
                    sunday = saturday = friday = record[1].encode('utf-8')
                else:
                    cannot_parse = i
            else:
                print "many record"
                for i in record:
                    print i.encode('utf-8')
    return {'weekday' : weekday, 'friday': friday, 'saturday': saturday, 'sunday': sunday, 'unknown_openhour' : cannot_parse}

def parse_detailpage(detailpage_raw_data):
    #detailpage_raw_data = fetch_detailpage(storeid)
    root = lxml.html.fromstring(detailpage_raw_data)
    retval = dict()

    detailinfotable = root.xpath('//table[@class="storeInfo"]/tr')
    for row in detailinfotable:
        item = row.xpath('./td[@class="item"]/text()')[0]
        detail = row.xpath('./td[@class="detail"]')
        if item == u"定休日":
            retval["closeday"] = detail[0].text.strip().encode('utf-8')
        elif item == u"電話番号":
            retval["telnum"] = detail[0].text.strip().encode('utf-8')
        elif item == u"無線LAN":
            available_services = detail[0].xpath('ul[@class="lan"]/li')
            retval["lan"] = []
            for service in available_services:
                retval["lan"].append(service[0].attrib['alt'].encode('utf-8') )
        elif item == u"営業時間":
            #import ipdb; ipdb.set_trace()
            #print detail[0].text.encode('utf-8')
            text_contents =  detail[0].text_content().strip().replace(u"　",u"").replace(u" ", u"").split(u"\n")
            #for i in  text_contents:
            #    print i.encode('utf-8')
            retval.update( parse_bzhour(text_contents) )
            #print "-------------------------------------------------------------"

    return retval

def extract_storeid(url):
    match = re.search(r'id=(\d*)', str(url) )
    if match is None:
        return None
    else:
        return int(match.group(1))

def fetch_listpage(prefcode):
    url = 'http://www.starbucks.co.jp/store/search/result.php?search_type=1&pref_code=%d' % prefcode
    html = urllib2.urlopen(url).read()
    return html

def scraping_prefecture(listpage_raw_data):
    store_list = list()
    root = lxml.html.fromstring(listpage_raw_data)
    searchResult = root.xpath('//div[@class="detailContainer"]')
    verbose_output("{0} stores found: ".format(len(searchResult))  )
    for storedata in searchResult:
        store_data = dict()
        storeurl = storedata.xpath('./div[@class="detailInfo"]/div[@class="storeSearchButtons"]/p[@class="searchButtonDetail"]/a')[0].attrib['href']
        store = storedata.xpath('./p[@class="storeName"]')[0].text
        address = storedata.xpath('./p[@class="storeAddress"]')[0].text

        store_data['id'] = extract_storeid(storeurl)
        store_data['store'] = store.encode('utf-8')
        store_data['address'] = address.encode('utf-8')
        store_list.append(store_data)
    verbose_output("Done\n")
    return store_list

def as_record(keys, store_data):
    retval = []
    for k in keys:
        if store_data.has_key(k):
            if k == 'lan':
                s = ""
                fst = True
                for i in store_data['lan']:
                    if fst == True:
                        s += i
                        fst = False
                    else:
                        s += ", %s" % i
                retval.append( s )
            else:
                retval.append( store_data[k] )
        elif k == 'openhour':
            if store_data.has_key('weekday') and store_data.has_key('friday') and store_data.has_key('saturday') and store_data.has_key('sunday'):
                    retval.append(store_data['weekday'])
                    retval.append(store_data['friday'])
                    retval.append(store_data['saturday'])
                    retval.append(store_data['sunday'])
        else:
            retval.append("")
    return retval;

def load_or_fetch_storelist(prefid, directory, load = True, save = True) :
    listfilepath = create_storelist_filepath(prefid, directory)
    if load == True and os.path.exists(listfilepath):
        f = open(listfilepath, 'r')
        storelist_html = f.read()
        f.close()
        return storelist_html
    else:
        storelist_html = fetch_listpage(prefid)
        if save == True:
            f = open(listfilepath, 'w')
            f.write(storelist_html)
            f.close()
        return storelist_html

def load_or_fetch_storedetail(storeid, directory, load = True, save = True):
    detailfilepath = create_storedetail_filepath(storeid, directory)
    if load == True and os.path.exists(detailfilepath):
        f = open(detailfilepath, 'r')
        detail_html = f.read()
        f.close()
        return detail_html
    else:
        detail_html = fetch_detailpage(storeid)
        if save == True:
            f = open(detailfilepath, 'w')
            f.write(detail_html)
            f.close()
        return detail_html

def survey_prefecture(prefid, savedir, list_load = False, list_save = True, store_load = True, store_save = True):
    storelist_html = load_or_fetch_storelist(prefid, savedir, list_load, list_save)
    data = scraping_prefecture(storelist_html)
    for i in data:
        detail_html = load_or_fetch_storedetail(i['id'], savedir, store_load, store_save)
        i.update( parse_detailpage(detail_html) )
    return data

def check_region_parameter(region_list):
    fst = True
    verbose_output("Surbey: ")
    for i in region_list:
        if not i in range(1,48):
            raise ValueError
        else:
            if fst == False:
                verbose_output("/")
            verbose_output("{0}".format(pref_id_dict[i]) )
            fst = False
    verbose_output("\n")

check_region_parameter(region)
data = []
for i in region:
    verbose_output( "{0}({1}): ".format(i, pref_id_dict[i]) )
    previous_length = len(data)
    data += survey_prefecture(i, savedir, load_list_cache, save_list_cache, load_storedetail_cache, save_storedetail_cache)

verbose_output( "Scraping Done. Next, write as CSV({0})\n".format(filename) )
f = open(filename, 'w')
writer = csv.writer(f)
writer.writerow(['店名', 'id', '月曜日〜木曜日開店時間', '金曜日開店時間', '土曜日開店時間', '日曜日開店時間', '電話番号', '無線LAN'] )
for i in data:
    writer.writerow(as_record(['store', 'id', 'openhour', 'telnum', 'lan'],  i ) )
f.close()
