#!/usr/bin/env python
# coding: utf-8


import copy
import math
import random
import string
from play_chord import init
from play_chord import play_notes

random.seed()
global_mode = ''

class Note:
    def __init__(self, note, octave):
        if type(note) is str:
            self.letter = note
            self.pitch = letterToNum(note)
        else:
            self.pitch = note
            self.letter = numToLetter(note, global_mode)
        self.octave = octave
        
    def transpose(self, steps, octs=0):
        self.pitch = self.pitch + steps
        
        self.octave += math.floor(steps / 12)
        # if (self.pitch < 0):
        #     self.octave -= 1
        # elif (self.pitch > 11):
        #     self.octave += 1

        self.octave += octs
        self.pitch %= 12
        self.letter = numToLetter(self.pitch, global_mode)


def letterToNum(letter):
    base = letter[0].upper()
    num = 0
    
    # translate main pitch name
    num = (ord(base) - ord('C')) * 2
    
    # accout for A/B "wrap"
    if (ord(base) < ord('C')):
        num += 2
    
    # account for single half-step between E and F
    if (ord(base) >= ord('F') or ord(base) < ord('C')):
        num -= 1
    
    # add sharp or flat
    if (len(letter) > 1):
        if (letter[1] is 'b'):
            num -= 1
        elif (letter[1] is '#'):
            num += 1
    
    # keep within 12-tone range
    return num % 12


def numToLetter(num, mode):
    
    # re-account for A/B "wrap"
    num = num % 12

    # base conversion
    offset = math.floor(num / 2)
    
    # account for half-step between E and F
    if (num > 4):
        offset += 1
    baseOrd = ord('C') + offset
    
    # accidentals
    accidental = ''
    if ((num % 2 is 1) and (num < 4)):
        if (mode is '#'):
            accidental = '#'
        else:
            baseOrd += 1
            accidental = 'b'
            
    elif ((num % 2 is 0) and (num > 5)):
        if (mode is '#'):
            baseOrd -= 1
            accidental = '#'
        else:
            accidental = 'b'
        
    # re-account for A/B "wrap"
    if (baseOrd > ord('G')):
        baseOrd -= (ord('H') - ord('A'))
    
    return chr(baseOrd) + accidental


def getRoleNum(note, tonic):

	pitch = note
	if type(note) is str:
		pitch = letterToNum(note)

	base = tonic
	if type(tonic) is str:
		base = letterToNum(tonic)

	return (pitch - base) % 12


def getRoleLetter(note, tonic):
	num = getRoleNum(note, tonic)
	interval = ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'TT', 'P5', 'm6', 'M6', 'm7', 'M7']
	return interval[num]


def printChord(notes):
	chord_string = '('
	for item in notes:
		chord_string += (item.letter + str(item.octave) + " ")
	chord_string = chord_string[0:-1] + ')'
	print(chord_string)


def parseChord(text):
    text = text[(text.index('(') + 1) : text.index(')')]
    
    notes = []
    octave = 3
    
    for itemLetter in text.split():
        itemNum = letterToNum(itemLetter)
        
        # account for octave change
        if (len(notes) > 0 and itemLetter < numToLetter(notes[-1].pitch, global_mode)):
            octave += 1
            
        notes.append(Note(itemNum, octave))
    return notes
    

def getTriadQuality(chord_notes):

	pitch_only = []
	root = chord_notes[0]
	for note in chord_notes:
		pitch_only.append((note.pitch - root.pitch) % 12)

	if (len(pitch_only) < 3):
		return ""

	pitch_base = pitch_only[0:3]

	if (pitch_base == [0, 4, 7]):
		return "M"

	if (pitch_base == [0, 3, 7]):
		return "m"

	if (pitch_base == [0, 4, 8]):
		return "+"

	if (pitch_base == [0, 3, 6]):
		return "°"

	return ""


def embellish(note_list, key):
	quality = getTriadQuality(note_list)
	root = note_list[0]
	role = getRoleNum(root.pitch, key)

	new_tones = []

	if (quality is 'M'):

		print("Major")

		if (role is 0): # I chord
			new_tones += [11, 14, 18, 21] # add M7, M9 (2), TTup, M13 (6)

		elif (role is 5): # IV chord
			new_tones += [10, 14, 18, 21] # add m7, M9 (2), TTup, M13 (6), 

		elif (role is 7): # V chord
			new_tones += [10, 14, 18, 21] # add m7, M9 (2), TTup, M13 (6) 

	elif (quality is 'm'):

		print("minor")

		if (role is 0): # vi chord
			new_tones += [10, 14, 17, 21] # add m7, M9 (2), M11 (4), M13 (6)
		
	pitch_index = 0
	while (round(random.random()) and pitch_index < len(new_tones)):
		add1 = Note(root.pitch, root.octave + 1)
		add1.transpose(new_tones[pitch_index], 0)
		note_list.append(add1)
		pitch_index += 1

	return note_list


# result = parseChord('(G B D)')
# printChord(result)
# printChord(embellish(result, 'G'))

def main():
    print("Welcome!\n")
    song_key = input("Please enter song key: ")
    print("Your song will be in the key of " + song_key + ".\n")
    sharp_keys = ['G', 'D', 'A', 'E', 'B']
    flat_keys = ['F']
    if ("b" in song_key):
    	mode = 'b'
    elif ("#" in song_key):
    	mode = '#'
    elif (song_key in flat_keys):
    	mode = 'b'
    elif (song_key in sharp_keys):
    	mode = '#'

    print("This program accepts root position triads in the following format:")
    print("(note1 note2 note3)-(note4 note5 note6)-(note7 note8 note9)\n")
    
    ins = input("Enter song chords: ")
    array_of_chord = ins.split("-")
    print(array_of_chord)
    result = []
    for idx in array_of_chord:
        result.append(embellish(parseChord(idx), song_key))

    #getQuality of each chord
    # print(result)

    quality = []
    for i in result:
        quality.append(getTriadQuality(i))

    for i in result:
        printChord(i)
    
    init()

    #for chord in chords:
    play_notes("C,E,G:.4 C,E,G:.4 C,E,G:.4 C,E,G:.4 C,E,G:.4 C,E,G:.4 C,E,G:.4 C,E,G:.4 C,E,G:.4 C,E,G:.4 ")

    play_notes("F,A,C,F:3 C,E,G:1 G,B,G:.3 G,B,G:2 E,A,C:1 F,A,C,F:.3 F,A,C,F:2 C,E,G:1 G,B,G:.4 G,B,G:2")
    play_notes("F,A,C,F:3 C,E,G:1 G,B,G:.3 G,B,G:2 E,A,C:1 F,A,C,F:.3 F,A,C,F:2 C,E,G:1 G,B,G:.4 G,B,G:2")
    play_notes("F,A,C,F:3 C,E,G:1 G,B,G:.3 G,B,G:2 E,A,C:1 F,A,C,F:.3 F,A,C,F:2 C,E,G:1 G,B,G:.4 G,B,G:2")

if __name__ == "__main__":
    main()
