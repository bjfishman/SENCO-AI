#######################################################
##   ____		      __ _		    ____ _   _ ___   ##
##  / ___|___  _ __  / _(_) __ _   / ___| | | |_ _|  ##
## | |   / _ \| '_ \| |_| |/ _` | | |  _| | | || |   ##
## | |__| (_) | | | |  _| | (_| | | |_| | |_| || |   ##
##  \____\___/|_| |_|_| |_|\__, |  \____|\___/|___|  ##
##						    |___/					 ##
## v 1.0.0										     ##
##												     ##
## Requires PySimpleGUI & pyttsx3.				     ##
##												     ##
## Simple GUI for configuring the Sentence Speller.  ##
## Because clicking on stuff is nicer than having to ##
## manually change entries in a config file.		 ##
##												     ##
##												     ##
## Don't look at this code too closely. It's awful.  ##
##												     ##
#######################################################

## Namespaces ############################
import os							    ##
import PySimpleGUI as sg				##
import configparser					    ##
import pyttsx3						    ##
from   pyttsx3.drivers import sapi5	    ##
##########################################

def initConfig(configFile):
	'''
	Initializes any configFile that is passed in and
	creates a global ConfigParser object that holds
	all values.
	'''
	global CONFIG
	
	## Create a ConfigParser object
	CONFIG = configparser.ConfigParser(allow_no_value=True)
	CONFIG.read(configFile)
	
	## Read in values
	
	# Screen settings
	CONFIG.fps_target		  = int(CONFIG.get('WINDOW_SETTINGS','fps_target')) 	
	CONFIG.fullscreen		  = eval(CONFIG.get('WINDOW_SETTINGS', 'fullscreen')) 
	if CONFIG.fullscreen: CONFIG.fullscreen = "Fullscreen"
	else: CONFIG.fullscreen = "Windowed"

	# Turbo-Satori settings
	CONFIG.data_folder		 = str(CONFIG.get('TURBO-SATORI SETTINGS', 'data_folder')) 
	CONFIG.thermo_on		   = eval(CONFIG.get('TURBO-SATORI SETTINGS', 'thermo_on'))
	CONFIG.thermo_during_planning = eval(CONFIG.get('TURBO-SATORI SETTINGS', 'thermo_during_planning'))
	CONFIG.NF_reader_frequency = int(CONFIG.get('TURBO-SATORI SETTINGS','NF_reader_frequency')) 
	CONFIG.NF_threshold		= int(CONFIG.get('TURBO-SATORI SETTINGS','NF_threshold'))
	CONFIG.NF_mode			 = str(CONFIG.get('TURBO-SATORI SETTINGS','NF_mode')) 
	if CONFIG.NF_mode   == "oxy":   CONFIG.NF_mode = "Oxy"
	elif CONFIG.NF_mode == "deoxy": CONFIG.NF_mode = "Deoxy"
	elif CONFIG.NF_mode == "avg":   CONFIG.NF_mode = "Average"
	CONFIG.localizer_lasttrial_duration = int(CONFIG.get('TURBO-SATORI SETTINGS','localizer_lasttrial_duration'))
	
	CONFIG.tutorial = eval(CONFIG.get('TURBO-SATORI SETTINGS','tutorial')) 
	CONFIG.localizer = eval(CONFIG.get('TURBO-SATORI SETTINGS','localizer')) 
	CONFIG.threshold = eval(CONFIG.get('TURBO-SATORI SETTINGS','threshold')) 
	CONFIG.training = eval(CONFIG.get('TURBO-SATORI SETTINGS','training')) 
	CONFIG.localizerrepetitions = int(CONFIG.get('TURBO-SATORI SETTINGS','localizerrepetitions'))
	CONFIG.localizer_rest_duration	= int(CONFIG.get('TURBO-SATORI SETTINGS','localizer_rest_duration'))
	CONFIG.localizer_task_duration	= int(CONFIG.get('TURBO-SATORI SETTINGS','localizer_task_duration'))
	CONFIG.progressbar = eval(CONFIG.get('TURBO-SATORI SETTINGS','progressbar')) 
	
	# Protocol settings
	CONFIG.experiment_name = str(CONFIG.get('TURBO-SATORI SETTINGS', 'experiment_name')) 
	CONFIG.prt_BackgroundColor = eval(CONFIG.get('TURBO-SATORI SETTINGS', 'prt_BackgroundColor'))
	CONFIG.prt_textcolor = eval(CONFIG.get('TURBO-SATORI SETTINGS', 'prt_textcolor'))
	CONFIG.prt_timecoursecolor = eval(CONFIG.get('TURBO-SATORI SETTINGS', 'prt_timecoursecolor'))
	CONFIG.prt_referencefunccolor = eval(CONFIG.get('TURBO-SATORI SETTINGS', 'prt_referencefunccolor'))
	CONFIG.prt_timecoursethick = eval(CONFIG.get('TURBO-SATORI SETTINGS', 'prt_timecoursethick'))
	CONFIG.prt_referencefuncthick = eval(CONFIG.get('TURBO-SATORI SETTINGS', 'prt_referencefuncthick'))
	CONFIG.prt_phase1ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_phase1ColorString'))
	CONFIG.prt_phase2ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_phase2ColorString'))
	CONFIG.prt_phase3ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_phase3ColorString'))
	CONFIG.prt_phase4ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_phase4ColorString'))
	CONFIG.prt_phase5ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_phase5ColorString'))
	CONFIG.prt_phase6ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','prt_phase6ColorString'))
	CONFIG.pred_prt_phase1ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','pred_prt_phase1ColorString'))
	CONFIG.pred_prt_phase2ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','pred_prt_phase2ColorString'))
	CONFIG.pred_prt_phase3ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','pred_prt_phase3ColorString'))
	CONFIG.pred_prt_phase4ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','pred_prt_phase4ColorString'))
	CONFIG.pred_prt_phase5ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','pred_prt_phase5ColorString'))
	CONFIG.pred_prt_phase6ColorString = eval(CONFIG.get('TURBO-SATORI SETTINGS','pred_prt_phase6ColorString'))
	
	CONFIG.returnColorString       = eval(CONFIG.get('TURBO-SATORI SETTINGS','returnColorString'))
	CONFIG.newsentenceColorString  = eval(CONFIG.get('TURBO-SATORI SETTINGS','newsentenceColorString'))
	
	# Misc settings
	CONFIG.dictionary		  = str(CONFIG.get('MISC', 'dictionary')) 
	CONFIG.debug_on			= eval(CONFIG.get('MISC', 'debug_on')) 
	CONFIG.input_type		  = str(CONFIG.get('MISC','input_type')) 
	if CONFIG.input_type == "KB":	 CONFIG.input_type = "Keyboard only"
	elif CONFIG.input_type  == "NF":  CONFIG.input_type = "fNIRS only"
	elif CONFIG.input_type == "BOTH": CONFIG.input_type = "Keyboard + fNIRS"
	CONFIG.timeout_iterlimit = int(CONFIG.get('MISC', 'timeout_iterlimit')) 
	CONFIG.indicator = eval(CONFIG.get('MISC', 'indicator'))
	CONFIG.indicatorPos = int(CONFIG.get('MISC', 'indicatorPos'))
	
	# TTS settings
	CONFIG.TTS_ON			  = eval(CONFIG.get('MISC', 'text_to_speech')) 
	CONFIG.TTS_VOICE		   = int(CONFIG.get('MISC','tts_voice')) 
	TTS_ENGINE = pyttsx3.init()
	CONFIG.ttsVoices		   = TTS_ENGINE.getProperty("voices")
	CONFIG.voiceList		   = []
	for voice in CONFIG.ttsVoices: CONFIG.voiceList.append(voice.name)
	
	# Timings
	CONFIG.initialDelay		= int(CONFIG.get('TIMINGS', 'initialDelay'))
	CONFIG.firstPhase		  = int(CONFIG.get('TIMINGS', 'firstPhase'))
	CONFIG.secondPhase		 = int(CONFIG.get('TIMINGS', 'secondPhase'))
	CONFIG.thirdPhase		  = int(CONFIG.get('TIMINGS', 'thirdPhase'))
	CONFIG.fourthPhase		 = int(CONFIG.get('TIMINGS', 'fourthPhase'))
	CONFIG.fifthPhase		  = int(CONFIG.get('TIMINGS', 'fifthPhase'))
	CONFIG.endPhase			= int(CONFIG.get('TIMINGS', 'endPhase'))
	CONFIG.pred_initialDelay   = int(CONFIG.get('TIMINGS', 'pred_initialDelay'))
	CONFIG.pred_firstPhase	 = int(CONFIG.get('TIMINGS', 'pred_firstPhase'))
	CONFIG.pred_secondPhase	= int(CONFIG.get('TIMINGS', 'pred_secondPhase'))
	CONFIG.pred_thirdPhase	 = int(CONFIG.get('TIMINGS', 'pred_thirdPhase'))
	CONFIG.pred_fourthPhase	= int(CONFIG.get('TIMINGS', 'pred_fourthPhase'))
	CONFIG.pred_fifthPhase	 = int(CONFIG.get('TIMINGS', 'pred_fifthPhase'))
	CONFIG.pred_endPhase	   = int(CONFIG.get('TIMINGS', 'pred_endPhase'))
	
	# Font settings
	CONFIG.FONT				= str(CONFIG.get('FONTS', 'font')) 
	CONFIG.STD_FONT			= int(CONFIG.get('FONTS', 'std_def'))
	CONFIG.SMALL_FONT		  = int(CONFIG.get('FONTS', 'small_def'))
	CONFIG.SMALLEST_FONT	   = int(CONFIG.get('FONTS', 'smallest_def'))
	CONFIG.scale = int(CONFIG.get('FONTS', 'scale'))
	CONFIG.fonttmplist		 = os.listdir(r'C:\Windows\fonts')
	CONFIG.fontlist = []
	for font in CONFIG.fonttmplist:
		# Get font names without file extension,
		# append them to a list
		font = font.rsplit( ".", 1 )[0]
		CONFIG.fontlist.append(font)
	
	# GPT-3 settings
	CONFIG.api_key			 = str(CONFIG.get("GPT-3 SETTINGS", "api_key")) 
	CONFIG.model_str		   = str(CONFIG.get("GPT-3 SETTINGS", "model")) 
	CONFIG.temperature		 = float(CONFIG.get('GPT-3 SETTINGS', 'temperature')) 
	CONFIG.length			  = int(CONFIG.get('GPT-3 SETTINGS', 'length')) 
	CONFIG.top_p			   = float(CONFIG.get('GPT-3 SETTINGS', 'top_p')) ## will not implement!
	CONFIG.predictions_on	   = eval(CONFIG.get('GPT-3 SETTINGS', 'predictions_on'))
	CONFIG.max_reroll  = int(CONFIG.get('GPT-3 SETTINGS', 'max_reroll'))

