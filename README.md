# keywrapper.py
This is a small python wrapper for the keyfinder-cli created by Evan Purkhiser (https://github.com/EvanPurkhiser/keyfinder-cli), which is another wrapper for the libKeyfinder (https://github.com/ibsh/libKeyFinder/) library Ibrahim Sha'ath.

I created it to automate my usage of keyfinder-cli.
It loops over all files/subfolders of the path specified as an argument, uses keyfinder-cli to find the camelotkey value and than writes it to either the id3 tag (for mp3s) or to the vorbis tag (for flac).
It only handles flac and mp3 files at the moment.

