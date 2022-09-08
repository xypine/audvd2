#!/usr/bin/env python3
v = 2.0

print("audvd v. " + str(v))
print("audvd written by Elias \"xypine\" Eskelinen <audvd@eliaseskelinen.fi>")

print("audvd importing libraries...")
import os
print("\tmoviepy...",end="")
from moviepy.editor import *
print("DONE")
print("\tsoundfile...",end="")
import soundfile as sf
print("DONE")

def getFiles(inp):
    import os
    filelist=os.listdir(inp)
    for fichier in filelist[:]: # filelist[:] makes a copy of filelist.
        if not(fichier.endswith(".wav")):
            filelist.remove(fichier)
    return(filelist)
def getLen(file):
    import math
    f = sf.SoundFile(file)
    l = len(f) / f.samplerate
    return(  int(math.ceil(l)+1)  )
def uic_divider():
    return("---------")
def ui_verify(inp, outp):
    print(uic_divider())
    print("Please verify that the parameters you have given are correct, no files will be deleted:")
    print("\tinput folder (subfolders not supported): " + inp)
    print("\toutput folder: " + outp)
    print("Press enter to continue or CTR+C to exit.")
    input("")
    print(uic_divider())

def convert(inp, outp):
    print("Starting edit...")
    
    print("-> Getting the length of the soundfile...")
    l = getLen(inp)
    
    #Resolution
    w = 1453#720
    h = 744#w*9/16 # 16/9 screen
    w = int(w)
    h = int(h)
    moviesize = w,h
    
    #Clips
    print("-> Creating clips...")
    name = os.path.basename(str(inp))
    name = "\n".join(name.split("-")[:2])
    cover = ImageClip("./img/web.jpg")
    ideal_img_name = inp.replace(".wav", ".jpg")
    try:
        cover = ImageClip(ideal_img_name)
    except:
        print(f"Image {ideal_img_name} not found – using default image ./img/web.jpg")
    audioclip = AudioFileClip(inp)
    new_audioclip = CompositeAudioClip([audioclip])

    font_size = 62
    name_part2 = name.split("\n")[1]
    if len(name_part2) > 15:
        font_size = 52
    if len(name_part2) > 20:
        font_size = 42
    if len(name_part2) > 25:
        font_size = 32

    # Generate a text clip 
    txt_clip = TextClip(name, fontsize = font_size, color = 'white', font = "Cantarell") 
        
    # setting position of text centered and duration will be the duration of the soundfile 
    txt_clip = txt_clip.set_pos(("center", "center")).set_duration(l)
    
    #Compose
    print("-> Composing clips...")
    txt_composite = CompositeVideoClip([txt_clip], size=(int(w/2),h))
    final = CompositeVideoClip([cover.resize(width=int(w/2)).set_position(("left", "center")), txt_composite.set_position(("right", "center"))], size = moviesize)
    final.audio = new_audioclip
    
    #Export
    print("-> Exporting clips...")
    final.set_duration(l).write_videofile(outp, fps=1)
    
    #Done
    print("Export done.")
    print(uic_divider())
def ui_main():
    inp = input("Soundfile to read (default ./music/bottles.wav): ")
    outp = input("Output filepath (default ./out.mp4): ")
    if outp == "":
        outp = "./out.mp4"
    if inp == "":
        inp = "./music/bottles.wav"
    ui_verify(inp, outp)
    convert(inp, outp)
if __name__ == "__main__":
    import sys
    minarg = 2
    minarg = minarg + 1
    if len(sys.argv) < minarg:
        print("Necessary parameters not given, parameters: " + str(sys.argv[1:]))
        print("-> Launching user interface...")
        ui_main()
    else:
        inp = sys.argv[1]
        outp = sys.argv[2]
        skip = False
        if len(sys.argv) > 3:
            skip = bool(sys.argv[3])
        if not skip:
            ui_verify(inp, outp)
        files = getFiles(inp)
        allc = len(files)
        i = 0
        print(f"{len(files)} files in total.")
        print("starting to process files... (press ctrl + C to cancel)")
        for fi in files:
            i = i + 1
            fi2 = inp + "/" + fi
            o = outp + "/" + os.path.basename(fi) + ".mp4"
            print("\t" + fi2 + " --> " + o)
            convert(fi2, o)
            print(str(i) + "/" + str(allc) + " done!")
