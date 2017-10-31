# coding=utf-8
import requests, json, time, random, datetime, threading, pickle, os
from selenium import webdriver

sitekey = "6LcMxjMUAAAAALhKgWsmmRM2hAFzGSQqYcpmFqHx"

"""
def notify(title, subtitle, message, sound):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    so = '-sound {!r}'.format(sound) 
    os.system('terminal-notifier {}'.format(' '.join([m, t, s, so])))
"""

def log(event):
	d = datetime.datetime.now().strftime("%H:%M:%S")
	print("Raffle by Azerpas :: " + str(d) + " :: " + event)
		
class Raffle(object):
	def __init__(self):
		self.s = requests.session()
		# "https://colette.sneakers-raffle.fr/","https://starcow.sneakers-raffle.fr/"
		self.shoes = [
		#{"url":"product/nike-air-jordan-1/","shoe_id":"2","shoe_name":"Nike Air Jordan 1","imgURL":"AirJordan.jpg"},
		#{"url":"product/nike-blazer/","shoe_id":"3","shoe_name":"Nike Blazer","imgURL":"Blazer.jpg"}
		{"url":"product/nike-air-max-90/","shoe_id":"6","shoe_name":"Nike Air Max 90","imgURL":"AirMax90.jpg"},
		{"url":"product/nike-air-presto/","shoe_id":"7","shoe_name":"Nike Air Presto","imgURL":"AirPresto.jpg"}
		]

		self.sites = [
			{"url":"https://shinzo.sneakers-raffle.fr/","siteid":"2","nomtemplate":"nike-raffle-confirm-shinzo"},
			{"url":"https://thebrokenarm.sneakers-raffle.fr/","siteid":"3","nomtemplate":"nike-raffle-confirm-the-broken-arm"},
			{"url":"https://colette.sneakers-raffle.fr/","siteid":"4","nomtemplate":"nike-raffle-confirm-colette"},
			{"url":"https://starcow.sneakers-raffle.fr/","siteid":"5","nomtemplate":"nike-raffle-confirm-starcow"}
			]
		self.api = "https://api.sneakers-raffle.fr/submit"
		self.driver = webdriver.Chrome()
		# interval etc

	def register(self,identity):
		# For each site...
		for sts in self.sites:
			# register to each shoes.
			for dshoes in self.shoes:

				
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

				self.driver.get(sts['url']+dshoes['url'])
				self.driver.find_element_by_xpath("""/html/body/div[2]/div/div[2]/div/form/div[1]/p[1]/input""").send_keys(identity['fname'])
				self.driver.find_element_by_xpath("""/html/body/div[2]/div/div[2]/div/form/div[1]/p[2]/input""").send_keys(identity['lname'])
				self.driver.find_element_by_xpath("""/html/body/div[2]/div/div[2]/div/form/div[1]/p[3]/input""").send_keys(identity['mail'])
				self.driver.find_element_by_xpath("""/html/body/div[2]/div/div[2]/div/form/div[1]/p[4]/input""").send_keys(identity['phone'])
				self.driver.find_element_by_xpath("""/html/body/div[2]/div/div[2]/div/form/div[1]/p[5]/input""").send_keys(identity['birthdate'])
				for option in self.driver.find_elements_by_tag_name('option'):
					if option.text.lower() == identity['shoesize'].lower():
						option.click()
						break
				self.driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML="%s";""" % captchaREP)
				self.driver.execute_script("""onSubmit("%s");""" % captchaREP)
				self.driver.execute_script("""document.getElementById("c1").click();""")
				try:
					self.driver.execute_script("""document.querySelector('.raffle-form .form-valid input[type="submit"]').click();""")
				except: 
					log("Already registered")
				time.sleep(1)
				self.driver.delete_all_cookies()
				"""req = self.s.post(self.api,headers=headers,data=payload)
				print(req)
				print(req.text)"""

if __name__ == "__main__":
	ra = Raffle()
	accounts = [

{"fname":"brice","lname":"denice","mail":"bricedenice@gmail.com","phone":"+33600449988","birthdate":"30/01/1998","shoesize":"10",},

] 
		
	# catpcha 
	z = 0 
	for i in accounts:
		z += 1
		print("----------------------------------")
		log("Sign in : " + str(i['fname']) +" "+ str(i['lname']))
		log("Account N°" + str(z) + " of " + str(len(accounts)))
		print("----------------------------------")
		ra.register(i)
    """
    in case you want to change your IP 
		if z % 4 == 0:
			log("ip needs to be changed")
			notify(title    = 'NIKE RAFFLE',
       		subtitle = 'Proxy changing',
       		message  = 'Need to change proxy to continue',
       		sound = 'default')
			raw_input("++")
     """
