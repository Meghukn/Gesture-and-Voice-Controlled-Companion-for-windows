import os
import eel
from backend.features import *
from backend.command import *
from backend.auth import recognize

def start():
  eel.init("frontend")

  playAssistantSound()
  @eel.expose
  def init():
    
    
    eel.hideLoader()
    speak("ready for face authentication")
    flag= recognize.AuthenticateFace()
    if flag==1:
      eel.hideFaceAuth()
      speak("Face authentication successful")
      eel.hideFaceAuthSuccess()
      speak("Hello")
      eel.hideStart()
      playAssistantSound()
    else:
      speak("face authentication fail")

  os.system('start msedge.exe --app="http://localhost:8000/index.html"')
  eel.start('index.html', mode=None, host='localhost', block=True)
