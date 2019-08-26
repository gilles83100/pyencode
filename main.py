# -*- coding: utf-8
import subprocess
import re
import os, sys, getopt
import progressbar

try:
    this_file = __file__
except NameError:
    this_file = sys.argv[0]
this_file = os.path.abspath(this_file)
if getattr(sys,'frozen', False):
    basepath = getattr(sys,'_MEIPASS', os.path.dirname(sys.executable))
else:
    basepath = os.path.dirname(this_file)

"""
"""
presets = ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow', 'placebo']
preset = presets[5]
vprofiles = ['baseline','main', 'high', 'high10', 'high422', 'high444']
vprofile = vprofiles[1]
# profile baseline = level = 3.0
levels = ['1.3', '3.0', '3.1', '3.2', '4.0', '4.1', '4.2', '5.0', '5.1', '5.2'] # 1.3 seulement avec profil 'baseline'
level = [6]

debitVideo = '1600k'

codecsVideo = ['libx264']

debitAudio = '160k'
codecAudio = 'aac'

scale = '-2:-2'
crop = ''
container = 'mp4'
simulate = [] # ['-ss', '00:30:00', '-t', '00:30']

def time2secs(duration):
    heures, minutes, secondes = duration.split(':')
    total = 0
    total += int(heures) * 3600
    total += int(minutes) * 60
    total += float(secondes)
    return total

def getCrop(filename,position = 5):
    if os.name in ("nt", "dos", "os2", "ce"):
        destNull = 'NUL'
    elif sys.platform == "darwin":
        destNull = '/dev/null'

    command = [FFMPEG_PATH, '-ss', '{}'.format(position), '-y', '-i', filename,
               '-t', '3', '-vf', 'cropdetect=24:16:0', '-an', '-f', 'mp4',
               destNull]
    p = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True)
    while True:
        chunk = p.stderr.readline()
        if chunk == '':
            break
        m = re.search("crop=(?P<crop>\S+)", chunk)
        if m is not None:
            return 'crop={}'.format(m.group('crop'))
            break

    return ""

def getDuration(filename):
    command = [FFPROBE_PATH, '-i', filename, '-show_format']
    p = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    while True:
        #chunk = p.stderr.readline()
        chunk = p.stdout.readline()
        if chunk == '':
            break
        m = re.search("duration=(?P<duration>\S+)", chunk)
        if m is not None:
            try:
                return float(m.group('duration'))
            except Exception as e:
                return 0.0
            break
    return 0.0

def encoding(infile, outfile, codecVideo=codecsVideo[0], preset = presets[5], vprofile=vprofiles[1], level=levels[6], simulate = []):

    print('codec = {} vprofile = {} level = {} simulate = {}'.format(codecVideo, vprofile, level, simulate))
    cmd = [FFMPEG_PATH]

    if simulate:
        cmd += simulate

    vf = ['scale='+scale]
    if crop != '':
        vf += ['crop={}'.format(crop)]
    vf += ['yadif=0:-1:0']

    cmd += ['-y', '-i', infile]
    cmd += ['-vf', ','.join(vf), '-c:v', codecVideo]
    cmd += ['-map', '0:0']
    cmd += ['-b:v', debitVideo]
    cmd += ['-preset', preset, '-profile:v', vprofile, '-pix_fmt', 'yuv420p']
    cmd += ['-map', '0:1', '-c:a', codecAudio, '-b:a', debitAudio, '-ac', '2']
    cmd += ['-async', '1']
    cmd += ['-f', container]
    cmd += [outfile]

    cli(cmd, infile)

    return cmd

def cli(cmd, filename=''):
    widget = ['Encodage',progressbar.Percentage(), ' ', progressbar.Bar(), ' ', progressbar.ETA()] #, ' ', filename]
    bar = progressbar.ProgressBar(widgets=widget)
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, universal_newlines=True)
    while True:
        chunk = p.stderr.readline()
        if chunk == '':
            break
        m = re.search("Duration: (?P<time>\S+),", chunk)
        if m is not None:
            durationTotal = time2secs(m.group('time'))
            bar.max_value = durationTotal

        m = re.search("time=(?P<time>\S+)", chunk)
        if m is not None:
            d = time2secs(m.group('time'))
            # print(d/durationTotal, m.group('time'))
            try:
                bar.update(min(d,durationTotal))
            except Exception as e:
                print(e)

        if re.search("Conversion failed!", chunk) is not None:
            print("Erreur de conversion pour le fichier {}".format(filename))
            print(' '.join(cmd))

FFMPEG_PATH = 'ffmpeg'
FFPROBE_PATH = 'ffprobe'

if os.name in ("nt", "dos", "os2", "ce"):
    FFMPEG_PATH = os.path.join(basepath, 'plugin\\ffmpeg.exe')
    FFPROBE_PATH = os.path.join(basepath, 'plugin\\ffprobe.exe')
    codecsVideo = ['libx264', 'h264_amf', 'h264_nvenc', 'h264_qsv', 'nvenc', 'nvenc_h264']
    codecVideo = codecsVideo[0]

elif sys.platform == 'darwin':
    FFMPEG_PATH = os.path.join(basepath, 'plugin/ffmpeg')
    FFPROBE_PATH = os.path.join(basepath, 'plugin/ffprobe')

    # ./ffmpeg -h encoder=h264_videotoolbox
    # ./ffmpeg -encoders | grep 264
    codecsVideo = ['libx264', 'h264_videotoolbox', 'libopenh264']
    codecVideo = codecsVideo[0]
elif sys.platform == 'linux':
    codecsVideo = ['libx264', 'h264_omx', 'h264_v4l2m2m', 'h264_vaapi']
    codecVideo = codecsVideo[0]

infile = ''
outfile = ''

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:c:v:a:", ['help', 'inputfile=', 'outputfile=', 'getcrop=', 'codecvideo='])
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)

    for opt, arg in opts:
        if opt in('--inputfile', '-i'):
            infile = arg
        elif opt in ('--outputfile', '-o'):
            outfile = arg
        elif opt in ('--getcrop', '-c'):
            print(getCrop(arg, position=int(getDuration(arg)/2)))
            sys.exit()
        elif opt in ('--codecvideo', '-v'):
            if arg in codecsVideo:
                codecVideo = arg
            else:
                codecVideo = codecsVideo[0]
                print("'{}' n'existe pas, le codec '{}' sera utilisé".format(arg, codecVideo))
        elif opt in ('--help', '-h'):
            print('pyencode')
            print('========')
            print('')
            print('Usage: pyencode.py -i source -o destination')
            sys.exit()

    infile = '/Users/gilles/Movies/08-20 20-55-01_TFX (fra) La colère des Titans.ts'
    outfile = '/Users/gilles/Movies/08-20 20-55-01_TFX (fra) La colère des Titans.mp4'

    if os.path.exists(infile):
        if outfile=='':
            outfile = os.path.splitext(infile)[0]+'_{}_{}.{}'.format(codecVideo, codecAudio, container)

        encoding(infile, outfile, codecVideo = codecVideo)
    else:
        if infile != '':
            print("Le fichier '{}' n'existe pas".format(infile))
        else:
            print('pyencode')
