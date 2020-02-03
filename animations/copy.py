import subprocess as sp

#frames=[1,5,15,19,33,34,35,36,37,38,46,47,48,42]
#frames = [0,58]
#frames = [61]
#frames = [2,3,4,53,54,55,56]
#frames=[6,7,8,9,10,11,20,50,51,52,]
#frames=[21,22,24,25,30,31,32,]
#frames=[23,28,29,57]
#frames = [39,40,41]
#frames = [43,44,45]
frames = [13,14,16,17,18,26,27,49,59,60]
animation_folder = "hero_scene"

frames_dir = "/home/k2/Documents/gamejam/GamesJam/frame_"

for frame in frames:
    cmd = "cp {}/*.jpg {}{}/animations".format(animation_folder,frames_dir,frame)
    print(cmd)
    sp.call(cmd, shell=True)