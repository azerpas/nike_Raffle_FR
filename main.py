# coding=utf-8
import requests, json, time, random, datetime, threading, pickle

sitekey = "6LcMxjMUAAAAALhKgWsmmRM2hAFzGSQqYcpmFqHx"

		
class Raffle(object):
	def __init__(self):
		self.s = requests.session()
		# "https://colette.sneakers-raffle.fr/","https://starcow.sneakers-raffle.fr/"
		self.shoes = [
		{"url":"product/nike-air-jordan-1/","shoe_id":"2","shoe_name":"Nike Air Jordan 1","imgURL":"AirJordan.jpg"},
		{"url":"product/nike-blazer/","shoe_id":"3","shoe_name":"Nike Blazer","imgURL":"Blazer.jpg"}]
		self.sites = [
			{"url":"https://shinzo.sneakers-raffle.fr/","siteid":"2","nomtemplate":"nike-raffle-confirm-shinzo"},
			{"url":"https://thebrokenarm.sneakers-raffle.fr/","siteid":"3","nomtemplate":"nike-raffle-confirm-the-broken-arm"},
			{"url":"https://colette.sneakers-raffle.fr/","siteid":"4","nomtemplate":"nike-raffle-confirm-colette"}
			]
		# interval etc

	def register(self,identity):
		# For each site...
		for sts in self.sites:
			# register to each shoes.
			for dshoes in self.shoes:

				# captcha
				headers = {
					"authority":"api.sneakers-raffle.fr",
					"method":"POST",
					"path":"/submit",
					"scheme":"https",
					"accept":"application/json, text/plain, */*",
					"accept-encoding":"gzip, deflate, br",
					"accept-language":"fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4",
					"content-length":"1820",
					"content-type":"application/json",
					"origin": sts['url'],
					"referer": sts['url'] + dshoes['url'],
					"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}

				payload = {"first_name":identity['fname'],
						"last_name":identity['lname'],
						"email":identity['mail'],
						"phone":identity['phone'],
						"birthdate":identity['birthdate'],
						"shoesize_id":identity['shoesize'], #### SIZE
						"completed_captcha":captcha,
						"shoe_id":dshoes['shoe_id'],
						"retailer_id":sts['siteid'],
						"g-recaptcha-response":captcha,
						"cc":"on",
						"mail":{
							"key":"tEUI-jW_JN_7y1h1B9bNJA",
							"template_name":sts['nomtemplate'],
							"template_content":[{"name":"example name","content":"example content"}],
							"message":{
								"subject":"Confirmation",
								"from_email":"verify@sneakers-raffle.fr",
								"from_name":"Sneakers Raffle",
								"to":[{"email":identity['mail'],"type":"to"}],
								"headers":{"Reply-To":"no.reply@sneakers-raffle.fr"},
								"merge_language":"handlebars",
								"global_merge_vars":[{"name":"shoe_name","content":dshoes['shoe_name']},{"name":"shoe_image","content":sts['url']+"app/uploads/2017/10/"+sts['imgURL']},{"name":"firstname"},{"name":"pickup_date","content":"11 November"}]
							}
						}
					}
					
				# getting captcha from threading harvester
				d = datetime.datetime.now().strftime('%H:%M')
				print("Getting Captcha")
				file = open(str(d)+'.txt','r') #r as reading only
				FileList = pickle.load(file) #FileList the list where i want to pick out the captcharep
				while len(FileList) == 0: #if len(FileList) it will wait for captcha scraper 
					file = open(str(d)+'.txt','r')
					FileList = pickle.load(file)
				captchaREP = random.choice(FileList) 
				FileList.remove(captchaREP)
				file  = open(str(d)+'.txt','w')
				pickle.dump(FileList,file)
				print("Captcha retrieved")


				req = s.post(i+z,headers=headers,payload=payload)
				print(req)
				

if __name__ = "__main__":
	ra = Raffle()
	accounts = [
		# 11 5US , 18 9US , 14 7US
		{"fname":"pete","lname":"james","mail":"petejames@gmail.com","phone":"+33612334455","birthdate":"01/01/1998","shoesize":"18",},
		]
	# catpcha 
	for i in accounts:
		ra.register(i)
