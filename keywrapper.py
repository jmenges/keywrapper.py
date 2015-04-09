#!/usr/bin/python
# author: Jonas Menges(dev.menges.jonas@gmail.com)
# at the moment this script only handles mp3 and flac

import os, sys
import subprocess
from mutagen.flac import FLAC as FLAC
import mutagen.id3 

def QuoteForPOSIX(string):
    '''quote a string so it can be used as an argument in a  posix shell

       According to: http://www.unix.org/single_unix_specification/
          2.2.1 Escape Character (Backslash)

          A backslash that is not quoted shall preserve the literal value
          of the following character, with the exception of a <newline>.

          2.2.2 Single-Quotes

          Enclosing characters in single-quotes ( '' ) shall preserve
          the literal value of each character within the single-quotes.
          A single-quote cannot occur within single-quotes.

    '''

    return "\\'".join("'" + p + "'" for p in string.split("'"))

path = str(sys.argv[1])
if not os.path.isdir(path):
   sys.exit(0)

fail = False
fStr = ""

for dirpath, dirnames, files in os.walk(path):
      print("Active Directory: " + dirpath)
      if files:
         os.chdir(dirpath)
         for fn in files:
            ext = os.path.splitext(fn)[1]
            if ext == ".flac":
               try:
                  print("Processing FLAC: ", fn);
                  flac = FLAC(fn)
               except:
                  print("Processing failed")
                  continue
            elif ext == ".mp3":
               try:
                  print("Processing MP3: ", fn);
                  mp3 = mutagen.id3.ID3(fn)
               except:
                  print("Processing failed")
                  continue 
            else:
               print("Skipping File. File extension not supported: " + ext)  
               continue
            try:
               args = "-n camelot " + QuoteForPOSIX(fn)
               output = subprocess.check_output("keyfinder-cli " + args, shell=True);
               key = output.strip().decode('ascii')
               print("NewKey: " + key)
               if ext == ".flac":    
                  try:              
                     flac['key'] = key
                     flac.save()
                  except:          
                     print("FLAC keysave failed")
               elif ext == ".mp3":
                  try:          
                     frame = mutagen.id3.TKEY(encoding=3, text=key)
                     mp3.add(frame)
                     mp3.save()
                  except:        
                     print("Frame: " + frame)
                     print("Mp3 keysave failed")

            except:
               if fail:
                  fStr = fStr + fn + "\n"
               else:     
                  fail = True
                  fStr = fn + "\n"
if fail:
      print("There was an error with the following track/s:", fStr)