def rgb_to_hex(rgb):
	return '%02x%02x%02x' % rgb

def color_chooser():
	"""
	:return: Any(str, None) Returns hex string of color chosen or None if nothing was chosen
	"""
	color_map = {
		'AliceBlue': '#F0F8FF',
		'antique white': '#FAEBD7',
		'AntiqueWhite': '#FAEBD7',
		'AntiqueWhite1': '#FFEFDB',
		'AntiqueWhite2': '#EEDFCC',
		'AntiqueWhite3': '#CDC0B0',
		'AntiqueWhite4': '#8B8378',
		'aquamarine': '#7FFFD4',
		'aquamarine1': '#7FFFD4',
		'aquamarine2': '#76EEC6',
		'aquamarine3': '#66CDAA',
		'aquamarine4': '#458B74',
		'azure': '#F0FFFF',
		'azure1': '#F0FFFF',
		'azure2': '#E0EEEE',
		'azure3': '#C1CDCD',
		'azure4': '#838B8B',
		'beige': '#F5F5DC',
		'bisque': '#FFE4C4',
		'bisque1': '#FFE4C4',
		'bisque2': '#EED5B7',
		'bisque3': '#CDB79E',
		'bisque4': '#8B7D6B',
		'black': '#000000',
		'blanched almond': '#FFEBCD',
		'BlanchedAlmond': '#FFEBCD',
		'blue': '#0000FF',
		'blue violet': '#8A2BE2',
		'blue1': '#0000FF',
		'blue2': '#0000EE',
		'blue3': '#0000CD',
		'blue4': '#00008B',
		'BlueViolet': '#8A2BE2',
		'brown': '#A52A2A',
		'brown1': '#FF4040',
		'brown2': '#EE3B3B',
		'brown3': '#CD3333',
		'brown4': '#8B2323',
		'burlywood': '#DEB887',
		'burlywood1': '#FFD39B',
		'burlywood2': '#EEC591',
		'burlywood3': '#CDAA7D',
		'burlywood4': '#8B7355',
		'cadet blue': '#5F9EA0',
		'CadetBlue': '#5F9EA0',
		'CadetBlue1': '#98F5FF',
		'CadetBlue2': '#8EE5EE',
		'CadetBlue3': '#7AC5CD',
		'CadetBlue4': '#53868B',
		'chartreuse': '#7FFF00',
		'chartreuse1': '#7FFF00',
		'chartreuse2': '#76EE00',
		'chartreuse3': '#66CD00',
		'chartreuse4': '#458B00',
		'chocolate': '#D2691E',
		'chocolate1': '#FF7F24',
		'chocolate2': '#EE7621',
		'chocolate3': '#CD661D',
		'chocolate4': '#8B4513',
		'coral': '#FF7F50',
		'coral1': '#FF7256',
		'coral2': '#EE6A50',
		'coral3': '#CD5B45',
		'coral4': '#8B3E2F',
		'cornflower blue': '#6495ED',
		'CornflowerBlue': '#6495ED',
		'cornsilk': '#FFF8DC',
		'cornsilk1': '#FFF8DC',
		'cornsilk2': '#EEE8CD',
		'cornsilk3': '#CDC8B1',
		'cornsilk4': '#8B8878',
		'cyan': '#00FFFF',
		'cyan1': '#00FFFF',
		'cyan2': '#00EEEE',
		'cyan3': '#00CDCD',
		'cyan4': '#008B8B',
		'dark blue': '#00008B',
		'dark cyan': '#008B8B',
		'dark goldenrod': '#B8860B',
		'dark gray': '#A9A9A9',
		'dark green': '#006400',
		'dark grey': '#A9A9A9',
		'dark khaki': '#BDB76B',
		'dark magenta': '#8B008B',
		'dark olive green': '#556B2F',
		'dark orange': '#FF8C00',
		'dark orchid': '#9932CC',
		'dark red': '#8B0000',
		'dark salmon': '#E9967A',
		'dark sea green': '#8FBC8F',
		'dark slate blue': '#483D8B',
		'dark slate gray': '#2F4F4F',
		'dark slate grey': '#2F4F4F',
		'dark turquoise': '#00CED1',
		'dark violet': '#9400D3',
		'DarkBlue': '#00008B',
		'DarkCyan': '#008B8B',
		'DarkGoldenrod': '#B8860B',
		'DarkGoldenrod1': '#FFB90F',
		'DarkGoldenrod2': '#EEAD0E',
		'DarkGoldenrod3': '#CD950C',
		'DarkGoldenrod4': '#8B6508',
		'DarkGray': '#A9A9A9',
		'DarkGreen': '#006400',
		'DarkGrey': '#A9A9A9',
		'DarkKhaki': '#BDB76B',
		'DarkMagenta': '#8B008B',
		'DarkOliveGreen': '#556B2F',
		'DarkOliveGreen1': '#CAFF70',
		'DarkOliveGreen2': '#BCEE68',
		'DarkOliveGreen3': '#A2CD5A',
		'DarkOliveGreen4': '#6E8B3D',
		'DarkOrange': '#FF8C00',
		'DarkOrange1': '#FF7F00',
		'DarkOrange2': '#EE7600',
		'DarkOrange3': '#CD6600',
		'DarkOrange4': '#8B4500',
		'DarkOrchid': '#9932CC',
		'DarkOrchid1': '#BF3EFF',
		'DarkOrchid2': '#B23AEE',
		'DarkOrchid3': '#9A32CD',
		'DarkOrchid4': '#68228B',
		'DarkRed': '#8B0000',
		'DarkSalmon': '#E9967A',
		'DarkSeaGreen': '#8FBC8F',
		'DarkSeaGreen1': '#C1FFC1',
		'DarkSeaGreen2': '#B4EEB4',
		'DarkSeaGreen3': '#9BCD9B',
		'DarkSeaGreen4': '#698B69',
		'DarkSlateBlue': '#483D8B',
		'DarkSlateGray': '#2F4F4F',
		'DarkSlateGray1': '#97FFFF',
		'DarkSlateGray2': '#8DEEEE',
		'DarkSlateGray3': '#79CDCD',
		'DarkSlateGray4': '#528B8B',
		'DarkSlateGrey': '#2F4F4F',
		'DarkTurquoise': '#00CED1',
		'DarkViolet': '#9400D3',
		'deep pink': '#FF1493',
		'deep sky blue': '#00BFFF',
		'DeepPink': '#FF1493',
		'DeepPink1': '#FF1493',
		'DeepPink2': '#EE1289',
		'DeepPink3': '#CD1076',
		'DeepPink4': '#8B0A50',
		'DeepSkyBlue': '#00BFFF',
		'DeepSkyBlue1': '#00BFFF',
		'DeepSkyBlue2': '#00B2EE',
		'DeepSkyBlue3': '#009ACD',
		'DeepSkyBlue4': '#00688B',
		'dim gray': '#696969',
		'dim grey': '#696969',
		'DimGray': '#696969',
		'DimGrey': '#696969',
		'dodger blue': '#1E90FF',
		'DodgerBlue': '#1E90FF',
		'DodgerBlue1': '#1E90FF',
		'DodgerBlue2': '#1C86EE',
		'DodgerBlue3': '#1874CD',
		'DodgerBlue4': '#104E8B',
		'firebrick': '#B22222',
		'firebrick1': '#FF3030',
		'firebrick2': '#EE2C2C',
		'firebrick3': '#CD2626',
		'firebrick4': '#8B1A1A',
		'floral white': '#FFFAF0',
		'FloralWhite': '#FFFAF0',
		'forest green': '#228B22',
		'ForestGreen': '#228B22',
		'gainsboro': '#DCDCDC',
		'ghost white': '#F8F8FF',
		'GhostWhite': '#F8F8FF',
		'gold': '#FFD700',
		'gold1': '#FFD700',
		'gold2': '#EEC900',
		'gold3': '#CDAD00',
		'gold4': '#8B7500',
		'goldenrod': '#DAA520',
		'goldenrod1': '#FFC125',
		'goldenrod2': '#EEB422',
		'goldenrod3': '#CD9B1D',
		'goldenrod4': '#8B6914',
		'green': '#00FF00',
		'green yellow': '#ADFF2F',
		'green1': '#00FF00',
		'green2': '#00EE00',
		'green3': '#00CD00',
		'green4': '#008B00',
		'GreenYellow': '#ADFF2F',
		'grey': '#BEBEBE',
		'grey0': '#000000',
		'grey1': '#030303',
		'grey2': '#050505',
		'grey3': '#080808',
		'grey4': '#0A0A0A',
		'grey5': '#0D0D0D',
		'grey6': '#0F0F0F',
		'grey7': '#121212',
		'grey8': '#141414',
		'grey9': '#171717',
		'grey10': '#1A1A1A',
		'grey11': '#1C1C1C',
		'grey12': '#1F1F1F',
		'grey13': '#212121',
		'grey14': '#242424',
		'grey15': '#262626',
		'grey16': '#292929',
		'grey17': '#2B2B2B',
		'grey18': '#2E2E2E',
		'grey19': '#303030',
		'grey20': '#333333',
		'grey21': '#363636',
		'grey22': '#383838',
		'grey23': '#3B3B3B',
		'grey24': '#3D3D3D',
		'grey25': '#404040',
		'grey26': '#424242',
		'grey27': '#454545',
		'grey28': '#474747',
		'grey29': '#4A4A4A',
		'grey30': '#4D4D4D',
		'grey31': '#4F4F4F',
		'grey32': '#525252',
		'grey33': '#545454',
		'grey34': '#575757',
		'grey35': '#595959',
		'grey36': '#5C5C5C',
		'grey37': '#5E5E5E',
		'grey38': '#616161',
		'grey39': '#636363',
		'grey40': '#666666',
		'grey41': '#696969',
		'grey42': '#6B6B6B',
		'grey43': '#6E6E6E',
		'grey44': '#707070',
		'grey45': '#737373',
		'grey46': '#757575',
		'grey47': '#787878',
		'grey48': '#7A7A7A',
		'grey49': '#7D7D7D',
		'grey50': '#7F7F7F',
		'grey51': '#828282',
		'grey52': '#858585',
		'grey53': '#878787',
		'grey54': '#8A8A8A',
		'grey55': '#8C8C8C',
		'grey56': '#8F8F8F',
		'grey57': '#919191',
		'grey58': '#949494',
		'grey59': '#969696',
		'grey60': '#999999',
		'grey61': '#9C9C9C',
		'grey62': '#9E9E9E',
		'grey63': '#A1A1A1',
		'grey64': '#A3A3A3',
		'grey65': '#A6A6A6',
		'grey66': '#A8A8A8',
		'grey67': '#ABABAB',
		'grey68': '#ADADAD',
		'grey69': '#B0B0B0',
		'grey70': '#B3B3B3',
		'grey71': '#B5B5B5',
		'grey72': '#B8B8B8',
		'grey73': '#BABABA',
		'grey74': '#BDBDBD',
		'grey75': '#BFBFBF',
		'grey76': '#C2C2C2',
		'grey77': '#C4C4C4',
		'grey78': '#C7C7C7',
		'grey79': '#C9C9C9',
		'grey80': '#CCCCCC',
		'grey81': '#CFCFCF',
		'grey82': '#D1D1D1',
		'grey83': '#D4D4D4',
		'grey84': '#D6D6D6',
		'grey85': '#D9D9D9',
		'grey86': '#DBDBDB',
		'grey87': '#DEDEDE',
		'grey88': '#E0E0E0',
		'grey89': '#E3E3E3',
		'grey90': '#E5E5E5',
		'grey91': '#E8E8E8',
		'grey92': '#EBEBEB',
		'grey93': '#EDEDED',
		'grey94': '#F0F0F0',
		'grey95': '#F2F2F2',
		'grey96': '#F5F5F5',
		'grey97': '#F7F7F7',
		'grey98': '#FAFAFA',
		'grey99': '#FCFCFC',
		'grey100': '#FFFFFF',
		'honeydew': '#F0FFF0',
		'honeydew1': '#F0FFF0',
		'honeydew2': '#E0EEE0',
		'honeydew3': '#C1CDC1',
		'honeydew4': '#838B83',
		'hot pink': '#FF69B4',
		'HotPink': '#FF69B4',
		'HotPink1': '#FF6EB4',
		'HotPink2': '#EE6AA7',
		'HotPink3': '#CD6090',
		'HotPink4': '#8B3A62',
		'indian red': '#CD5C5C',
		'IndianRed': '#CD5C5C',
		'IndianRed1': '#FF6A6A',
		'IndianRed2': '#EE6363',
		'IndianRed3': '#CD5555',
		'IndianRed4': '#8B3A3A',
		'ivory': '#FFFFF0',
		'ivory1': '#FFFFF0',
		'ivory2': '#EEEEE0',
		'ivory3': '#CDCDC1',
		'ivory4': '#8B8B83',
		'khaki': '#F0E68C',
		'khaki1': '#FFF68F',
		'khaki2': '#EEE685',
		'khaki3': '#CDC673',
		'khaki4': '#8B864E',
		'lavender': '#E6E6FA',
		'lavender blush': '#FFF0F5',
		'LavenderBlush': '#FFF0F5',
		'LavenderBlush1': '#FFF0F5',
		'LavenderBlush2': '#EEE0E5',
		'LavenderBlush3': '#CDC1C5',
		'LavenderBlush4': '#8B8386',
		'lawn green': '#7CFC00',
		'LawnGreen': '#7CFC00',
		'LemonChiffon': '#FFFACD',
		'LemonChiffon1': '#FFFACD',
		'LemonChiffon2': '#EEE9BF',
		'LemonChiffon3': '#CDC9A5',
		'LemonChiffon4': '#8B8970',
		'light blue': '#ADD8E6',
		'light coral': '#F08080',
		'light cyan': '#E0FFFF',
		'light goldenrod': '#EEDD82',
		'light goldenrod yellow': '#FAFAD2',
		'light gray': '#D3D3D3',
		'light green': '#90EE90',
		'light grey': '#D3D3D3',
		'light pink': '#FFB6C1',
		'light salmon': '#FFA07A',
		'light sea green': '#20B2AA',
		'light sky blue': '#87CEFA',
		'light slate blue': '#8470FF',
		'light slate gray': '#778899',
		'light slate grey': '#778899',
		'light steel blue': '#B0C4DE',
		'light yellow': '#FFFFE0',
		'LightBlue': '#ADD8E6',
		'LightBlue1': '#BFEFFF',
		'LightBlue2': '#B2DFEE',
		'LightBlue3': '#9AC0CD',
		'LightBlue4': '#68838B',
		'LightCoral': '#F08080',
		'LightCyan': '#E0FFFF',
		'LightCyan1': '#E0FFFF',
		'LightCyan2': '#D1EEEE',
		'LightCyan3': '#B4CDCD',
		'LightCyan4': '#7A8B8B',
		'LightGoldenrod': '#EEDD82',
		'LightGoldenrod1': '#FFEC8B',
		'LightGoldenrod2': '#EEDC82',
		'LightGoldenrod3': '#CDBE70',
		'LightGoldenrod4': '#8B814C',
		'LightGoldenrodYellow': '#FAFAD2',
		'LightGray': '#D3D3D3',
		'LightGreen': '#90EE90',
		'LightGrey': '#D3D3D3',
		'LightPink': '#FFB6C1',
		'LightPink1': '#FFAEB9',
		'LightPink2': '#EEA2AD',
		'LightPink3': '#CD8C95',
		'LightPink4': '#8B5F65',
		'LightSalmon': '#FFA07A',
		'LightSalmon1': '#FFA07A',
		'LightSalmon2': '#EE9572',
		'LightSalmon3': '#CD8162',
		'LightSalmon4': '#8B5742',
		'LightSeaGreen': '#20B2AA',
		'LightSkyBlue': '#87CEFA',
		'LightSkyBlue1': '#B0E2FF',
		'LightSkyBlue2': '#A4D3EE',
		'LightSkyBlue3': '#8DB6CD',
		'LightSkyBlue4': '#607B8B',
		'LightSlateBlue': '#8470FF',
		'LightSlateGray': '#778899',
		'LightSlateGrey': '#778899',
		'LightSteelBlue': '#B0C4DE',
		'LightSteelBlue1': '#CAE1FF',
		'LightSteelBlue2': '#BCD2EE',
		'LightSteelBlue3': '#A2B5CD',
		'LightSteelBlue4': '#6E7B8B',
		'LightYellow': '#FFFFE0',
		'LightYellow1': '#FFFFE0',
		'LightYellow2': '#EEEED1',
		'LightYellow3': '#CDCDB4',
		'LightYellow4': '#8B8B7A',
		'lime green': '#32CD32',
		'LimeGreen': '#32CD32',
		'linen': '#FAF0E6',
		'magenta': '#FF00FF',
		'magenta1': '#FF00FF',
		'magenta2': '#EE00EE',
		'magenta3': '#CD00CD',
		'magenta4': '#8B008B',
		'maroon': '#B03060',
		'maroon1': '#FF34B3',
		'maroon2': '#EE30A7',
		'maroon3': '#CD2990',
		'maroon4': '#8B1C62',
		'medium aquamarine': '#66CDAA',
		'medium blue': '#0000CD',
		'medium orchid': '#BA55D3',
		'medium purple': '#9370DB',
		'medium sea green': '#3CB371',
		'medium slate blue': '#7B68EE',
		'medium spring green': '#00FA9A',
		'medium turquoise': '#48D1CC',
		'medium violet red': '#C71585',
		'MediumAquamarine': '#66CDAA',
		'MediumBlue': '#0000CD',
		'MediumOrchid': '#BA55D3',
		'MediumOrchid1': '#E066FF',
		'MediumOrchid2': '#D15FEE',
		'MediumOrchid3': '#B452CD',
		'MediumOrchid4': '#7A378B',
		'MediumPurple': '#9370DB',
		'MediumPurple1': '#AB82FF',
		'MediumPurple2': '#9F79EE',
		'MediumPurple3': '#8968CD',
		'MediumPurple4': '#5D478B',
		'MediumSeaGreen': '#3CB371',
		'MediumSlateBlue': '#7B68EE',
		'MediumSpringGreen': '#00FA9A',
		'MediumTurquoise': '#48D1CC',
		'MediumVioletRed': '#C71585',
		'midnight blue': '#191970',
		'MidnightBlue': '#191970',
		'mint cream': '#F5FFFA',
		'MintCream': '#F5FFFA',
		'misty rose': '#FFE4E1',
		'MistyRose': '#FFE4E1',
		'MistyRose1': '#FFE4E1',
		'MistyRose2': '#EED5D2',
		'MistyRose3': '#CDB7B5',
		'MistyRose4': '#8B7D7B',
		'moccasin': '#FFE4B5',
		'navajo white': '#FFDEAD',
		'NavajoWhite': '#FFDEAD',
		'NavajoWhite1': '#FFDEAD',
		'NavajoWhite2': '#EECFA1',
		'NavajoWhite3': '#CDB38B',
		'NavajoWhite4': '#8B795E',
		'navy': '#000080',
		'navy blue': '#000080',
		'NavyBlue': '#000080',
		'old lace': '#FDF5E6',
		'OldLace': '#FDF5E6',
		'olive drab': '#6B8E23',
		'OliveDrab': '#6B8E23',
		'OliveDrab1': '#C0FF3E',
		'OliveDrab2': '#B3EE3A',
		'OliveDrab3': '#9ACD32',
		'OliveDrab4': '#698B22',
		'orange': '#FFA500',
		'orange red': '#FF4500',
		'orange1': '#FFA500',
		'orange2': '#EE9A00',
		'orange3': '#CD8500',
		'orange4': '#8B5A00',
		'OrangeRed': '#FF4500',
		'OrangeRed1': '#FF4500',
		'OrangeRed2': '#EE4000',
		'OrangeRed3': '#CD3700',
		'OrangeRed4': '#8B2500',
		'orchid': '#DA70D6',
		'orchid1': '#FF83FA',
		'orchid2': '#EE7AE9',
		'orchid3': '#CD69C9',
		'orchid4': '#8B4789',
		'pale goldenrod': '#EEE8AA',
		'pale green': '#98FB98',
		'pale turquoise': '#AFEEEE',
		'pale violet red': '#DB7093',
		'PaleGoldenrod': '#EEE8AA',
		'PaleGreen': '#98FB98',
		'PaleGreen1': '#9AFF9A',
		'PaleGreen2': '#90EE90',
		'PaleGreen3': '#7CCD7C',
		'PaleGreen4': '#548B54',
		'PaleTurquoise': '#AFEEEE',
		'PaleTurquoise1': '#BBFFFF',
		'PaleTurquoise2': '#AEEEEE',
		'PaleTurquoise3': '#96CDCD',
		'PaleTurquoise4': '#668B8B',
		'PaleVioletRed': '#DB7093',
		'PaleVioletRed1': '#FF82AB',
		'PaleVioletRed2': '#EE799F',
		'PaleVioletRed3': '#CD687F',
		'PaleVioletRed4': '#8B475D',
		'papaya whip': '#FFEFD5',
		'PapayaWhip': '#FFEFD5',
		'peach puff': '#FFDAB9',
		'PeachPuff': '#FFDAB9',
		'PeachPuff1': '#FFDAB9',
		'PeachPuff2': '#EECBAD',
		'PeachPuff3': '#CDAF95',
		'PeachPuff4': '#8B7765',
		'peru': '#CD853F',
		'pink': '#FFC0CB',
		'pink1': '#FFB5C5',
		'pink2': '#EEA9B8',
		'pink3': '#CD919E',
		'pink4': '#8B636C',
		'plum': '#DDA0DD',
		'plum1': '#FFBBFF',
		'plum2': '#EEAEEE',
		'plum3': '#CD96CD',
		'plum4': '#8B668B',
		'powder blue': '#B0E0E6',
		'PowderBlue': '#B0E0E6',
		'purple': '#A020F0',
		'purple1': '#9B30FF',
		'purple2': '#912CEE',
		'purple3': '#7D26CD',
		'purple4': '#551A8B',
		'red': '#FF0000',
		'red1': '#FF0000',
		'red2': '#EE0000',
		'red3': '#CD0000',
		'red4': '#8B0000',
		'rosy brown': '#BC8F8F',
		'RosyBrown': '#BC8F8F',
		'RosyBrown1': '#FFC1C1',
		'RosyBrown2': '#EEB4B4',
		'RosyBrown3': '#CD9B9B',
		'RosyBrown4': '#8B6969',
		'royal blue': '#4169E1',
		'RoyalBlue': '#4169E1',
		'RoyalBlue1': '#4876FF',
		'RoyalBlue2': '#436EEE',
		'RoyalBlue3': '#3A5FCD',
		'RoyalBlue4': '#27408B',
		'saddle brown': '#8B4513',
		'SaddleBrown': '#8B4513',
		'salmon': '#FA8072',
		'salmon1': '#FF8C69',
		'salmon2': '#EE8262',
		'salmon3': '#CD7054',
		'salmon4': '#8B4C39',
		'sandy brown': '#F4A460',
		'SandyBrown': '#F4A460',
		'sea green': '#2E8B57',
		'SeaGreen': '#2E8B57',
		'SeaGreen1': '#54FF9F',
		'SeaGreen2': '#4EEE94',
		'SeaGreen3': '#43CD80',
		'SeaGreen4': '#2E8B57',
		'seashell': '#FFF5EE',
		'seashell1': '#FFF5EE',
		'seashell2': '#EEE5DE',
		'seashell3': '#CDC5BF',
		'seashell4': '#8B8682',
		'sienna': '#A0522D',
		'sienna1': '#FF8247',
		'sienna2': '#EE7942',
		'sienna3': '#CD6839',
		'sienna4': '#8B4726',
		'sky blue': '#87CEEB',
		'SkyBlue': '#87CEEB',
		'SkyBlue1': '#87CEFF',
		'SkyBlue2': '#7EC0EE',
		'SkyBlue3': '#6CA6CD',
		'SkyBlue4': '#4A708B',
		'slate blue': '#6A5ACD',
		'slate gray': '#708090',
		'slate grey': '#708090',
		'SlateBlue': '#6A5ACD',
		'SlateBlue1': '#836FFF',
		'SlateBlue2': '#7A67EE',
		'SlateBlue3': '#6959CD',
		'SlateBlue4': '#473C8B',
		'SlateGray': '#708090',
		'SlateGray1': '#C6E2FF',
		'SlateGray2': '#B9D3EE',
		'SlateGray3': '#9FB6CD',
		'SlateGray4': '#6C7B8B',
		'SlateGrey': '#708090',
		'snow': '#FFFAFA',
		'snow1': '#FFFAFA',
		'snow2': '#EEE9E9',
		'snow3': '#CDC9C9',
		'snow4': '#8B8989',
		'spring green': '#00FF7F',
		'SpringGreen': '#00FF7F',
		'SpringGreen1': '#00FF7F',
		'SpringGreen2': '#00EE76',
		'SpringGreen3': '#00CD66',
		'SpringGreen4': '#008B45',
		'steel blue': '#4682B4',
		'SteelBlue': '#4682B4',
		'SteelBlue1': '#63B8FF',
		'SteelBlue2': '#5CACEE',
		'SteelBlue3': '#4F94CD',
		'SteelBlue4': '#36648B',
		'tan': '#D2B48C',
		'tan1': '#FFA54F',
		'tan2': '#EE9A49',
		'tan3': '#CD853F',
		'tan4': '#8B5A2B',
		'thistle': '#D8BFD8',
		'thistle1': '#FFE1FF',
		'thistle2': '#EED2EE',
		'thistle3': '#CDB5CD',
		'thistle4': '#8B7B8B',
		'tomato': '#FF6347',
		'tomato1': '#FF6347',
		'tomato2': '#EE5C42',
		'tomato3': '#CD4F39',
		'tomato4': '#8B3626',
		'turquoise': '#40E0D0',
		'turquoise1': '#00F5FF',
		'turquoise2': '#00E5EE',
		'turquoise3': '#00C5CD',
		'turquoise4': '#00868B',
		'violet': '#EE82EE',
		'violet red': '#D02090',
		'VioletRed': '#D02090',
		'VioletRed1': '#FF3E96',
		'VioletRed2': '#EE3A8C',
		'VioletRed3': '#CD3278',
		'VioletRed4': '#8B2252',
		'wheat': '#F5DEB3',
		'wheat1': '#FFE7BA',
		'wheat2': '#EED8AE',
		'wheat3': '#CDBA96',
		'wheat4': '#8B7E66',
		'white': '#FFFFFF',
		'white smoke': '#F5F5F5',
		'WhiteSmoke': '#F5F5F5',
		'yellow': '#FFFF00',
		'yellow green': '#9ACD32',
		'yellow1': '#FFFF00',
		'yellow2': '#EEEE00',
		'yellow3': '#CDCD00',
		'yellow4': '#8B8B00',
		'YellowGreen': '#9ACD32',
	}

	sg.change_look_and_feel('Dark Blue 3')
	button_size = (None,None)		 # for very compact buttons

	def ColorButton(color):
		"""
		A User Defined Element - returns a Button that configured in a certain way.
		:param color: Tuple[str, str] ( color name, hex string)
		:return: sg.Button object
		"""
		return sg.B(button_color=('white', color[1]), pad=(0,0), size=button_size,key=color, tooltip=f'{color[0]}:{color[1]}', border_width=0)

	num_colors = len(list(color_map.keys()))
	row_len=40

	grid = [[ColorButton(list(color_map.items())[c+j*row_len]) for c in range(0,row_len)] for j in range(0,num_colors//row_len)]
	grid += [[ColorButton(list(color_map.items())[c+num_colors-num_colors%row_len]) for c in range(0,num_colors%row_len)]]

	layout =  grid + \
				[[sg.Button('OK'), sg.T(size=(30,1), key='-OUT-')]]

	window = sg.Window('Color Picker', layout,  icon='config/icon1.ico', grab_anywhere=True, use_ttk_buttons=True)
	color_chosen = None
	while True:			 # Event Loop
		event, values = window.read()
		if event in (None, 'OK'):
			if event is None:
				color_chosen = None
			break
		window['-OUT-'](f'Chosen color: {event[0]} : {event[1]}')
		color_chosen = event[1]
	window.close()
	
	
	return color_chosen




def showWindow(tab=None):
	'''
	Shows the setup window.
	'''
	global CONFIG
	
	## Create tab layouts
	
	Screen_Settings_layout =  [
					[sg.Text("Screen mode", size = (10,0)),
					 sg.Combo(['Fullscreen', 'Windowed'], size=(45,0), default_value = CONFIG.fullscreen)],
					[sg.Text("FPS limit", size = (10,0)), 
					 sg.Slider(range=(20, 120), orientation='h', size=(37, 10), default_value=CONFIG.fps_target), 
					 sg.Button('?', key = "help_FPS")]
							  ]

	GPT3_Settings_layout = [
					[sg.Text("Predictions", size=(10,0)), sg.Checkbox(None, default=CONFIG.predictions_on, size = (38,0), key="predictions"), 
					 sg.Button('?', key = "help_prediction")],
					[sg.Text("Model", size = (10,0)), 
					 sg.Combo(['davinci', 'ada', 'babbage', 'curie'], size=(45,0), default_value = CONFIG.model_str), 
					 sg.Button('?', key = "help_model")],
					[sg.Text("Temperature", size = (10,0)), 
					 sg.Slider(range=(0.1, 1.0), resolution=.1, orientation='h', size=(37, 10), default_value=CONFIG.temperature), 
					 sg.Button('?', key = "help_temperature")],
					[sg.Text("Length", size = (10,0)), 
					 sg.Slider(range=(1, 4), resolution=1, orientation='h', size=(37, 10), default_value=CONFIG.length), 
					 sg.Button('?', key = "help_length")],
					[sg.Text("Maximum rerolls", size = (10,0)), 
					 sg.Slider(range=(0, 50), resolution=1, orientation='h', size=(37, 10), default_value=CONFIG.max_reroll, key = "max_reroll"), 
					 sg.Button('?', key = "help_reroll")],
					[sg.Text("API key", size = (10,0)), 
					 sg.InputText(default_text=CONFIG.api_key,password_char="*", size = (47, 10)), 
					 sg.Button('?', key = "help_apiKey")],
						   ]
	
	Misc_Settings_layout = [
					[sg.Text("Debug info", size = (11,0)),
					 sg.Checkbox(None, default=CONFIG.debug_on, size = (38,0)), 
					 sg.Button('?', key = "help_debug")],
					[sg.Text("Input method", size = (10,0)), 
					 sg.Combo(['Keyboard only', 'fNIRS only', 'Keyboard + fNIRS'], size=(46,0), default_value = CONFIG.input_type), 
					 sg.Button('?', key = "help_input")],
					[sg.Text("Text-To-Speech", size=(11,0)),
					 sg.Checkbox(None, default=CONFIG.TTS_ON, size = (38,0)), 
					 sg.Button('?', key = "help_tts")],
					[sg.Text("TTS Voice", size=(10,0)),
					 sg.Combo(CONFIG.voiceList, size=(46,0), default_value = CONFIG.voiceList[CONFIG.TTS_VOICE]),
					 sg.Button('?', key = "help_ttsVoices")],
					[sg.Text("Dictionary", size=(10,0)),
					 sg.Input(size=(39,0),default_text=CONFIG.dictionary), 
					 sg.FileBrowse(file_types=(("Text Files", "*.txt"),)), 
					 sg.Button('?', key = "help_dict")],
					[sg.Text("Timeout after", size = (11,0)),
					 sg.Slider(range=(1, 10), resolution=1, orientation='h', size=(37, 10), default_value=CONFIG.timeout_iterlimit, key="maxIter"),
					 sg.Button('?', key = "help_maxIter")],
					[sg.Text("Progress bar", size = (11,0)),
					 sg.Checkbox(None, default=CONFIG.progressbar, size = (38,0), key = "progressbar_on"), 
					 sg.Button('?', key = "help_progressbar")],					 
					[sg.Text("Progress bar indicator", size=(11,0)),
					 sg.Checkbox(None, default=CONFIG.indicator, key="indicator", size = (38,0)), 
					 sg.Button('?', key = "help_indicator")],
					[sg.Text("Indicator position", size = (11,0)),
					 sg.Slider(range=(1, 1000), resolution=10, orientation='h', size=(37, 10), default_value=CONFIG.indicatorPos, key="indicatorPos"),
					 sg.Button('?', key = "help_indicatorPos")]					 
						   ]
	
	TurboSatori_Settings_layout = [
					[sg.Text("Data folder", size=(10,0)),
					 sg.Input(size=(39,0),default_text=CONFIG.data_folder), 
					 sg.FolderBrowse(), 
					 sg.Button('?', key = "help_datafolder")],
					[sg.Text("Thermometer", size=(11,0)),
					 sg.Checkbox(None, default=CONFIG.thermo_on, size = (38,0)), 
					 sg.Button('?', key = "help_thermometer")],
					 [sg.Text("Feedback during planning", size=(11,0)),
					 sg.Checkbox(None, default=CONFIG.thermo_during_planning, size = (38,0), key = "thermo_during_planning"), 
					 sg.Button('?', key = "help_thermometer_during_planning")],
					[sg.Text("Data read rate", size = (11,0)),
					 sg.Slider(range=(1, 20), resolution=1, orientation='h', size=(37, 10), default_value=CONFIG.NF_reader_frequency), 
					 sg.Button('?', key = "help_datarate")],
					[sg.Text("Mode", size = (10,0)), 
					 sg.Combo(['Oxy', 'Deoxy', 'Average'], size=(46,None), default_value = CONFIG.NF_mode),
					 sg.Button('?', key = "help_nfmode")],
					[sg.Text("Threshold", size = (11,0)),
					 sg.Slider(range=(1, 30), resolution=1, orientation='h', size=(37, 10), default_value=CONFIG.NF_threshold, key="act_thresh"),
					 sg.Button('?', key = "help_threshold")]
								  ]

	Font_Settings_layout = [
					[sg.Text("Font", size = (10,0)),
					 sg.Combo(CONFIG.fontlist, size=(45,None), default_value = CONFIG.FONT),
					 sg.Button('?', key = "help_font")],
					[sg.Text("Font scale", size = (10,0)),
					 sg.Slider(range=(1, 3), resolution=1, orientation='h', key="fontScale", size=(37, 10), default_value=CONFIG.scale),
					 sg.Button('?', key = "help_fontscale")],
						   ]
	
	Intro_Settings_layout = [
					[sg.Text("Tutorial", size = (10,0)),
					 sg.Checkbox(None, default=CONFIG.tutorial, size = (38,0), key = "tutorial_on"), 
					 sg.Button('?', key = "help_tutorial")],
					[sg.Text("Localizer", size = (10,0)),
					 sg.Checkbox(None, default=CONFIG.localizer, size = (38,0), key = "localizer_on"), 
					 sg.Button('?', key = "help_localizer")],
					[sg.Text("Threshold detection", size = (10,0)),
					 sg.Checkbox(None, default=CONFIG.threshold, size = (38,0), key = "threshold_on"), 
					 sg.Button('?', key = "help_thresholdOn")],
					[sg.Text("Instructed encoding run", size = (10,0)),
					 sg.Checkbox(None, default=CONFIG.training, size = (38,0), key = "training_on"), 
					 sg.Button('?', key = "help_training")],
					[sg.Text("Localizer TASK duration", size = (11,0)),
					 sg.Slider(range=(5, 60), resolution=1, orientation='h', size=(36, 10), default_value=CONFIG.localizer_task_duration, key="localizer_task_duration"),
					 sg.Button('?', key = "help_localizer_duration1")],
					[sg.Text("Localizer REST duration", size = (11,0)),
					 sg.Slider(range=(5, 60), resolution=1, orientation='h', size=(36, 10), default_value=CONFIG.localizer_rest_duration, key="localizer_rest_duration"),
					 sg.Button('?', key = "help_localizer_duration2")],
					[sg.Text("Localizer repetitions", size = (11,0)),
					 sg.Slider(range=(1, 10), resolution=1, orientation='h', size=(36, 10), default_value=CONFIG.localizerrepetitions, key="localizer_repetitions"),
					 sg.Button('?', key = "help_localizer_repetitions")],
					[sg.Text("Localizer last rest duration", size=(11,0)),  
					 sg.Slider(range=(1, 200), resolution=1, orientation='h', size=(36, 10), default_value=CONFIG.localizer_lasttrial_duration, key="localizer_lasttrial_duration"),
					 sg.Button('?', key = "help_localizer_lasttrial_duration")]				 
							]
	
	## Create layout for the timings tab
	
	headings = ['       ', 'Initial', 'Ph. 1', 'Ph. 2','Ph. 3', 'Ph. 4', 'Ph. 5', 'End']
	header =  [[sg.Text('  ')] + [sg.Text(h) for h in headings]]
	field_size = 4
	input_row1 = [[
				   sg.Text('        Main'),
				   sg.Input(size=(field_size,0), key="initial_main", default_text=CONFIG.initialDelay),
				   sg.Input(size=(field_size,0), key="1_main", default_text=CONFIG.firstPhase),
				   sg.Input(size=(field_size,0), key="2_main", default_text=CONFIG.secondPhase),
				   sg.Input(size=(field_size,0), key="3_main", default_text=CONFIG.thirdPhase),
				   sg.Input(size=(field_size,0), key="4_main", default_text=CONFIG.fourthPhase),
				   sg.Input(size=(field_size,0), key="5_main", default_text=CONFIG.fifthPhase),
				   sg.Input(size=(field_size,0), key="end_main", default_text=CONFIG.endPhase),
				   sg.Button('?', key = "help_timings")
				 ]]
	input_row2 = [[
				   sg.Text('Prediction'),
				   sg.Input(size=(field_size,0), key="initial_pred", default_text=CONFIG.pred_initialDelay),
				   sg.Input(size=(field_size,0), key="1_pred", default_text=CONFIG.pred_firstPhase),
				   sg.Input(size=(field_size,0), key="2_pred", default_text=CONFIG.pred_secondPhase),
				   sg.Input(size=(field_size,0), key="3_pred", default_text=CONFIG.pred_thirdPhase),
				   sg.Input(size=(field_size,0), key="4_pred", default_text=CONFIG.pred_fourthPhase),
				   sg.Input(size=(field_size,0), key="5_pred", default_text=CONFIG.pred_fifthPhase),
				   sg.Input(size=(field_size,0), key="end_pred", default_text=CONFIG.pred_endPhase)
				 ]]
	Timings_layout = header + input_row1 + input_row2
	
	## Create layout for the protocol tab
	Protocol_Settings_layout = [
					[sg.Text("Experiment name", size = (10,0)),
					 sg.InputText(default_text=CONFIG.experiment_name, size = (47, 10), key = "experimentName"),
					 sg.Button('?', key = "help_experimentName")],
					[sg.Text("Background color", size = (10,0)),
					 sg.InputText(default_text=str(CONFIG.prt_BackgroundColor), size = (15, 10), key = "prt_BackgroundColor"),
					 sg.Button(' ', key = "prt_BackgroundColor_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.prt_BackgroundColor))),
					 sg.Text("Text color"),
					 sg.InputText(default_text=str(CONFIG.prt_textcolor), size = (15, 10), key = "prt_textcolor"),
					 sg.Button(' ', key = "prt_textcolor_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.prt_textcolor)))
					],
					[sg.Text("Time course color", size = (10,0)),
					 sg.InputText(default_text=str(CONFIG.prt_timecoursecolor), size = (15, 10), key = "prt_timecoursecolor"),
					 sg.Button(' ', key = "prt_timecoursecolor_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.prt_timecoursecolor))),
					 sg.Text("Reference function color", size=(7,0)),
					 sg.InputText(default_text=str(CONFIG.prt_referencefunccolor), size = (15, 10), key = "prt_referencefunccolor"),
					 sg.Button(' ', key = "prt_referencefunccolor_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.prt_referencefunccolor)))
					],
					[sg.Text("Time course thickness", size = (10,0)),
					 sg.Slider(range=(1, 5), resolution=1, orientation='h', size=(37, 10), default_value=CONFIG.prt_timecoursethick, key='prt_timecoursethick'), 
					 sg.Button('?', key = "help_prt_timecoursethick")
					],
					[sg.Text("Reference function thickness", size = (10,0)),
					 sg.Slider(range=(1, 5), resolution=1, orientation='h', size=(37, 10), default_value=CONFIG.prt_referencefuncthick, key='prt_referencefuncthick'), 
					 sg.Button('?', key = "help_prt_referencefuncthick")
					]
						   ]
						   
	Protocol2_Settings_layout = [
					[sg.Text("Main loop colors")],
					[sg.Text("Planning phase", size = (11,0)),
					 sg.InputText(default_text=str(CONFIG.prt_phase1ColorString), size = (15, 10), key = "prt_phase1ColorString"),
					 sg.Button(' ', key = "prt_phase1ColorString_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.prt_phase1ColorString))),
					 sg.Text("BEFORE", size=(11,0)),
					 sg.InputText(default_text=str(CONFIG.prt_phase2ColorString), size = (15, 10), key = "prt_phase2ColorString"),
					 sg.Button(' ', key = "prt_phase2ColorString_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.prt_phase2ColorString)))
					],
					[sg.Text("AFTER", size = (11,0)),
					 sg.InputText(default_text=str(CONFIG.prt_phase3ColorString), size = (15, 10), key = "prt_phase3ColorString"),
					 sg.Button(' ', key = "prt_phase3ColorString_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.prt_phase3ColorString))),
					 sg.Text("ERROR", size=(11,0)),
					 sg.InputText(default_text=str(CONFIG.prt_phase4ColorString), size = (15, 10), key = "prt_phase4ColorString"),
					 sg.Button(' ', key = "prt_phase4colorString_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.prt_phase4ColorString)))
					],
					[sg.Text("MIDDLE WORD", size = (11,0)),
					 sg.InputText(default_text=str(CONFIG.prt_phase5ColorString), size = (15, 10), key = "prt_phase5ColorString"),
					 sg.Button(' ', key = "prt_phase5ColorString_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.prt_phase5ColorString))),
					 sg.Text("PREDICT", size=(11,0)),
					 sg.InputText(default_text=str(CONFIG.prt_phase6ColorString), size = (15, 10), key = "prt_phase6ColorString"),
					 sg.Button(' ', key = "prt_phase6ColorString_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.prt_phase6ColorString)))
					],
					[sg.Text("Prediction loop colors")],
					[sg.Text("Planning phase", size = (11,0)),
					 sg.InputText(default_text=str(CONFIG.pred_prt_phase1ColorString), size = (15, 10), key = "pred_prt_phase1ColorString"),
					 sg.Button(' ', key = "pred_prt_phase1ColorString_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.pred_prt_phase1ColorString))),
					 sg.Text("PREDICTION 1", size=(11,0)),
					 sg.InputText(default_text=str(CONFIG.pred_prt_phase2ColorString), size = (15, 10), key = "pred_prt_phase2ColorString"),
					 sg.Button(' ', key = "pred_prt_phase2ColorString_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.pred_prt_phase2ColorString)))
					],
					[sg.Text("PREDICTION 2", size = (11,0)),
					 sg.InputText(default_text=str(CONFIG.pred_prt_phase3ColorString), size = (15, 10), key = "pred_prt_phase3ColorString"),
					 sg.Button(' ', key = "pred_prt_phase3ColorString_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.pred_prt_phase3ColorString))),
					 sg.Text("PREDICTION 3", size=(11,0)),
					 sg.InputText(default_text=str(CONFIG.pred_prt_phase4ColorString), size = (15, 10), key = "pred_prt_phase4ColorString"),
					 sg.Button(' ', key = "pred_prt_phase4colorString_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.pred_prt_phase4ColorString)))
					],
					[sg.Text("BACK", size = (11,0)),
					 sg.InputText(default_text=str(CONFIG.pred_prt_phase5ColorString), size = (15, 10), key = "pred_prt_phase5ColorString"),
					 sg.Button(' ', key = "pred_prt_phase5ColorString_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.pred_prt_phase5ColorString))),
					 sg.Text("REROLL", size=(11,0)),
					 sg.InputText(default_text=str(CONFIG.pred_prt_phase6ColorString), size = (15, 10), key = "pred_prt_phase6ColorString"),
					 sg.Button(' ', key = "pred_prt_phase6ColorString_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.pred_prt_phase6ColorString)))
					],
					[sg.Text("Timeout colors")],
					[sg.Text("RETURN", size = (11,0)),
					 sg.InputText(default_text=str(CONFIG.returnColorString), size = (15, 10), key = "returnColorString"),
					 sg.Button(' ', key = "returnColorString_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.returnColorString))),
					 sg.Text("NEW SENTENCE", size=(11,0)),
					 sg.InputText(default_text=str(CONFIG.newsentenceColorString), size = (15, 10), key = "newsentenceColorString"),
					 sg.Button(' ', key = "newsentenceColorString_Pickers", button_color=('#000000', '#'+rgb_to_hex(CONFIG.newsentenceColorString)))
					],
						   ]
						   
	## Bring layouts together
	layout = [[sg.TabGroup(
				[[sg.Tab('Screen', Screen_Settings_layout), 
				  sg.Tab('GPT-3', GPT3_Settings_layout), 
				  sg.Tab('Misc', Misc_Settings_layout), 
				  sg.Tab('Turbo-Satori', TurboSatori_Settings_layout),
				  sg.Tab('Protocol 1', Protocol_Settings_layout),
				  sg.Tab('Protocol 2', Protocol2_Settings_layout),
				  sg.Tab('Fonts', Font_Settings_layout),
				  sg.Tab('Startup', Intro_Settings_layout),
				  sg.Tab('Timings', Timings_layout)]], key='tabgroup')],
				[sg.Button('Save'), sg.Button('Restore defaults'), sg.Button('Quit')]]
	
	## Create the window
	window = sg.Window('Sentence Speller Config', layout,  icon='config/icon1.ico', finalize = True)
	
	## Switch tab
	if tab == "protocol":
		window['tabgroup'].Widget.select(4)
	if tab == "protocol2":
		window['tabgroup'].Widget.select(5)
	
	## Event loop
	while True:
	
		event, values = window.read()
		
		## QUIT
		if event == sg.WINDOW_CLOSED or event == 'Quit': break
		
		## HELP
		if event == "help_localizer_lasttrial_duration":
			sg.popup('Duration of the last REST trial of the localizer in whole seconds.', title = "Help")
		if event == "help_training":
			sg.popup('Tick this box to enable a combined instructed encoding run & interface training at startup.\n\nIt will run after the tutorial, localizer & threshold if they are enabled.', title = "Help")
		if event == "help_progressbar":
			sg.popup('Tick this box to display progress bars at the bottom of the screen.', title = "Help")
		if event == "help_indicator":
			sg.popup('Tick this box to display a small indicator on the progress bar that tells the user when to start doing the mental activity.', title = "Help")	
		if event == "help_indicatorPos":
			sg.popup('Sets where the indicator will be drawn. Value is the distance between the indicator and the right edge of the progress bar.', title = "Help")		
		if event == "help_localizer_duration1":
			sg.popup('Duration of each TASK condition during the localizer run, in whole seconds.', title = "Help")
		if event == "help_localizer_duration2":
			sg.popup('Duration of each REST condition during the localizer run, in whole seconds.', title = "Help")
		if event == "help_localizer_repetitions":
			sg.popup('How many times each condition is ran through during the localizer.\n\nA value of 1 means the run will contain one TASK condition and one REST condition.', title = "Help")
		if event == "help_tutorial":
			sg.popup('Tick this box to run through participant information on the mental task on startup.', title = "Help")
		if event == "help_localizer":
			sg.popup('Tick this box to perform a localizer run on startup.\n\nIf tutorial is also on, the localizer will run after the tutorial.', title = "Help")
		if event == "help_thresholdOn":
			sg.popup('Tick this box to perform threshold detection on startup.\n\nWill run after the tutorial and localizer if they are set to on.', title = "Help")
		if event == "help_FPS":
			sg.popup('This option limits the framerate at which the program runs.\n\nShould be set equal or higher than the fNIRS sampling rate.', title = "Help")
		if event == "help_model":
			sg.popup('Selects which GPT-3 model will be used for predictions.\n\nDavinci gives the best predictions, but costs the most money and takes the most processing time.\n\nAda is the cheapest both in terms of money and processing time, but gives hit & miss predictions.\n\nI haven\'t tested Babbage or Curie yet.\n\nSee beta.openai.com/docs/engines for more info.', title = "Help")
		if event == "help_temperature":
			sg.popup('How \"creative\" the AI gets with its output.\n\nSetting this too low results in repetitive output.\n\nSetting this too high results in nonsense.', title = "Help")
		if event == "help_length":
			sg.popup('Length of the generated text in tokens. One token roughly equals four letters.\n\nSee beta.openai.com/docs/ for more information.\n\nThree predictions are generated, one with this length, one with length + 1, one with length +2.', title = "Help")
		if event == "help_apiKey":
			sg.popup('My access key for the GPT-3 Beta.\n\nDO NOT ALTER.\nPredictions will stop working if you change the key.\n\nDO NOT GIVE TO ANYONE ELSE.\nIf I lose my beta access because someone misuses my key, I\'ll be quite irate.', title = "Help")
		if event == "help_debug":
			sg.popup('Toggles debug information (FPS, raw fNIRS values, Turbo-Satori connection) on or off.', title = "Help")
		if event == "help_input":
			sg.popup('Which input method(s) to use.\n\nCAUTION:\n\"fNIRS only\" currently has a bug that causes the program to crash if it\'s also in windowed mode and the window is moved or clicked outside of.', title = "Help")
		if event == "help_tts":
			sg.popup('Toggles Text-To-Speech on or off.\n\nCAUTION:\nTTS causes performance issues.', title = "Help")
		if event == "help_ttsVoices":
			sg.popup('Which voice to use for TTS.\n\nShould detect all SAPI5 voices installed on your system.', title = "Help")
		if event == "help_dict":
			sg.popup('Which dictionary file to use for binary search.\n\nCan be any .txt file that separates words with line breaks.', title = "Help")
		if event == "help_datafolder":
			sg.popup('Folder that contains the experiment\'s neurofeedback data points.\n\nIf configured to do so, Turbo-Satori will create a folder called \"NeurofeedbackValues\" in the same location that the .hdr file of your experiment is in. Use that one.', title = "Help")
		if event == "help_thermometer":
			sg.popup('Toggles a neurofeedback-style thermometer displaying the ratio of current activation to threshold for command selection.\n\nCorresponds 1:1 to Turbo-Satori\'s default neurofeedback thermometer if threshold is set to 10.', title = "Help")
		if event == "help_datarate":
			sg.popup('Data points from Turbo-Satori are read in every x frames. Set x here.', title = "Help")
		if event == "help_nfmode":
			sg.popup('Which values to use for activation.\n\n\"Average\" sums up the most recent data points for oxy and deoxy, then divides them by two.', title = "Help")
		if event == "help_font":
			sg.popup('Which font to use. Don\'t use Comic Sans.', title = "Help")
		if event == "help_fontscale":
			sg.popup('Scale up text by a factor of x.\n\nUse this if you\'re running in fullscreen mode on a large screen and the text is too small.', title = "Help")
		if event == "help_threshold":
			sg.popup('Activation value at which commands are triggered.\n\nWhich values count for this are set by Mode.', title = "Help")			
		if event == "help_timings":
			sg.popup('Sets the duration (in whole seconds) for each control phase.\n\n\"Initial delay\" controls how long the middle word (or prediction list) is shown without any control elements before the trial starts.\n\n\"Phase 1\" already shows the control elements, but does not highlight anything yet for main. For predictions, it\'s the duration of the first control element.\n\n\"End\" controls how long the main loop lingers on the middle word, or how long the prediction loop waits before restarting after timing out.\n\nThe phases inbetween control how quickly the program cycles through the control elements.', title = "Help")
		if event == "help_experimentName":
			sg.popup('Name of the experiment used by Turbo-Satori.', title = "Help")
		if event == "help_thermometer_during_planning":
			sg.popup('Sets whether the thermometer is shown during the planning phase.\n\nIf off, the thermometer will only be shown once BEFORE is highlighted.', title = "Help")
		if event == "help_prt_timecoursethick":
			sg.popup('Thickness of the time course line in Turbo-Satori.', title = "Help")
		if event == "help_prt_referencefuncthick":
			sg.popup('Thickness of the reference function line in Turbo-Satori.', title = "Help")		
		if event == "help_prediction":
			sg.popup('Toggles predictions on or off.\n\nIf off, the PREDICT command will be hidden during the run.', title = "Help")
		if event == "help_reroll":
			sg.popup('Sometimes GPT-3 generates multiple predictions that are identical and thus not helpful to the user. To prevent this, the program checks for identical predictions and re-generates them if they occur.\n\nUnfortunately, this rerolling process has a slight risk of ending in an infinite loop (if GPT-3 insists on generating identical predictions over and over). To prevent this case, the program stops trying to reroll predictions after XX attempts. Set XX here.', title = "Help")
		if event == "help_maxIter":
			sg.popup('If there are X iterations of the main loop without any user input, the speller will go into time-out mode.\nIn time-out mode, the user can select RETURN (returning them to the main loop) or NEW SENTENCE (restarting the main loop and discarding the current output string). Set X here.', title = "Help")		
   
		## COLOR PICKER

		if event == "prt_BackgroundColor_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","prt_BackgroundColor",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol")
			
		if event == "prt_textcolor_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","prt_textcolor",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol")
			
		if event == "prt_timecoursecolor_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","prt_timecoursecolor",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol")		
		
		if event == "prt_referencefunccolor_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","prt_referencefunccolor",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol")	

		if event == "prt_phase1ColorString_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","prt_phase1ColorString",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol2")	

		if event == "prt_phase2ColorString_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","prt_phase2ColorString",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol2")	

		if event == "prt_phase3ColorString_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","prt_phase3ColorString",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol2")	

		if event == "prt_phase4colorString_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","prt_phase4ColorString",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol2")	

		if event == "prt_phase5ColorString_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","prt_phase5ColorString",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol2")	

		if event == "prt_phase6ColorString_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","prt_phase6ColorString",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol2")	

		if event == "pred_prt_phase1ColorString_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","pred_prt_phase1ColorString",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol2")	

		if event == "pred_prt_phase2ColorString_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","pred_prt_phase2ColorString",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol2")	

		if event == "pred_prt_phase3ColorString_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","pred_prt_phase3ColorString",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol2")	

		if event == "pred_prt_phase4colorString_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","pred_prt_phase4ColorString",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol2")	

		if event == "pred_prt_phase5ColorString_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","pred_prt_phase5ColorString",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol2")	

		if event == "pred_prt_phase6ColorString_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","pred_prt_phase6ColorString",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol2")	
				
		if event == "returnColorString_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","returnColorString",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol2")					

		if event == "newsentenceColorString_Pickers":
			color_chosen = color_chooser()
			if color_chosen != None:
				h = color_chosen.lstrip('#')
				rgb_h = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
				CONFIG.set("TURBO-SATORI SETTINGS","newsentenceColorString",str(rgb_h))
				with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
				initConfig("config\config.ini")
				window.close()
				showWindow(tab="protocol2")		

		## RESET
		if event == "Restore defaults":
			initConfig("config\defaults.ini")
			window.close()
			showWindow()
		
		## SAVE
		if event == 'Save':
			# Screen mode
			if values[0]   == "Fullscreen"  : CONFIG.set("WINDOW_SETTINGS","fullscreen","True")
			elif values[0] == "Windowed"	: CONFIG.set("WINDOW_SETTINGS","fullscreen","False")
			# FPS limit
			CONFIG.set("WINDOW_SETTINGS","fps_target",str(int(values[1])))
			# GPT 3 Model
			CONFIG.set("GPT-3 SETTINGS","model",values[2])
			# Predictions
			CONFIG.set("GPT-3 SETTINGS","predictions_on",str(values["predictions"]))			
			# GPT 3 Temp
			CONFIG.set("GPT-3 SETTINGS","temperature",str(values[3]))
			# GPT 3 Length
			CONFIG.set("GPT-3 SETTINGS","length",str(int(values[4])))
			# API Key
			CONFIG.set("GPT-3 SETTINGS","api_key",str(values[5]))
			# Max rerolls
			CONFIG.set("GPT-3 SETTINGS", "max_reroll",str(int(values["max_reroll"])))
			# Debug
			CONFIG.set("MISC","debug_on",str(values[6]))
			# Input method
			if values[7] == "Keyboard only": CONFIG.set("MISC","input_type","KB")
			elif values[7] == "fNIRS only": CONFIG.set("MISC","input_type","NF")
			elif values[7] == "Keyboard + fNIRS": CONFIG.set("MISC","input_type","BOTH")
			# TTS
			CONFIG.set("MISC","text_to_speech",str(values[8]))
			# TTS Voice
			CONFIG.set("MISC","tts_voice",str(CONFIG.voiceList.index(values[9])))
			# Dictionary file
			CONFIG.set("MISC","dictionary",str(values[10]))
			# TSI Data folder
			CONFIG.set("TURBO-SATORI SETTINGS","data_folder",str(values[11]))
			# Thermometer
			CONFIG.set("TURBO-SATORI SETTINGS","thermo_on",str(values[12]))
			# Thermo during planning
			CONFIG.set("TURBO-SATORI SETTINGS", "thermo_during_planning", str(values["thermo_during_planning"]))
			# Data read rate
			CONFIG.set("TURBO-SATORI SETTINGS","nf_reader_frequency",str(int(values[13])))
			# Data mode
			if values[14] == "Oxy": CONFIG.set("TURBO-SATORI SETTINGS","nf_mode","oxy")
			elif values[14] == "Deoxy": CONFIG.set("TURBO-SATORI SETTINGS","nf_mode","deoxy")
			elif values[14] == "Average": CONFIG.set("TURBO-SATORI SETTINGS","nf_mode","avg")
			# Threshold
			CONFIG.set("TURBO-SATORI SETTINGS","NF_threshold",str(int(values["act_thresh"])))
			# Font
			CONFIG.set("FONTS","font",str(values[15]))
			# Font scale
			CONFIG.set("FONTS","smallest",str(int(values["fontScale"]*CONFIG.SMALLEST_FONT)))
			CONFIG.set("FONTS","small",str(int(values["fontScale"]*CONFIG.SMALL_FONT)))
			CONFIG.set("FONTS","std",str(int(values["fontScale"]*CONFIG.STD_FONT)))
			# Timings
			CONFIG.set("TIMINGS","initialDelay",values["initial_main"])
			CONFIG.set("TIMINGS","firstPhase",values["1_main"])
			CONFIG.set("TIMINGS","secondPhase",values["2_main"])
			CONFIG.set("TIMINGS","thirdPhase",values["3_main"])
			CONFIG.set("TIMINGS","fourthPhase",values["4_main"])
			CONFIG.set("TIMINGS","fifthPhase",values["5_main"])
			CONFIG.set("TIMINGS","endPhase",values["end_main"])
			CONFIG.set("TIMINGS","pred_initialDelay",values["initial_pred"])
			CONFIG.set("TIMINGS","pred_firstPhase",values["1_pred"])
			CONFIG.set("TIMINGS","pred_secondPhase",values["2_pred"])
			CONFIG.set("TIMINGS","pred_thirdPhase",values["3_pred"])
			CONFIG.set("TIMINGS","pred_fourthPhase",values["4_pred"])
			CONFIG.set("TIMINGS","pred_fifthPhase",values["5_pred"])
			CONFIG.set("TIMINGS","pred_endPhase",values["end_pred"])
			# Protocol
			CONFIG.set("TURBO-SATORI SETTINGS","experiment_name",values["experimentName"])
			CONFIG.set("TURBO-SATORI SETTINGS","prt_timecoursethick",str(int(values["prt_timecoursethick"])))
			CONFIG.set("TURBO-SATORI SETTINGS","prt_referencefuncthick",str(int(values["prt_referencefuncthick"])))
			# Startup stuff
			CONFIG.set("TURBO-SATORI SETTINGS","tutorial",str(values["tutorial_on"]))
			CONFIG.set("TURBO-SATORI SETTINGS","threshold",str(values["threshold_on"]))
			CONFIG.set("TURBO-SATORI SETTINGS","localizer",str(values["localizer_on"]))
			CONFIG.set("TURBO-SATORI SETTINGS","training",str(values["training_on"]))
			CONFIG.set("TURBO-SATORI SETTINGS","localizer_task_duration",str(int(values["localizer_task_duration"])))
			CONFIG.set("TURBO-SATORI SETTINGS","localizer_rest_duration",str(int(values["localizer_rest_duration"])))
			CONFIG.set("TURBO-SATORI SETTINGS","localizerrepetitions",str(int(values["localizer_repetitions"])))
			CONFIG.set("MISC","timeout_iterlimit",str(int(values["maxIter"])))
			CONFIG.set("TURBO-SATORI SETTINGS", "localizer_lasttrial_duration", str(int(values["localizer_lasttrial_duration"])))
			# Misc stuff
			CONFIG.set("TURBO-SATORI SETTINGS","progressbar",str(values["progressbar_on"]))
			CONFIG.set("MISC","indicator",str(values["indicator"]))
			CONFIG.set("MISC","indicatorPos",str(int(values["indicatorPos"])))
			
			with open('config/config.ini', 'w') as configfile: CONFIG.write(configfile)
			
			sg.popup('Settings saved!', title = "")
			
			
	## Close window when done
	window.close()

## RUNTIME
if __name__ == '__main__':
	initConfig("config\config.ini")
	showWindow()