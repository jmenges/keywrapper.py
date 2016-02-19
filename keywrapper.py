#!/usr/bin/python
# author: Jonas Menges(dev.menges.jonas@gmail.com)
# at the moment this script only handles mp3 and flac

import os, sys
import subprocess
from mutagen.flac import FLAC as FLAC
import mutagen.id3 
import mutagen.aiff

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
            elif ext == ".aif":
               try:
                  print("Processing AIF: ", fn);
                  aif = mutagen.aiff.AIFF(fn)
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
               key = "01A" if key == "1A" else key
               key = "01B" if key == "1B" else key
               key = "02A" if key == "2A" else key
               key = "02B" if key == "2B" else key
               key = "03A" if key == "3A" else key
               key = "03B" if key == "3B" else key
               key = "04A" if key == "4A" else key
               key = "04B" if key == "4B" else key
               key = "05A" if key == "5A" else key
               key = "05B" if key == "5B" else key
               key = "06A" if key == "6A" else key
               key = "06B" if key == "6B" else key
               key = "07A" if key == "7A" else key
               key = "07B" if key == "7B" else key
               key = "08A" if key == "8A" else key
               key = "08B" if key == "8B" else key
               key = "09A" if key == "9A" else key
               key = "09B" if key == "9B" else key


               print("NewKey: " + key)
               if ext == ".flac":    
                  try:              
                     flac['comment'] = key
                     flac.save()
                  except:          
                     print("FLAC keysave failed")
               elif ext == ".aif":
                  try:          
                     frame = mutagen.id3.COMM(encoding=3, lang="eng", desc="", text=key)
                     aif.tags.delall('COMM');
                     aif.tags.add(frame);
                     aif.save()
                  except:        
                     print("Frame: " + frame)
                     print("AIFF keysave failed")
               elif ext == ".mp3":
                  try:          
                     frame = mutagen.id3.COMM(encoding=3, lang="eng", desc="", text=key)
                     mp3.delall('COMM');
                     mp3.add(frame)
                     mp3.save()
                  except:        
                     print("Frame: " + frame)
                     print("MP3 keysave failed")

            except:
               if fail:
                  fStr = fStr + fn + "\n"
               else:     
                  fail = True
                  fStr = fn + "\n"
if fail:
      print("There was an error with the following track/s:", fStr)
