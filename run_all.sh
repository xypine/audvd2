
[ ! -f ./app.py ] && echo "$FILE does not exist. Please verify you are running the script in the correct folder" && exit
# Remove files from previous runs
echo "Removing files from previous runs"
rm -rf ./out
rm -rf ./music

# Install audvd dependencies
./install_dependencies.sh

# Download all podcasts from soundcloud as .wav files to ./music (which is the only format audvd supports)
echo "Downloading all podcasts from soundcloud as .wav files to ./music"
mkdir music
cd music
youtube-dl --extract-audio --audio-format wav --write-thumbnail https://soundcloud.com/user-208824705-387464785/tracks
# Convert all audiofiles in ./music to videos in ./out, skip confirmations
echo "Converting all audiofiles in ./music to videos in ./out"
cd ..
mkdir out
python3 app.py ./music ./out true
# Done
echo "Everything done, have a good day."