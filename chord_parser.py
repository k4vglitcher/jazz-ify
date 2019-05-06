#!/usr/bin/env python
# coding: utf-8

# In[5]:


import math
import string


# In[49]:


class Note:
    def __init__(self, note, octave):
        if type(note) is 'str':
            self.letter = note
            self.pitch = letterToNum(note)
        else:
            self.pitch = note
            self.letter = numToLetter(note, '')
        self.octave = octave
        
    def transpose(self, steps, octs):
        self.pitch = self.pitch + steps
        
        if (self.pitch < 0):
            self.octave -= 1
        elif (self.pitch > 11):
            self.octave += 1
        
        self.octave += octs
        self.pitch %= 12


# In[25]:


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
        


# In[26]:


print(letterToNum('A'))


# In[27]:


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


# In[28]:


for i in range(13):
    print(numToLetter(i, 'b'))


# In[29]:


def getRoleNum(note, tonic):
    return (letterToNum(note) - letterToNum(tonic)) % 12


# In[30]:


print(getRoleNum('C', 'C'), getRoleNum('C', 'A'), getRoleNum('A', 'C'))


# In[31]:


def getRoleLetter(note, tonic):
    num = getRoleNum(note, tonic)
    interval = ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'TT', 'P5', 'm6', 'M6', 'm7', 'M7']
    return interval[num]


# In[32]:


print(getRoleLetter('C', 'C'), getRoleLetter('C', 'A'), getRoleLetter('A', 'C'))


# In[43]:


def parseChord(text):
    text = text[(text.index('(') + 1) : text.index(')')]
    print(text)
    
    notes = []
    octave = 3
    
    for itemLetter in text.split():
        itemNum = letterToNum(itemLetter)
        
        # account for octave change
        if (len(notes) > 0 and itemLetter < numToLetter(notes[-1].pitch, '')):
            octave += 1
            
        notes.append(Note(itemNum, octave))
    return notes
    


# In[54]:


result = parseChord('(C E G Bb C)')
for item in result:
    print("Note object")
    print("pitch: ", item.pitch)
    print("letter: ", item.letter)
    print("octave: ", item.octave)
    print("")
 
print("(")
for item in result:
    print(item.letter)
print(")")


# In[ ]:




