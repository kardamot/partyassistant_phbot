from phBot import *
import QtBind
from threading import Timer
from time import sleep
import phBotChat
import struct
import json
import os

Version = '2.0'
Name = 'PartyAssistant'
Author = 'Hellixir'

### Global ###
DEFAULT_CHECK_DELAY = 1.0 # seconds

#0 General / 1 Champion / 4 Giant / 5 Titan / 6 Strong / 7 Elite / 8 Unique / 16 General Party / 17 Champion Party / 20 Giant Party
lstYOKSAY = ('0','1','4','6','7','8','16','17')
lstTERCIH = ('5','20')
Koordinat1 = ("X: -11842,  Y: -1926")
Script1 = "C:/Users/Mustafa/AppData/Local/Programs/phBot Testing1/Scripts/TITAN1.txt"
Koordinat2 = ("X: -11605,  Y: -1842")
Script2 = ("C:/Users/Mustafa/AppData/Local/Programs/phBot Testing1/Scripts/Dewil Worm Titan 2.txt")
Koordinat3 = ("X: -12085,  Y: -1642")
Script3 = ("C:/Users/Mustafa/AppData/Local/Programs/phBot Testing1/Scripts/Dewil Worm Titan 3.txt")
Koordinat4 = ("X: -12742,  Y: -1542")
Script4 = ("C:/Users/Mustafa/AppData/Local/Programs/phBot Testing1/Scripts/Dewil Worm Titan 4.txt")

# Arayüz
gui = QtBind.init(__name__,Name)

QtBind.createLabel(gui,"#-------------------------------------------------------------------- Komut Listesi --------------------------------------------------------------------#",20,8)
QtBind.createLabel(gui,"--> ENERY        :  Energy of Life potunu kullanır. (Envanterde 2. sayfa 3. satır 2.sütunda olmalıdır.)",20,30)
QtBind.createLabel(gui,"--> FILL            :  Kullanılan Energy of Life ile berserki doldurur.",20,42)
QtBind.createLabel(gui,"--> TITAN1       :  Ayarlanan titan noktasına hareket ettirecektir.(1-4 noktaya)",20,54)
QtBind.createLabel(gui,"--> TitanCheck :  Titan kontrol argümanı. Bu komut chat ile yakalanmayacaktır. (TitanCheck & TitanCheck,5 & TitanCheck,5,100)",20,66)


QtBind.createLabel(gui,"#-------------------------------------------------------------- Titan Kontrol Noktaları --------------------------------------------------------------#",20,100)
QtBind.createLabel(gui,"1. Titan Koordinat:",20,125)
QtBind.createLineEdit(gui,Koordinat1,20,140,105,19)
QtBind.createLabel(gui,"1. Titan Konumu Script Dosya Yolu:",140,125)
QtBind.createLineEdit(gui,Script1,140,140,500,19)

QtBind.createLabel(gui,"2. Titan Koordinat:",20,165)
QtBind.createLineEdit(gui,Koordinat2,20,180,105,19)
QtBind.createLabel(gui,"2. Titan Konumu Script Dosya Yolu:",140,165)
QtBind.createLineEdit(gui,Script2,140,180,500,19)

QtBind.createLabel(gui,"3. Titan Koordinat:",20,205)
QtBind.createLineEdit(gui,Koordinat3,20,220,105,19)
QtBind.createLabel(gui,"3. Titan Konumu Script Dosya Yolu:",140,205)
QtBind.createLineEdit(gui,Script3,140,220,500,19)

QtBind.createLabel(gui,"4. Titan Koordinat:",20,245)
QtBind.createLineEdit(gui,Koordinat4,20,260,105,19)
QtBind.createLabel(gui,"4. Titan Konumu Script Dosya Yolu:",140,245)
QtBind.createLineEdit(gui,Script4,140,260,500,19)

QtBind.createLabel(gui,"#by Hellixir",668,268)

# Notice Mesajı - Inject Packet to Client 
def InjectClient_SendNotice(message):
    m = struct.pack('B',7)
    m += struct.pack('H', len(message))
    m += message.encode('ascii')
    inject_silkroad(0x3026,m,False)

# Karakter yapılandırma (JSON)
def getPath():
	return get_config_dir()+Name+"\\"

def getConfig():
	return getPath()+Name+".json"

# Karakter yapılandırma dosyası yükleyicisi
def loadConfigs():
	if os.path.exists(getConfig()):
		data = {}
		with open(getConfig(),"r") as f:
			data = json.load(f)

def ListContains(text,lst):
	for i in range(len(lst)):
		if lst[i].lower() == text.lower():
			return True
	return False

def QtBind_ItemsContains(text,lst):
	return ListContains(text,QtBind.getItems(gui,lst))

