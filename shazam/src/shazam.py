import json
import os
import subprocess
import sys
import time
from typing import Union, AsyncGenerator, Any

from shazamio import *
from pydub import AudioSegment


def parse_args(args: list[str]) -> list[dict[str, Union[str, int]]]:
    data = {}
    output = []
    index = 0
    while index < len(args):
        match args[index]:
            case '-d':
                index += 1
                data['url'] = args[index]
                output.append(data)
                data = {}
            case '-s':
                index += 1
                data['split'] = int(args[index]) * 1000
            case _:
                data['path'] = args[index]
                output.append(data)
                data = {}
        index += 1
    return output


def serialize(result: dict[str, Any]) -> tuple[str, dict[str, Union[str, int]]]:
    song = {}
    string = "\n"
    if 'matches' in result and result['matches']:
        stamp = ', '.join(map(str, set(
            '{:0>2}:{:0>2}'.format(int(match['offset'] // 60), int(match['offset'] % 60)) for match in
            result['matches']
            if 'offset' in match)))
        if 'track' in result:
            track = result['track']
            if 'title' in track:
                song['title'] = track['title']
                string += f"\nTitle: {track['title']}"
            if 'subtitle' in track:
                song['artist'] = track['subtitle']
                string += f"\nArtist: {track['subtitle']}"
        if stamp:
            song['time'] = stamp
            string += f"\nTime: {stamp}"
        if 'location' in result and 'accuracy' in result['location']:
            song['accuracy'] = result['location']['accuracy'] * 10000
            string += f"\nAccuracy: {song['accuracy']}%"
    return string, song


class Recognizer:
    def __init__(self, save_name: str):
        self.total = []
        self.to_delete = []
        self.save_name = save_name

    def save(self, data: tuple[str, dict[str, str | int]], file) -> None:
        if not data[0].isspace():
            file.seek(0)
            self.total.append(data[1])
            json.dump(self.total, file, indent=4, ensure_ascii=False)
            print(data[0])
        else:
            print("\n\nTrack not found.")

    async def recognize(self) -> AsyncGenerator[dict[str, Any], None]:
        args = parse_args(sys.argv[1:])
        for arg in args:
            if 'url' in arg:
                if 'path' not in arg:
                    arg['path'] = f".temp_{time.time()}.wav"
                subprocess.check_call(
                    ['bin/yt-dlp.exe', '-x', '--audio-format', 'wav', arg['url'], '-o', arg['path']])
            if 'split' in arg:
                if not arg['path'].endswith('.wav'):
                    source = arg['path']
                    arg['path'] = f".temp_{time.time()}.wav"
                    subprocess.check_call(['bin/ffmpeg.exe', arg['path'], '-i', source, '-loglevel', 'error'])
                buffer = AudioSegment.from_wav(arg['path'])
                seg = 0
                while seg < buffer.duration_seconds * 1000:
                    yield await Shazam().recognize_song(buffer[seg:seg + arg['split']])
                    seg += arg['split']
            else:
                yield await Shazam().recognize_song(arg['path'])
            if arg['path'].startswith('.temp_'):
                self.to_delete.append(arg['path'])

    def __del__(self):
        for file in self.to_delete:
            os.remove(file)

    async def run(self):
        with open(self.save_name, "w", encoding="UTF-8") as file:
            async for result in self.recognize():
                self.save(serialize(result), file)
