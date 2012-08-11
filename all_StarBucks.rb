#!/usr/bin/ruby -Ku
require 'kconv'
require 'open-uri'
require 'csv'

$print_header = true

def remove_space(str)
	str.gsub!(%r{<br\s*/>}, " ")
	str.gsub!(/\s+/, " ")
	return str
end

Weekday = 0
Friday	= 1
Saturday= 2
Sunday	= 3	# 日祝
#  ["月～金：07:00～21:00", "定休日：不定休", "07:00～21:00"]
def parse_bzhour(str_v)
	def remove_dot(a_str)
		return a_str.gsub("・", "")
	end
	bzhour = [nil, nil, nil, nil]	# 月〜木　金　土 日祝

	str_v.each do |str|
		tmp = str.split(/：/)
		if tmp[0] == "定休日"
			#不定休の時はbzhourを変更しない
			if tmp[1] == "不定休"
				;# 休みなしの時は変えない 
			else
				if tmp[1] =~ /土/ then bzhour[Saturday] = "" end
				if tmp[1] =~ /日/ then bzhour[Sunday] = "" end
				if tmp[1] =~ /祝/ then bzhour[Sunday] = "" end
				if tmp[1] =~ /金/ then bzhour[Friday] = "" end
			end
		elsif tmp.size == 2
			tmp[1].sub!("～", "-")
			if tmp[0] == "月～金"
				bzhour[Weekday] = tmp[1]
				bzhour[Friday]  = tmp[1]
			elsif tmp[0] == "月～木"
				bzhour[Weekday] = tmp[1]
			elsif tmp[0] == "月～土"
				bzhour[Weekday] = tmp[1]
				bzhour[Friday]  = tmp[1]
				bzhour[Saturday]= tmp[1]
			else
				remove_dot(tmp[0]).each_char do |c|
					case c
					when "土"
						bzhour[Saturday] = tmp[1]
					when "日"
						bzhour[Sunday] = tmp[1]
					when "金"
						bzhour[Friday] = tmp[1]
					when "祝"
						;
					end
				end
			end
		elsif tmp.size == 1	#多分これが毎日いっしょのパターン
			tmp[0].sub!("～", "-")
			bzhour[Weekday] = tmp[0]
			bzhour[Friday]  = tmp[0]
			bzhour[Saturday]= tmp[0]
			bzhour[Sunday]  = tmp[0]
		end
	end
	return bzhour
end


#そのリストのページのリストは有効かどうか
def validListP(body)
	#	1</span>-<span class="fwB">10</span>件
	content = body
	pattern = %r{<span\s+class=.*?>(\d+)</span>-<span\s+class=.*?>(\d+)</span>}
	if content =~ pattern
		start = $1.to_i
		finish= $2.to_i
		if start <= finish
			return true
		else
			return false
		end
	else
		return false
	end
end

#ListPattern = %r{<td\s+class="storeName"><a\shref="/store/search/detail\.php\?id=(\d+)&search_condition=.*?&pref_code=(\d+)&pageID=(\d+)">(.*?)</a><br>\s?<span\s+>class="fontS">\s?\((.*?)\)\s?</span> }
ListPattern = %r{<td\s+class="storeName"><a\shref="/store/search/detail\.php\?id=(\d+)&search_condition=.*?&pref_code=(\d+)&pageID=(\d+)">(.*?)</a>}
PlacePattern = %r{<span\s+class=".*?">\s?（(.*?)）\s?</span>}
BisHourPattern = %r{<td\s+class="vaT">\s+(.*?)</td>\s+<td class="vaT">\s+(.*?)</td>\s+</tr>}m
TelephonePattern=%r{<td\s+class="telephone\s+txtAC">(.*?)</td>}
SeatsPattern= 	%r{<td\s+class="seats\s+txtAC">(\d*)</td>}

#店舗一覧から情報を取得する
def parse_listpage(content)
	one_page = Array.new
	pos = 0
	while	pos = content.index(ListPattern, pos + 1)	# 店名, ID
		res = Regexp.last_match 
		data = []
		data << res[1]	#id
		data << res[4]	#店名
		id = res[1]
		pos = content.index(PlacePattern, pos + 1)
		data << $1
		
		pos = content.index(BisHourPattern, pos + 1)	#時間 
		m = Regexp.last_match
		jikoku = []
		jikoku += m[1].gsub(/\s+/,"").split(/<br.*?>/)
		jikoku += m[2].gsub(/\s+/,"").split(/<br.*?>/)
		ret =  parse_bzhour(jikoku)
		ret.each { |time| data << time }
		pos = content.index(TelephonePattern, pos + 1)
		data << Regexp.last_match[1]

		if  content.index(SeatsPattern, pos+1)
			data << $1
		else
			data << ""
		end
		data << "http://www.starbucks.co.jp/store/search/detail.php?id=#{id}"
		one_page << data
	end
	return one_page
end

def all_star_bucks(outputpath = nil)
	csv = outputpath ? CSV.open(outputpath, "w") : nil

	#pref_code = 13	#Tokyo
	csv << ["id", "店名", "地区",  "月〜木", "金", "土", "日", "電話番号", "座席数", "URL"]	if $print_header == true && csv

	1.upto(47) do |pref_code|
		id_list = []
		pageID = 1
		flg = true
		while flg == true
			page = open("http://www.starbucks.co.jp/store/search/result_store.php?pref_code=#{pref_code}&pageID=#{pageID}")
			body = page.read
			if validListP(body)
				list = parse_listpage(body)
				list.each do  |record| 
					if not id_list.include?(record[0])
						if csv then csv << record else p record end	#else p record end }
						id_list << record[0]
					end
				end
				pageID += 1
			else
				flg = false
			end
		end
	end
	if csv then csv.close end 
	
end

# For Debugging
def one_list_StarBucks(pref_code, pageID)
	# search_by_address_flgを立たせたほうがいいんかな
	page = open("http://www.starbucks.co.jp/store/search/result_store.php?free_word=&search_type=1&pref_code=#{pref_code}&city=&search_by_address_flg=1&x=60&y=22&store_type_3=&pageID=#{pageID}")
	body = page.read
	if validListP(body) then print parse_listpage(body)	end
end

all_star_bucks("StarBucks_All_____.csv")