# Chat komutları okuma yönergesi "FILL" , "ENERGY" , "TITAN"
def handle_chat(t,player,msg):
	# Kullanılan energy of life'ı doldurmak için
	if msg == "FILL":
		inject_joymax(0x715F, b'\x8B\x5D\x00\x00\x81\x5D\x00\x00', False)
		log('PartyAssistant: Energy of Life filled.')
		InjectClient_SendNotice("Berserk dolduruldu")
	# Energy of life'ı kullanmak için -Dikkat: Envanter 2.sayfasında 3.satır 2.sütunda olmalı-
	if msg == "ENERGY":
		inject_joymax(0x704C, b'\x36\xEC\x76', False)
		log('PartyAssistant: Energy of Life used.')
		InjectClient_SendNotice("Energy of Life kullanildi")
	# 1.Titan Noktası
	if msg == "TITAN1":
		stop_bot()
		InjectClient_SendNotice("Titan bildirimi geldi! Belirlenen koordinatlara hareket ediliyor.")
		set_training_script(Script1)
		Timer(1.0,start_bot).start()
		log("PartyAssistant: Belirlenen titan bölgesine gidiliyor.")

# Titan saldırı yönergesi
def AttackTitan(wait,isAttacking,x,y,z,radius):
	count = TitanCounter(radius)
	if count > 0:
		# Titanı öldürmeye başla
		if isAttacking:
			log("PartyAssistant: Bölgede ("+str(count)+") titan tespit edildi.")
			InjectClient_SendNotice("Titan bulundu!")
		else:
			start_bot()
			log("PartyAssistant: Bölgedeki ("+str(count)+") titana saldırı başlıyor. Mesafe: "+(str(radius) if radius != None else "Maximum."))		# Check if there is not mobs to continue script
		# Titan yoksa slota geri dön
		Timer(wait,AttackTitan,(wait,True,x,y,z,radius)).start()
	else:
		log("PartyAssistant: Titan öldürüldü. Slota geri dönülüyor.")
		InjectClient_SendNotice("Tebrikler! Titan kesildi.")
		# Düşen itemleri topla
		waitAttemptsMax = 15
		drops = get_drops()
		while drops:
			if not waitAttemptsMax:
				log("PartyAssistant: Toplama zamanı bekleniyor!")
				break
			log("Plugin: ("+str(len(drops))+") toplanması bekleniyor...")
			# wait 1s
			sleep(1.0)
			# check data again
			waitAttemptsMax -= 1
			drops = get_drops()
		# Titan ölünce botu durdur
		stop_bot()
		# Standart kasılma koordinatı
		set_training_position(0,0,0)
		# Slota geri dön
		move_to(x,y,z)
		log("PartyAssistant: Slota geri dönülüyor...")
		# Delay
		Timer(2.5,start_bot).start()

# Titan algılama yönergesi. Maximum tahmini menzil 65-75
def TitanCounter(radius):
	count = 0
	# Radius hesaplama
	p = get_position() if radius != None else None
	# Mobları kontrol et
	monsters = get_monsters()
	if monsters:
		for key, mob in monsters.items():
			# Yoksayılacak mob tipleri
			if ListContains(str(mob['type']),lstYOKSAY):
				continue
			# Tercih edilecek mob tipi(Sadece Titan)
			if len(lstTERCIH) > 0:
				if not ListContains(str(mob['type']),lstTERCIH):
					continue
			# Menzil kontrol
			if radius != None:
				if round(GetDistance(p['x'], p['y'],mob['x'],mob['y']),2) > radius:
					continue
			count+=1
	return count

# Mesafe hesaplama yönetgesi
def GetDistance(ax,ay,bx,by):
	return ((bx-ax)**2 + (by-ay)**2)**(0.5)


# Titan kontrol yönergesi. Kullanım: "TitanCheck" , "TitanCheck,5" , "TitanCheck,5,100"
# Çevredeki titanları belirlenen süre kadar tara. Varsayılan olarak 5 saniye.
# Belirlenen tarama menzili. Varsayılan olarak 100.
def TitanCheck(args):
	# Varsayılan azami menzil
	radius = None
	if len(args) >= 2:
		radius = round(float(args[1]),2)
	# Botu durdurarak titanı öldür
	if TitanCounter(radius) > 0:
		stop_bot()
		p = get_position()
		set_training_position(p['region'], p['x'], p['y'])
		if radius != None:
			set_training_radius(radius)
		else:
			set_training_radius(100.0)
		# Titan arama gecikmesi
		wait = DEFAULT_CHECK_DELAY
		if len(args) >= 3 and float(args[2]) > 0:
			wait = float(args[2])
		Timer(5.0,AttackTitan,(wait,False,p['x'],p['y'],p['z'],radius)).start()
	# Titan yoksa veya ölünce slota dönüş
	else:
		log("PartyAssistant: Titan bulunamadı. Mesafe: "+(str(radius) if radius != None else "Maximum."))
		InjectClient_SendNotice("Titan tespit edilemedi. Slota donuluyor")
		stop_bot()
		set_training_position(0,-11612,-1838)
		set_training_script('C:/Users/Mustafa/AppData/Local/Programs/phBot Testing1/Scripts/Dewil Worm.txt')
		Timer(2.5,start_bot).start()
	return 0

# Plugin loading success
log('Eklenti: '+Name+' v'+Version+' yüklemesi başarılı. by '+Author+'.')

if os.path.exists(getPath()):
	# Adding RELOAD plugin support
	try:
		loadConfigs()
	except:
		# Just in case omg -_-
		log('PartyAssistant: Config dosyası yüklenemedi!')
else:
	# Creating configs folder
	os.makedirs(getPath())
	log('PartyAssistant: '+Name+' için klasör oluşturuldu.')