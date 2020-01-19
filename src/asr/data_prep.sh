data=/CDShare/magicspeech/MagicSpeech/

mkdir -p data/train/wav
mkdir -p data/dev/wav
mkdir -p data/test/wav
rm -r data/*/wav/*
rm data/*/text

for x in train test dev;do
	echo $data$x
	for file in `ls ${data}audio/$x`;do
	    let i+=1
        if [ $x == train ];then
            json=${data}transcription/${x}/${file%.*}.json
        else
            json=${data}transcription/${x}/${file%_*}.json
        fi
        audio_file=${data}audio/${x}/$file
        mkdir -p data/$x/wav/${file%.*}
        python -W ignore split_audio.py $audio_file $json $x>> data/$x/text || exit 1;
        echo "$audio_file finished!"
	done
    echo "$x audio segment finished!"
done

mkdir -p uttid
mkdir -p wavscp
for x in `ls data/train/wav`;do
	    ls data/train/wav/$x |sort -t'_' -k 5 -g|sed 's/.wav//'>uttid/${x%.*};
	    find data/train/wav/$x -iname '*.wav' |sort  -t'_' -k 7 -g>wavscp/${x%.*}
done
sort -m uttid/* >uttid1
sort -m wavscp/* >wavscp1
paste -d' ' uttid1 wavscp1 >data/train/wav.scp
rm -r uttid/*
rm -r wavscp/*
rm uttid1 wavscp1

for x in `ls data/dev/wav`;do
	    ls data/dev/wav/$x |sort -t'_' -k 6 -g|sed 's/.wav//'>uttid/${x%.*};
	    find data/dev/wav/$x -iname '*.wav' |sort -t'_' -k 9 -g>wavscp/${x%.*}
done
sort -m uttid/* >uttid1
sort -m wavscp/* >wavscp1
paste -d' ' uttid1 wavscp1 >data/dev/wav.scp
rm -r uttid/*
rm -r wavscp/*
rm uttid1 wavscp1
