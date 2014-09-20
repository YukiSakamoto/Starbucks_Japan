# -*- coding: utf-8 -*-

#XXX
# To use, see the bottom of this code"

import urllib2
import lxml.html
import re

class Store:
    def __init__(self, store_id):
        self.__id = store_id
        self.__details = dict()
    def __setitem__(self, name, value):
        self.__details[name] = value
    def __getitem__(self, name):
        if name == 'id':
            return self.__id
        #elif name not in self.__details:
        #    return u""
        else:
            return self.__details[name]
    def __str__(self):
        retval = "id: %3d, name: %s" % (self['id'], self['name'])
        return retval
    def as_record(self, keys):
        retval = list()
        for k in keys:
            s = u""
            if k == 'id':
                s = u"%d" % self.__id
            elif k not in self.__details:
                # Guard
                s = u""
            elif k == 'lan':
                if self['has_lan_service'] is False:
                    s = u"None"
                else:
                    # Enum wireless lan services
                    fst = True
                    for lan_name in self['lan']:
                        if fst == True:
                            fst = False
                        else:
                            s += u"/ "
                        tmp = u"%s" % lan_name
                        s += tmp
            else:
                s = u"%s" %self[k]
            retval.append( s.encode('utf_8') )
        return retval

def parse_bzhour(desc, data):
    base = desc.strip().replace(" ", "")
    if len(base) == 0:
        return
    #print base
    record = base.split(u"：")
    if len(record) == 2:
        if record[0] == u"定休日":
            if record[1] == u"不定休":
                pass
            else:
                if re.search(u"土", record[1]):
                    data['saturday'] = "None"
                if re.search(u"日", record[1]):
                    data['sunday'] = "None"
                if re.search(u"金", record[1]):
                    data['friday'] = "None"
        else:
            if record[0] == u"月～木":
                data['weekday'] = record[1]
            elif record[0] == u"月～金":
                data['weekday'] = record[1]
                data['friday'] = record[1]
            elif record[0] == u"月～土":
                data['weekday'] = record[1]
                data['friday'] = record[1]
                data['saturday'] = record[1]
            else:
                if re.search(u"土", record[0]):
                    data['saturday'] = record[1]
                if re.search(u"日", record[0]):
                    data['sunday'] = record[1]
                if re.search(u"金", record[0]):
                    data['friday'] = record[1]
    elif len(record) == 1:
        data['weekday'] = record[0]
        data['friday'] = record[0]
        data['saturday'] = record[0]
        data['sunday'] = record[0]
    else:
        pass

def parse_listpage(pref_code, pageId):
    def extract_storeid(url):
        match = re.search(
                r'/store/search/detail.php\?id=(\d*)&search_condition',
                str(url) )  
        if match is None:
            return None
        else:
            return int(match.group(1))

    datas = list()
    url = "http://www.starbucks.co.jp/store/search/result_store.php?pref_code=%d&pageID=%d" % (pref_code, pageId)
    html = urllib2.urlopen(url).read()
    root = lxml.html.fromstring(html)
    searchResult = root.xpath('//p[@class="searchResultTxt"]/span[@class="fwB"]/text()')
    
    if len(searchResult) == 0:  # Error check for the prefecture where no store exists.
        return list()
    (start, end) = ( int(searchResult[1]), int(searchResult[2]))
    if end < start:
        return list()

    table = root.xpath('//table[@class="table"]/tbody/tr')
    for row in table:
        store = row.xpath('./td[@class="storeName"]/a')
        store_name = row.xpath('./td[@class="storeName"]/a/text()')
        region = row.xpath('./td[@class="storeName"]/span/text()')
        tel  = row.xpath('./td[@class="telephone txtAC"]/text()')
        seats= row.xpath('./td[@class="seats txtAC"]/text()')
        has_lan_service = row.xpath('./td[@class="wirelessHotspot txtAC"]/text()')
        business_hour = row.xpath('./td[@class="businessHours"]/table[@class="timeTable"]/tr/td[@class="vaT"]/text()')

        data = Store(extract_storeid(store[0].attrib['href']))
        data['name'] = store_name[0]
        data['region'] = region[0].rstrip(u")）").lstrip(u"(（")
        data['tel']  = tel[0]
        data['seats']= seats[0]
        #import ipdb; ipdb.set_trace()
        if re.search(u"〇", has_lan_service[0]):
            data['has_lan_service'] = True
        else:
            data['has_lan_service'] = False

        #print "======================================================="
        #print data['name']
        #print data['has_lan_service']

        for bz in business_hour:
            parse_bzhour(bz, data)
        #print "Weekday  : %s "% data['weekday']
        #print "Friday   : %s" % data['friday']
        #print "Saturday : %s" % data['saturday']
        #print "Sunday   : %s" % data['sunday']
        datas.append(data)

    return datas

