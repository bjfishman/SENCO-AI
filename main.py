##################################################################################
##                                                                              ##
##            _____ ______ _   _  _____ ____                _____               ##
##           / ____|  ____| \ | |/ ____/ __ \         /\   |_   _|              ##
##          | (___ | |__  |  \| | |   | |  | |______ /  \    | |                ##
##           \___ \|  __| | . ` | |   | |  | |______/ /\ \   | |                ##
##           ____) | |____| |\  | |___| |__| |     / ____ \ _| |_               ##
##          |_____/|______|_| \_|\_____\____/     /_/    \_\_____|              ##
##                                                                              ##
##                                                    v 0.18                    ##
## 												      Started: 29.11.2020       ##
##                                                                              ##
##################################################################################
##                                                                              ##
##                              DEPENDENCIES:                                   ##
##                                                                              ##
##	  -	  pygame == 1.9.6 or 1.9.3, newer versions cause issues				    ##
##	  -   pyttsx3                                                               ##
##	  -   openai                                                                ##
##	  -	  openpyxl                                                              ##
##	  -   natsort                                                               ##
##                                                                              ##
##################################################################################
##                                                                              ##
##   TODO: Implement censor filter in configurator                              ##
##                                                                              ##
##################################################################################

## Namespaces #######################################
import os, sys                                     ##
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  ##
import pygame                                      ##
import openpyxl as excel                           ##
import openai                                      ##
import configparser                                ##
import pyttsx3                                     ##
from   pyttsx3.drivers import sapi5                ##
import time                                        ##
from   datetime import datetime                    ##
from   natsort  import natsorted                   ##
import ctypes					                   ##
import _turbosatorinetworkinterface as BCI         ##
import playsound                                   ##
import censoredWords as censor					   ##
import allowedChars as whiteList				   ##
#####################################################

