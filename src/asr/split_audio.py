#! ~/work/anaconda3/envs/py36/bin/python
from pydub import AudioSegment
import json
import os
import sys


def read_json(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        temp = json.loads(f.read())
        # print(temp)
        for x in temp:
            print(x['start_time']['original'])
            print(x['end_time']['original'])


def split_audio(audio_file, json_file,type):
    # print(audio_file)
    sound = AudioSegment.from_file(audio_file, format='wav')
    # json_name = dirpath + filename.split('.')[0] + '.json'
    i = 1
    id=audio_file.split('/')[-1].split('.')[0]

    with open(json_file, 'r', encoding="utf-8") as f:
        if type == 'test':
            lines = f.readlines()
            for _index, line in enumerate(lines):
                if 'uttid' in line and 'words' not in lines[_index + 1]:
                    lines[_index] = line.replace('",', '"')
            file = ''.join(lines)
            temp = json.loads(file)
            for x in temp:
                start_time1 = x['start_time']
                end_time = x['end_time']
                session_id = x['session_id']
                save_name = id + '_' + str(i).zfill(4) + '.wav'
                start_time = int((int(start_time1.split(':')[0]) * 3600 + int(start_time1.split(':')[1]) * 60 + float(
                    start_time1.split(':')[2])) * 1000)
                stop_time = int(
                    (int(end_time.split(':')[0]) * 3600 + int(end_time.split(':')[1]) * 60 + float(
                        end_time.split(':')[2])) * 1000)
                # print("time:", start_time1, "~", end_time, "ms:", start_time, "~", stop_time)
                crop_audio = sound[start_time:stop_time]
                i += 1
                crop_audio.export('data/'+type+'/wav/'+id+'/'+save_name, format="wav")
        else:
            temp = json.loads(f.read())
            for x in temp:
                start_time1 = x['start_time']['original']
                end_time = x['end_time']['original']
                speaker = x['speaker']
                session_id = x['session_id']
                words = x['words']
                if speaker == '':
                    speaker = 'None'
                save_name = id + '_' + speaker + '_' + str(i).zfill(4) + '.wav'

                start_time = int((int(start_time1.split(':')[0]) * 3600 + int(start_time1.split(':')[1]) * 60 + float(
                    start_time1.split(':')[2])) * 1000)
                stop_time = int(
                    (int(end_time.split(':')[0]) * 3600 + int(end_time.split(':')[1]) * 60 + float(
                        end_time.split(':')[2])) * 1000)
                # print("time:", start_time1, "~", end_time, "ms:", start_time, "~", stop_time)
                crop_audio = sound[start_time:stop_time]
                print(save_name.split('.')[0] + ' ' + words)
                i += 1
                crop_audio.export('data/'+type+'/wav/'+id+'/'+save_name, format="wav")



if __name__ == '__main__':
    audio = sys.argv[1]
    json_file = sys.argv[2]
    type = sys.argv[3]
    split_audio(audio, json_file,type)
