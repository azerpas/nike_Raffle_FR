# coding=utf-8
import requests, json, time, random, datetime, threading, pickle

sitekey = "6LcMxjMUAAAAALhKgWsmmRM2hAFzGSQqYcpmFqHx"


def log(event):
	d = datetime.datetime.now().strftime("%H:%M:%S")
	print("Raffle by Azerpas :: " + str(d) + " :: " + event)
		
class Raffle(object):
	def __init__(self):
		self.s = requests.session()
		# "https://colette.sneakers-raffle.fr/","https://starcow.sneakers-raffle.fr/"
		self.shoes = [
		#{"url":"product/nike-air-jordan-1/","shoe_id":"2","shoe_name":"Nike Air Jordan 1","imgURL":"AirJordan.jpg"},
		#{"url":"product/nike-blazer/","shoe_id":"3","shoe_name":"Nike Blazer","imgURL":"Blazer.jpg"},
		{"url":"product/air-jordan-1-white/","shoe_id":"14","shoe_name":"The Ten: Air Jordan 1","imgURL":"AirJordan@100cropped.jpg"}]
		self.sites = [
			#{"url":"https://shinzo.sneakers-raffle.fr/","siteid":"2","nomtemplate":"nike-raffle-confirm-shinzo"},
			#{"url":"https://thebrokenarm.sneakers-raffle.fr/","siteid":"3","nomtemplate":"nike-raffle-confirm-the-broken-arm"},
			#{"url":"https://colette.sneakers-raffle.fr/","siteid":"4","nomtemplate":"nike-raffle-confirm-colette"},
			{"url":"https://off---white.sneakers-raffle.fr/","siteid":"8","nomtemplate":"nike-raffle-confirm-off-white-popup"}
			]
		# interval etc
		self.api = "https://api.sneakers-raffle.fr/submit"

	def register(self,identity):
		# For each site...
		for sts in self.sites:
			# register to each shoes.
			for dshoes in self.shoes:

				# getting captcha from threading harvester
				d = datetime.datetime.now().strftime('%H:%M')
				log("Getting Captcha")
				flag = False
				while flag != True:
					d = datetime.datetime.now().strftime('%H:%M')
					try:
						file = open(str(d)+'.txt','r') #r as reading only
						flag = True
					except IOError:
						time.sleep(2)
						log("No captcha available(1)")
						flag = False
				try:
					FileList = pickle.load(file) #FileList the list where i want to pick out the captcharep
				except:
					log("Can't open file")
				while len(FileList) == 0: #if len(FileList) it will wait for captcha scraper 
						d = datetime.datetime.now().strftime('%H:%M')
						try:
							file = open(str(d)+'.txt','r')
							FileList = pickle.load(file)
							if FileList == []:
								log("No captcha available(2)")
								time.sleep(3)
						except IOError as e:
							log("No file, waiting...")
							print(e)
							time.sleep(3)
				captchaREP = random.choice(FileList) 
				FileList.remove(captchaREP)
				file  = open(str(d)+'.txt','w')
				pickle.dump(FileList,file)
				log("Captcha retrieved")

				headers = {
					"authority":"api.sneakers-raffle.fr",
					"method":"OPTIONS",
					"path":"/submit",
					"scheme":"https",
					"accept":"*/*",
					"accept-encoding":"gzip, deflate, br",
					"accept-language":"fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
					"access-control-request-headers":"content-type",
					"access-control-request-method":"POST",
					"origin": sts['url'],
					"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
				}

				rep = self.s.options(self.api,headers=headers)
				print(rep)
				print(rep.text)

				# captcha
				headers = {
					"authority":"api.sneakers-raffle.fr",
					"method":"POST",
					"path":"/submit",
					"scheme":"https",
					"accept":"application/json, text/plain, */*",
					"accept-encoding":"gzip, deflate, br",
					"accept-language":"fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
					"content-type":"application/json",
					"origin": sts['url'],
					"referer": sts['url'] + dshoes['url'],
					"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"}

				payload = {"first_name":identity['fname'],
						"last_name":identity['lname'],
						"email":identity['mail'],
						"phone":identity['phone'],
						"birthdate":identity['birthdate'],
						"shoesize_id":identity['shoesize'], #### SIZE
						"completed_captcha":captchaREP,
						"shoe_id":dshoes['shoe_id'],
						"retailer_id":sts['siteid'],
						"g-recaptcha-response":captchaREP,
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
								"global_merge_vars":[{"name":"shoe_name","content":dshoes['shoe_name']},{"name":"shoe_image","content":sts['url']+"app/uploads/2018/02/"+dshoes['imgURL']},{"name":"firstname"},{"name":"pickup_date","content":"11 November"}]
							}
						}
				}

				req = self.s.post(self.api,headers=headers,json=payload)
				print(req)
				

if __name__ == "__main__":
	ra = Raffle()
	accounts = [
		# ["36","36.5","37.5","38","38.5","39","40","40.5","41","42","42.5","43","44","44.5","45","45.5","46","47","47.5","48.5","49.5"]
		{"fname":"pete","lname":"james","mail":"petejames@gmail.com","phone":"+33612334455","birthdate":"01/01/1998","shoesize":"42",},
		]
	for i in accounts:
		ra.register(i)