def initialization():
	'''
	Parses config file, initializes all modules and then waits
	for a keypress before advancing to the next phase.
	'''
	
	################
	##   Globals  ##
	################
	
	global clickPlayed
	clickPlayed = False
	
	## Config file global
	global CONFIG
	## Font handles
	global STD_FONT, SMALL_FONT, SMALLEST_FONT
	## Pygame window & clock
	global SURFACE_MAIN, SCREEN_HEIGHT, SCREEN_WIDTH, CLOCK
	## Main loop globals
	global CMD_HISTORY, WORD_HISTORY, COUNTER, OUTPUT_STRING, WORD_LIST, TIMEOUT_COUNTER, timeoutPhase1List, timeoutPhase2List, OUTPUT_LIST
	## TTS globals
	global TTS_ENGINE, TTS_ON
	## Excel step tracking globals
	global STEP_COUNTER, INTERNAL_COUNTER
	## Turbo-Satori globals
	global FILELIST, NFOXYVALUE, NFDEOXYVALUE, RAWOXY, RAWDEOXY, NO_DATA, SAME_COUNTER, WRONG_FOLDER
	## Protocol globals
	global phase1List, phase2List, phase3List, phase4List, phase5List, phase6List
	global pred_phase1List, pred_phase2List, pred_phase3List, pred_phase4List, pred_phase5List, pred_phase6List
	## Localizer globals
	global taskList, restList
	## Frequency calc
	global DATA_FREQUENCY
	## TSI Network interface
	global TSI_Error_Raised, BCIConnected
	## Prediction list globals
	global predictionList, predictionLetterFlag, censorWordList

	################
	## config.ini ##
	################
	
	predictionList = []
	predictionLetterFlag = False
	
	# Logging
	writeToLog("-------INITIALIZATION-------")
	
	# Disable Windows UI scaling
	ctypes.windll.user32.SetProcessDPIAware()
	
	# Read config.ini
	CONFIG = configparser.ConfigParser()  
	CONFIG.read('config/CONFIG.ini')
	writeToLog("Config file loaded")
	
	# FPS limit
	CONFIG.fps_target = int(CONFIG.get('WINDOW_SETTINGS','fps_target'))
	
	# Splash screen jingle
	CONFIG.splashAudio = eval(CONFIG.get('MISC', 'splashAudio'))
	
	# PG-13 mode
	CONFIG.censorMode = eval(CONFIG.get('MISC', 'censorMode'))
	censorWordList = censor.wordList if CONFIG.censorMode == True else []
	
	# Colors
	CONFIG.black = eval(CONFIG.get('COLOR DEFINITIONS', 'black'))
	CONFIG.white = eval(CONFIG.get('COLOR DEFINITIONS', 'white'))
	CONFIG.green = eval(CONFIG.get('COLOR DEFINITIONS', 'green'))
	CONFIG.red   = eval(CONFIG.get('COLOR DEFINITIONS', 'red'))
	
	# Turbo-Satori settings
	CONFIG.data_folder = str(CONFIG.get('TURBO-SATORI SETTINGS', 'data_folder'))
	CONFIG.thermo_on   = eval(CONFIG.get('TURBO-SATORI SETTINGS', 'thermo_on'))
	CONFIG.thermo_during_planning = eval(CONFIG.get('TURBO-SATORI SETTINGS', 'thermo_during_planning'))
	CONFIG.NF_reader_frequency    = int(CONFIG.get('TURBO-SATORI SETTINGS','NF_reader_frequency'))
	CONFIG.NF_mode      = str(CONFIG.get('TURBO-SATORI SETTINGS','NF_mode'))
	CONFIG.NF_threshold = int(CONFIG.get('TURBO-SATORI SETTINGS','NF_threshold'))
	writeToLog("Experiment data folder: " + CONFIG.data_folder)
	
	# NF vars
	FILELIST       = []
	NFOXYVALUE     = 0
	NFDEOXYVALUE   = 0
	RAWOXY         = 0
	RAWDEOXY       = 0
	SAME_COUNTER   = 0
	NO_DATA        = True
	WRONG_FOLDER   = False
	DATA_FREQUENCY = 0
	
	# Main loop vars
	TIMEOUT_COUNTER = 0
	CONFIG.timeout_iterlimit = int(CONFIG.get('MISC','timeout_iterlimit'))
	OUTPUT_LIST = []
	
	# Startup flags
	CONFIG.progressbarAudio = eval(CONFIG.get('TURBO-SATORI SETTINGS','progressbarAudio'))
	CONFIG.progressbar = eval(CONFIG.get('TURBO-SATORI SETTINGS','progressbar'))
	CONFIG.localizer   = eval(CONFIG.get('TURBO-SATORI SETTINGS','localizer'))
	CONFIG.tutorial    = eval(CONFIG.get('TURBO-SATORI SETTINGS','tutorial'))
	CONFIG.threshold   = eval(CONFIG.get('TURBO-SATORI SETTINGS','threshold'))
	CONFIG.training    = eval(CONFIG.get('TURBO-SATORI SETTINGS','training'))
	CONFIG.localizerRepetitions = int(CONFIG.get('TURBO-SATORI SETTINGS','localizerRepetitions'))
	CONFIG.localizer_task_duration    = int(CONFIG.get('TURBO-SATORI SETTINGS','localizer_task_duration'))
	CONFIG.localizer_rest_duration    = int(CONFIG.get('TURBO-SATORI SETTINGS','localizer_rest_duration'))
	CONFIG.localizer_lasttrial_duration = int(CONFIG.get('TURBO-SATORI SETTINGS','localizer_lasttrial_duration'))
	
	# Localizer protocol
	taskList = []
	restList = []
	
	# Protocol
	timeoutPhase1List = []
	timeoutPhase2List = []
	phase1List = []
	phase2List = []
	phase3List = []
	phase4List = []
	phase5List = []
	phase6List = []
	pred_phase1List = []
	pred_phase2List = []
	pred_phase3List = []
	pred_phase4List = []
	pred_phase5List = []
	pred_phase6List = []
	CONFIG.experiment_name            = str(CONFIG.get('TURBO-SATORI SETTINGS','experiment_name'))	
	CONFIG.prt_backgroundcolor        = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_backgroundcolor'))
	CONFIG.prt_textcolor              = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_textcolor'))
	CONFIG.prt_timecoursecolor        = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_timecoursecolor'))
	CONFIG.prt_referencefunccolor     = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_referencefunccolor'))
	CONFIG.prt_phase1ColorString      = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_phase1ColorString'))
	CONFIG.prt_phase2ColorString      = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_phase2ColorString'))
	CONFIG.prt_phase3ColorString      = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_phase3ColorString'))
	CONFIG.prt_phase4ColorString      = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_phase4ColorString'))
	CONFIG.prt_phase5ColorString      = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_phase5ColorString'))
	CONFIG.prt_phase6ColorString      = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_phase6ColorString'))
	CONFIG.prt_timecoursethick        = int(CONFIG.get('TURBO-SATORI SETTINGS','prt_timecoursethick'))
	CONFIG.prt_referencefuncthick     = int(CONFIG.get('TURBO-SATORI SETTINGS','prt_referencefuncthick'))
	CONFIG.pred_prt_phase1ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','pred_prt_phase1ColorString'))
	CONFIG.pred_prt_phase2ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','pred_prt_phase2ColorString'))
	CONFIG.pred_prt_phase3ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','pred_prt_phase3ColorString'))
	CONFIG.pred_prt_phase4ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','pred_prt_phase4ColorString'))
	CONFIG.pred_prt_phase5ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','pred_prt_phase5ColorString'))
	CONFIG.pred_prt_phase6ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','pred_prt_phase6ColorString'))
	CONFIG.returnColorString      	  = eval(CONFIG.get('TURBO-SATORI SETTINGS','returnColorString'))
	CONFIG.newSentenceColorString 	  = eval(CONFIG.get('TURBO-SATORI SETTINGS','newsentenceColorString'))
	
	# Debug
	CONFIG.debug_on = eval(CONFIG.get('MISC', 'debug_on'))

	# Input type
	CONFIG.input_type = str(CONFIG.get('MISC','input_type'))
	writeToLog("Input mode: " + CONFIG.input_type)
	
	# TTS
	TTS_ON = eval(CONFIG.get('MISC', 'text_to_speech'))
	if TTS_ON: writeToLog("Text-To-Speech: On")
	else: writeToLog("Text-To-Speech: Off")
	
	# TTS init
	if TTS_ON:
		TTS_ENGINE = pyttsx3.init()
		tts_voice  = int(CONFIG.get('MISC','tts_voice'))
		voices     = TTS_ENGINE.getProperty("voices")
		TTS_ENGINE.setProperty("voice", voices[tts_voice].id)
		writeToLog("Text-To-Speech initialized with voice " + str(tts_voice))
	
	# GPT-3
	CONFIG.predictions_on =  eval(CONFIG.get("GPT-3 SETTINGS", "predictions_on"))
	CONFIG.model_str      =       CONFIG.get("GPT-3 SETTINGS", "model")
	CONFIG.temperature    = float(CONFIG.get('GPT-3 SETTINGS', 'temperature'))
	CONFIG.length         =   int(CONFIG.get('GPT-3 SETTINGS', 'length'))
	CONFIG.top_p          = float(CONFIG.get('GPT-3 SETTINGS', 'top_p'))
	CONFIG.max_reroll     =   int(CONFIG.get('GPT-3 SETTINGS', 'max_reroll'))
	
	# Log GPT-3 parameters
	writeToLog("-----GPT-3 Settings-----")
	writeToLog("Model: "       + CONFIG.model_str)
	writeToLog("Temperature: " + str(CONFIG.temperature))
	writeToLog("Length: "      + str(CONFIG.length))
	writeToLog("top_p: "       + str(CONFIG.top_p))
	
	# Timings
	CONFIG.initialDelay = int(CONFIG.get('TIMINGS', 'initialDelay'))
	CONFIG.firstPhase   = int(CONFIG.get('TIMINGS', 'firstPhase'))
	CONFIG.secondPhase  = int(CONFIG.get('TIMINGS', 'secondPhase'))
	CONFIG.thirdPhase   = int(CONFIG.get('TIMINGS', 'thirdPhase'))
	CONFIG.fourthPhase  = int(CONFIG.get('TIMINGS', 'fourthPhase'))
	CONFIG.fifthPhase   = int(CONFIG.get('TIMINGS', 'fifthPhase'))
	CONFIG.endPhase     = int(CONFIG.get('TIMINGS', 'endPhase'))
	CONFIG.pred_initialDelay = int(CONFIG.get('TIMINGS', 'pred_initialDelay'))
	CONFIG.pred_firstPhase   = int(CONFIG.get('TIMINGS', 'pred_firstPhase'))
	CONFIG.pred_secondPhase  = int(CONFIG.get('TIMINGS', 'pred_secondPhase'))
	CONFIG.pred_thirdPhase   = int(CONFIG.get('TIMINGS', 'pred_thirdPhase'))
	CONFIG.pred_fourthPhase  = int(CONFIG.get('TIMINGS', 'pred_fourthPhase'))
	CONFIG.pred_fifthPhase   = int(CONFIG.get('TIMINGS', 'pred_fifthPhase'))
	CONFIG.pred_endPhase     = int(CONFIG.get('TIMINGS', 'pred_endPhase'))
	
	# Log timings
	writeToLog("-----Timings------")
	writeToLog("Main initial delay: " + str(CONFIG.initialDelay))
	writeToLog("Main first phase: "   + str(CONFIG.firstPhase))
	writeToLog("Main second phase: "  + str(CONFIG.secondPhase))
	writeToLog("Main third phase: "   + str(CONFIG.thirdPhase))
	writeToLog("Main fourth phase: "  + str(CONFIG.fourthPhase))
	writeToLog("Main fifth phase: "   + str(CONFIG.fifthPhase))
	writeToLog("Main end phase: "     + str(CONFIG.endPhase))
	writeToLog("Prediction initial delay: " + str(CONFIG.pred_initialDelay))
	writeToLog("Prediction first phase: "   + str(CONFIG.pred_firstPhase))
	writeToLog("Prediction second phase: "  + str(CONFIG.pred_secondPhase))
	writeToLog("Prediction third phase: "   + str(CONFIG.pred_thirdPhase))
	writeToLog("Prediction fourth phase: "  + str(CONFIG.pred_fourthPhase))
	writeToLog("Prediction fifth phase: "   + str(CONFIG.pred_fifthPhase))
	writeToLog("Prediction end phase: "     + str(CONFIG.pred_endPhase))
	
	# Progress bar
	CONFIG.indicator = eval(CONFIG.get('MISC', 'indicator'))
	CONFIG.indicatorPos = int(CONFIG.get('MISC', 'indicatorPos'))
	
	# Pygame init
	writeToLog("-----Pygame------")
	pygame.init()
	pygame.font.init()
	CLOCK = pygame.time.Clock()
	pygame.key.set_repeat(100, 150)
	writeToLog("Pygame initialized")
	
	# Fonts
	writeToLog("-----Fonts------")
	font = str(CONFIG.get('FONTS', 'font'))
	writeToLog("Font selected: " + font)
	STD_FONT      = pygame.font.SysFont(font, int(CONFIG.get('FONTS', 'std')))
	SMALL_FONT    = pygame.font.SysFont(font, int(CONFIG.get('FONTS', 'small')))
	SMALLEST_FONT = pygame.font.SysFont(font, int(CONFIG.get('FONTS', 'smallest')))	
	writeToLog("Font sizes: ")
	writeToLog("Smallest: " + str(CONFIG.get('FONTS', 'smallest')))
	writeToLog("Small: "    + str(CONFIG.get('FONTS', 'small')))
	writeToLog("Standard: " + str(CONFIG.get('FONTS', 'std')))
	writeToLog("Fonts loaded")
	
	# Get screen size
	writeToLog("-----Screen------")
	infoObject = pygame.display.Info()
	writeToLog( "Screen size detected: " + str(infoObject.current_w) + "x" + str(infoObject.current_h) )
	
	# Fullscreen
	fullscreen = eval(CONFIG.get('WINDOW_SETTINGS', 'fullscreen'))
	if fullscreen: writeToLog("Window mode: Fullscreen")
	else: writeToLog("Window mode: Windowed")
	writeToLog("-----------------")
	
	# Main surface init
	if fullscreen == True:
		SCREEN_WIDTH  = infoObject.current_w
		SCREEN_HEIGHT = infoObject.current_h
		SURFACE_MAIN  = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN )
		pygame.mouse.set_visible(False)
	else:
		SCREEN_WIDTH  = infoObject.current_w - infoObject.current_w // 3
		SCREEN_HEIGHT = infoObject.current_h - infoObject.current_h // 3 + 200
		SURFACE_MAIN  = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )	
		
	# Set window caption and icon
	pygame.display.set_caption("SENCO-AI")
	
	# Set icon
	pygame.display.set_icon(pygame.image.load('config/gfx/icon2.png'))
	
	# GPT-3 init
	openai.api_key = str(CONFIG.get("GPT-3 SETTINGS", "api_key"))

	# Dictionary init
	WORD_LIST = []
	CONFIG.dictionary = str(CONFIG.get('MISC', 'dictionary'))
	writeToLog("Dictionary file: " + CONFIG.dictionary)
	with open(CONFIG.dictionary, "r") as file:
		word_temp = file.readlines()
	for word in word_temp:
		word = word.replace('\n', '') 
		WORD_LIST.append(word)
	writeToLog("Length of dictionary: " + str(len(WORD_LIST)))
	
	# Main loop prep
	OUTPUT_STRING    = ""
	CMD_HISTORY      = []
	WORD_HISTORY     = []
	COUNTER          = 0
	STEP_COUNTER     = 0
	INTERNAL_COUNTER = 0
	
	# Prepare xlsx log
	makeExcel()
	
	# Instructions on or off?
	CONFIG.showInstructions = eval(CONFIG.get("MISC", "showInstructions"))

	# Connect to TCP interface
	TSI_Error_Raised = False
	BCIConnected = False
	connectToTSI()
	if BCIConnected:
		writeToLog("TSI network interface connected!")
	else:
		writeToLog("TSI network interface connection failed...")
	
	# Clear NF Folder
	if not CONFIG.input_type == "KB":
		clearNFFolder(silent=True)
	else:
		print("Input type set to KB only, skipping NF folder wipe.")
		
		
	# Splash screen init
	img_splash = pygame.image.load("config/gfx/title.png").convert_alpha()
	img_splash = pygame.transform.smoothscale(img_splash, (800, 500))
	img_splash_coords = (SCREEN_WIDTH//2-400, SCREEN_HEIGHT//2 - 250)	
	timer_fade = 0
	timer_fadeOut = 0
	limit = 2
	limit_fadeOut = 1
	keyPressed = False
	
	
	### Init done, show splash screen ###
	print("Press any key to continue...")
	writeToLog("-------INITIALIZATION DONE-------")
	pygame.display.flip()
		
	waiting = True
	soundPlayed = False
	TTS_said = False
	fadedIn = False
	
	while waiting:
		
		# play jingle
		if not soundPlayed and CONFIG.splashAudio:
			playsound.playsound("config/sfx/startup.mp3", block = False)
			soundPlayed = True
		
		# say TTS line
		if TTS_ON and soundPlayed and not TTS_said and fadedIn:
			TTS_said = True
			sayVoiceLine("Press any key to continue!")
			
		# splash screen gfx fade-in
		if not keyPressed:
			timer_fade += 1
			timer_fine = getMilliseconds(timer_fade)
			percentage = timer_fine / (limit/2)
			if percentage < 0: percentage = 0
			if percentage > 1: percentage = 1
			alpha = percentage * 255
			blit_alpha(SURFACE_MAIN, img_splash, img_splash_coords, alpha)	
		
		# raise flag when fully faded in
		if alpha >= 255:
			fadedIn = True
		
		# fade-out & continue if key is pressed
		if keyPressed:
			timer_fadeOut += 1
			timer_fine = getMilliseconds(timer_fadeOut)
			percentage = timer_fine / (limit_fadeOut/2)
			if percentage < 0: percentage = 0
			if percentage > 1: percentage = 1
			alpha = 255 - (percentage * 255)
			blit_alpha(SURFACE_MAIN, img_splash, img_splash_coords, alpha)	
			if alpha <= 0:
				waiting = False
		
		# update screen & tick time		
		pygame.display.flip()
		SURFACE_MAIN.fill((0,0,0))
		CLOCK.tick(CONFIG.fps_target)		
		
		# input		
		events_list = pygame.event.get()
		for event in events_list:
			if event.type == pygame.KEYDOWN:
				keyPressed = True
			if event.type == pygame.QUIT:
				quitProgram()
	
	### Advance ###
	if CONFIG.tutorial:
		tutorial()
	elif CONFIG.localizer:
		localizer()
	elif CONFIG.threshold:
		threshold()
	elif CONFIG.training:
		training()
	else:
		main_loop(WORD_LIST)
	
def threshold():
	'''
	Threshold selection
	'''
	global CONFIG
	
	print("Starting threshold detection")
	writeToLog("Start of threshold detection")

	#########
	## Init #
	#########
	
	# display
	SURFACE_MAIN.fill((0,0,0))
	pygame.display.flip()
	
	# assets
	image_task = pygame.image.load("config/gfx/mental_task.png")
	image_task = pygame.transform.smoothscale(image_task, (350, 350))
	image_task_coords = (SCREEN_WIDTH//2 + 130, SCREEN_HEIGHT//2 - 170)
	
	# timer
	timer = 0
	limit = 6
	
	# NF ticker
	NFTicker = 1
	
	# TTS
	TTS_said = False
	
	# flags
	
	if CONFIG.showInstructions:
		section1Done  = False
		section2Done  = False
		section3Done  = False
		section4Done  = False
		section5Done  = False
		section6Done  = False
		section7Done  = False
		section8Done  = False
		section9Done  = False
	else:
		section1Done  = True
		section2Done  = True
		section3Done  = True
		section4Done  = True
		section5Done  = True
		section6Done  = True
		section7Done  = True
		section8Done  = False
		section9Done  = False		
	
	# start loop
	while True:
		
		# maintenance
		updateSlide()
		timer += 1
		timer_sec = getSeconds(timer)		
		
		############
		## slides ##
		############
		
		### Section 1 ###
		while not section1Done:
			
			# prep slide
			textList = [("We will now determine the right threshold for you.", None, "std", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))]
			imageList = []
			
			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True
			
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)
			
			# input
			slideInput()

			# timeout			
			if timer_sec >= limit:
				section1Done = True
				TTS_said = False
				
		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 6		
		
		### Section 2 ###
		while not section2Done:
			
			# prep slide
			textList = [("This is the \"thermometer\". It indicates how.", "This is the thermometer. It indicates how intensely you are performing the mental task at any given moment.", 
						 "std", (SCREEN_WIDTH//2, 50)),
						("intensely you are performing the mental task", "", "std", (SCREEN_WIDTH//2, 105)),
						("at any given moment.", "", "std", (SCREEN_WIDTH//2, 160))]
			imageList = []			

			# draw thermo outline
			pygame.draw.rect(SURFACE_MAIN, (255,255,255), pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2), 5) 
			# draw thermo inner area
			pygame.draw.rect(SURFACE_MAIN, (0,0,0),       pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2))
			# draw thermo fill area
			pygame.draw.rect(SURFACE_MAIN, (0,255,0),     pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//4 +100, 30, -10))

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)
			
			# input
			slideInput()	

			# timeout			
			if timer_sec >= limit:
				section2Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 8
		timer_fade = 0
		
		### Section 3 ###
		while not section3Done:

			# prep slide
			textList = [("As you perform the mental task, the thermometer.", "As you perform the mental task, the thermometer fills up.", "std", (SCREEN_WIDTH//2, 50)),
						("fills up.", "", "std", (SCREEN_WIDTH//2, 105))]
			imageList = []#[(image_task, image_task_coords)]	

			# calculate height of thermo fill area
			barheight = (timer_sec / limit) * 510
			# limit thermo fill area
			if barheight > SCREEN_HEIGHT//2: barheight = SCREEN_HEIGHT//2
			
			# draw thermo
			pygame.draw.rect(SURFACE_MAIN, (255,255,255), pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2), 5) 
			pygame.draw.rect(SURFACE_MAIN, (0,0,0),       pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2))
			pygame.draw.rect(SURFACE_MAIN, (0,255,0),     pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//4 +100, 30, barheight*-1))			
			
			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True

			# image fade-in
			if TTS_said and timer_sec > 0:
				timer_fade += 1
			
			timer_fine = getMilliseconds(timer_fade)
			percentage = timer_fine / (limit/2)
			if percentage < 0: percentage = 0
			if percentage > 1: percentage = 1
			alpha = percentage * 255
			blit_alpha(SURFACE_MAIN, image_task, image_task_coords, alpha)
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)
			
			# input
			slideInput()
			
			# timeout 			
			if timer_sec >= limit:
				section3Done = True
				TTS_said = False					

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 6		

		### Section 4 ###
		while not section4Done:
			
			# prep slide
			textList = [("To activate a command, you need to fill the", "To activate a command, you need to fill the thermometer up completely.", "std", (SCREEN_WIDTH//2, 50)),
						("thermometer up completely.", "", "std", (SCREEN_WIDTH//2, 105))]
			imageList = [(image_task, image_task_coords)]	
			
			# draw thermo
			pygame.draw.rect(SURFACE_MAIN, (255,255,255), pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2), 5) 
			pygame.draw.rect(SURFACE_MAIN, (0,0,0),       pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2))
			pygame.draw.rect(SURFACE_MAIN, (0,255,0),     pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2*-1))		

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True
			
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)
			
			# input
			slideInput()
			
			# timeout			
			if timer_sec >= limit:
				section4Done = True
				TTS_said = False
				
		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 6

		### Section 5 ###
		while not section5Done:
			
			# prep slide
			textList = [("The number next to the thermometer is your threshold.", 
						 "The number next to the thermometer is your threshold. The threshold indicates how intensely you need to perform the mental task to fill the thermometer.", "small", 
						 (SCREEN_WIDTH//2, 50)),
						("The threshold indicates how intensely you need to perform", "", "small", (SCREEN_WIDTH//2, 105)),
						("the mental task to fill the thermometer.", "", "small", (SCREEN_WIDTH//2, 160))]
			imageList = [(image_task, image_task_coords)]	
			
			# draw threshold number
			drawText(str(CONFIG.NF_threshold), "std", (SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2), CONFIG.white, True)
			
			# draw thermo
			pygame.draw.rect(SURFACE_MAIN, (255,255,255), pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2), 5) 
			pygame.draw.rect(SURFACE_MAIN, (0,0,0),       pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2))
			pygame.draw.rect(SURFACE_MAIN, (0,255,0),     pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2*-1))				

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)
			
			# input
			slideInput()

			# timeout 			
			if timer_sec >= limit:
				section5Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 6
		timer_fade = 0

		### Section 6 ###
		while not section6Done:

			# prep slide
			textList = [("In the next step, we'll try filling up the thermometer.", 
						 "In the next step, we will try filling up the thermometer. While you perform the mental task, observe the level of the thermometer.", "small", (SCREEN_WIDTH//2, 50)),
						("While you perform the mental task, observe the", "", "small", (SCREEN_WIDTH//2, 105)),
						("level of the thermometer.", "", "small", (SCREEN_WIDTH//2, 160))]
			if timer_sec < 1: imageList = [(image_task, image_task_coords)]
			else: imageList = []
			
			# draw threshold number
			drawText(str(CONFIG.NF_threshold), "std", (SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2), CONFIG.white, True)
			
			# calculate thermo fill area
			barheight = (timer_sec / limit) * 510
			# limit thermo fill area
			if barheight > SCREEN_HEIGHT//2: barheight = SCREEN_HEIGHT//2
			
			# draw thermo
			pygame.draw.rect(SURFACE_MAIN, (255,255,255), pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2), 5) 
			pygame.draw.rect(SURFACE_MAIN, (0,0,0),       pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2))
			pygame.draw.rect(SURFACE_MAIN, (0,255,0),     pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2*-1 + barheight))				

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()


			# image fade-out
			if TTS_said and timer_sec > 0:
				timer_fade += 1
			
			timer_fine = getMilliseconds(timer_fade)
			percentage = timer_fine / (limit/2)
			if percentage < 0: percentage = 0
			if percentage > 1: percentage = 1
			alpha = (percentage * 255) - 255
			blit_alpha(SURFACE_MAIN, image_task, image_task_coords, abs(alpha))
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)
			
			# input
			slideInput()

			# timeout			
			if timer_sec >= limit:
				section6Done = True
				TTS_said = False			

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 8

		### Section 7 ###
		while not section7Done:

			# prep slide
			textList = [("If it is too hard to fill the thermometer completely,", 
						 "If it is too hard to fill the thermometer completely, press the DOWN ARROW key to lower the threshold. If the thermometer fills up too quickly, press the UP ARROW key to raise the threshold.", 
						 "small", (SCREEN_WIDTH//2, 50)),
						("press the DOWN ARROW KEY to lower the threshold.", "", "small", (SCREEN_WIDTH//2, 105)),
						("If the thermometer fills up too quickly,", "", "small", (SCREEN_WIDTH//2, 160)),
						("press the UP ARROW KEY to raise the threshold.", "", "small", (SCREEN_WIDTH//2, 215))]
			imageList = []

			# draw threshold number
			drawText(str(CONFIG.NF_threshold), "std", (SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2), CONFIG.white, True)
			
			# draw thermo
			pygame.draw.rect(SURFACE_MAIN, (255,255,255), pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2), 5) 
			pygame.draw.rect(SURFACE_MAIN, (0,0,0),       pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2))
			pygame.draw.rect(SURFACE_MAIN, (0,255,0),     pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//4 +100, 30, -1))				

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
	
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# input
			slideInput()

			# timeout
			if timer_sec >= limit:
				section7Done = True
				TTS_said = False			

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 5
		TTS_said2 = False
		
		### Section 8: Check for TSI input ###
		while not section8Done:

			# read NF values
			if NFTicker <= CONFIG.NF_reader_frequency:
				readNFValues()
				NFTicker+=1
			else:
				NFTicker = 1	
			
			# draw threshold number
			drawText(str(CONFIG.NF_threshold), "std", (SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2), CONFIG.white, True)
			
			# draw thermometer
			pygame.draw.rect(SURFACE_MAIN, (255,255,255), pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2), 5) 
			pygame.draw.rect(SURFACE_MAIN, (0,0,0),       pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2))
			pygame.draw.rect(SURFACE_MAIN, (0,255,0),     pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//4 +100, 30, -1))						
			
			# check for TSI input
			if "DATAPOINT_NUMBER" not in globals():
			
				# prep slide
				textList = [("Not detecting input from Turbo-Satori...", "Not detecting input from Turbo-Satori. Please check if the Neurofeedback settings are correct.", "small", (SCREEN_WIDTH//2, 50)),
							("Please check if the Neurofeedback settings are correct.", "", "small", (SCREEN_WIDTH//2, 105))]
				imageList = []			

				# draw slide
				drawSlide(textList, imageList, TTS_said)
				TTS_said = True
			
				# put on indefinite hold until TSI sends input
				timer = 0
			
			# input found!
			else:
				
				# prep slide
				textList = [("Input detected! Threshold detection starts in...", "Input detected! Threshold detection starts in 5 seconds.", "small", (SCREEN_WIDTH//2, 50))]
				imageList = []			

				# draw slide
				drawSlide(textList, imageList, TTS_said2)		
				TTS_said2 = True
				
				# draw timer
				drawText(str(limit - timer_sec), "small", (SCREEN_WIDTH//2, 105), CONFIG.white, True)
				
				# draw progress bar
				timer_fine = int((timer / CONFIG.fps_target) *100)
				drawProgressBar(timer_fine, limit*100)
			
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# input
			slideInput()

			# timeout
			if timer_sec >= limit:
				# clear NF value
				clearNFFolder()
				section8Done = True

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 5
		TTS_said = False
		clearNFFolder()

		### Section 9: Threshold detection ###
		while not section9Done:

			# prep slide
			textList = [("Try it out now!", "Try it out now! Press UP to raise the threshold and DOWN to lower it. Press SPACEBAR when you've found a comfortable threshold.", "small", (SCREEN_WIDTH//2, 50)),
						("Press UP to raise the threshold and DOWN to lower it.", "", "small", (SCREEN_WIDTH//2, 105)), 
						("Press SPACEBAR when you've found a comfortable threshold.", "", "small", (SCREEN_WIDTH//2, 160))]
			imageList = []		

			# draw threshold number
			drawText(str(CONFIG.NF_threshold), "std", (SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2), CONFIG.white, True)
			
			# read NF values
			if NFTicker <= CONFIG.NF_reader_frequency:
				readNFValues()
				NFTicker+=1
			else:
				NFTicker = 1	
			
			# calculate thermo fill percentage
			if CONFIG.NF_mode == "oxy":
				percentage = (float(NFOXYVALUE)/CONFIG.NF_threshold)
			elif CONFIG.NF_mode == "deoxy":
				percentage = (float(NFDEOXYVALUE)/CONFIG.NF_threshold)
			elif CONFIG.NF_mode == "avg":
				percentage = float( int(NFDEOXYVALUE) + int(NFOXYVALUE))//2/CONFIG.NF_threshold
			
			# limit fill percentage
			if percentage > 1: percentage = 1
			
			# calculate fill area size
			barheight = int((459 * percentage )) * -1
			
			# limit fill area
			if barheight > 0: barheight = 0
			
			# draw thermo outline
			pygame.draw.rect(SURFACE_MAIN, (255,255,255), pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2), 5) 
			# draw thermo inner area
			pygame.draw.rect(SURFACE_MAIN, (0,0,0), pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2))
			# draw thermo fill
			pygame.draw.rect(SURFACE_MAIN, (0,255,0), pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//4 +100, 30, barheight))		

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True
			
			# input
			events_list = pygame.event.get()
			for event in events_list:
				
				# quit program via X
				if event.type == pygame.QUIT:
					quitProgram()				
				
				# keypress events
				if event.type == pygame.KEYDOWN:
					
					# advance
					if event.key == pygame.K_SPACE:
						# clear NF folder
						clearNFFolder()
						# end slide
						section9Done = True
						TTS_said = False
						# save threshold value
						CONFIG.set("TURBO-SATORI SETTINGS","nf_threshold",str(CONFIG.NF_threshold))
						with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)			
						writeToLog("New threshold: " + str(CONFIG.NF_threshold))
						# advance
						if CONFIG.training: training()
						else: main_loop(WORD_LIST)
					
					# change threshold
					if event.key == pygame.K_UP:
						CONFIG.NF_threshold += 1
					if event.key == pygame.K_DOWN and CONFIG.NF_threshold > 1:
						CONFIG.NF_threshold -= 1
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			
			# NF wipe every 10 seconds
			if timer_sec >= 10:
				clearNFFolder()
				timer = 0

def localizer():
	'''
	Localizer run
	'''
	global taskList, restList
	
	# logging
	print("Starting localizer")
	writeToLog("Start of localizer run")
	
	# only allow localizer if input set correctly
	if CONFIG.input_type == "KB":
		print("Input type set to Keyboard only! Skipping localizer...")
		writeToLog("Localizer error: Input set to KB only! Skipping...")
		writeToLog("Starting main loop.")
		main_loop(WORD_LIST)	
	
	#########
	## Init #
	#########
	
	# display
	SURFACE_MAIN.fill((0,0,0))
	pygame.display.flip()
	
	# timer
	timer = 0
	limit = 6
	
	# NF ticker
	NFTicker = 1
	
	# TTS
	TTS_said = False
	
	# flags
	
	if CONFIG.showInstructions:
		section1Done  = False
		section2Done  = False
		section3Done  = False
		section4Done  = False
		section5Done  = False
		section6Done  = False
		section7Done  = False
		localizerDone = False
	else:
		section1Done  = True
		section2Done  = True
		section3Done  = False
		section4Done  = False
		section5Done  = False
		section6Done  = False
		section7Done  = False
		localizerDone = False		
	
	#########
	## loop #
	#########
	
	while True:
		
		# loop maintenance
		timer += 1
		timer_sec = getSeconds(timer)
		updateSlide()
		
		
		############
		## slides ##
		############
		
		### Section 1 ###
		while not section1Done:
			
			# prep slide
			textList = [("We will now perform a localizer run to determine", "We will now perform a localizer run to determine which channel picks up the mental task the best.", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)),
						("which channel picks up the mental task the best.", "", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 +55))]
			imageList = []		

			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True

			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()			
			
			# input
			slideInput()				
			
			# timeout
			if timer_sec >= limit:
				section1Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 6				
				
		### Section 2 ###
		while not section2Done:
			
			# prep slide
			textList = [("Please perform the mental task while the screen says \"DRAW NUMBERS\".", "Please perform the mental task while the screen says, DRAW NUMBERS. When the screen says, REST, just sit back and relax.", 
					 	 "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)),
						("When the screen says \"REST\", just sit back and relax.", "", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 +55))]
			imageList = []	
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True
	
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)	
			updateSlide()

			# input
			slideInput()
			
			# timeout
			if timer_sec >= limit:
				section2Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	

		### Section 3 ###
		while not section3Done:
			
			# prep slide
			textList = [("Please make sure that Turbo-Satori is running and collecting data.", "Please make sure that Turbo-Satori is running and collecting data. Press the Space Bar when you're ready to start with the localizer.", 
					 	 "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)),
						("Press the Space Bar when you're ready to start with the localizer.", "", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 +55))]
			imageList = []	

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True
			
			# no timeout for this section; advance with spacebar instead
			section3Done = slideInput(pressSpace = True, default = False)
			
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 5
		TTS_said = False
		TTS_said2 = False
		
		### Section 4: Check for TSI input ###
		while not section4Done:
			
			# timeout
			if timer_sec >= limit:
				section4Done = True

			# read NF values
			if NFTicker <= CONFIG.NF_reader_frequency:
				readNFValues()
				NFTicker+=1
			else:
				NFTicker = 1	
			
			# TSI is not streaming...
			if "DATAPOINT_NUMBER" not in globals():
				
				# prep slide
				textList = [("Not detecting input from Turbo-Satori...", "Not detecting input from Turbo-Satori. Please check if the Neurofeedback settings are correct.", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)),
							("Please check if the Neurofeedback settings are correct.", "", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 +55))]
				imageList = []					

				# draw slide
				drawSlide(textList, imageList, TTS_said)
				TTS_said = True				
				
				# freeze timer until there's input
				timer = 0

			# TSI is streaming!			
			else:
				
				# draw timer
				drawText(str(limit - timer_sec), "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+55), CONFIG.white, True)

				# prep slide
				textList = [("Input detected! Localizer run starts in...", "Input detected! Localizer run starts in 5 seconds.", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))]
				imageList = []					

				# draw slide
				drawSlide(textList, imageList, TTS_said2)
				TTS_said2 = True		
				
				# draw progress bar
				timer_fine = int((timer / CONFIG.fps_target) *100)
				drawProgressBar(timer_fine, limit*100)
			
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# input
			slideInput()

		######################
		### localizer loop ###
		######################
		
		# set run ticker
		runNumber = 0
		
		# start loop
		while not localizerDone:
		
			# reset inbetween conditions
			timer = 0
			timer_sec = getSeconds(timer)
			limit = CONFIG.localizer_task_duration
			TTS_said = False
			
			# clear NF value
			clearNFFolder()
			
			# console output
			print("Trial #" + str(runNumber+1) + " \\ " + str( CONFIG.localizerRepetitions ))
			if runNumber + 1 >= CONFIG.localizerRepetitions: print("Long rest phase")
			
			### (Sub)section 5: Task ###
			
			# log condition start point
			taskStartPoint = DATAPOINT_NUMBER
			
			# start loop
			while not section5Done:
				
				# prep slide
				textList = [("DRAW NUMBERS", "Draw numbers.", "std", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))]
				imageList = []				
				
				# read NF values
				if NFTicker <= CONFIG.NF_reader_frequency:
					readNFValues()
					NFTicker+=1
				else:
					NFTicker = 1		
				
				# loop maintenance				
				timer += 1
				timer_sec = getSeconds(timer)
				updateSlide()
				
				# draw progress bar
				timer_fine = int((timer / CONFIG.fps_target) *100)
				drawProgressBar(timer_fine, limit*100)

				# draw slide
				drawSlide(textList, imageList, TTS_said)
				TTS_said = True
				
				# timeout
				if timer_sec >= limit:
				
					# log condition end point & append to list
					taskEndPoint = DATAPOINT_NUMBER
					taskList.append((taskStartPoint, taskEndPoint))
					
					# end loop
					section5Done = True
				
					# clear NF value
					clearNFFolder()
				
				# input
				slideInput()
	
			## reset
			timer = 0
			timer_sec = getSeconds(timer)
			limit = CONFIG.localizer_rest_duration
			TTS_said = False
						
			### (Sub)section 6: Rest ###
			
			# log condition start point
			restStartPoint = DATAPOINT_NUMBER
			
			# start loop
			while not section6Done:

				# prep slide
				textList = [("REST", "Rest.", "std", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))]
				imageList = []	

				# read NF values
				if NFTicker <= CONFIG.NF_reader_frequency:
					readNFValues()
					NFTicker+=1
				else:
					NFTicker = 1		
				
				# loop maintenance				
				timer += 1
				timer_sec = getSeconds(timer)
				updateSlide()
				
				# draw progress bar
				timer_fine = int((timer / CONFIG.fps_target) *100)
				drawProgressBar(timer_fine, limit*100)
				
				# draw slide
				drawSlide(textList, imageList, TTS_said)
				TTS_said = True			
				
				
				# last rest phase? Set limit to CONFIG.localizer_lasttrial_duration
				if runNumber + 1 >= CONFIG.localizerRepetitions:
					limit = CONFIG.localizer_lasttrial_duration
				
				# timeout
				if timer_sec >= limit:
					
					# log condition end point & append to list
					restEndPoint = DATAPOINT_NUMBER
					restList.append((restStartPoint, restEndPoint))
					
					# end loop
					section6Done = True
				
				# input
				slideInput()	
			
			# loop maintenance
			runNumber += 1
			section5Done = False
			section6Done = False
			TTS_said = False
			
			### localizer done! ###
			if runNumber == CONFIG.localizerRepetitions:
			
				# logging
				makeLocalizerProtocol()
				print("Localizer .prt generated")
				writeToLog("Localizer run finished, protocol generated.")
				
				# end loop
				localizerDone = True
				
				# clear NF value
				clearNFFolder()

		### Section 7: End ###
		while not section7Done:
				
			# prep slide
			textList = [("Localizer complete. Press Space Bar to continue.", None , "std", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))]
			imageList = []
				
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input 
			section7Done = slideInput(pressSpace = True, default = False)
					
			if section7Done: TTS_said = False	
		
		### advance ###
		if CONFIG.threshold:
			threshold()
		else:
			main_loop(WORD_LIST)


def tutorial():
	'''
	Greeting & task introduction
	'''
	
	############
	### init ###
	############
	
	# assets
	image_pen = pygame.image.load("config/gfx/pen.jpg")
	image_poster = pygame.image.load("config/gfx/poster.jpg")
	image_poster2 = pygame.image.load("config/gfx/poster2.jpg")
	image_pen_coords = (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 100)
	image_poster_coords = (SCREEN_WIDTH//2 - 280, SCREEN_HEIGHT//2 - 220)
	
	# display
	SURFACE_MAIN.fill((0,0,0))
	pygame.display.flip()
	
	# timer
	timer = 0
	limit = 6
	
	# TTS
	TTS_said = False
	
	# flags
	section1Done  = False
	section2Done  = False
	section3Done  = False
	section4Done  = False
	section5Done  = False
	section6Done  = False
	section7Done  = False
	section8Done  = False
	section9Done  = False
	section10Done = False
	section11Done = False
	section12Done = False
	section13Done = False
	section14Done = False
	section15Done = False
	section16Done = False
	section17Done = False
	
	############
	### loop ###
	############
	
	while True:
		
		# Maintenance
		updateSlide()
		timer += 1
		timer_sec = getSeconds(timer)
		
		# Input
		slideInput()	
		
		### Section 1 ###
		while not section1Done:
			
			# prep slide
			textList = [("Welcome to the fNIRS Sentence Speller!", "Welcome to the f nears Sentence Speller!", "std", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))]
			imageList = []
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True		
			
			# input
			slideInput()				

			# timeout			
			if timer_sec >= limit:
				section1Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 6
		
		### Section 2 ###
		while not section2Done:
	
			# prep slide
			textList = [("In this tutorial, you will learn how to control the speller.", None, "std", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))]
			imageList = []
			
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input
			slideInput()
			
			# timeout
			if timer_sec >= limit:
				section2Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 6
		
		### Section 3 ###
		while not section3Done:

			# prep slide
			textList = [("Please ensure that your room is as dark as possible.", None, "std", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))]
			imageList = []

			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
		
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	

			# input
			slideInput()			
	
			# timeout
			if timer_sec >= limit:
				section3Done = True
				TTS_said = False
	

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 6
		
		### Section 4 ###
		while not section4Done:

			# prep slide
			textList = [("Turn off the lights, and close the curtains if possible.", None, "std", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))]
			imageList = []

			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	

			# input
			slideInput()						

			# timeout
			if timer_sec >= limit:
				section4Done = True
				TTS_said = False
			

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		
		### Section 5 ###
		while not section5Done:

			# prep slide
			textList = [("Press Space Bar once you're ready to continue.", None, "std", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))]
			imageList = []
			
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input
			section5Done = slideInput(pressSpace = True, default = False)

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 6
		TTS_said = False
		
		### Section 6 ###
		while not section6Done:
			
			# prep slide
			textList = [("We will now practice the mental task used to control the speller.", None, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))]
			imageList = []
			
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input
			slideInput()

			# timeout			
			if timer_sec >= limit:
				section6Done = True
				TTS_said = False	

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 6
		
		### Section 7 ###
		while not section7Done:
			
			# prep slide
			textList = [("Sit back comfortably, relax your jaw and attend to the middle of the screen.", None, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))]
			imageList = []

			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input
			slideInput()
			
			# timeout
			if timer_sec >= limit:
				section7Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 6
		
		### Section 8 ###
		while not section8Done:
			
			# prep slide
			textList = [("Imagine that you're holding a metal ballpoint pen in your dominant hand.", None, "small", (SCREEN_WIDTH//2, 55))]
			imageList = [(image_pen, image_pen_coords)]

			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input
			slideInput()	
			
			# timeout			
			if timer_sec >= limit:
				section8Done = True
				TTS_said = False
			

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 10
		
		### Section 9 ###
		while not section9Done:

			# prep slide
			textList = [("Take a moment to imagine it as vividly as possible.", None, "small", (SCREEN_WIDTH//2, 55))]
			imageList = [(image_pen, image_pen_coords)]

			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input 
			slideInput()
			
			# timeout
			if timer_sec >= limit:
				section9Done = True
				TTS_said = False
			
		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 10
		
		### Section 10 ###
		while not section10Done:

			# prep slide
			textList = [("Focus on how the hexagonal profile of the pen feels.", None, "small", (SCREEN_WIDTH//2, 55))]
			imageList = [(image_pen, image_pen_coords)]
			
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input 
			slideInput()

			# timeout
			if timer_sec >= limit:
				section10Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 10
		
		### Section 11 ###
		while not section11Done:

			# prep slide
			textList = [("Imagine turning it around in your hand.", None, "small", (SCREEN_WIDTH//2, 55))]
			imageList = [(image_pen, image_pen_coords)]
				
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input 
			slideInput()
					
			# timeout
			if timer_sec >= limit:
				section11Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 10
		
		### Section 12 ###
		while not section12Done:

			# prep slide
			textList = [("Imagine clicking it a few times.", None, "small", (SCREEN_WIDTH//2, 55))]
			imageList = [(image_pen, image_pen_coords)]
				
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input 
			slideInput()
					
			# timeout
			if timer_sec >= limit:
				section12Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 5
		
		### Section 13 ###
		while not section13Done:
			
			# prep slide
			textList = [("Click it to \"On\" now.", "Click it to: On, now.", "small", (SCREEN_WIDTH//2, 55))]
			imageList = [(image_pen, image_pen_coords)]
				
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input 
			slideInput()
					
			# timeout
			if timer_sec >= limit:
				section13Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 10
		
		### Section 14 ###
		while not section14Done:

			# prep slide
			textList = [("Now, imagine that an A3 poster is hanging in front of you,", "Now, imagine that an A3 poster is hanging in front of you, a bit less than an arm's length away." , "small", (SCREEN_WIDTH//2, 55)),
						("a bit less than an arm's length away.", "" , "small", (SCREEN_WIDTH//2, 110))]
			imageList = [(image_poster, image_poster_coords)]
				
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input 
			slideInput()
					
			# timeout
			if timer_sec >= limit:
				section14Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 10
		
		### Section 15 ###
		while not section15Done:

			# prep slide
			textList = [("Imagine drawing some numbers onto the poster.", None, "small", (SCREEN_WIDTH//2, 55))]
			imageList = [(image_poster2, image_poster_coords)]
				
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input 
			slideInput()
					
			# timeout
			if timer_sec >= limit:
				section15Done = True
				TTS_said = False
			
		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 10

		### Section 16 ###	
		while not section16Done:

			# prep slide
			textList = [("Draw them big, as if you were standing at the podium of a lecture hall", 
					     "Draw them big, as if you were standing at the podium of a lecture hall and wanted people in the last row to be able to read them!" , "small", (SCREEN_WIDTH//2, 55)),
						("and wanted people in the last row to be able to read them!", "" , "small", (SCREEN_WIDTH//2, 110))]
			imageList = [(image_poster2, image_poster_coords)]
				
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input 
			slideInput()
					
			# timeout
			if timer_sec >= limit:
				section16Done = True
				TTS_said = False	

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		
		### Section 17 ###
		while not section17Done:
				
			# prep slide
			textList = [("Try it a few times. Draw up to the number 20.", 
					     "Try it a few times. Draw up to the number 20. Once you're comfortable with this task, press Space Bar to continue." , "small", (SCREEN_WIDTH//2, 55)),
						("Once you're comfortable with this task, press Space Bar to continue.", "" , "small", (SCREEN_WIDTH//2, 110))]
			imageList = [(image_poster2, image_poster_coords)]
				
			# loop maintenance
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True	
			
			# input 
			section17Done = slideInput(pressSpace = True, default = False)
					
			if section17Done: TTS_said = False	
		
		###############
		### advance ###
		###############
		
		# start localizer
		if CONFIG.localizer:
			print("Introduction done. Starting localizer...")
			writeToLog("Starting localizer.")
			localizer()
		# localizer turned off, start threshold
		elif CONFIG.threshold:
			print("Introduction done. Skipping localizer, starting threshold...")
			writeToLog("Skipping localizer, starting threshold.")
			threshold()
		# localizer and threshold turned of, start training
			print("Introduction done. Skipping localizer & threshold, starting training...")
			writeToLog("Skipping localizer & threshold, starting training.")
			training()		
		# everything else turned off, start main loop
		else:
			print("Introduction done. Sipping localizer, threshold & training. Starting main loop...")
			writeToLog("Skipping all, starting main loop.")
			main_loop(WORD_LIST)

def training():
	'''
	Interface training & instructed encoding run. WIP
	'''
	
	# logging
	print("Starting training.")
	writeToLog("Start of training run")
	
	#########
	## Init #
	#########

	# assets
	image_task = pygame.image.load("config/gfx/mental_task.png").convert_alpha()
	image_task = pygame.transform.smoothscale(image_task, (200, 200))
	image_task_coords = (SCREEN_WIDTH//2 + 230, SCREEN_HEIGHT//2 + 130)
	
	# display
	SURFACE_MAIN.fill((0,0,0))
	pygame.display.flip()
	
	# timer
	timer = 0
	limit = 5
	
	# NF ticker
	NFTicker = 1
	
	# TTS
	TTS_said = False
	
	# flags
	section1Done  = False
	section2Done  = False
	section3Done  = False
	section4Done  = False
	section5Done  = False
	section6Done  = False
	section7Done  = False
	section8Done  = False
	
	### LOOP ###
	while True:
	
		# Maintenance
		updateSlide()
		timer += 1
		timer_sec = getSeconds(timer)
		
		# Input
		slideInput()	
		
		### Section 1 ###
		while not section1Done:
			
			# prep slide
			textList = [("We'll try out the user interface now,", "We'll try out the user interface now, and after that it's time for the first proper test run!", "std", (SCREEN_WIDTH//2, 55)),
						("and after that it's time for the first proper test run!", "", "std", (SCREEN_WIDTH//2, 115))]
			imageList = []
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True		
			
			# input
			slideInput()				

			# timeout			
			if timer_sec >= limit:
				section1Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 8	

		### Section 2 ###
		while not section2Done:
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw UI
			drawText("MIDDLE",  "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("BEFORE",  "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("AFTER",   "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("ERROR",   "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.white, True)
			drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.white, True)		

			# prep slide
			textList = [("This is the user interface of the speller. It consists of", "This is the user interface of the speller. It consists of BEFORE, AFTER, ERROR, the MIDDLE WORD and PREDICT.", "small", (SCREEN_WIDTH//2, 55)),
						("BEFORE, AFTER, ERROR, the MIDDLE WORD and PREDICT.", "", "small", (SCREEN_WIDTH//2, 110))]
			imageList = []
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True		
			
			# input
			slideInput()				

			# timeout			
			if timer_sec >= limit:
				section2Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 15	
		tts_before  = False
		tts_after   = False
		tts_error   = False
		tts_predict = False
		tts_middle  = False

		### Section 3 ###
		while not section3Done:
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			timer_mil = getMilliseconds(timer)
			
			# draw UI
			drawText("MIDDLE", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.white, True)
			drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.white, True)		

			# prep slide
			textList = [("Each of these control elements will be highlighted", "Each of these control elements will be highlighted for a short time, like this:", "small", (SCREEN_WIDTH//2, 55)),
						("for a short time, like this:", "", "small", (SCREEN_WIDTH//2, 110))]
			imageList = []
			
			# cycle through control elements
			if timer_mil > 0.4 and timer_sec <= limit//5:
				drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.green, True)
				if TTS_ON and not tts_before:
					TTS_ENGINE.say("BEFORE.")
					TTS_ENGINE.runAndWait()
					tts_before = True
			elif timer_sec >= 1*(limit//5) and timer_sec <= 2*(limit//5):
				drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.green, True)
				if TTS_ON and not tts_after:
					TTS_ENGINE.say("AFTER.")
					TTS_ENGINE.runAndWait()
					tts_after = True
			elif timer_sec >= 2*(limit//5) and timer_sec <= 3*(limit//5):
				drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.green, True)
				if TTS_ON and not tts_error:
					TTS_ENGINE.say("ERROR.")
					TTS_ENGINE.runAndWait()
					tts_error = True
			elif timer_sec >= 3*(limit//5) and timer_sec <= 4*(limit//5):
				drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.green, True)	
				if TTS_ON and not tts_predict:
					TTS_ENGINE.say("PREDICT.")
					TTS_ENGINE.runAndWait()
					tts_predict = True
			elif timer_sec >= 4*(limit//5) and timer_sec <= 5*(limit//5):
				drawText("MIDDLE", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.green, True)
				if TTS_ON and not tts_middle:
					TTS_ENGINE.say("MIDDLE WORD.")
					TTS_ENGINE.runAndWait()
					tts_middle = True
				
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True		
			
			# input
			slideInput()				

			# timeout			
			if timer_sec >= limit:
				section3Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 8	

		### Section 4 ###
		while not section4Done:
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw UI
			drawText("MIDDLE",  "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.green, True)
			drawText("BEFORE",  "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("AFTER",   "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("ERROR",   "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.white, True)
			drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.white, True)		

			# prep slide
			textList = [("To activate a command, you will need to perform the mental", "To activate a command, you will need to perform the mental task while the command is highlighted.", "small", (SCREEN_WIDTH//2, 55)),
						("task while the command is highlighted.", "", "small", (SCREEN_WIDTH//2, 110))]
			imageList = []

			# calculate height of thermo fill area
			barheight = (timer_sec / limit) * 510
			# limit thermo fill area
			if barheight > 459: barheight = 459
			
			# draw thermo
			pygame.draw.rect(SURFACE_MAIN, (255,255,255), pygame.Rect(55, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2), 5) 
			pygame.draw.rect(SURFACE_MAIN, (0,0,0),       pygame.Rect(55, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2))
			pygame.draw.rect(SURFACE_MAIN, (0,255,0),     pygame.Rect(55, SCREEN_HEIGHT//2+SCREEN_HEIGHT//4 +100, 30, barheight*-1))		
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True		

			# image fade-in
			if timer_sec > 0:
				timer_mil = getMilliseconds(timer) -1
				percentage = timer_mil / (limit/2)
				if percentage > 1: percentage = 1
				alpha = percentage * 255
				blit_alpha(SURFACE_MAIN, image_task, image_task_coords, alpha)
			
			# input
			slideInput()				

			# timeout			
			if timer_sec >= limit:
				section4Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 10
		timer_fade = 0
		
		### Section 5 ###
		while not section5Done:
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()

			# draw UI
			if timer_sec < 1: drawText("MIDDLE", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.green, True)
			else: drawText("MIDDLE", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.white, True)
			drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.white, True)		

			# prep slide
			textList = [("In this example, we just selected the MIDDLE WORD.", "In this example, we just selected the MIDDLE WORD. After you select, the whole process restarts.", "small", (SCREEN_WIDTH//2, 55)),
						("After you select, the whole process restarts.", "", "small", (SCREEN_WIDTH//2, 110))]
			imageList = []

			# image fade-out
			if TTS_said and timer_sec > 0:
				timer_fade += 1
			
			timer_fine = getMilliseconds(timer_fade)
			percentage = timer_fine / (limit/2)
			if percentage < 0: percentage = 0
			if percentage > 1: percentage = 1
			alpha = (percentage * 255) - 255
			blit_alpha(SURFACE_MAIN, image_task, image_task_coords, abs(alpha))

			# calculate height of thermo fill area
			barheight = 459 - ((timer_sec / limit) * 510)
			# limit thermo fill area
			if barheight > 459: barheight = 459
			if barheight < 0: barheight = 0
			
			# draw thermo
			pygame.draw.rect(SURFACE_MAIN, (255,255,255), pygame.Rect(55, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2), 5) 
			pygame.draw.rect(SURFACE_MAIN, (0,0,0),       pygame.Rect(55, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 +100, 30, SCREEN_HEIGHT//2))
			pygame.draw.rect(SURFACE_MAIN, (0,255,0),     pygame.Rect(55, SCREEN_HEIGHT//2+SCREEN_HEIGHT//4 +100, 30, barheight*-1))		
			
			timer_mil = getMilliseconds(timer)
			# cycle through control elements
			if timer_mil > 1.0 and timer_sec <= limit//5:
				drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.green, True)
			elif timer_sec >= 1*(limit//5) and timer_sec <= 2*(limit//5):
				drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.green, True)
			elif timer_sec >= 2*(limit//5) and timer_sec <= 3*(limit//5):
				drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.green, True)
			elif timer_sec >= 3*(limit//5) and timer_sec <= 4*(limit//5):
				drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.green, True)	
			elif timer_sec >= 4*(limit//5) and timer_sec <= 5*(limit//5):
				drawText("MIDDLE", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.green, True)
			
			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True		
			
			# input
			slideInput()				

			# timeout			
			if timer_sec >= limit:
				section5Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 7			

		### Section 6 ###
		while not section6Done:
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			middleWord = findMiddle(WORD_LIST)
			
			# draw UI
			if timer > 1: drawText(middleWord, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.green, True)
			else: drawText("MIDDLE", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.green, True)
			drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.white, True)
			drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.white, True)		

			# prep slide
			textList = [("\"Middle\" is the word you're currently selecting from the dictionary.", "Middle, is the word you're currently selecting from the dictionary. On the start of each run, it will be. " +middleWord+ ". By default.", "small", (SCREEN_WIDTH//2, 55)),
						("On the start of each trial, it will be " +middleWord+ " by default.", "", "small", (SCREEN_WIDTH//2, 110))]
			imageList = []

			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True		
			
			# input
			slideInput()				

			# timeout			
			if timer_sec >= limit:
				section6Done = True
				TTS_said = False

		## reset
		timer = 0
		timer_sec = getSeconds(timer)	
		limit = 6	

		### Section 7 ###
		while not section7Done:
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			middleWord = findMiddle(WORD_LIST)
			
			# draw UI
			if timer_sec < 2: drawText(middleWord, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.green, True)
			else: 
				drawText(middleWord, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.white, True)
				drawText("Look", "small", (SCREEN_WIDTH//2-300, SCREEN_HEIGHT-200), CONFIG.white, True)
			drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.white, True)
			drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.white, True)		

			# prep slide
			textList = [("Activate the MIDDLE WORD command to confirm the selected", "Activate the MIDDLE WORD command to confirm the selected word. It's then written down, and a new trial starts.", "small", (SCREEN_WIDTH//2, 55)),
						("word. It's then written down, and a new trial starts.", "", "small", (SCREEN_WIDTH//2, 110))]
			imageList = []

			timer_mil = getMilliseconds(timer)
			# cycle through control elements
			if timer_sec > 2:
				drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.green, True)
			

			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True		
			
			# input
			slideInput()				

			# timeout			
			if timer_sec >= limit:
				section7Done = True
				TTS_said = False

		### Section 8 ###
		while not section8Done:
			
			# loop maintenance			
			timer += 1
			timer_sec = getSeconds(timer)
			updateSlide()
			middleWord = findMiddle(WORD_LIST)
			
			# draw UI
			drawText("Look", "small", (SCREEN_WIDTH//2-300, SCREEN_HEIGHT-200), CONFIG.white, True)
			drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.green, True)
			drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
			drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.white, True)
			drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.white, True)		

			# prep slide
			textList = [("To select a different word, decide if the word you want", "", "small", (SCREEN_WIDTH//2, 55)),
						("comes BEFORE or AFTER the current word alphabetically,", "", "small", (SCREEN_WIDTH//2, 110)),
						("and select the according command.", "", "small", (SCREEN_WIDTH//2, 165))]
			imageList = []
			
			# cycle through control elements
			if timer_sec > 2:
				drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.green, True)
			

			# draw progress bar
			timer_fine = int((timer / CONFIG.fps_target) *100)
			drawProgressBar(timer_fine, limit*100)

			# draw slide
			drawSlide(textList, imageList, TTS_said)
			TTS_said = True		
			
			# input
			slideInput()				

			# timeout			
			if timer_sec >= limit:
				section8Done = True
				TTS_said = False
	
def main_loop(list):
	'''
	The star of the show. Takes in a list of words, draws UI & command elements and
	cycles through them. 
	'''
	
	## NF globals
	global COUNTER, STEP_COUNTER, INTERNAL_COUNTER, CMD_HISTORY, WORD_HISTORY, OUTPUT_STRING, WORD_LIST, NFOXYVALUE, DATA_FREQUENCY, middle
	## Logging globals
	global phase1StartPoint, phase2StartPoint, phase3StartPoint, phase4StartPoint, phase5StartPoint, phase6StartPoint
	global phase1EndPoint, phase2EndPoint, phase3EndPoint, phase4EndPoint, phase5EndPoint, phase6EndPoint
	global timeoutPhase1StartPoint, timeoutPhase1EndPoint, timeoutPhase2StartPoint, timeoutPhase2EndPoint
	## Timeout phase globals
	global TIMEOUT_COUNTER
	global predictionLetterFlag
	global clickPlayed
	
	## Mini-init ####################################################
	'''
	Runs each time a new main_loop() is called. Clears the NF folder, 
	resets all flags & timers and sets the logging start point.
	'''
	#################################################################
	
	# audio cliok
	clickPlayed = False
	
	# Clear NF folder, save frames
	if BCIConnected:
		clearNFFolder()
	
	# Reset TTS flags
	if TTS_ON:
		tts_before  = False
		tts_after   = False
		tts_error   = False
		tts_predict = False
		tts_middle  = False
		wordsaid    = False
	
	# Set selection to None
	sel = None
	
	# Reset main timer
	timer = 0
	
	# Set fine timer
	timer_fine = int((timer / CONFIG.fps_target) *100)
	
	# Reset NF ticker
	NFTicker = 1
	
	# Reset time-out flag
	timed_out = False
	
	# Reset logging flag
	logWritten = False
	
	# Clear display
	SURFACE_MAIN.fill((0,0,0))
	pygame.display.flip()
	
	# Reset progress bar timers
	timeoutPhasePBTimer = 0
	phase0PBTimer = None
	phase1PBTimer = None
	phase2PBTimer = None
	phase3PBTimer = None
	phase4PBTimer = None
	phase5PBTimer = None
	
	postPhase = False
	postPhaseTimer = 0
	
	# Reset freq timers
	freq_timer = 0
	freq_seconds = 0
	
	# Reset protocol flags
	timeoutPhase1StartPoint = None
	timeoutPhase1EndPoint   = None
	timeoutPhase2StartPoint = None
	timeoutPhase2EndPoint   = None
	phase1StartPoint        = None
	phase1EndPoint          = None
	phase2StartPoint        = None
	phase2EndPoint          = None	
	phase3StartPoint        = None
	phase3EndPoint          = None	
	phase4StartPoint        = None
	phase4EndPoint          = None		
	phase5StartPoint        = None
	phase5EndPoint          = None
	phase6StartPoint        = None
	phase6EndPoint          = None		
	
	# Start loop
	running = True
	
	# Start logging
	start = time.time()
	writeToLog("New main loop called.")
	
	## ## ## ## ## ## ## ##
	## The loop itself   ##
	## ## ## ## ## ## ## ##

	while running:
		
		## Drawing ##########################################
		'''
		Draw debug info, thermo, middle word & output string
		'''
		#####################################################
		
		# draw debug info
		drawDebug()
		
		# draw thermometer if thermo_on & thermo_during_planning
		if CONFIG.thermo_during_planning:
			drawThermometer(CONFIG.NF_mode)
			
		# draw middle word if not in timeout mode
		middle = findMiddle(list)
		if not timed_out: drawText(middle, "std", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.white, True, scale = True)
		
		# draw output string
		drawText(OUTPUT_STRING, "std", (100, SCREEN_HEIGHT - SCREEN_HEIGHT//4), CONFIG.white, False, scale = True)
		
		## Loop maintenance #################################################################
		'''
		Get NF input, handle time, log current middle word, calculate data read rate.
		'''
		#####################################################################################
		
		# If NF input is enabled, read NF values every few ticks (set by NF_reader_frequency)
		
		if BCIConnected:
			if CONFIG.input_type == "BOTH" or CONFIG.input_type == "NF":
				if NFTicker <= CONFIG.NF_reader_frequency:
					readNFValues()
					NFTicker+=1
				else:
					NFTicker = 1
				
		# fix framerate
		CLOCK.tick(CONFIG.fps_target)
		
		# tick clock forwards
		timer += 1
		timer_sec = int(timer//CONFIG.fps_target)
		
		# logging
		if not logWritten: 
			writeToLog("Current middle word: " + middle)
			logWritten = True
		
		# calculate data read rate
		if BCIConnected:		
			if 'DATAPOINT_NUMBER' in globals():
				if freq_timer == 0:
					firstVal = int(DATAPOINT_NUMBER)		
				if freq_seconds >= 2:
					secondVal = int(DATAPOINT_NUMBER)
					DATA_FREQUENCY = (secondVal - firstVal) / 2
					freq_timer = 0
					freq_seconds = 0
				else:
					freq_timer += 1
					freq_seconds = getSeconds(freq_timer)	

		## Input handling ##########################
		'''
		Pass along any input to mainLoopInput()
		'''
		############################################
		
		if CONFIG.input_type == "BOTH":
			mainLoopKBInput(sel, start, list, middle)
			mainLoopNFInput(sel, start, list, middle)
		elif CONFIG.input_type == "KB":
			mainLoopKBInput(sel, start, list, middle)
		elif CONFIG.input_type == "NF":
			mainLoopNFInput(sel, start, list, middle)
		else:
			print("Input type incorrectly configured! Check config.ini!")
			writeToLog("Input configuration error!")
			quitProgram()
				
		## Timeout phase ###############################################
		'''                                                             
		If more than iterLimit iterations without user input, go into   
		a timeout mode showing RETURN and NEW SENTENCE CEs              
		'''                                                             
		################################################################
		
		# too many iters w/o user input?
		if TIMEOUT_COUNTER >= CONFIG.timeout_iterlimit:
			
			# raise timeout flag
			timed_out = True
			
			# fix framerate
			CLOCK.tick(CONFIG.fps_target)

			# flip & clear main surface
			pygame.display.flip()
			SURFACE_MAIN.fill((0,0,0))	
			
			# tick clock forwards
			timer += 1
			timer_sec = int(timer//CONFIG.fps_target)

			# draw UI
			drawText("RETURN", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//3), CONFIG.white, True)
			drawText("NEW SENTENCE", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//3 + 100), CONFIG.white, True)
			sel = None

			# draw output string
			drawText(OUTPUT_STRING, "std", (100, SCREEN_HEIGHT - SCREEN_HEIGHT//4), CONFIG.white, False, scale = True)
			
			#####################
			## RETURN Subphase ##
			#####################
			
			returnPhase = True
			returnTTS = False
			clickPlayed = False
			while returnPhase:

				# draw debug info
				drawDebug()
				
				# draw thermometer if thermo_on & thermo_during_planning
				if CONFIG.thermo_during_planning:
					drawThermometer(CONFIG.NF_mode)

				# If NF input is enabled, read NF values every few ticks (set by NF_reader_frequency)
				if CONFIG.input_type == "BOTH" or CONFIG.input_type == "NF":
					if NFTicker <= CONFIG.NF_reader_frequency:
						readNFValues()
						NFTicker+=1
					else:
						NFTicker = 1

				# input handling
				if CONFIG.input_type == "BOTH":
					mainLoopKBInput(sel, start, list, middle)
					mainLoopNFInput(sel, start, list, middle)
				elif CONFIG.input_type == "KB":
					mainLoopKBInput(sel, start, list, middle)
				elif CONFIG.input_type == "NF":
					mainLoopNFInput(sel, start, list, middle)
				else:
					print("Input type incorrectly configured! Check config.ini!")
					writeToLog("Input configuration error!")
					quitProgram()
				
				# highlight RETURN
				drawText("RETURN", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//3), CONFIG.green, True)
				drawText("NEW SENTENCE", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//3 + 100), CONFIG.white, True)
				sel = "return"			

				# draw output string
				drawText(OUTPUT_STRING, "std", (100, SCREEN_HEIGHT - SCREEN_HEIGHT//4), CONFIG.white, False, scale = True)
			
				# fix framerate
				CLOCK.tick(CONFIG.fps_target)			
				# flip & clear main surface
				pygame.display.flip()
				SURFACE_MAIN.fill((0,0,0))	
				
				# timers
				timeoutPhasePBTimer += 1
				timer_sec = int(timeoutPhasePBTimer//CONFIG.fps_target)
				
				# terminate phase if timer > limit
				if timer_sec > CONFIG.firstPhase: returnPhase = False
				
				# TTS
				if TTS_ON and not returnTTS:
					#TTS_ENGINE.say("Return.")
					#TTS_ENGINE.runAndWait()
					sayVoiceLine("Return.")
					returnTTS = True	

				# logging start
				if timeoutPhase1StartPoint == None and 'DATAPOINT_NUMBER' in globals():
					timeoutPhase1StartPoint = DATAPOINT_NUMBER	
					
				# draw progress bar
				timer_fine = int((timeoutPhasePBTimer / CONFIG.fps_target) *100)
				limit = CONFIG.firstPhase
				drawProgressBar(timer_fine, limit*100)
			
			###########################
			## NEW SENTENCE Subphase ##
			###########################
			
			timeoutPhasePBTimer = 0
			newSentencePhase = True
			newSentenceTTS = False
			clickPlayed = False
			while newSentencePhase:

				# If NF input is enabled, read NF values every few ticks (set by NF_reader_frequency)
				if CONFIG.input_type == "BOTH" or CONFIG.input_type == "NF":
					if NFTicker <= CONFIG.NF_reader_frequency:
						readNFValues()
						NFTicker+=1
					else:
						NFTicker = 1

				# draw debug info
				drawDebug()
				
				# draw thermometer if thermo_on & thermo_during_planning
				if CONFIG.thermo_during_planning:
					drawThermometer(CONFIG.NF_mode)
				
				# input handling
				if CONFIG.input_type == "BOTH":
					mainLoopKBInput(sel, start, list, middle)
					mainLoopNFInput(sel, start, list, middle)
				elif CONFIG.input_type == "KB":
					mainLoopKBInput(sel, start, list, middle)
				elif CONFIG.input_type == "NF":
					mainLoopNFInput(sel, start, list, middle)
				else:
					print("Input type incorrectly configured! Check config.ini!")
					writeToLog("Input configuration error!")
					quitProgram()
				
				# highlight NEW SENTENCE
				drawText("RETURN", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//3), CONFIG.white, True)
				drawText("NEW SENTENCE", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//3 + 100), CONFIG.green, True)
				sel = "newsentence"

				# draw output string
				drawText(OUTPUT_STRING, "std", (100, SCREEN_HEIGHT - SCREEN_HEIGHT//4), CONFIG.white, False, scale = True)
				
				# timers
				timeoutPhasePBTimer += 1
				timer_sec = int(timeoutPhasePBTimer//CONFIG.fps_target)
				
				# terminate phase
				if timer_sec > CONFIG.firstPhase: newSentencePhase = False

				# fix framerate
				CLOCK.tick(CONFIG.fps_target)
				
				# flip & clear main surface
				pygame.display.flip()
				SURFACE_MAIN.fill((0,0,0))	
				
				# TTS
				if TTS_ON and not newSentenceTTS:
					#TTS_ENGINE.say("New sentence.")
					#TTS_ENGINE.runAndWait()
					sayVoiceLine("New sentence.")
					newSentenceTTS = True	
					
				# logging
				if timeoutPhase1EndPoint == None and 'DATAPOINT_NUMBER' in globals():
					timeoutPhase1EndPoint = DATAPOINT_NUMBER
					timeoutPhase1List.append((timeoutPhase1StartPoint, timeoutPhase1EndPoint))
				if timeoutPhase2StartPoint == None and 'DATAPOINT_NUMBER' in globals():
					timeoutPhase2StartPoint = DATAPOINT_NUMBER		
					
				# draw progress bar
				timer_fine = int((timeoutPhasePBTimer / CONFIG.fps_target) *100)
				limit = CONFIG.secondPhase
				drawProgressBar(timer_fine, limit*100)									
			
			#############			
			## Restart ##
			#############
			
			# logging
			if timeoutPhase2EndPoint == None and 'DATAPOINT_NUMBER' in globals():
				timeoutPhase2EndPoint = DATAPOINT_NUMBER
				timeoutPhase2List.append((timeoutPhase2StartPoint, timeoutPhase2EndPoint))
				
			# re-init				
			timer = 0
			timeoutPhasePBTimer = 0
			timeoutPhase1StartPoint = None
			timeoutPhase1EndPoint   = None
			timeoutPhase2StartPoint = None
			timeoutPhase2EndPoint   = None
			
			# highlight nothing
			drawText("RETURN", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//3), CONFIG.white, True)
			drawText("NEW SENTENCE", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//3 + 100), CONFIG.white, True)
			
			# reset selection
			sel = None
			
			# TTS flags
			returnTTS = False
			newSentenceTTS = False
			clickPlayed = False
				
			# flip & clear main surface
			pygame.display.flip()
			SURFACE_MAIN.fill((0,0,0))			
		
		## Main Phase ###################################################
		else:
			
			# logging start
			if phase1StartPoint == None and 'DATAPOINT_NUMBER' in globals():
				phase1StartPoint = DATAPOINT_NUMBER	
			
			##########################################
			## Phase 1: Render all control elements ##
			##########################################
			
			# if statement handles timing
			# TODO: find a less stupid way to do this
			if (
				timer_sec >= CONFIG.initialDelay 
				and 
				(timer_sec - CONFIG.initialDelay) <= CONFIG.firstPhase
				):
				
				# set selection flag
				sel = None

				# progress bar timers
				if phase0PBTimer == None: 
					phase0PBTimer = 0
					clickPlayed = False
				else: phase0PBTimer += 1

				# draw progress bar
				timer_fine = int((phase0PBTimer / CONFIG.fps_target) *100)
				limit = CONFIG.firstPhase
				drawProgressBar(timer_fine, limit*100)
	
				# draw UI
				drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
				drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
				drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.white, True)
				if len(OUTPUT_STRING) > 0 and CONFIG.predictions_on: drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.white, True)	

			#################################
			## Phase 2: Highlight "Before" ##
			#################################
			
			# timing
			if (
				timer_sec - CONFIG.initialDelay >= CONFIG.firstPhase 
				and 
				timer_sec - CONFIG.initialDelay - CONFIG.firstPhase <= CONFIG.secondPhase
				):

				# progress bar timers
				if phase1PBTimer == None: 
					phase1PBTimer = 0
					clickPlayed = False
				else: phase1PBTimer += 1

				# draw progress bar
				timer_fine = int((phase1PBTimer / CONFIG.fps_target) *100)
				limit = CONFIG.secondPhase
				drawProgressBar(timer_fine, limit*100)
				
				# TTS
				if TTS_ON and not tts_before:
					# flip & clear main surface
					pygame.display.flip()
					SURFACE_MAIN.fill((0,0,0))						
					#TTS_ENGINE.say("Before.")
					#TTS_ENGINE.runAndWait()
					sayVoiceLine("Before.")
					tts_before = True	
		
				# logging
				if phase1EndPoint == None and 'DATAPOINT_NUMBER' in globals():
					phase1EndPoint = DATAPOINT_NUMBER
					phase1List.append((phase1StartPoint, phase1EndPoint))
				if phase2StartPoint == None and 'DATAPOINT_NUMBER' in globals():
					phase2StartPoint = DATAPOINT_NUMBER			
				
				# draw thermometer
				if not CONFIG.thermo_during_planning: drawThermometer(CONFIG.NF_mode)
				
				# set selection flag
				sel = "before"
	
				# draw UI
				drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
				drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.white, True)
				drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.green, True)
				if len(OUTPUT_STRING) > 0 and CONFIG.predictions_on: drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.white, True)
			
			################################			
			## Phase 3: Highlight "After" ##
			################################
			
			# timing
			if (
				timer_sec - CONFIG.initialDelay - CONFIG.firstPhase >= CONFIG.secondPhase 
				and 
				timer_sec - CONFIG.initialDelay - CONFIG.firstPhase - CONFIG.secondPhase <= CONFIG.thirdPhase
				):
				
				# progress bar timers
				if phase2PBTimer == None: 
					phase2PBTimer = 0
					clickPlayed = False
				else: phase2PBTimer += 1

				# draw progress bar
				timer_fine = int((phase2PBTimer / CONFIG.fps_target) *100)
				limit = CONFIG.thirdPhase
				drawProgressBar(timer_fine, limit*100)
				
				# TTS
				if TTS_ON and not tts_after:
					# flip & clear main surface
					pygame.display.flip()
					SURFACE_MAIN.fill((0,0,0))					
					#TTS_ENGINE.say("After.")
					#TTS_ENGINE.runAndWait()
					sayVoiceLine("After.")
					tts_after = True				
				
				# logging
				if phase2EndPoint == None and 'DATAPOINT_NUMBER' in globals():
					phase2EndPoint = DATAPOINT_NUMBER
					phase2List.append((phase2StartPoint, phase2EndPoint))
					phase3StartPoint = DATAPOINT_NUMBER
	
				# draw thermometer
				if not CONFIG.thermo_during_planning:
					drawThermometer(CONFIG.NF_mode)
	
				# set selection flag
				sel = "after"
				
				# draw UI
				drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.green, True)
				drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.white, True)
				drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
				if len(OUTPUT_STRING) > 0 and CONFIG.predictions_on: drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.white, True)
			
			################################
			## Phase 4: Highlight "Error" ##
			################################
			
			# timing
			if (
				timer_sec - CONFIG.initialDelay - CONFIG.firstPhase - CONFIG.secondPhase >= CONFIG.thirdPhase 
				and 
				timer_sec - CONFIG.initialDelay - CONFIG.firstPhase - CONFIG.secondPhase - CONFIG.thirdPhase <= CONFIG.fourthPhase
				):
				
				# progress bar timers
				if phase3PBTimer == None: 
					phase3PBTimer = 0
					clickPlayed = False
				else: phase3PBTimer += 1

				# draw progress bar
				timer_fine = int((phase3PBTimer / CONFIG.fps_target) *100)
				limit = CONFIG.fourthPhase
				drawProgressBar(timer_fine, limit*100)	
				
				# TTS
				if TTS_ON and not tts_error:
					# flip & clear main surface
					pygame.display.flip()
					SURFACE_MAIN.fill((0,0,0))					
					#TTS_ENGINE.say("Error.")
					#TTS_ENGINE.runAndWait()
					sayVoiceLine("Error.")
					tts_error = True
				
				# logging
				if phase3EndPoint == None and 'DATAPOINT_NUMBER' in globals():
					phase3EndPoint = DATAPOINT_NUMBER
					phase3List.append((phase3StartPoint, phase3EndPoint))
					phase4StartPoint = DATAPOINT_NUMBER
				
				# draw thermometer
				if not CONFIG.thermo_during_planning:
					drawThermometer(CONFIG.NF_mode)
				
				# set selection flag
				sel = "error"
				
				# draw UI
				drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
				drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.green, True)
				drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
				if len(OUTPUT_STRING) > 0 and CONFIG.predictions_on: drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.white, True)
			
			################################		
			## Phase 5: Highlight predict ##
			################################
			
			# timing:
			# third clause makes sure PREDICT doesn't show up if nothing's encoded yet
			# or predictions are turned off in config.ini
			if (
				timer_sec - CONFIG.initialDelay - CONFIG.firstPhase - CONFIG.secondPhase - CONFIG.thirdPhase >= CONFIG.fourthPhase 
				and 
				timer_sec - CONFIG.initialDelay - CONFIG.firstPhase - CONFIG.secondPhase - CONFIG.thirdPhase - CONFIG.fourthPhase <= CONFIG.fifthPhase
				and 
				(len(OUTPUT_STRING) > 0 and CONFIG.predictions_on)
				): 
				
				# progress bar timers
				if phase4PBTimer == None: 
					phase4PBTimer = 0
					clickPlayed = False
				else: phase4PBTimer += 1

				# draw progress bar
				timer_fine = int((phase4PBTimer / CONFIG.fps_target) *100)
				limit = CONFIG.fifthPhase
				drawProgressBar(timer_fine, limit*100)	
				
				# TTS
				if TTS_ON and not tts_predict:
					# flip & clear main surface
					pygame.display.flip()
					SURFACE_MAIN.fill((0,0,0))					
					#TTS_ENGINE.say("Predict.")
					#TTS_ENGINE.runAndWait()
					sayVoiceLine("Predict.")
					tts_predict = True			
				
				# logging
				if phase4EndPoint == None and 'DATAPOINT_NUMBER' in globals():
					phase4EndPoint = DATAPOINT_NUMBER
					phase4List.append((phase4StartPoint, phase4EndPoint))
					phase5StartPoint = DATAPOINT_NUMBER
				
				# draw thermometer
				if not CONFIG.thermo_during_planning:
					drawThermometer(CONFIG.NF_mode)
			
				# set selection flag
				sel = "predict"
				
				# draw UI
				drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
				drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
				drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.white, True)
				drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.green, True)
			
			####################################			
			## Phase 6: Highlight middle word ##
			####################################
			
			# # # # # # # # # # #
			# No prediction yet #
			# # # # # # # # # # #
			
			# timing
			if (
				(timer_sec - CONFIG.initialDelay - CONFIG.firstPhase - CONFIG.secondPhase - CONFIG.thirdPhase >= CONFIG.fourthPhase 
				and not 
				len(OUTPUT_STRING) > 0) or 
				(timer_sec - CONFIG.initialDelay - CONFIG.firstPhase - CONFIG.secondPhase - CONFIG.thirdPhase >= CONFIG.fourthPhase 
				and not 
				CONFIG.predictions_on)
				) and not postPhase:
				
				# progress bar timers
				if phase5PBTimer == None: 
					phase5PBTimer = 0
					clickPlayed = False
				else: phase5PBTimer += 1

				# draw progress bar
				timer_fine = int((phase5PBTimer / CONFIG.fps_target) *100)
				limit = CONFIG.fourthPhase
				drawProgressBar(timer_fine, limit*100)	
				
				# TTS
				if TTS_ON and not tts_middle:
					# flip & clear main surface
					pygame.display.flip()
					SURFACE_MAIN.fill((0,0,0))					
					#TTS_ENGINE.say("Middle.")
					#TTS_ENGINE.runAndWait()
					sayVoiceLine("Middle.")
					tts_middle = True
				
				# logging
				if phase4EndPoint == None and 'DATAPOINT_NUMBER' in globals():
					phase4EndPoint = DATAPOINT_NUMBER
					phase4List.append((phase4StartPoint, phase4EndPoint))
					phase6StartPoint = DATAPOINT_NUMBER
				
				# draw thermometer
				if not CONFIG.thermo_during_planning:
					drawThermometer(CONFIG.NF_mode)
				
				# set selection flag
				sel = "middle"
				
				# draw UI
				drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
				drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
				drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.white, True)
				if len(OUTPUT_STRING) > 0 and CONFIG.predictions_on: drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.white, True)
				drawText(middle, "std", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.green, True)
				
				## post delay
				if timer_fine >= limit*100: 
					postPhase = True
	
			# # # # # # # # # # # # # # # # #			
			# There's a prediction already  #
			# # # # # # # # # # # # # # # # #
			
			if (
				timer_sec - CONFIG.initialDelay - CONFIG.firstPhase - CONFIG.secondPhase - CONFIG.thirdPhase - CONFIG.fourthPhase >= CONFIG.fifthPhase 
				and 
				len(OUTPUT_STRING) > 0
				and
				CONFIG.predictions_on
				) and not postPhase: 
				
				# progress bar timers
				if phase5PBTimer == None: 
					phase5PBTimer = 0
					clickPlayed = False
				else: phase5PBTimer += 1

				# draw progress bar
				timer_fine = int((phase5PBTimer / CONFIG.fps_target) *100)
				limit = CONFIG.fifthPhase
				drawProgressBar(timer_fine, limit*100)	
				
				# TTS
				if TTS_ON and not tts_middle:
					# flip & clear main surface
					pygame.display.flip()
					SURFACE_MAIN.fill((0,0,0))					
					#TTS_ENGINE.say("Middle.")
					#TTS_ENGINE.runAndWait()
					sayVoiceLine("Middle.")
					tts_middle = True	
	
				# logging
				if phase5EndPoint == None and 'DATAPOINT_NUMBER' in globals():
					phase5EndPoint = DATAPOINT_NUMBER
					phase5List.append((phase5StartPoint, phase5EndPoint))
					phase6StartPoint = DATAPOINT_NUMBER		
				
				# draw thermometer
				if not CONFIG.thermo_during_planning:
					drawThermometer(CONFIG.NF_mode)
				
				# set selection flag
				sel = "middle"
				
				# draw UI
				drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
				drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
				drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.white, True)
				drawText(middle, "std", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.green, True)
				drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.white, True)
				## post delay
				if timer_fine >= limit*100: 
					postPhase = True
			
			# flip & clear main surface
			pygame.display.flip()
			SURFACE_MAIN.fill((0,0,0))
			
			# TTS
			if TTS_ON and not wordsaid:		
				#TTS_ENGINE.say(middle)
				#TTS_ENGINE.runAndWait()
				sayVoiceLine(middle)
				wordsaid = True
				
			
			################ Post phase #################
			if postPhase:
			
				sel = None
				postPhaseTimer += 1
				timer_sec = int(postPhaseTimer//CONFIG.fps_target)

				# draw progress bar
				timer_fine = int((postPhaseTimer / CONFIG.fps_target) *100)
				limit = CONFIG.endPhase
				drawProgressBar(timer_fine, limit*100)	

				# logging
				if phase6EndPoint == None and 'DATAPOINT_NUMBER' in globals():
					phase6EndPoint = DATAPOINT_NUMBER
					phase6List.append((phase6StartPoint, phase6EndPoint))				
						
				### restart
				if timer_sec >= CONFIG.endPhase:
					
					writeToLog("Main loop timed out.")
					
					INTERNAL_COUNTER += 1
					
					end = time.time()
					
					writeToExcel(str(end - start), ("main loop timeout"), True)			
					
					# set selection flag
					sel = None
					
					# tick timeout counter
					TIMEOUT_COUNTER += 1
					
					clickPlayed = False
					
					# restart loop
					main_loop(list)					
				
				# draw UI
				drawText("BEFORE", "small", (SCREEN_WIDTH//2-SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
				drawText("AFTER", "small", (SCREEN_WIDTH//2+SCREEN_WIDTH//4, SCREEN_HEIGHT//2), CONFIG.white, True)
				drawText("ERROR", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-SCREEN_HEIGHT//7), CONFIG.white, True)
				drawText(middle, "std", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CONFIG.white, True)
				if len(OUTPUT_STRING) > 0 and CONFIG.predictions_on: 
					drawText("PREDICT", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+SCREEN_HEIGHT//7), CONFIG.white, True)
					
			

def mainLoopInput(sel, start, list, middle):
	'''
	General input handling for the main loop.
	'''
	global COUNTER, STEP_COUNTER, INTERNAL_COUNTER, CMD_HISTORY, WORD_HISTORY, OUTPUT_STRING, TIMEOUT_COUNTER, OUTPUT_LIST
	global phase2StartPoint, phase3StartPoint, phase4StartPoint, phase5StartPoint, phase6StartPoint
	global phase2EndPoint, phase3EndPoint, phase4EndPoint, phase5EndPoint, phase6EndPoint
	global timeoutPhase1StartPoint, timeoutPhase1EndPoint, timeoutPhase2StartPoint, timeoutPhase2EndPoint
	global predictionList, predictionLetterFlag
	
	## Protocol
	if 'DATAPOINT_NUMBER' in globals():
		
		if sel == "before":
			phase2EndPoint = DATAPOINT_NUMBER
			phase2List.append((phase2StartPoint, phase2EndPoint))
	
		if sel == "after":
			phase3EndPoint = DATAPOINT_NUMBER
			phase3List.append((phase3StartPoint, phase3EndPoint))
	
		if sel == "error":
			phase4EndPoint = DATAPOINT_NUMBER
			phase4List.append((phase4StartPoint, phase4EndPoint))
	
		if sel == "middle":
			phase6EndPoint = DATAPOINT_NUMBER
			phase6List.append((phase6StartPoint, phase6EndPoint))		
	
		if sel == "predict":
			phase5EndPoint = DATAPOINT_NUMBER
			phase5List.append((phase5StartPoint, phase5EndPoint))
	
	## TTS
	if TTS_ON:
	
		if sel == "middle":
			TTS_ENGINE.say("You selected: " + middle)
		else:
			TTS_ENGINE.say(sel + " selected.")
		
		TTS_ENGINE.runAndWait()
	
	## Input outside of a valid selection window
	if sel == None:
		pass
	## Reset timeout counter if there's valid input
	else:
		TIMEOUT_COUNTER = 0

	## Timeout Return
	if sel == "return":
		if timeoutPhase1EndPoint == None and 'DATAPOINT_NUMBER' in globals():
			timeoutPhase1EndPoint = DATAPOINT_NUMBER
			timeoutPhase1List.append((timeoutPhase1StartPoint, timeoutPhase1EndPoint))

		end = time.time()
		
		writeToLog("SELECTION: Return to main loop")
		writeToLog("Time to select: " + str(end - start))
		
		STEP_COUNTER += 1
		INTERNAL_COUNTER += 1
		writeToExcel(str(end - start), ("Return to main loop"))

		pass
	
	## Timeout New Sentence
	if sel == "newsentence":
	
		OUTPUT_LIST.append(OUTPUT_STRING)
		OUTPUT_STRING = ""
		WORD_HISTORY = []
		CMD_HISTORY = []
		
		end = time.time()
		
		writeToLog("SELECTION: Start new sentence")
		writeToLog("Time to select: " + str(end - start))
		
		STEP_COUNTER += 1
		INTERNAL_COUNTER += 1
		writeToExcel(str(end - start), ("New sentence"))

		if timeoutPhase2EndPoint == None and 'DATAPOINT_NUMBER' in globals():
			timeoutPhase2EndPoint = DATAPOINT_NUMBER
			timeoutPhase2List.append((timeoutPhase2StartPoint, timeoutPhase2EndPoint))

		# Start new loop
		main_loop(WORD_LIST)	
	
	## MIDDLE WORD IS TARGET
	if sel == "middle":
		
		# Prep next run
		WORD_HISTORY.append(middle)
		if len(WORD_HISTORY)>0: OUTPUT_STRING += " " + middle
		else: OUTPUT_STRING += middle
		COUNTER = 0	
		CMD_HISTORY = []
		
		end = time.time()
		writeToLog("SELECTION: Middle word")
		writeToLog("Middle word selected: " + middle)
		writeToLog("Time to select: " + str(end - start))
		
		STEP_COUNTER += 1
		INTERNAL_COUNTER += 1
		writeToExcel(str(end - start), ("middle: " + middle))

		# Start new loop
		predictionLetterFlag = False
		main_loop(WORD_LIST)
			
	## BEFORE
	if sel == "before":

		new_list = list[:list.index(middle)+1]
		CMD_HISTORY.append(list)
		COUNTER += 1
		
		predictionLetterFlag = True
		
		end = time.time()
		writeToLog("SELECTION: Before")
		writeToLog("Time to select: " + str(end - start))
		
		STEP_COUNTER += 1
		INTERNAL_COUNTER += 1
		writeToExcel(str(end - start), ("before"))
		
	## AFTER	
	if sel == "after":

		# special case: only two left in dict, want to select!
		if len(list) <= 2:
			
			WORD_HISTORY.append(middle)
			if len(WORD_HISTORY)>0: OUTPUT_STRING += " " + middle
			else: OUTPUT_STRING += middle
			COUNTER = 0	
			CMD_HISTORY = []
			
			predictionLetterFlag = False
			
			end = time.time()
			writeToLog("SELECTION: After (with word selection)")
			writeToLog("Time to select: " + str(end - start))
			
			STEP_COUNTER += 1
			INTERNAL_COUNTER += 1
			writeToExcel(str(end - start), ("after with selection: " + middle))
			
			main_loop(WORD_LIST)
			
		# regular case
		else:	
			
			new_list = list[list.index(middle):]	
			CMD_HISTORY.append(list)
			COUNTER += 1
			
			predictionLetterFlag = True
			
			end = time.time()
			writeToLog("SELECTION: After")
			writeToLog("Time to select: " + str(end - start))
			
			STEP_COUNTER += 1
			INTERNAL_COUNTER += 1
			writeToExcel(str(end - start), ("after"))
			
	## ERROR
	
	# Go back one encoding step
	if sel == "error" and COUNTER > 0:
		
		COUNTER -= 1
		new_list = CMD_HISTORY[COUNTER]	
		del CMD_HISTORY[-1]
		
		end = time.time()
		writeToLog("SELECTION: Error (encoding step)")
		writeToLog("Time to select: " + str(end - start))
		
		STEP_COUNTER += 1
		INTERNAL_COUNTER += 1
		writeToExcel(str(end - start), ("error"))
		
	# Can't go back one encoding step!
	elif sel == "error" and len(WORD_HISTORY) == 0 and COUNTER == 0:
		
		new_list = list						
		
		end = time.time()
		writeToLog("SELECTION: Error (but there's nothing encoded yet!)")
		writeToLog("Time to select: " + str(end - start))
		
		STEP_COUNTER += 1
		INTERNAL_COUNTER += 1
		writeToExcel(str(end - start), ("error"))
	
	# Go back one word
	elif sel == "error" and len(WORD_HISTORY) > 0 and COUNTER == 0:
		
		del WORD_HISTORY[-1]
		OUTPUT_STRING = ""
		for item in WORD_HISTORY:
			OUTPUT_STRING += item.strip() + " "
		new_list = list
		
		end = time.time()
		writeToLog("SELECTION: Error (last word)")
		writeToLog("Time to select: " + str(end - start))
		
		STEP_COUNTER += 1
		INTERNAL_COUNTER += 1
		writeToExcel(str(end - start), ("error"))
	
	## PREDICTION
	if sel == "predict":

		end = time.time()
		writeToLog("SELECTION: Predict")
		writeToLog("Time to select: " + str(end - start))
		
		STEP_COUNTER += 1
		INTERNAL_COUNTER += 1
		writeToExcel(str(end - start), ("predict"))
		
		predictionList = []
		predictionLoop(list)
		main_loop(list)	
		
	# restart the main loop
	if 'new_list' in locals() and sel != None:
		main_loop(new_list)
	else:
		if sel != None: main_loop(list)	

def mainLoopNFInput(sel, start, list, middle):
	'''
	Handles Neurofeedback input for the main loop.
	'''
	
	## NF mode set to oxy
	if CONFIG.NF_mode == "oxy":
		if int(NFOXYVALUE) >= CONFIG.NF_threshold:
			try:
				mainLoopInput(sel, start, list, middle)
			except TypeError as error:
				print("Input error: " + str(error))
	
	## NF mode set to deoxy
	elif CONFIG.NF_mode == "deoxy":
		if int(NFDEOXYVALUE) >= CONFIG.NF_threshold:
			try:
				mainLoopInput(sel, start, list, middle)
			except TypeError as error:
				print("Input error: " + str(error))
	
	## NF mode set to avg 
	elif CONFIG.NF_mode == "avg":
		if (int(NFDEOXYVALUE) + int(NFOXYVALUE))//2 >= CONFIG.NF_threshold:
			try:
				mainLoopInput(sel, start, list, middle)
			except TypeError as error:
				print("Input error: " + str(error))
				
def mainLoopKBInput(sel, start, list, middle):
	'''
	Handles keyboard/pygame input for the main loop.
	''' 
	
	events_list = pygame.event.get()
	for event in events_list:
		
		# Quit event (clicking on the X)
		if event.type == pygame.QUIT:
			quitProgram()
			
		# Keypress events
		if event.type == pygame.KEYDOWN:
			
			# Escape key quits program
			if event.key == pygame.K_ESCAPE:
				quitProgram()
			
			if event.key == pygame.K_F1:
				if not BCIConnected:
					print("Trying to connect to TSI interface...")
					connectToTSI()
					if BCIConnected:
						print("Connection established.")
					else:
						print("Connection failed. Is TSI running & broadcasting on port 55555?")
					break
			
			try:
				mainLoopInput(sel, start, list, middle)
			except TypeError as error:
				print("Input error: " + str(error))

def predictionLoop(list):
	'''
	Displays three sentence predictions that can be chosen between. 
	Allows return to main loop with a BACK command. Allows re-rolling predictions via REROLL command.
	'''
	global OUTPUT_STRING, WORD_HISTORY, CMD_HISTORY, COUNTER, STEP_COUNTER, INTERNAL_COUNTER
	global pred_phase1StartPoint, pred_phase2StartPoint, pred_phase3StartPoint, pred_phase4StartPoint, pred_phase5StartPoint, pred_phase6StartPoint
	global pred_phase1EndPoint, pred_phase2EndPoint, pred_phase3EndPoint, pred_phase4EndPoint, pred_phase5EndPoint, pred_phase6EndPoint	
	global DATA_FREQUENCY
	global predictionList
	global clickPlayed
	
	
	# Fetch predictions
	prediction1, prediction2, prediction3 = generatePredictions()
	
	# Add predictions to list
	predictionList.append(prediction1)
	predictionList.append(prediction2)
	predictionList.append(prediction3)
	
	#print(predictionList)
	
	## Mini-init
	sel = None
	timer = 0
	SURFACE_MAIN.fill((0,0,0))
	pygame.display.flip()
	start = time.time()
	freq_timer = 0
	freq_seconds = 0
	
	# reset NF ticker
	NFTicker = 0

	# Reset progress bar timers
	phase0PBTimer = None
	phase1PBTimer = None
	phase2PBTimer = None
	phase3PBTimer = None
	phase4PBTimer = None
	phase5PBTimer = None
	
	# Reset TTS
	if TTS_ON:
		tts_1 = False
		tts_2 = False
		tts_3 = False
		tts_4 = False
		tts_5 = False
	
	clickPlayed = False
	
	# protocol flags
	pred_phase1StartPoint = None
	pred_phase1EndPoint   = None
	pred_phase2StartPoint = None
	pred_phase2EndPoint   = None	
	pred_phase3StartPoint = None
	pred_phase3EndPoint   = None	
	pred_phase4StartPoint = None
	pred_phase4EndPoint   = None		
	pred_phase5StartPoint = None
	pred_phase5EndPoint   = None
	pred_phase6StartPoint = None
	pred_phase6EndPoint   = None

	# initial drawing of UI so it's displayed when TTS plays
	drawText("REROLL", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-250), CONFIG.white, True)		
	drawText("BACK", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-150), CONFIG.white, True)
	drawText(OUTPUT_STRING.replace("  "," ").strip().capitalize() + prediction1, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-50), CONFIG.white, True, scale = True)
	drawText(OUTPUT_STRING.replace("  "," ").strip().capitalize() + prediction2, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+50), CONFIG.white, True, scale = True)
	drawText(OUTPUT_STRING.replace("  "," ").strip().capitalize() + prediction3, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+150), CONFIG.white,  True, scale = True)	
	pygame.display.flip()
	SURFACE_MAIN.fill((0,0,0))	
	
	
	sayVoiceLine("Predictions:    \n" 
				 + "1:   \n" + OUTPUT_STRING.replace("  "," ").strip().capitalize() + prediction1
				 + ".    \n" 
				 + "2:   \n" + OUTPUT_STRING.replace("  "," ").strip().capitalize() + prediction2
				 + ".    \n" 
				 + "3:   \n" + OUTPUT_STRING.replace("  "," ").strip().capitalize() + prediction3
				 + ".",
				 block = True)
	
	
	## loop
	running = True
	while running == True:
		
		# Make sure loop runs at a fixed framerate
		CLOCK.tick(CONFIG.fps_target)
		
		# draw debug info & thermometer
		drawDebug()
		if CONFIG.thermo_during_planning:
			drawThermometer(CONFIG.NF_mode)
		
		if pred_phase1StartPoint == None and 'DATAPOINT_NUMBER' in globals():
			pred_phase1StartPoint = DATAPOINT_NUMBER
		
		# read NF values 
		if CONFIG.input_type == "BOTH" or CONFIG.input_type == "NF":
			if NFTicker <= CONFIG.NF_reader_frequency:
				readNFValues()
				NFTicker+=1
			else:
				NFTicker = 1
		
		# Draw UI
		drawText("REROLL", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-250), CONFIG.white, True)		
		drawText("BACK", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-150), CONFIG.white, True)
		drawText(OUTPUT_STRING.replace("  "," ").strip().capitalize() + prediction1, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-50), CONFIG.white, True, scale = True)
		drawText(OUTPUT_STRING.replace("  "," ").strip().capitalize() + prediction2, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+50), CONFIG.white, True, scale = True)
		drawText(OUTPUT_STRING.replace("  "," ").strip().capitalize() + prediction3, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+150), CONFIG.white,  True, scale = True)

		# draw output string
		drawText(OUTPUT_STRING, "std", (100, SCREEN_HEIGHT - SCREEN_HEIGHT//4), CONFIG.white, False, scale = True)


		# Update screen, tick time forwards
		timer += 1
		#timer_sec = getSeconds(timer)
		timer_sec = timer // CONFIG.fps_target
		
		## Input handling ###########################
		if CONFIG.input_type == "BOTH":
			predictionLoopKBInput(sel, start, list, prediction1, prediction2, prediction3)
			predictionLoopNFInput(sel, start, list, prediction1, prediction2, prediction3)
		elif CONFIG.input_type == "KB":
			predictionLoopKBInput(sel, start, list, prediction1, prediction2, prediction3)
		elif CONFIG.input_type == "NF":
			predictionLoopNFInput(sel, start, list, prediction1, prediction2, prediction3)
		else:
			print("Input type incorrectly configured! Check config.ini!")
			writeToLog("Input configuration error!")
			quitProgram()
		#############################################

		# calculate data read rate		
		if 'DATAPOINT_NUMBER' in globals():
			if freq_timer == 0:
				firstVal = int(DATAPOINT_NUMBER)		
			if freq_seconds >= 2:
				secondVal = int(DATAPOINT_NUMBER)
				DATA_FREQUENCY = (secondVal - firstVal) / 2
				freq_timer = 0
				freq_seconds = 0
			else:
				freq_timer += 1
				freq_seconds = getSeconds(freq_timer)

		## Phase 0: Pre-Delay
		if timer_sec <= CONFIG.pred_initialDelay:
			
			if not CONFIG.pred_initialDelay == 0:
			
				# progress bar timers
				if phase0PBTimer == None: 
					phase0PBTimer = 0
					clickPlayed = False
				else: phase0PBTimer += 1
				
				# draw progress bar
				timer_fine = int((phase0PBTimer / CONFIG.fps_target) *100)
				limit = CONFIG.pred_initialDelay
				drawProgressBar(timer_fine, limit*100)			

		## Phase 1: Reroll
		if (
			 timer_sec >= CONFIG.pred_initialDelay 
			and 
			(timer_sec - CONFIG.pred_initialDelay) <= CONFIG.pred_firstPhase
			):
			
			sel = "reroll"	
			drawText("REROLL", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-250), CONFIG.green, True)

			# progress bar timers
			if phase1PBTimer == None: 
				phase1PBTimer = 0
				clickPlayed = False
			else: phase1PBTimer += 1

			# draw progress bar
			timer_fine = int((phase1PBTimer / CONFIG.fps_target) *100)
			limit = CONFIG.pred_firstPhase
			drawProgressBar(timer_fine, limit*100)
			
			if TTS_ON and tts_1 == False:
				#TTS_ENGINE.say("Reroll.")
				#TTS_ENGINE.runAndWait()
				sayVoiceLine("Reroll.")
				tts_1 = True 

			if pred_phase1EndPoint == None and 'DATAPOINT_NUMBER' in globals():
				pred_phase1EndPoint = DATAPOINT_NUMBER
				pred_phase1List.append((pred_phase1StartPoint, pred_phase1EndPoint))
				
			if pred_phase2StartPoint == None and 'DATAPOINT_NUMBER' in globals():
				pred_phase2StartPoint = DATAPOINT_NUMBER		

			
			if not CONFIG.thermo_during_planning:
				drawThermometer(CONFIG.NF_mode)			
			
		## Phase 2: BACK
		if (
			timer_sec - CONFIG.pred_initialDelay >= CONFIG.pred_firstPhase 
			and 
			timer_sec - CONFIG.pred_initialDelay - CONFIG.pred_firstPhase <= CONFIG.pred_secondPhase
			):
			
			sel = "back"
			drawText("REROLL", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-250), CONFIG.white, True)
			drawText("BACK", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-150), CONFIG.green, True)

			# progress bar timers
			if phase2PBTimer == None: 
				phase2PBTimer = 0
				clickPlayed = False
			else: phase2PBTimer += 1

			# draw progress bar
			timer_fine = int((phase2PBTimer / CONFIG.fps_target) *100)
			limit = CONFIG.pred_secondPhase
			drawProgressBar(timer_fine, limit*100)
			
			if TTS_ON and tts_2 == False:
				#TTS_ENGINE.say("Back.")
				#TTS_ENGINE.runAndWait()
				sayVoiceLine("Back.")
				tts_2 = True

			if pred_phase2EndPoint == None and 'DATAPOINT_NUMBER' in globals():
				pred_phase2EndPoint = DATAPOINT_NUMBER
				pred_phase2List.append((pred_phase2StartPoint, pred_phase2EndPoint))
			
				pred_phase3StartPoint = DATAPOINT_NUMBER

			if not CONFIG.thermo_during_planning:
				drawThermometer(CONFIG.NF_mode)

		## Phase 3: PRED 1
		if (
			timer_sec - CONFIG.pred_initialDelay - CONFIG.pred_firstPhase >= CONFIG.pred_secondPhase 
			and 
			timer_sec - CONFIG.pred_initialDelay - CONFIG.pred_firstPhase - CONFIG.pred_secondPhase <= CONFIG.pred_thirdPhase
			):

			sel = "1"
			drawText("BACK", "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-150), CONFIG.white, True)
			drawText(OUTPUT_STRING.replace("  "," ").strip().capitalize() + prediction1, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-50), CONFIG.green, True, scale = True)

			# progress bar timers
			if phase3PBTimer == None: 
				phase3PBTimer = 0
				clickPlayed = False
			else: phase3PBTimer += 1

			# draw progress bar
			timer_fine = int((phase3PBTimer / CONFIG.fps_target) *100)
			limit = CONFIG.pred_thirdPhase
			drawProgressBar(timer_fine, limit*100)
			
			if TTS_ON and tts_3 == False:
				#TTS_ENGINE.say("1: " + OUTPUT_STRING.replace("  "," ").strip().capitalize() + " " + prediction1)
				#TTS_ENGINE.runAndWait()
				line = "1: " + OUTPUT_STRING.replace("  "," ").strip().capitalize() + " " + prediction1
				sayVoiceLine(line)
				tts_3 = True

			if pred_phase3EndPoint == None and 'DATAPOINT_NUMBER' in globals():
				pred_phase3EndPoint = DATAPOINT_NUMBER
				pred_phase3List.append((pred_phase3StartPoint, pred_phase3EndPoint))
				pred_phase4StartPoint = DATAPOINT_NUMBER

			if not CONFIG.thermo_during_planning:
				drawThermometer(CONFIG.NF_mode)
				
		## Phase 4: PRED 2
		if (
			timer_sec - CONFIG.pred_initialDelay - CONFIG.pred_firstPhase - CONFIG.pred_secondPhase >= CONFIG.pred_thirdPhase 
			and 
			timer_sec - CONFIG.pred_initialDelay - CONFIG.pred_firstPhase - CONFIG.pred_secondPhase - CONFIG.pred_thirdPhase <= CONFIG.pred_fourthPhase
			):

			sel = "2"
			drawText(OUTPUT_STRING.replace("  "," ").strip().capitalize() + prediction1, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-50), CONFIG.white, True, scale = True)
			drawText(OUTPUT_STRING.replace("  "," ").strip().capitalize() + prediction2, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+50), CONFIG.green, True, scale = True)

			# progress bar timers
			if phase4PBTimer == None: 
				phase4PBTimer = 0
				clickPlayed = False
			else: phase4PBTimer += 1

			# draw progress bar
			timer_fine = int((phase4PBTimer / CONFIG.fps_target) *100)
			limit = CONFIG.pred_fourthPhase
			drawProgressBar(timer_fine, limit*100)
			
			if TTS_ON and tts_4 == False:
				#TTS_ENGINE.say("2: " + OUTPUT_STRING.replace("  "," ").strip().capitalize() + " " + prediction2)
				#TTS_ENGINE.runAndWait()
				line = "2: " + OUTPUT_STRING.replace("  "," ").strip().capitalize() + " " + prediction2
				sayVoiceLine(line)				
				tts_4 = True

			if pred_phase4EndPoint == None and 'DATAPOINT_NUMBER' in globals():
				pred_phase4EndPoint = DATAPOINT_NUMBER
				pred_phase4List.append((pred_phase4StartPoint, pred_phase4EndPoint))
				pred_phase5StartPoint = DATAPOINT_NUMBER

			if not CONFIG.thermo_during_planning:
				drawThermometer(CONFIG.NF_mode)
		
		## Phase 5: PRED 3
		if (
			timer_sec - CONFIG.pred_initialDelay - CONFIG.pred_firstPhase - CONFIG.pred_secondPhase - CONFIG.pred_thirdPhase >= CONFIG.pred_fourthPhase 
			and 
			timer_sec - CONFIG.pred_initialDelay - CONFIG.pred_firstPhase - CONFIG.pred_secondPhase - CONFIG.pred_thirdPhase - CONFIG.pred_fourthPhase <= CONFIG.pred_fifthPhase
			):		
		
			sel = "3"
			drawText(OUTPUT_STRING.replace("  "," ").strip().capitalize() + prediction2, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+50), CONFIG.white, True, scale = True)	
			drawText(OUTPUT_STRING.replace("  "," ").strip().capitalize() + prediction3, "small", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+150), CONFIG.green, True, scale = True)

			# progress bar timers
			if phase5PBTimer == None: 
				phase5PBTimer = 0
				clickPlayed = False
			else: phase5PBTimer += 1

			# draw progress bar
			timer_fine = int((phase5PBTimer / CONFIG.fps_target) *100)
			limit = CONFIG.pred_fifthPhase
			drawProgressBar(timer_fine, limit*100)
			
			if TTS_ON and tts_5 == False:
				#TTS_ENGINE.say("3: " + OUTPUT_STRING.replace("  "," ").strip().capitalize() + " " + prediction3)
				#TTS_ENGINE.runAndWait()
				line = "3: " + OUTPUT_STRING.replace("  "," ").strip().capitalize() + " " + prediction3
				sayVoiceLine(line)				
				tts_5 = True		

			if pred_phase5EndPoint == None and 'DATAPOINT_NUMBER' in globals():
				pred_phase5EndPoint = DATAPOINT_NUMBER
				pred_phase5List.append((pred_phase5StartPoint, pred_phase5EndPoint))
				pred_phase6StartPoint = DATAPOINT_NUMBER

			if not CONFIG.thermo_during_planning:
				drawThermometer(CONFIG.NF_mode)
				
		## Loop timeout
		if (
			timer_sec - CONFIG.pred_initialDelay - CONFIG.pred_firstPhase - CONFIG.pred_secondPhase - CONFIG.pred_thirdPhase - CONFIG.fourthPhase - CONFIG.pred_fifthPhase >= CONFIG.pred_endPhase 
			):
			
			if pred_phase6EndPoint == None and 'DATAPOINT_NUMBER' in globals():
				pred_phase6EndPoint = DATAPOINT_NUMBER
				pred_phase6List.append((pred_phase6StartPoint, pred_phase6EndPoint))			
			
			sel = None
			timer = 0
			writeToLog("Prediction loop timed out.")
			INTERNAL_COUNTER += 1
			end = time.time()
			writeToExcel(str(end - start), ("prediction loop timeout"), True)
			
			# Reset TTS
			if TTS_ON:
				tts_1 = False
				tts_2 = False
				tts_3 = False
				tts_4 = False
				tts_5 = False
			
			# Reset progress bar timers
			phase0PBTimer = None
			phase1PBTimer = None
			phase2PBTimer = None
			phase3PBTimer = None
			phase4PBTimer = None
			phase5PBTimer = None			

			# Reset protocol flags
			pred_phase1StartPoint = None
			pred_phase1EndPoint   = None
			pred_phase2StartPoint = None
			pred_phase2EndPoint   = None	
			pred_phase3StartPoint = None
			pred_phase3EndPoint   = None	
			pred_phase4StartPoint = None
			pred_phase4EndPoint   = None		
			pred_phase5StartPoint = None
			pred_phase5EndPoint   = None
			pred_phase6StartPoint = None
			pred_phase6EndPoint   = None

		pygame.display.flip()
		SURFACE_MAIN.fill((0,0,0))

def predictionLoopInput(sel, start, list, prediction1, prediction2, prediction3):
	'''
	General input handling for the prediction loop.
	'''
	global OUTPUT_STRING, WORD_HISTORY, CMD_HISTORY, COUNTER, STEP_COUNTER, INTERNAL_COUNTER
	global pred_phase1StartPoint, pred_phase2StartPoint, pred_phase3StartPoint, pred_phase4StartPoint, pred_phase5StartPoint, pred_phase6StartPoint
	global pred_phase1EndPoint, pred_phase2EndPoint, pred_phase3EndPoint, pred_phase4EndPoint, pred_phase5EndPoint, pred_phase6EndPoint	
	
	end = time.time()
	writeToLog("SELECTION: " + sel)
	writeToLog("Time to select: " + str(end - start))
	
	STEP_COUNTER += 1
	INTERNAL_COUNTER += 1

	## Protocol
	if 'DATAPOINT_NUMBER' in globals():
		
		if sel == "1":
			pred_phase4EndPoint = DATAPOINT_NUMBER
			pred_phase4List.append((pred_phase4StartPoint, pred_phase4EndPoint))
	
		elif sel == "2":
			pred_phase5EndPoint = DATAPOINT_NUMBER
			pred_phase5List.append((pred_phase5StartPoint, pred_phase5EndPoint))
	
		elif sel == "3":
			pred_phase6EndPoint = DATAPOINT_NUMBER
			pred_phase6List.append((pred_phase6StartPoint, pred_phase6EndPoint))
	
		elif sel == "back":
			pred_phase3EndPoint = DATAPOINT_NUMBER
			pred_phase3List.append((pred_phase3StartPoint, pred_phase3EndPoint))
			
		elif sel == "reroll":
			pred_phase2EndPoint = DATAPOINT_NUMBER
			pred_phase2List.append((pred_phase2StartPoint, pred_phase2EndPoint))		

	# excel logging
	if sel == "1":
		writeToExcel(str(end - start), ("prediction: " + prediction1.upper().strip()))
	elif sel == "2":
		writeToExcel(str(end - start), ("prediction: " + prediction2.upper().strip()))
	elif sel == "3":
		writeToExcel(str(end - start), ("prediction: " + prediction3.upper().strip()))
	elif sel == "reroll":
		writeToExcel(str(end - start), ("reroll predictions"))
	elif sel == "back":
		writeToExcel(str(end - start), ("back to main loop"))
		
	if TTS_ON and sel != None:
		TTS_ENGINE.say("Selected " + sel)
		TTS_ENGINE.runAndWait()
	
	## BACK
	if sel == "reroll":
		predictionLoop(list)
	
	if sel == "back":
		main_loop(list)
	
	## PRED 1					
	if sel == "1":
		writeToLog("Prediction selected: " + prediction1)
		OUTPUT_STRING = OUTPUT_STRING.strip()
		OUTPUT_STRING += prediction1.upper()
		WORD_HISTORY.append(prediction1.upper())
		COUNTER = 0	
		CMD_HISTORY = []
		#main_loop(WORD_LIST)
		predictionLoop(list)
	
	## PRED 2
	if sel == "2":
		writeToLog("Prediction selected: " + prediction2)
		OUTPUT_STRING = OUTPUT_STRING.strip()
		OUTPUT_STRING += prediction2.upper()
		WORD_HISTORY.append(prediction2.upper())
		COUNTER = 0	
		CMD_HISTORY = []
		#main_loop(WORD_LIST)
		predictionLoop(list)		
	
	## PRED 3
	if sel == "3":
		writeToLog("Prediction selected: " + prediction3)
		OUTPUT_STRING = OUTPUT_STRING.strip()
		OUTPUT_STRING += prediction3.upper()
		WORD_HISTORY.append(prediction3.upper())
		COUNTER = 0	
		CMD_HISTORY = []
		#main_loop(WORD_LIST)
		predictionLoop(list)

def predictionLoopNFInput(sel, start, list, prediction1, prediction2, prediction3):
	'''
	Handles Neurofeedback input for the prediction loop.
	'''
	
	## NF mode set to oxy
	if CONFIG.NF_mode == "oxy":
		if int(NFOXYVALUE) >= CONFIG.NF_threshold:
			try:
				predictionLoopInput(sel, start, list, prediction1, prediction2, prediction3)
			except TypeError as error:
				print("Input error: " + str(error))
	
	## NF mode set to deoxy			
	elif CONFIG.NF_mode == "deoxy":
		if int(NFDEOXYVALUE) >= CONFIG.NF_threshold:
			try:
				predictionLoopInput(sel, start, list, prediction1, prediction2, prediction3)
			except TypeError as error:
				print("Input error: " + str(error))
	
	## NF mode set to avg	
	elif CONFIG.NF_mode == "avg":
		if (int(NFDEOXYVALUE) + int(NFOXYVALUE))//2 >= CONFIG.NF_threshold:
			try:
				predictionLoopInput(sel, start, list, prediction1, prediction2, prediction3)
			except TypeError as error:
				print("Input error: " + str(error))
				
def predictionLoopKBInput(sel, start, list, prediction1, prediction2, prediction3):
	'''
	Handles keyboard input for the prediction loop.
	'''
	
	events_list = pygame.event.get()
	for event in events_list:
	
		if event.type == pygame.QUIT:
			quitProgram()
	
		if event.type == pygame.KEYDOWN:
		
			if event.key == pygame.K_ESCAPE:
				quitProgram()			
			
			try:				
				predictionLoopInput(sel, start, list, prediction1, prediction2, prediction3)
			except TypeError as error:
				print("Input error: " + str(error))

def generatePredictions(verbose = True):
	'''
	Makes an API call to OpenAI and returns three prediction strings.
	'''
	global INTERNAL_COUNTER, predictionList
	
	writeToLog("Generating predictions...")
	
	if TTS_ON:
		TTS_ENGINE.say("Predicting from..." + OUTPUT_STRING)
		TTS_ENGINE.runAndWait()	
		
	pred_list = []
	
	start = time.time()
	
	CLOCK.tick(CONFIG.fps_target)
	
	## TODO: Find functional way to implement predictionLetterFlag
	firstChar = ""
	promptString = OUTPUT_STRING.replace("  "," ").strip().capitalize()
	
	## draw PB
	SURFACE_MAIN.fill((0,0,0))
	drawText("Generating predictions...", "small", (SCREEN_WIDTH//2,SCREEN_HEIGHT//2), CONFIG.white, True)
	drawProgressBar(0, 100, indicator = False)
	pygame.display.flip()			
	
	## Prediction 1
	try:
		response = openai.Completion.create(
							engine = CONFIG.model_str, 
							prompt = promptString, 
							max_tokens = CONFIG.length, 
							temperature = CONFIG.temperature,
							#top_p = CONFIG.top_p,
							n=1, 
							)
	
		for choice in response.choices:
			pred_list.append(firstChar.lower() + str(choice.text))
		
		## Prediction 2	
		response = openai.Completion.create(
								engine = CONFIG.model_str, 
								prompt = promptString, 
								max_tokens = CONFIG.length+1, 
								temperature = CONFIG.temperature,
								#top_p = CONFIG.top_p,
								n=1, 
								)
								
		for choice in response.choices:
			pred_list.append(firstChar.lower() + str(choice.text))		
		
		## Prediction 3
		response = openai.Completion.create(
								engine = CONFIG.model_str, 
								prompt = promptString, 
								max_tokens = CONFIG.length+1, 
								temperature = CONFIG.temperature,
								#top_p = CONFIG.top_p,
								n=1, 
								)
								
		for choice in response.choices:
			pred_list.append(firstChar.lower() + str(choice.text))
								
	except Exception as e:
		print("Something went wrong while requesting predictions from the GPT-3 API.")
		print("Exception raised:")
		print(e)
		writeToLog(e)
		print("This exception was written to the log file.")
		print("Now returning to main loop.")
		main_loop(WORD_LIST)
		
	# Text cleanup
	for item in pred_list:
		
		index = pred_list.index(item)
		
		## Exclusive method
		for char in item:
			if char not in whiteList.charList:
				item = item.replace(char,"")
		
		## Conditionally inclusive method
		#if "." in item:
		#	item = item[:item.rfind(".")]
		#if "," in item:
		#	item = item[:item.rfind(",")]
		#if "!" in item:
		#	item = item[:item.rfind("!")]		
		#if ":" in item:
		#	item = item[:item.rfind(":")]				
		#if "?" in item:
		#	item = item[:item.rfind("?")]
		#if "\"" in item:
		#	item = item[:item.rfind("\"")]
		#if "\n" in item:
		#	item = item.replace("\n"," ")
		#if "\"" in item:
		#	item = item.replace("\"","")	
		#if "\"," in item:
		#	item = item.replace("\",",",")
		#if "”" in item:
		#	item = item.replace("”","")
		
		pred_list[index] = item
	
	## Get strings
	prediction1 = str( pred_list[0] )
	prediction2 = str( pred_list[1] )
	prediction3 = str( pred_list[2] )
	
	#########################################
	## Kill duplicates & filter swearwords ##
	#########################################
	
	## Prediction 1
	
	# mini init
	iter_count = 0
	censorFlag = False
	
	# first pass censor
	for word in prediction1.split():
		if word in censorWordList: censorFlag = True
	
	while (prediction1 == prediction2 or prediction1 == prediction3 or len(prediction1) <= 1 or prediction1 in predictionList or censorFlag == True) and iter_count < CONFIG.max_reroll:
		
		# tick time
		CLOCK.tick(CONFIG.fps_target)
		
		# draw PB
		SURFACE_MAIN.fill((0,0,0))		
		drawText("Generating predictions...", "small", (SCREEN_WIDTH//2,SCREEN_HEIGHT//2), CONFIG.white, True)
		drawProgressBar(iter_count+30, 100, indicator = False)
		pygame.display.flip()		
		
		# logging
		if verbose:
			print("Rerolling Prediction 1 (Attempt " + str(iter_count) + "/" + str(CONFIG.max_reroll) + ")")   		
			if prediction1 == prediction2 or prediction1 == prediction3:
				print("Reason: Duplicate")
			if len(prediction1) <= 1:
				print("Reason: Too short")
			if prediction1 in predictionList:
				print("Reason: Rejected by user")
			if censorFlag:
				print("Reason: Censored")
		
		# reroll
		prediction1 = rerollDuplicate(0)
		
		# second pass censor
		for word in prediction1.split():
			if word in censorWordList: censorFlag = True
		
		# tick iterator		
		iter_count += 1
		
		if prediction1 == prediction2 or prediction1 == prediction3:
			iter_count -= 1
		if prediction1 in predictionList:
			iter_count -= 1
		
		# too many naughty rerolls, give up
		if iter_count == CONFIG.max_reroll and censorFlag:
			
			print("Censoring 1:")
			print(prediction1)
			
			# prep string wrangling
			newString = ""
			y = 0
		
			# iterate through prediction, replace every letter in swearword except first one with "*"
			for word in prediction1.split():
				if word in censorWordList:
					i = 0
					temp = ""
					for character in word:
						if i != 0:
							temp += "*"
						i += 1
					newWord = word[0] + temp
					if y == 0: newString += newWord
					else: newString += " " + newWord
				else:
					if y == 0: newString += word
					else: newString += " " + word
			prediction1 = " " + newString
			censorFlag = False
		
	## Prediction 2
	
	# mini init
	iter_count = 0
	censorFlag = False
	
	# first pass censor
	for word in prediction2.split():
		if word in censorWordList: censorFlag = True
		
	while (prediction2 == prediction3 or prediction2 == prediction1 or len(prediction2) <= 1 or prediction2 in predictionList or censorFlag == True) and iter_count < CONFIG.max_reroll:
	
		# tick time
		CLOCK.tick(CONFIG.fps_target)                                                   

		# draw PB
		SURFACE_MAIN.fill((0,0,0))		
		drawText("Generating predictions...", "small", (SCREEN_WIDTH//2,SCREEN_HEIGHT//2), CONFIG.white, True)
		drawProgressBar(iter_count+60, 100, indicator = False)
		pygame.display.flip()

		# logging
		if verbose:
			print("Rerolling Prediction 2 (Attempt " + str(iter_count) + "/" + str(CONFIG.max_reroll) + ")")
			if prediction2 == prediction1 or prediction2 == prediction3:
				print("Reason: Duplicate")
			if len(prediction2) <= 1:
				print("Reason: Too short")
			if prediction2 in predictionList:
				print("Reason: Rejected by user")
			if censorFlag:
				print("Reason: Censored")
		
		# reroll
		prediction2 = rerollDuplicate(1)
		
		# second pass censor
		for word in prediction2.split():
			if word in censorWordList: censorFlag = True			
		
		# tick iterator		
		iter_count += 1

		if prediction2 == prediction1 or prediction2 == prediction3:
			iter_count -= 1
		if prediction2 in predictionList:
			iter_count -= 1

		# too many naughty rerolls, give up
		if iter_count == CONFIG.max_reroll and censorFlag:
			
			print("Censoring 2:")
			print(prediction2)			
			
			
			# prep string wrangling
			newString = ""
			y = 0
		
			# iterate through prediction, replace every letter in swearword except first one with "*"
			for word in prediction2.split():
				if word in censorWordList:
					i = 0
					temp = ""
					for character in word:
						if i != 0:
							temp += "*"
						i += 1
					newWord = word[0] + temp
					if y == 0: newString += newWord
					else: newString += " " + newWord
				else:
					if y == 0: newString += word
					else: newString += " " + word
			prediction2 = " " + newString
			censorFlag = False
	
	## Prediction 3	
	
	# mini init
	iter_count = 0             
	censorFlag = False
	
	# first pass censor
	for word in prediction3.split():
		if word in censorWordList: censorFlag = True
	
	while (prediction3 == prediction1 or prediction3 == prediction2 or len(prediction3) <= 1 or prediction3 in predictionList or censorFlag == True) and iter_count < CONFIG.max_reroll:
		
		#tick time
		CLOCK.tick(CONFIG.fps_target)

		# draw PB
		SURFACE_MAIN.fill((0,0,0))	
		drawText("Generating predictions...", "small", (SCREEN_WIDTH//2,SCREEN_HEIGHT//2), CONFIG.white, True)
		drawProgressBar(iter_count+90, 100, indicator = False)
		pygame.display.flip()		
		
		# logging
		if verbose:
			print("Rerolling Prediction 3 (Attempt " + str(iter_count) + "/" + str(CONFIG.max_reroll) + ")")
			if prediction3 == prediction1 or prediction3 == prediction2:
				print("Reason: Duplicate")
			if len(prediction3) <= 1:
				print("Reason: Too short")
			if prediction3 in predictionList:
				print("Reason: Rejected by user")
			if censorFlag:
				print("Reason: Censored")
		
		# reroll
		prediction3 = rerollDuplicate(1)
		
		# second pass censor
		for word in prediction3.split():
			if word in censorWordList: censorFlag = True
		
		# tick iterator		
		iter_count += 1	

		if prediction3 == prediction2 or prediction3 == prediction1:
			iter_count -= 1
		if prediction3 in predictionList:
			iter_count -= 1
		
		# too many naughty rerolls, give up
		if iter_count == CONFIG.max_reroll and censorFlag:
			
			print("Censoring 3:")
			print(prediction3)			
			
			# prep string wrangling
			newString = ""
			y = 0
		
			# iterate through prediction, replace every letter in swearword except first one with "*"
			for word in prediction3.split():
				if word in censorWordList:
					i = 0
					temp = ""
					for character in word:
						if i != 0:
							temp += "*"
						i += 1
					newWord = word[0] + temp
					if y == 0: newString += newWord
					else: newString += " " + newWord
				else:
					if y == 0: newString += word
					else: newString += " " + word
			prediction3 = " " + newString
			censorFlag = False
			
	###################################################
	
	## Logging
	end = time.time()
	writeToLog("Time to calculate predictions: " + str(end - start))
	INTERNAL_COUNTER += 1
	writeToExcel(str(end - start), ("processing time"), True)
	
	## Return predictions
	return (prediction1, prediction2, prediction3)

def rerollDuplicate(reroll_length):
	'''
	Rerolls a single prediction, in case there's a duplicate.
	'''
	
	pred_list = []
	
	if predictionLetterFlag == True:
		firstChar = " " + middle[:1]
		promptString = (OUTPUT_STRING + firstChar).replace("  "," ").strip().capitalize()
	else:
		firstChar = ""
		promptString = OUTPUT_STRING.replace("  "," ").strip().capitalize()	
	
	
	try:
		response = openai.Completion.create(
						engine = CONFIG.model_str, 
						prompt = promptString, 
						max_tokens = CONFIG.length + reroll_length, 
						temperature = CONFIG.temperature,
						#top_p = CONFIG.top_p,
						n=1, 
						)
	except Exception:
		print("Something went wrong while requesting predictions from the GPT-3 API.")
		print("Exception raised:")
		print(Exception)
		writeToLog(Exception)
		print("This exception was written to the log file.")
		print("Now returning to main loop.")
		main_loop(WORD_LIST)

	for choice in response.choices:
		pred_list.append(firstChar.lower() + str(choice.text))
		
	# Text cleanup
	for item in pred_list:
		
		index = pred_list.index(item)
		
		#print("Dirty:" + item)
		
		if "." in item:
			item = item[:item.rfind(".")]
		if "," in item:
			item = item[:item.rfind(",")]
		if "!" in item:
			item = item[:item.rfind("!")]	
		if ":" in item:
			item = item[:item.rfind(":")]							
		if "?" in item:
			item = item[:item.rfind("?")]
		if "\"" in item:
			item = item[:item.rfind("\"")]
		if "\n" in item:
			item = item.replace("\n"," ")
		if "\"" in item:
			item = item.replace("\"","")	
		if "\"," in item:
			item = item.replace("\",",",")
		if "”" in item:
			item = item.replace("”","")
			
		#print("Clean:" + item)
		
		pred_list[index] = item
	
	return (str(pred_list[0]))

##  _   _ _____ _     ____  _____ ____  ____  
## | | | | ____| |   |  _ \| ____|  _ \/ ___| 
## | |_| |  _| | |   | |_) |  _| | |_) \___ \ 
## |  _  | |___| |___|  __/| |___|  _ < ___) |
## |_| |_|_____|_____|_|   |_____|_| \_\____/ 
##                                            

def drawDebug():
	'''
	Display debug info if debug is set to True in config
	'''
	
	if CONFIG.debug_on:
			
		# FPS
		fps = str(int(CLOCK.get_fps()))
		drawText("FPS: " + fps, "smallest", (0, 0), CONFIG.white, False)
		
		if CONFIG.input_type == "BOTH" or CONFIG.input_type == "NF":
			
			if not BCIConnected:
				drawText("TSI interface not connected!", "smallest", (0, 35), CONFIG.red, False)
			else:
				# Folder set correctly in config.ini?
				if WRONG_FOLDER == True:
					drawText("TSI Neurofeedback data folder incorrectly configured!", "smallest", (0, 35), CONFIG.red, False)
				else:
				
					# No data?
					if NO_DATA:
						drawText("No data coming from TSI!", "smallest", (0, 35), CONFIG.red, False)
					
					else:	
						# Display NF value
						if CONFIG.NF_mode == "oxy":
							drawText("Oxy  NF  Value:  " + str(NFOXYVALUE) + " / " + str(CONFIG.NF_threshold), "smallest", (0, 35), CONFIG.white, False)
						elif CONFIG.NF_mode == "deoxy":
							drawText("DeOxy  NF  Value: " + str(NFDEOXYVALUE) + " / " + str(CONFIG.NF_threshold), "smallest", (0, 35), CONFIG.white, False)
						elif CONFIG.NF_mode == "avg":
							drawText(
									"Avg. NF Value (De/Oxy): " + 
									str((int(NFDEOXYVALUE) + int(NFOXYVALUE))//2) + 
									" (" + str(int(NFDEOXYVALUE)) + "/" + str(int(NFOXYVALUE)) + ")"  + " / " + str(CONFIG.NF_threshold), 
									"smallest", 
									(0, 35), 
									CONFIG.white, 
									False
									)
							
						# Display raw oxy value
						if float(RAWOXY) >= 0    and float(RAWOXY) <= 0.1: color = (0,50,0)
						elif float(RAWOXY) > 0.1 and float(RAWOXY) <= 0.2: color = (0,100,0)
						elif float(RAWOXY) > 0.2 and float(RAWOXY) <= 0.3: color = (0,150,0)
						elif float(RAWOXY) > 0.3 and float(RAWOXY) <= 0.4: color = (0,200,0)
						elif float(RAWOXY) > 0.4:                          color = (0,255,0)
						if float(RAWOXY)   < 0    and float(RAWOXY) >= -0.1: color = (50,0,0)
						elif float(RAWOXY) < -0.1 and float(RAWOXY) >= -0.2: color = (100,0,0)
						elif float(RAWOXY) < -0.2 and float(RAWOXY) >= -0.3: color = (150,0,0)
						elif float(RAWOXY) < -0.3 and float(RAWOXY) >= -0.4: color = (200,0,0)
						elif float(RAWOXY) < -0.4:                           color = (255,0,0)
						
						if CONFIG.NF_mode == "oxy":
							drawText("Oxy Raw Value: ", "smallest", (0, 70), CONFIG.white, False)
							drawText(str(RAWOXY), "smallest", (155, 70), color, False)
						
						# Display raw deoxy value
						if float(RAWDEOXY) >= 0    and float(RAWDEOXY) <= 0.1: color = (0,50,0)
						elif float(RAWDEOXY) > 0.1 and float(RAWDEOXY) <= 0.2: color = (0,100,0)
						elif float(RAWDEOXY) > 0.2 and float(RAWDEOXY) <= 0.3: color = (0,150,0)
						elif float(RAWDEOXY) > 0.3 and float(RAWDEOXY) <= 0.4: color = (0,200,0)
						elif float(RAWDEOXY) > 0.4:                          color = (0,255,0)
						if float(RAWDEOXY)   < 0    and float(RAWDEOXY) >= -0.1: color = (50,0,0)
						elif float(RAWDEOXY) < -0.1 and float(RAWDEOXY) >= -0.2: color = (100,0,0)
						elif float(RAWDEOXY) < -0.2 and float(RAWDEOXY) >= -0.3: color = (150,0,0)
						elif float(RAWDEOXY) < -0.3 and float(RAWDEOXY) >= -0.4: color = (200,0,0)
						elif float(RAWDEOXY) < -0.4:                           color = (255,0,0)
						
						if CONFIG.NF_mode == "deoxy":
							drawText("DeOxy Raw Value: ", "smallest", (0, 70), CONFIG.white, False)
							drawText(str(RAWDEOXY), "smallest", (175, 70), color, False)
							
						if CONFIG.NF_mode == "avg":
							drawText("Oxy Value: ", "smallest", (0, 70), CONFIG.white, False)
							drawText(str(RAWOXY), "smallest", (100, 70), color, False)
							drawText("DeOxy Value: ", "smallest", (0, 105), CONFIG.white, False)
							drawText(str(RAWDEOXY), "smallest", (135, 105), color, False)
						
						# Display datapoint number
						drawText("Datapoint: ", "smallest", (SCREEN_WIDTH - 200, 40), CONFIG.white, False)
						drawText(DATAPOINT_NUMBER, "smallest", (SCREEN_WIDTH - 100, 40), CONFIG.white, False)
						
						# Display measured data read rate
						drawText("Read rate: ", "smallest", (SCREEN_WIDTH - 200, 0), CONFIG.white, False)
						if DATA_FREQUENCY >= 0:
							drawText(str(DATA_FREQUENCY) + " Hz", "smallest", (SCREEN_WIDTH - 100, 0), CONFIG.white, False)
						else:
							drawText(str(DATA_FREQUENCY) + " Hz?!", "smallest", (SCREEN_WIDTH - 100, 0), CONFIG.white, False)

def drawThermometer(mode):
	'''
	Draws the thermometer
	'''
	# only draw thermo if thermo_on
	if CONFIG.thermo_on:
		# calculate percentage filled
		if mode == "oxy":
			percentage = (float(NFOXYVALUE)/CONFIG.NF_threshold)
		elif mode == "deoxy":
			percentage = (float(NFDEOXYVALUE)/CONFIG.NF_threshold)
		elif mode == "avg":
			percentage = float( int(NFDEOXYVALUE) + int(NFOXYVALUE))//2/CONFIG.NF_threshold
		# limit percentage
		if percentage > 1: percentage = 1
		# calculate size of filled area
		barheight = int((SCREEN_HEIGHT//2 * percentage ))*-1
		# limit filled area
		if barheight > 0: barheight = 0
		# small offset to make some clearance between output string and thermometer
		offset = 20
		# draw outline
		pygame.draw.rect(SURFACE_MAIN, (255,255,255), pygame.Rect(50, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 - offset, 30, SCREEN_HEIGHT//2), 5) 
		# draw inside area
		pygame.draw.rect(SURFACE_MAIN, (0,0,0), pygame.Rect(50, SCREEN_HEIGHT//2-SCREEN_HEIGHT//4 - offset, 30, SCREEN_HEIGHT//2))
		# draw filled area
		pygame.draw.rect(SURFACE_MAIN, (0,255,0), pygame.Rect(50, SCREEN_HEIGHT//2+SCREEN_HEIGHT//4 - offset, 30, barheight))

def drawProgressBar(currentTime, timeLimit, indicator = True):
	'''
	Draws a progress bar to indicate when the next slide will begin
	'''
	global clickPlayed
	
	# only draw progress bar if set to on
	if CONFIG.progressbar:
		# calculate percentage filled
		percentage = float(currentTime+1) / timeLimit
		# set limits
		if percentage > 1: percentage = 0
		# calculate size of filled area
		barwidth = int( ((SCREEN_WIDTH-200)* percentage) )
		# draw outline
		pygame.draw.rect(SURFACE_MAIN, (255,255,255), pygame.Rect(100, SCREEN_HEIGHT-50, SCREEN_WIDTH-200, 8), 3)
		# draw inside area
		pygame.draw.rect(SURFACE_MAIN, (0,0,0), pygame.Rect(100, SCREEN_HEIGHT-50, SCREEN_WIDTH-200, 8))
		# draw filled area
		pygame.draw.rect(SURFACE_MAIN, (255,255,255), pygame.Rect(100, SCREEN_HEIGHT-50, barwidth, 8))
		# draw indicator
		## TODO: Find smarter way to do this 
		if CONFIG.indicator and indicator == True:
			if barwidth >= SCREEN_WIDTH-CONFIG.indicatorPos-100: 
				color = (0,220,0)
				if not clickPlayed and (CONFIG.progressbarAudio == True):
					playsound.playsound("config/sfx/click.mp3", block=False)
					clickPlayed = True
			else: color = (190,190,190)
			pygame.draw.rect(SURFACE_MAIN, color, pygame.Rect(SCREEN_WIDTH-CONFIG.indicatorPos, SCREEN_HEIGHT-50, 5, 8))

def drawText(text, size, pos, color, centered, scale = False):
	'''
	Draws a text element to SURFACE_MAIN. 
	Takes text string, size string, coord tuple, (R,G,B) color, bool centered.
	Also does some string wrangling to keep overly long strings on screen.
	BUGGED: Wreaks havok on long strings in the prediction loop. Probably easier to fix 
	there instead of here.
	'''
	
	x,y = pos
	
	if size == "std":
		textsurface = STD_FONT.render(text, False, color)
	elif size == "small":
		textsurface = SMALL_FONT.render(text, False, color)
	elif size == "smallest":
		textsurface = SMALLEST_FONT.render(text, False, color)
		
	font_rect = textsurface.get_rect()
	
	## If text is too large for the screen, try rendering it smaller and smaller until it fits
	if scale and font_rect.width >= SCREEN_WIDTH-100:
		textsurface = SMALL_FONT.render(text, False, color)
		font_rect = textsurface.get_rect()
		
	if scale and font_rect.width >= SCREEN_WIDTH-100:
		textsurface = SMALLEST_FONT.render(text, False, color)
		font_rect = textsurface.get_rect()
	
	if centered:
		x = x - font_rect.width // 2
		y = y - font_rect.height // 2	
	
	## Still too big... try splitting it into multiple lines	
	if scale and font_rect.width >= SCREEN_WIDTH-100:
		halfway = len(text) // 2
		try:
			next_one = text.index(" ", halfway)
		except ValueError:
			next_one = None
		try:
			previous_one = text.rindex(" ", 0, halfway)
		except ValueError:
			previous_one = None
		if next_one == None and previous_one == None:
			return
		elif next_one == None:
			pos = previous_one
		elif previous_one == None:
			pos = next_one
		elif next_one - halfway < halfway - previous_one:
			pos = next_one
		else:
			pos = previous_one
			
		a = text[:pos]
		b = text[pos + 1:]
		
		textsurface = SMALLEST_FONT.render(a, False, color)
		textsurface2 = SMALLEST_FONT.render(b, False, color)		
		
		## Render
		SURFACE_MAIN.blit(textsurface, (x, y) )
		SURFACE_MAIN.blit(textsurface2, (x, y+50) )
		
		return
		
		
	## Render	
	SURFACE_MAIN.blit(textsurface, (x, y) )

def updateSlide():
	'''
	Helper that redraws / ticks slides forward.
	'''
	global CLOCK
	pygame.display.flip()
	SURFACE_MAIN.fill((0,0,0))
	CLOCK.tick(CONFIG.fps_target)	

def slideInput(pressSpace = False, pressAnyKey = False, default = True):
	'''
	Input handling for slides.
	'''
	
	# input
	events_list = pygame.event.get()
	for event in events_list:
		
		# quit via X
		if event.type == pygame.QUIT:
			quitProgram()	
		
		# advance slide with any key
		if pressAnyKey:
			if event.type == pygame.KEYDOWN:
				return True
		
		# advance slide with space bar
		elif pressSpace:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					return True

		elif default:
			return False


def blit_alpha(target, source, location, opacity):
	'''
	Alternative blit function for images with opacity.
	Thanks Nerdparadise! https://nerdparadise.com/programming/pygameblitopacity
	'''
	x = location[0]
	y = location[1]
	temp = pygame.Surface((source.get_width(), source.get_height())).convert()
	temp.blit(target, (-x, -y))
	temp.blit(source, (0, 0))
	temp.set_alpha(opacity)        
	target.blit(temp, location)
	
def drawSlide(textList, imageList, TTS_said):
	'''
	Draw a slide.
		textList = [(textString, ttsString, sizeString, (x, y))]
			ttsString can be none - in this case, textString will be used for TTS
			set ttsString to "" to exclude an item from TTS
		imageList = [(asset, (x,y))]
	'''
	
	# initiate clean ttsList
	ttsList = []
	
	# go through textList
	for textItem in textList:
		# read values
		string, ttsString, sizeString, coords = textItem
		# draw text
		drawText(string, sizeString, coords, CONFIG.white, True)
		# no ttsString - fallback to textString
		if ttsString == None:
			ttsString = string
		# append to ttsList
		ttsList.append(ttsString)
	# go through imageList
	for imageItem in imageList:
		# read values
		asset, coords = imageItem
		# blit image
		SURFACE_MAIN.blit(asset, coords)
	# go through ttsList
	for ttsItem in ttsList:
		# do tts things
		if TTS_ON and not TTS_said:
			pygame.display.flip()
			#TTS_ENGINE.say(ttsItem)
			#TTS_ENGINE.runAndWait()
			sayVoiceLine(ttsItem)
	
def findMiddle(input_list):
	'''
	Returns the middle element of a list.
	'''
	middle = float(len(input_list))/2
	if middle % 2 != 0: return input_list[int(middle - .5)]
	else: return input_list[int(middle)]

def getFPS():
	fps = CLOCK.get_fps()
	if fps == 0: fps = 1
	return fps

def getSeconds(timer):
	fps = CLOCK.get_fps()
	if fps == 0: fps = CONFIG.fps_target
	return int(timer//CONFIG.fps_target)#int(timer//fps)

def getMilliseconds(timer):
	fps = CLOCK.get_fps()
	if fps == 0: fps = CONFIG.fps_target
	return timer/fps


def sayVoiceLine(string, block = False):
	'''
	Alternative to pyttsx3's runandwait() that doesn't block the stack while speaking.
	'''
	
	if TTS_ON:
		filestring = string.replace(":","")
		filestring = filestring.replace("!","")
		filestring = filestring.replace(".","")
		filestring = filestring.replace("?","")
		filestring = filestring.replace(" ","")
		filestring = filestring.replace("\n","")
		
		newString = ""
		i = 0
		for word in string.split(" "):
			if "*" in word:
				newWord = "beep"
				if i == 0: newString += newWord
				else: newString += " " + newWord
			else:
				if i == 0: newString += word
				else: newString += " " + word
			i += 1
			
		
		while len(filestring) > 8: 
			filestring = filestring[:-1]
		filename = filestring+'.wav'
		
		i = 1
		while filename in os.listdir("ttsOutput"):
			filestring = filestring[:-3] + "_" + str(i)
			filename = filestring+'.wav'
			i += 1		
		
		print(newString)
		TTS_ENGINE.save_to_file(newString , "ttsOutput/" + filename)
		TTS_ENGINE.runAndWait()
		try:
			playsound.playsound("ttsOutput/" + filename, block)
		except error as e:
			print(e)
			pass
	else:
		pass

def makeExcel():
	'''
	Creates an xlsx file.
	'''
	global WB, WS1, EXCEL_PATH
	
	WB    = excel.Workbook()
	today = datetime.now()
	today = today.strftime("%c")
	today = today.replace(":","-")
	EXCEL_PATH = "logs/" + today + ".xlsx"
	WS1   = WB.active
	
	WS1['A1'] = "Steps:"
	WS1['B1'] = "Time taken (in seconds):"
	WS1['C1'] = "Command encoded:"
	WS1['D1'] = "Datapoint:"
	if CONFIG.predictions_on:
		WS1['G1'] = "Model:"
		WS1['H1'] = CONFIG.model_str
		WS1['G2'] = "Temperature:"
		WS1['H2'] = CONFIG.temperature
		WS1['G3'] = "top_p:"
		WS1['H3'] = CONFIG.top_p
	else:
		WS1['G1'] = "Predictions turned off"
	
	## does this even do anything?
	WS1.page_setup.fitToWidth = 1
	
	WB.save(filename = EXCEL_PATH)

def writeToExcel(time, command, nostep = False):
	'''
	Writes the time datapoint and command encoded to a line in the xlsx file.
	Bool nostep indicates whether the line is counted as a new encoding step.
	'''
	global WB, WS1
	
	if not nostep:
		WS1['A'+str(INTERNAL_COUNTER+1)] = int(STEP_COUNTER)
		WS1['B'+str(INTERNAL_COUNTER+1)] = float(time)
		WS1['C'+str(INTERNAL_COUNTER+1)] = command
		# log number of current datapoint if there's TSI input flowing in
		if 'DATAPOINT_NUMBER' in globals():
			WS1['D'+str(INTERNAL_COUNTER+1)] = int(DATAPOINT_NUMBER)
	else:
		WS1['A'+str(INTERNAL_COUNTER+1)] = " "
		WS1['B'+str(INTERNAL_COUNTER+1)] = float(time)
		WS1['C'+str(INTERNAL_COUNTER+1)] = command
		if 'DATAPOINT_NUMBER' in globals():
			WS1['D'+str(INTERNAL_COUNTER+1)] = int(DATAPOINT_NUMBER)
			
	WB.save(filename = EXCEL_PATH)

def finishExcel():
	'''
	Calculates total time taken and writes it to the xlsx log.
	'''
	global STEP_COUNTER, WB, WS1, EXCEL_PATH, INTERNAL_COUNTER, OUTPUT_STRING
	
	# this list will contain all time values
	steplist = []
	
	# iterate over all time values in the xlsx, append each one to the list
	for i in range(2,INTERNAL_COUNTER+2):
		value = WS1['B'+str(i)].value
		steplist.append(value)
	
	# write fields
	WS1['C'+str(INTERNAL_COUNTER+2)] = "taken in total"
	WS1['B'+str(INTERNAL_COUNTER+2)] = sum(steplist)
	
	# if it fits, use the output string as sheet title
	if len(OUTPUT_STRING) > 0 and len(OUTPUT_STRING) < 32: 
		WS1.title = OUTPUT_STRING
	else:
		WS1.title = "Run data"
	
	# save the file
	WB.save(filename = EXCEL_PATH)
	
def makeLog():
	'''
	Creates a log file.
	'''
	global LOG_FILE, LOG_PATH
	# take current timestamp as filename
	today = datetime.now()
	today = today.strftime("%c")
	today = today.replace(":","-")
	# make file
	LOG_PATH = "logs/" + today + ".log"
	LOG_FILE = open(LOG_PATH,"w+")
	# logging
	writeToLog("Log file created.")
	print("Log file created.")

def writeToLog(text):
	'''
	Writes text to the log file.
	'''
	global LOG_FILE
	
	# take timestamp
	now = datetime.now()
	now = now.strftime("%X")
	# append text
	with open(LOG_PATH, "a") as file:
		file.write(now + " - " + text + "\n")

def updateNFFolder(silent=False):
	'''
	Reads NF Folder path from TSI, updates path
	'''
	global CONFIG, WRONG_FOLDER, NO_DATA
	
	print("Updating folder...")
	
	if BCIConnected:
		folder = TSI.get_values_feedback_folder()[0]
		CONFIG.data_folder = folder
		CONFIG.set("TURBO-SATORI SETTINGS", "data_folder", folder)
		with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
		if not silent: print("New data folder: " + folder)

def connectToTSI():
	'''
	Attempts to connect the program to TSI's network interface
	'''
	global TSI, TSI_Error_Raised, BCIConnected
	
	print("Connecting...")
	
	try:
		TSI = BCI.TurbosatoriNetworkInterface('127.0.0.1', 55555)
		TSI_Error_Raised = False
		BCIConnected = True
		print("TSI connected!")
	except (RuntimeError, TypeError, NameError):
		if not TSI_Error_Raised:
			print("Can't connect to TurboSatori...")
			BCIConnected = False
			TSI_Error_Raised = True

def clearNFFolder(silent = False):
	'''
	Wipes the NF folder to make it ready for use in a new run.
	'''
	global FILELIST
	
	if BCIConnected:
		try:
			if not silent: print("Starting NF folder wipe...")
			for file in natsorted(os.listdir(CONFIG.data_folder)):
				os.remove(CONFIG.data_folder + "\\" + file)
			FILELIST = []
			if not silent: print("Wipe complete.")
		except Exception as error:
			if not silent: print("Something went wrong while trying to wipe the NF folder:")
			if not silent: print(error)
			writeToLog("NF wipe error: " + str(error))
	else:
		if not silent: print("TSI interface not connected, skipping wipe...")

def readNFValues():
	'''
	Read in contents of NF folder, convert text to variables
	'''
	global FILELIST, NFOXYVALUE, NFDEOXYVALUE, RAWOXY, RAWDEOXY, NO_DATA, SAME_COUNTER, WRONG_FOLDER, DATAPOINT_NUMBER
	
	try:
		
		# try updating data folder if no data is coming
		if (WRONG_FOLDER) and BCIConnected:
			updateNFFolder(silent=False)
		
		# access each file in a naturally sorted list of data_folder contents	
		for file in natsorted(os.listdir(CONFIG.data_folder))[-1:]:
			
			# have I seen this file before? Only proceed if I haven't
			if file not in FILELIST:
				
				# reset iteration counter and set flag for incoming data
				SAME_COUNTER = 0
				NO_DATA = False
				
				# retrieve number of current data point from filename
				DATAPOINT_NUMBER = ''.join([n for n in file if n.isdigit()])
				
				# try to read in the file, split text into chunks with space as a delimiter
				try:
					textfile = open(CONFIG.data_folder+"\\"+file,"r")
					text     = textfile.read()
					chunks   = text.split(' ')				
					NO_DATA  = False
				# no files incoming! Raise NO_DATA flag, set all values to 0 for this data point
				except FileNotFoundError:
					NO_DATA      = True
					RAWOXY       = 0
					RAWDEOXY     = 0
					NFOXYVALUE   = 0
					NFDEOXYVALUE = 0
				# data point is readable!
				try:
					# pack values into variables
					RAWOXY       = chunks[1]
					NFOXYVALUE   = chunks[2]
					RAWDEOXY     = chunks[6]
					NFDEOXYVALUE = chunks[7]
				# data point can't be read...
				except IndexError as error:
					# print error message and set all values to 0 for this data point
					print("Couldn't read data point for " + str(CONFIG.data_folder+"\\"+file))
					print("Error: " + str(error))
					print("Offending raw text: " + str(text))
					print("Offending data: " + str(chunks))
					writeToLog("Unreadable data point: " + str(CONFIG.data_folder+"\\"+file))
					RAWOXY  = 0
					RAWDEOXY = 0
					NFOXYVALUE = 0
					NFDEOXYVALUE = 0
					#break
				
				# remember this file so I won't read it in again next frame
				FILELIST.append(file)
				# finally, close the file so we don't needlessly clog up RAM 
				textfile.close()
			
			# I'm reading in the same file twice in a row! Tick iteration counter
			elif file == FILELIST[-1]:
				SAME_COUNTER += 1
				
				# I've read in the same file 100 times in a row now, raise NO_DATA flag and set values to 0
				if SAME_COUNTER == 100:
					NO_DATA = True				
					RAWOXY  = 0
					RAWDEOXY = 0
					NFOXYVALUE = 0
					NFDEOXYVALUE = 0
					
	# Data folder isn't even set up! Raise alarm
	except:
		if WRONG_FOLDER == False: 
			print("Neurofeedback data folder incorrectly configured!")
			print("Unable to read data points from Turbo-Satori. fNIRS input will not function.")
			writeToLog("Neurofeedback data folder incorrectly configured!")
		WRONG_FOLDER = True


def makeLocalizerProtocol():
	'''
	Creates the .prt file for the localizer run
	'''
	
	experimentString = CONFIG.experiment_name + "_localizer"
	bgColorString = str(CONFIG.prt_backgroundcolor).replace("(","").replace(")","").replace(", "," ")
	textColorString = str(CONFIG.prt_textcolor).replace("(","").replace(")","").replace(", "," ")
	timecourseColorString = str(CONFIG.prt_timecoursecolor).replace("(","").replace(")","").replace(", "," ")
	timecourseThicknessString = str(CONFIG.prt_timecoursethick)
	referenceColorString = str(CONFIG.prt_referencefunccolor).replace("(","").replace(")","").replace(", "," ")
	referenceThicknessString = str(CONFIG.prt_referencefuncthick)
	numConditionString = "2"
	restColorString = str(CONFIG.prt_phase1ColorString).replace("(","").replace(")","").replace(", "," ")
	taskColorString = str(CONFIG.prt_phase2ColorString).replace("(","").replace(")","").replace(", "," ")
	
	# take current datetime as filename
	today = datetime.now()
	today = today.strftime("%c")
	today = today.replace(":","-")
	
	with open('logs/' + experimentString + '_' + today + '.prt', 'w') as file:
		
		print("Protocol file created.")
		writeToLog("Protocol file: " + experimentString + '_' + today + '.prt')
			
		###########
		## Header #
		###########
		
		file.write('\n')
		file.write('FileVersion:        2')
		file.write('\n\n')
		file.write('ResolutionOfTime:   Volumes')
		file.write('\n\n')
		file.write('Experiment:         ' + experimentString)
		file.write('\n\n')
		file.write('BackgroundColor:    ' + bgColorString)
		file.write('\n')
		file.write('TextColor:          ' + textColorString)
		file.write('\n')
		file.write('TimeCourseColor:    ' + timecourseColorString)
		file.write('\n')
		file.write('TimeCourseThick:    ' + timecourseThicknessString)
		file.write('\n')
		file.write('ReferenceFuncColor: ' + referenceColorString)
		file.write('\n')
		file.write('ReferenceFuncThick: ' + referenceThicknessString)
		file.write('\n\n')
		file.write('NrOfConditions:  ' + numConditionString)
		file.write('\n\n')	
			
		###############
		## Conditions #
		###############
		
		appendCondition('Rest', restList, restColorString, file)
		appendCondition('Task', taskList, taskColorString, file)
		
		## done
		file.close()

def makeProtocolFile(silent=False):
	'''
	Creates the .prt file for Turbo-Satori
	'''
	
	##TODO: Triggers with TSINetworkInterface
	
	# set strings
	experimentString = CONFIG.experiment_name
	bgColorString = str(CONFIG.prt_backgroundcolor).replace("(","").replace(")","").replace(", "," ")
	textColorString = str(CONFIG.prt_textcolor).replace("(","").replace(")","").replace(", "," ")
	timecourseColorString = str(CONFIG.prt_timecoursecolor).replace("(","").replace(")","").replace(", "," ")
	timecourseThicknessString = str(CONFIG.prt_timecoursethick)
	referenceColorString = str(CONFIG.prt_referencefunccolor).replace("(","").replace(")","").replace(", "," ")
	referenceThicknessString = str(CONFIG.prt_referencefuncthick)
	
	# get number of conditions
	i = 0 
	listOfPhases = [
		phase1List, 
		phase2List, 
		phase3List, 
		phase4List, 
		phase5List, 
		phase6List, 
		pred_phase1List, 
		pred_phase2List, 
		pred_phase3List, 
		pred_phase4List, 
		pred_phase5List, 
		pred_phase6List, 
		timeoutPhase1List,
		timeoutPhase2List]
		
	for phase in listOfPhases:
		if len(phase) > 0: i+=1
	
	numConditionString = str(i)
	
	# only proceed if there's more than one condition
	if i > 1:
		
		# set color strings
		phase1ColorString = str(CONFIG.prt_phase1ColorString).replace("(","").replace(")","").replace(", "," ")
		phase2ColorString = str(CONFIG.prt_phase2ColorString).replace("(","").replace(")","").replace(", "," ")
		phase3ColorString = str(CONFIG.prt_phase3ColorString).replace("(","").replace(")","").replace(", "," ")
		phase4ColorString = str(CONFIG.prt_phase4ColorString).replace("(","").replace(")","").replace(", "," ")
		phase5ColorString = str(CONFIG.prt_phase5ColorString).replace("(","").replace(")","").replace(", "," ")
		phase6ColorString = str(CONFIG.prt_phase6ColorString).replace("(","").replace(")","").replace(", "," ")
		pred_phase1ColorString = str(CONFIG.pred_prt_phase1ColorString).replace("(","").replace(")","").replace(", "," ")
		pred_phase2ColorString = str(CONFIG.pred_prt_phase2ColorString).replace("(","").replace(")","").replace(", "," ")
		pred_phase3ColorString = str(CONFIG.pred_prt_phase3ColorString).replace("(","").replace(")","").replace(", "," ")
		pred_phase4ColorString = str(CONFIG.pred_prt_phase4ColorString).replace("(","").replace(")","").replace(", "," ")
		pred_phase5ColorString = str(CONFIG.pred_prt_phase5ColorString).replace("(","").replace(")","").replace(", "," ")
		pred_phase6ColorString = str(CONFIG.pred_prt_phase6ColorString).replace("(","").replace(")","").replace(", "," ")
		returnColorString = str(CONFIG.returnColorString).replace("(","").replace(")","").replace(", "," ")
		newSentenceColorString = str(CONFIG.newSentenceColorString).replace("(","").replace(")","").replace(", "," ")
		
		
		# take current datetime for filename
		today = datetime.now()
		today = today.strftime("%c")
		today = today.replace(":","-")
		
		# make file
		with open('logs/' + experimentString + '_' + today + '.prt', 'w') as file:
			
			# logging
			if not silent: print("Protocol file created.")
			writeToLog("Protocol file: " + experimentString + '_' + today + '.prt')
				
			###########
			## Header #
			###########
			
			file.write('\n')
			file.write('FileVersion:        2')
			file.write('\n\n')
			file.write('ResolutionOfTime:   Volumes')
			file.write('\n\n')
			file.write('Experiment:         ' + experimentString)
			file.write('\n\n')
			file.write('BackgroundColor:    ' + bgColorString)
			file.write('\n')
			file.write('TextColor:          ' + textColorString)
			file.write('\n')
			file.write('TimeCourseColor:    ' + timecourseColorString)
			file.write('\n')
			file.write('TimeCourseThick:    ' + timecourseThicknessString)
			file.write('\n')
			file.write('ReferenceFuncColor: ' + referenceColorString)
			file.write('\n')
			file.write('ReferenceFuncThick: ' + referenceThicknessString)
			file.write('\n\n')
			file.write('NrOfConditions:  ' + numConditionString)
			file.write('\n\n')
			
			###############
			## Conditions #
			###############
			
			try:
				if len(phase1List) > 0: appendCondition('PlanningPhase', phase1List, phase1ColorString, file)
				if len(phase2List) > 0: appendCondition('Before', phase2List, phase2ColorString, file)
				if len(phase3List) > 0: appendCondition('After', phase3List, phase3ColorString, file)
				if len(phase4List) > 0: appendCondition('Error', phase4List, phase4ColorString, file)
				if len(phase5List) > 0: appendCondition('Predict', phase5List, phase5ColorString, file)
				if len(phase6List) > 0: appendCondition('MiddleWord', phase6List, phase6ColorString, file)
				if len(pred_phase1List) > 0: appendCondition('PredictionPlanningPhase', pred_phase1List, pred_phase1ColorString, file)
				if len(pred_phase2List) > 0: appendCondition('Pred_Reroll', pred_phase2List, pred_phase2ColorString, file)
				if len(pred_phase3List) > 0: appendCondition('Pred_Back', pred_phase3List, pred_phase3ColorString, file)
				if len(pred_phase4List) > 0: appendCondition('Pred_1', pred_phase4List, pred_phase4ColorString, file)
				if len(pred_phase5List) > 0: appendCondition('Pred_2', pred_phase5List, pred_phase5ColorString, file)
				if len(pred_phase6List) > 0: appendCondition('Pred_3', pred_phase6List, pred_phase6ColorString, file)
				if len(timeoutPhase1List) > 0: appendCondition('TimeoutReturn', timeoutPhase1List, returnColorString, file)
				if len(timeoutPhase2List) > 0: appendCondition('TimeoutNewSentence', timeoutPhase2List, newSentenceColorString  , file)
				if not silent: print("Protocol file successfully written.")
				writeToLog("Protocol file good.")			
			except Exception as error:
				if not silent: print("Something went wrong while trying to write the protocol file:")
				if not silent: print(error)
				writeToLog("Protocol file error: " + str(error))
		
			file.close()
	
	else:
		
		print("WARNING: Not enough conditions measured to create a protocol file.")
		writeToLog("Protocol file error: Not enough conditions measured to create a protocol.")

def appendCondition(name, phaseList, color, file):
	'''
	Appends a condition to the protocol file.
	'''
	
	file.write(name + '\n')
	file.write(str(len(phaseList)) + '\n')
	
	for item in phaseList:
	
		whitespace = '        '
		for char in range(0, len(item[0])):
			whitespace = whitespace[:-1]
		
		file.write(whitespace)
		file.write(item[0])
		
		whitespace = '         '
		for char in range(0, len(item[1])):
			whitespace = whitespace[:-1]			
			
		file.write(whitespace)
		file.write(item[1])
		file.write('\n')
		
	file.write('Color: ' + color)	
	file.write('\n\n')

def quitProgram():
	'''
	Ends the program more gracefully than having to CTRL-C in N++.
	'''
	
	#playsound.playsound("config/sfx/shutdown_short.mp3", block = True)
	
	try:
		# Make the xlsx log ready for primetime
		finishExcel()
		# Make .prt file
		makeProtocolFile()

	except Exception as e:
		print("Unable to make excel & text log!")
		print(e)
	
	# try to clean up tts audio folder
	for file in os.listdir("ttsOutput"):
		try:
			os.remove("ttsOutput/" + file)
		except Exception as e:
			pass
	
	# Logging call
	writeToLog("Quitting")
	# Bye bye!
	pygame.quit()
	sys.exit()
	
##  ____  _   _ _   _ _____ ___ __  __ _____ 
## |  _ \| | | | \ | |_   _|_ _|  \/  | ____|
## | |_) | | | |  \| | | |  | || |\/| |  _|  
## |  _ <| |_| | |\  | | |  | || |  | | |___ 
## |_| \_\\___/|_| \_| |_| |___|_|  |_|_____|
##                                          

if __name__ == '__main__':
	makeLog()
	initialization()

############################################################################################################
##                                                                                                        ##
##                                                                                                        ##
##                    ________                __           ____                                           ##
##                   /_  __/ /_  ____ _____  / /_______   / __/___  _____                                 ##
##                    / / / __ \/ __ `/ __ \/ //_/ ___/  / /_/ __ \/ ___/                                 ##
##                   / / / / / / /_/ / / / / ,< (__  )  / __/ /_/ / /                                     ##
##                  /_/ /_/ /_/\__,_/_/ /_/_/|_/____/  /_/  \____/_/                                      ##
##                                                                                                        ##
##                                               ___             __                                       ##
##                          ________  ____ _____/ (_)___  ____ _/ /                                       ##
##                         / ___/ _ \/ __ `/ __  / / __ \/ __ `/ /                                        ##
##                        / /  /  __/ /_/ / /_/ / / / / / /_/ /_/                                         ##
##                       /_/   \___/\__,_/\__,_/_/_/ /_/\__, (_)                                          ##
##                                                     /____/                                             ##
##                                                                                                        ##
##                                                                                                        ##
##           	                                                                                          ##
##                                                  ,aaa,                                                 ##
##                                                ,dP"'Y8,                                                ##
##                                               dP"   `8b                                                ##
##                                              dI      I8                                                ##
##               ,ad88b,                       ,8'      I8d88b,                                           ##
##              d8"' `"8,                      fP      ,8"  `"8,                                          ##
##              8I     `8,                     8'      dP     I8                                          ##
##              8b      `8,                   ,8       8'     8I                                          ##
##              I8,      Ib,                  dP      ,8      8I                                          ##
##            ad88b,     `Yb                 ,8'      I8      8I                                          ##
##           dP' `8b,     `8,                dP       IP      8I                                          ##
##           8'   `8I      "8,              ,8'       8I      8'                                          ##
##           8     Yb,      "8,            ,8'        8'      8                                           ##
##           8     `8I       Ib,           dP        ,8      ,8                                           ##
##           8,     `8,      `8I          ,8'        dP      I8                                           ##
##           8I      YI       `8,         dP        ,8'      8I                                           ##
##           Ib      `8,       `8,       ,8'        8P       8'                                           ##
##           I8       8I        Yb       dP        f8'       8                                            ##
##           `8,      I8,       `8,     dP'        8I       ,8                                            ##
##            8I      `8I        Yb    dP'        ,8'       I8                                            ##
##            Ib       `8,       `YbaadP'         d8        8I                                            ##
##            `8,       YI         `""'           8P        8'                                            ##
##             Ib,      `8,                                 8                                             ##
##             `8I       YI                                ,8                                             ##
##              I8       `"                                I8                                             ##
##              I8                                         I8                                             ##
##              I8                                         I8                                             ##
##              I8                                         I8                        ______               ##
##              `8                                         `8,                  _,add8888888bba,.         ##
##               8,                                         YI               ,ad8P"'         ``"Yb        ##
##               8I                                         `8b,          ,ad8P"'               I8)       ##
##               8b                                           "8ba,___,ad8P"'          ,aaaaaaad8P'       ##
##               I8                                             `"Y888P"'          ,adPP"""""""''         ##
##               `8,                                                             ,dP"'                    ##
##                8I                                                           ,8P"                       ##
##                8b                                                         ,8P"                         ##
##                I8                                                       ,8P"                           ##
##                Y8                                                     ,8P"                             ##
##                I8                                                   ,8P"                               ##
##                `8,                                                ,dP"                                 ##
##                 8I                                              a8P"                                   ##
##                 `8,                                          ,d8P'                                     ##
##                  `8,                                      ,adP"                                        ##
##                   `8,                                  ,adP"'                                          ##
##                    8I                               ,adP"                                              ##
##                    I8                             ,dP'                                                 ##
##                    8I                           ,8P'                                                   ##
##                    8P                         ,dP"                                                     ##
##                   ,8'                        ,8P'                                                      ##
##                   dI                        ,8P                                                        ##
##                  ,8'                       ,8P                                                         ##
##                  IP        Normand        ,8P                                                          ##
##                            Veilleux       8P                                                           ##
##                                          dP                                                            ##
##                                         ""                                                             ##
##                                                                                                        ##
############################################################################################################