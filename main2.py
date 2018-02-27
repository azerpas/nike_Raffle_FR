# coding=utf-8
import requests, json, time, random, datetime, threading, pickle, os
from selenium import webdriver
from termcolor import colored

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
		#{"url":"product/nike-air-max-90/","shoe_id":"6","shoe_name":"Nike Air Max 90","imgURL":"AirMax90.jpg"},
		#{"url":"product/nike-air-presto/","shoe_id":"7","shoe_name":"Nike Air Presto","imgURL":"AirPresto.jpg"},
		#{"url":"product/nike-react-hyperdunk/","shoe_id":"8","shoe_name":"Nike React Hyperdunk","imgURL":"ReactHyperdunk.jpg"},
		#{"url":"product/nike-zoom-vaporfly/","shoe_id":"9","shoe_name":"Nike Zoom Vaporfly","imgURL":"ZoomVaporfly.jpg"},
		#{"url":"product/nike-vapor-max/","shoe_id":"10","shoe_name":"Nike Vapormax","imgURL":"Vapormax.jpg"},
		#{"url":"product/nike-force-1-low/","shoe_id":"11","shoe_name":"Nike Air Force 1 Low","imgURL":"AirForce1.jpg"},
		#{"url":"product/product/nike-air-max-97/","shoe_id":"12","shoe_name":"Nike Air Max 97","imgURL":"AirMax97.jpg"},
		{"url":"product/air-jordan-1-white/","shoe_id":"14","shoe_name":"The Ten: Air Jordan 1","imgURL":"AirJordan@100cropped.jpg"},
		]
		self.count = 0 
		self.sites = [
			#{"url":"https://shinzo.sneakers-raffle.fr/","siteid":"2","nomtemplate":"nike-raffle-confirm-shinzo"},
			#{"url":"https://thebrokenarm.sneakers-raffle.fr/","siteid":"3","nomtemplate":"nike-raffle-confirm-the-broken-arm"},
			#{"url":"https://colette.sneakers-raffle.fr/","siteid":"4","nomtemplate":"nike-raffle-confirm-colette"},
			#{"url":"https://starcow.sneakers-raffle.fr/","siteid":"5","nomtemplate":"nike-raffle-confirm-starcow"}
			{"url":"https://off---white.sneakers-raffle.fr/","siteid":"8","nomtemplate":"nike-raffle-confirm-off---white"}
			]
		self.api = "https://api.sneakers-raffle.fr/submit"
		self.driver = webdriver.Firefox() #webdriver.Chrome()  #service_args
		# interval etc

	def register(self,identity):
		log("Entering: " + str(identity['fname']) +" "+ str(identity['lname']))
		# For each site...
		for sts in self.sites:
			# register to each shoes.
			for dshoes in self.shoes:
				log("Entering: " + dshoes['shoe_name'] + " on " + sts['url'])
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

				if sts['siteid'] == "5" and dshoes['shoe_id'] == "11":
					self.driver.get(sts['url']+"product/nike-air-force-1/")
				else:
					self.driver.get(sts['url']+dshoes['url'])
				self.driver.find_element_by_xpath("""/html/body/div[2]/div/div[2]/div/form/div[1]/p[1]/input""").send_keys(identity['fname'])
				self.driver.find_element_by_xpath("""/html/body/div[2]/div/div[2]/div/form/div[1]/p[2]/input""").send_keys(identity['lname'])
				self.driver.find_element_by_xpath("""/html/body/div[2]/div/div[2]/div/form/div[1]/p[3]/input""").send_keys(identity['mail'])
				self.driver.find_element_by_xpath("""/html/body/div[2]/div/div[2]/div/form/div[1]/p[4]/input""").send_keys(identity['phone'])
				self.driver.find_element_by_xpath("""/html/body/div[2]/div/div[2]/div/form/div[1]/p[5]/input""").send_keys(identity['birthdate'])
				if identity['shoesize'] == "18":
					log("Changing shoe size....")
					identity['shoesize'] = random.choice(["36","36.5","37.5","38","38.5","39","40","40.5","41","42","42.5","43","44","44.5","45","45.5","46","47","47.5","48.5","49.5"]) #["6","9","10","11","12"]) #"4","5",
					log("Shoe size is now = " + str(identity['shoesize']))
				for option in self.driver.find_elements_by_tag_name('option'):
					if option.text.lower() == identity['shoesize'].lower():
						option.click()
						break
				self.driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML="%s";""" % captchaREP)
				self.driver.execute_script("""onSubmit("%s");""" % captchaREP)
				self.driver.execute_script("""document.getElementById("c1").click();""")
				time.sleep(random.uniform(3.4,4.5))
				try:
					self.driver.execute_script("""document.querySelector('.raffle-form .form-valid input[type="submit"]').click();""")
					log("Registered")
					self.count += 1
				except Exception as e:
					print(e) 
					log("Already registered")
					self.driver.execute_script("""onSubmit("%s");""" % captchaREP)
					try:
						self.driver.execute_script("""document.querySelector('.raffle-form .form-valid input[type="submit"]').click();""")
						print(colored("Registered",'red', attrs=['bold']))
						self.count += 1
					except Exception as e:
						print(e)
						log("Problem while trying to register")
				time.sleep(1)
				self.driver.delete_all_cookies()


if __name__ == "__main__":
	ra = Raffle()
	accounts = [
		# ["36","36.5","37.5","38","38.5","39","40","40.5","41","42","42.5","43","44","44.5","45","45.5","46","47","47.5","48.5","49.5"]
{"fname":"Frederic","lname":"Ronaldo","mail":"fredericronaldo@yahoo.com","phone":"+33612603602","birthdate":"23/12/1997","shoesize":"42"},
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
		# Dumb IP changing process as I mostly work manual you can't add proxy support easily
		"""
		if z % 4 == 0:
			
			log("ip needs to be changed")
			notify(title    = 'NIKE RAFFLE',
       		subtitle = 'Proxy changing',
       		message  = 'Need to change proxy to continue',
       		sound = 'default')
			raw_input("++")
		"""

	log("Signed to: " + str(ra.count) + " raffles" )