def parse_storedetail(store_data):
    store_id = store_data['id']
    url = 'http://www.starbucks.co.jp/store/search/detail.php?id=%d' % store_id
    html = urllib2.urlopen(url).read()
    root = lxml.html.fromstring(html)
    detail_table = root.xpath('//table[@class="table mapTable"]/tr')
    for row in detail_table:
        label = row.xpath('./th/text()')[0]
        if label == u"住所":
            pass
            #value = row.xpath('./td/text()')
            #print value[0], value[1]
        elif label == u"電話番号":
            pass
            #value = row.xpath('./td/text()')[0]
            #print value[0]
        elif label == u"無線LAN":
            values = row.xpath('./td/span[@class="lanService"]/img')
            lan_names = list()
            for val in values:
                lan_names.append( val.attrib['alt'] )
            store_data['lan'] = lan_names

def scraping_per_prefecture(prefcode, survey_detail = True, verbose = True):
    store_list = list()
    i = 1
    while True:
        a_listpage = parse_listpage(prefcode, i)
        if len(a_listpage) == 0:
            break
        else:
            store_list.extend(a_listpage)
        i += 1

    if survey_detail:
        for index, store in enumerate(store_list):
            if verbose:
                print u"%s  (%d / %d)" % (store['name'], index + 1, len(store_list))
            parse_storedetail(store)
        #ok, parse done
    return store_list

pref_id_dict = { 
        1: "Hokkaido",  2: "Aomori",    3: "Iwate",     4: "Miyagi",    5: "Akita", 6: "Yamagata",  7: "Fukushima",
        8: "Tokyo",     9: "Ibaraki",   10:"Gunnma",    11:"Saitama",   12:"Chiba", 13:"Tokyo",     14:"Kanagawa",
        15:"Niigata",   16:"Toyama",    17:"Ishikawa",  18:"Fukui",     19:"Yamanashi", 20: "Nagano",  
        21:"Gifu",      22:"Sizuoka",   23:"Aichi",     24:"Mie",   
        25:"Shiga",     26:"Kyoto",     27:"Osaka",     28:"Hyogo",     29:"Nara",  30:"Wakayama",
        31:"Tottori",   32:"Shimane",   33:"Okayama",   34:"Hiroshima", 35:"Yamaguchi",
        36:"Tokushima", 37:"Kagawa",    38:"Ehime",     39:"Kochi",     
        40:"Fukuoka",   41:"Saga",      42:"Nagasaki",  43:"Kumamoto",  44:"Oita",  45:"Miyazaki",  46:"Kagoshima", 47:"Okinawa"
        }

#============================================================
prefid = 32
filename = "%s.csv" % pref_id_dict[prefid]
print_header = True
#============================================================

store_list = scraping_per_prefecture(prefid, True, True)
import csv
f = open(filename, 'w')
writer = csv.writer(f)
columns = ['id', 'name','region','weekday', 'friday', 'saturday', 'sunday', 'tel', 'seats', 'lan' ]
header  = ['id', '店名','地域','月〜木', '金', '土', '日', 'Tel', 'Seats', '無線Lanサービス' ]
if print_header:
    writer.writerow(header)
for i in store_list:
    writer.writerow(i.as_record(columns))
f.close()
