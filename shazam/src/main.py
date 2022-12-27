import asyncio
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


async def recognize() -> AsyncGenerator[dict[str, Any], None]:
    args = parse_args(sys.argv[1:])
    for arg in args:
        if 'url' in arg:
            if 'path' not in arg:
                arg['path'] = f".temp_{time.time()}.wav"
            subprocess.check_call(['bin/yt-dlp.exe', '-x', '--audio-format', 'wav', arg['url'], '-o', arg['path']])
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
            recognize.to_delete.append(arg['path'])


recognize.to_delete = []


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


def save(data: tuple[str, dict[str, str | int]], file) -> None:
    if not hasattr(save, "total"):
        save.total = []
    if not data[0].isspace():
        file.seek(0)
        save.total.append(data[1])
        json.dump(save.total, file, indent=4, ensure_ascii=False)
        print(data[0])
    else:
        print("\n\nTrack not found.")


async def main() -> None:
    with open("results.json", "w", encoding="UTF-8") as file:
        [save(serialize(result), file) async for result in recognize()]
    [os.remove(path) for path in recognize.to_delete]
    print("\nDone!")


asyncio.run(main())
