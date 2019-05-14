# jazz-ify

Developed by Lucie le Blanc and Julio Melchor
Designed by Madelyn Baker and Ryan Daar

### Setup
The following instructions are for any UNIX-style terminal. First, make sure python3 is installed. Create and start a virtualenv:
```
$ virtualenv venv
$ venv/bin/activate
```
Then `pip install` the dependencies `pygame`, `numpy` and `scipi`.


### Run
To run the program, enter the command: 
```
python3 chord_parser.py
```

This program accepts input in the following format:
`(note1 note2 note3)-(note4 note5 note6)-(note7 note8 note9)`
* "note1" should be a letter (A through G). For accidentals, append # or b to the letter. 
* Each set of parentheses should contain a triad. So far, our program accepts root position only.
* Output will be in the same format! Each run will randomly embellish the original triads. 

To hear the notes being played, make sure sound is turned on. Different operating systems and terminals might have different sound capabilities.

### Example

Song: "Call Me Maybe" by Carly Rae Jepsen
key of: `G`
input: `(G B D)-(E G B)-(E G B)-(D F# A)`
