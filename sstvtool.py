# 画像SSTV変換ツール sstvtool.py Ver. 1.0.1(W) by JA1XPM & Microsoft Copilot 2024.06.18
# Ver1.0.1変更点: 使えるSSTVモードを増やした。ストリーミング時、起動パラメーターで オーディオ出力デバイスを -d/--device {device_id}で数字を指定するとそこに出力する。
#

import wave
import argparse
import sys
from PIL import Image, ImageOps, ImageFont, ImageDraw
import numpy as np
import pyaudio
from pysstv.color import Robot36, MartinM1, MartinM2, ScottieS1, ScottieS2
from pysstv.grayscale import Robot8BW, Robot24BW

SSTV_MODES = {
     'Robot36': Robot36,
     'MartinM1': MartinM1,
     'MartinM2': MartinM2,
     'ScottieS1': ScottieS1,
     'ScottieS2': ScottieS2,
     'Robot8BW': Robot8BW, 
     'Robot24BW': Robot24BW,
}

def play_audio(stream, samples):
    stream.write(samples.tobytes())

def save_to_file(samples, output_path):
    with wave.open(output_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(samples.tobytes())

def resize_and_fill(image, target_width, target_height):
    original_width, original_height = image.size
    ratio = min(target_width/original_width, target_height/original_height)
    new_size = (int(original_width * ratio), int(original_height * ratio))
    image = image.resize(new_size, Image.Resampling.LANCZOS)
    background = Image.new('RGB', (target_width, target_height), (0, 0, 0))
    offset = ((target_width - new_size[0]) // 2, (target_height - new_size[1]) // 2)
    background.paste(image, offset)
    return background

def add_text_to_image(image, text, position, font_path, font_size, text_color):
    if text:
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, font_size)
        text_bbox = font.getbbox(text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = calculate_position(image.size, position, (text_width, text_height))
        draw.text(position, text, fill=text_color, font=font)
    return image

def calculate_position(image_size, base_position, text_size):
    image_width, image_height = image_size
    text_width, text_height = text_size
    x, y = base_position
    x = min(x, image_width - text_width)
    y = min(y, image_height - text_height)
    return x, y

def generate_sstv_signal(image_path, mode='Robot36', stream=False, output_path=None, size=None, text='JA1XPM', font_path='arial.ttf', font_size=32, text_color='green', text_position=(5, 5), device_id=None):
    try:
        img = Image.open(image_path)
        if size:
            img = resize_and_fill(img, *size)
        img = add_text_to_image(img, text, text_position, font_path, font_size, text_color)
        if mode not in SSTV_MODES:
            raise ValueError(f'Invalid SSTV mode: {mode}')
        sstv_class = SSTV_MODES[mode]
        sstv = sstv_class(img, 44100, 16)
        sstv.vox_enabled = False
        samples = np.fromiter(sstv.gen_samples(), dtype=np.int16)

        if stream:
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(2),
                            channels=1,
                            rate=44100,
                            output=True,
                            output_device_index=device_id)  # Use the device ID from the command line argument
            play_audio(stream, samples)
            stream.stop_stream()
            stream.close()
            p.terminate()
        elif output_path:
            save_to_file(samples, output_path)
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate and play or save an SSTV signal')
    parser.add_argument('-i', '--image', required=True, help='Path to the input image file')
    parser.add_argument('-m', '--mode', default='Robot36', help='SSTV mode to use')
    parser.add_argument('-s', '--stream', action='store_true', help='Stream the SSTV signal')
    parser.add_argument('-o', '--output', help='Path to save the SSTV signal')
    parser.add_argument('-p', '--pixel', help='Pixel size to resize the image to (e.g., 320x240)')
    parser.add_argument('-d', '--device', type=int, help='Device ID to use when streaming')

    args = parser.parse_args()

    size = None
    if args.pixel:
        try:
            width, height = map(int, args.pixel.split('x'))
            size = (width, height)
        except ValueError:
            print('Error: Pixel size should be specified in the format widthxheight (e.g., 320x240)')
            sys.exit(1)

    generate_sstv_signal(args.image, args.mode, args.stream, args.output, size, device_id=args.device)
