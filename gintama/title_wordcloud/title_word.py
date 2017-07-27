filepath = r'D:\DownLoad\python\simple_spiders\gintama\gintama.txt'
filepath2 = r'D:\DownLoad\python\simple_spiders\gintama\title_wordcloud\gintamatitle.txt'
with open(filepath, 'r') as f:
	title_d = [eval(x) for x in f.readlines()]
gintamatitle = [x['gintamatitle'] for x in title_d]
with open(filepath2, 'w') as f:
	f.writelines(str(x) + '\n' for x in gintamatitle)
