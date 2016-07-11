import os
import csv
import argparse
import unicodedata as ud
import datetime
"""
Simple script to generate whois.conf file from CSV eport from https://domainpunch.com/tlds/

Author: Njoroge John
"""
def generate(tld_file,out):
	if(not os.path.exists(tld_file)):
		print("TLD file <%s>not found"%tld_file)
		return
	tld=csv.DictReader(open(tld_file,'r'))
	output="whois.conf"
	if(out is not None and os.path.isdir(out)):
		if(out.endswith('/')):
			output="{0}whois.conf".format(out)
		else:
			output="{0}/whois.conf".format(out)
	#Date
	dates=datetime.datetime.today().strftime("%d/%m/%Y")
	text="##\n# WHOIS servers for new TLDs (http://www.iana.org/domains/root/db)\n# Current as of {0}\n ##\n\n".format(dates)
	file_name=open(output,'w');
	file_name.write(text) #Write header
	for row in tld:
		try:
			#Adding UTF-8 removes all TLD that cannot be represented in english 0-256 characters
			line="\\.{0:<}$\t{1:<}\n".format(row.get("TLD"),row.get("Whois Server")).encode('utf-8')
			file_name.write(line)
		except Exception as e:
			print("Error adding: {}".format(row))
def main():
	parser=argparse.ArgumentParser(description="Simple whois.conf file generator")
	parser.add_argument('-f','--file',help="Filename that contains the whois record, This should end with .csv and be valid CSV file.",nargs='?',default='./tld_table.csv')
	parser.add_argument('-d','--dir',help="Directory to generate file in, may require sudo. Directory must exist.",nargs='?',default='./')
	args=parser.parse_args()
	generate(args.file,args.dir)
if (__name__=='__main__'):
	main()
