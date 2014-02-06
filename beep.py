# -*- coding: cp1252 -*-


#raise Exception (" --- ")


import winsound, time
#import ossaudiodev, wave, time
class BeepMusic:

    notes = {
        "Do":   (  65  ,  131  ,  262  ,  523 ),
        "Do#":  (  69  ,  139  ,  277  ,  554 ),
        "Re":   (  73  ,  147  ,  294  ,  587 ),
        "Re#":  (  78  ,  156  ,  311  ,  622 ),
        "Mi":   (  82  ,  165  ,  330  ,  659 ),
        "Fa":   (  87  ,  175  ,  349  ,  698 ),
        "Fa#":  (  92  ,  185  ,  370  ,  740 ),
        "Sol":  (  98  ,  196  ,  392  ,  784 ),
        "Sol#": ( 104  ,  208  ,  415  ,  830 ),
        "La":   ( 110  ,  220  ,  440  ,  880 ),
        "La#":  ( 117  ,  233  ,  466  ,  932 ),
        "Si":   ( 123  ,  247  ,  494  ,  988 ),
        "NN":   (   0  ,    0  ,    0  ,    0 )
     }

    temps = {
        "o."  : 6,
        "o"   : 4,
        "b."  : 3,
        "b"   : 2,
        "n."  : 1.5,
        "n"   : 1,
        "c."  : 0.75,
        "c"   : 0.5,
        "cc." : 0.375,
        "cc"  : 0.25,
        "ccc.": 0.1875,
        "ccc" : 0.125
    }
    _float60 = float(60)
    _comp = []
    def __init__(self, tempo=120):
        self.noteform = ["name", "octave", "duration", "effect"]
        self.tempo = tempo
    def flipNoteForm(self):
        if self.noteform == ["name", "octave", "duration", "effect"]:
            self.noteform = ["duration", "name", "octave", "effect"]
        else:
            self.noteform = ["name", "duration", "effect"]
    def getNoteFrequencyTupleIndex(self):
        if self.noteform[0] == "name":
            return 0
        elif self.noteform[1] == "name":
            return 1
        else:
            raise Exception("Error in note form (name)")

    def getNoteDurationTupleIndex(self):
        if self.noteform[0] == "duration":
            return 0
        elif self.noteform[2] == "duration":
            return 2
        else:
            raise Exception("Error in note form (duration)")

    def getNoteOctaveTupleIndex(self):
        if self.noteform[1] == "octave":
            return 1
        elif self.noteform[2] == "octave":
            return 2
        else:
            raise Exception("Error in note form (octave)")

    def noteLength (self, fraction):
        return int(round(( self._float60 / float(self.tempo) * fraction ) * 1000))

    def __call__(self, song, tempo=0):
        try:
            self.play(song, tempo)
        except KeyError:
            print "erreur de clés dans le morceau transmis"
            return

        self.playcomp()

    def play(self, song, tempo=0):
        self._comp = []
        self.tempo = tempo != 0 and tempo or self.tempo
        #song : [ (note name , octave , duration name), ]
        ifreq = self.getNoteFrequencyTupleIndex()
        itime = self.getNoteDurationTupleIndex()
        iocta = self.getNoteOctaveTupleIndex()
        if ifreq + itime + iocta != 3:
                raise Exception("Error in note form (duration == name) ... But this CANNOT Happen")
        for note in song:
            octave = note[iocta] - 1 # - 1 car pour le client le tuple octave commence à l'index 1
            frequency = self.notes[note[ifreq]][octave]
            duration = self.temps[note[itime]]
            duration = self.noteLength(duration)
            if len(note[3:]) == 0 : #no effect for this note
                self._comp.append( (frequency, duration) )
            else:
               self._comp.extend( self.applyEffect(frequency, duration, effect=note[3]))


    def playcomp(self):
        for (freq, dur) in self._comp:
            if not freq < 37 :
                winsound.Beep(freq, dur)
                #print (freq,dur)
 #               print winsound.Beep.__doc__
            else:
#                print time.sleep.__doc__
                time.sleep(dur / 1000)



    def applyEffect (self, frequency, duration, effect):
        print "on applique un effet " + effect
        return [(frequency, duration),]


    def __doc__(self):
        sep = 10
        print "Beep Music Module".upper()
        print "Notes prédéfinies:"
        print ("note".ljust(4) + ":").ljust(sep)+ "".join([("Octave %d" % i).ljust(sep) for i in [1,2,3,4]])
        print "\n".join([(("%s" % a).ljust(4) + ":").ljust(sep)
                     + ("%d" % b[0]).ljust(sep)  # b[0], b[1], b[2], b[3])
                     + ("%d" % b[1]).ljust(sep)
                     + ("%d" % b[2]).ljust(sep)
                     + ("%d" % b[3])
                     for a , b  in BeepMusic.notes.items()] )
        print
        print "Fractions de Temps prédéfinies"
        print " \tà tempo 120, 1 vaut 1/2 seconde (60 / tempo = beattime)(60 / 120 = 0.5)"

        print "\n".join([(("%s" % a).ljust(4) + ":").ljust(sep) + ("%.4f" % b) for a, b in BeepMusic.temps.items() ])

"""
frequency = 440
duration = 100
winsound.Beep(frequency, duration)
"""

if __name__ == "__main__":
    player = BeepMusic()
#    player.flipNoteForm()
    #print player.__doc__

    #song : [ (note name , octave , duration name), ]
    song1 = [
        ("Do", 3, "c"),
        ("Do", 3, "c"),
        ("Do", 3, "c"),
        ("Re", 3, "c"),
        ("Mi", 3, "n"),
        ("Re", 3, "n"),
        ("Do", 3, "c"),
        ("Mi", 3, "c"),
        ("Re", 3, "c"),
        ("Re", 3, "c"),
        ("Do", 3, "n", "fullbend")
        ]
    song2 = [
        ("Mi",3,"c"),
        ("Mi",3,"c"),
        ("Sol#",3,"c"),
        ("Si",3,"c"),
        ("Re",4,"c"),
        ("Re",4,"c"),
        ("Fa#",4,"c"),
        ("La",4,"c"),
        ("La",3,"c"),
        ("La",3,"c"),
        ("Do#",4,"c"),
        ("Mi",4,"c"),
        ("Si",3,"c"),
        ("Si",3,"c"),
        ("Fa#",4,"c"),
        ("Mi",4,"c"),
    ]
    player(song2, 130)

