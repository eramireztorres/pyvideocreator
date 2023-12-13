import re
from pyvideocreator.text_animator import TextAnimator

import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
    return chardet.detect(rawdata)['encoding']



class SubtitleParser:
    def __init__(self, filename):
        self.filename = filename
        self.format = self._determine_format(filename)

    def parse(self):
        if self.format == 'srt':
            return self._parse_srt()
        else:
            return self._parse_vtt_manual()

    def _parse_vtt_manual(self):
        # with open(self.filename, 'r', encoding='utf-8') as file:
        #     lines = file.readlines()
        
        # with open(self.filename, 'r', encoding='utf-8', errors='replace') as file:
        #     lines = file.readlines()
        
        encoding = detect_encoding(self.filename)
        with open(self.filename, 'r', encoding=encoding) as file:
            lines = file.readlines()


        subtitles = []
        current_times = None
        current_text = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith("WEBVTT"):
                continue

            if '-->' in line:
                if current_times and current_text:
                    subtitles.append({
                        'start': current_times[0],
                        'end': current_times[1],
                        'text': ' '.join(current_text)
                    })
                    current_text = []
                current_times = [time.strip() for time in line.split('-->')]
            else:
                current_text.append(line)

        if current_times and current_text:
            subtitles.append({
                'start': current_times[0],
                'end': current_times[1],
                'text': ' '.join(current_text)
            })
        return subtitles

    def _determine_format(self, filename):
        if filename.endswith('.srt'):
            return 'srt'
        elif filename.endswith('.vtt'):
            return 'vtt'
        elif filename.endswith('.sub'):
            return 'sub'
        else:
            raise ValueError(f"Unsupported file extension in {filename}")

    def _parse_srt(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            content = file.read()

        pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n'
        matches = re.findall(pattern, content, re.DOTALL)

        subtitles = [{'start': start, 'end': end, 'text': text.replace('\n', ' ')}
                     for _, start, end, text in matches]
        return subtitles


class SubtitleStyler:

    def __init__(self, srt_filename,fontsize=70, font='Gill-Sans-MT-Bold', 
                 color='yellow', stroke_color='black', 
                 x_offset=0, y_offset=300, video_format='standard'):
        self.parser = SubtitleParser(srt_filename)
        self.subtitles = self.parser.parse()
        self.fontsize = fontsize
        self.font = font
        self.color = color
        self.stroke_color = stroke_color
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.animator = TextAnimator(video_format=video_format)

    def style(self):
        """Assigns a default style to all subtitles."""
        default_style = [self.animator.standard_subtitle, self.fontsize, self.font, 
                         self.color, self.stroke_color, self.x_offset, self.y_offset]
        styled_subtitles = [default_style for _ in self.subtitles]
        return styled_subtitles
    
import joblib
import random

class KeyWordStyler:

    def __init__(self, srt_filename, video_format='standard',
                 keyword_dict_filename='keyword_styles.joblib'):
        self.parser = SubtitleParser(srt_filename)
        self.subtitles = self.parser.parse()
        
        # print(f'subitles after parse in KeyWordStyler: {self.subtitles}')
        
        self.keyword_dict = joblib.load(keyword_dict_filename)
        self.animator = TextAnimator(video_format=video_format)

    def _choose_from_dict(self, d):
        """Chooses an item from dictionary values based on its type."""
        if isinstance(d, list):
            return random.choice(d)
        elif isinstance(d, dict):
            return {k: self._choose_from_dict(v) for k, v in d.items()}
        return d

    def style(self):
        """Assigns a style based on keywords found in the subtitle."""
        styled_subtitles = []
        for sub in self.subtitles:
            text = sub['text']
            style = [self.animator.standard_subtitle, 70, 'Gill-Sans-MT-Bold', 'yellow', 'black', 0, 300]  # Default style
            for keyword, kw_style in self.keyword_dict.items():
                if keyword in text:
                    # Override the default style
                    kw_style_selected = self._choose_from_dict(kw_style)
                    animator_method = getattr(self.animator, kw_style_selected["animator"])
                    style = [animator_method, kw_style_selected["fontsize"], kw_style_selected["font"], 
                             kw_style_selected["color"], kw_style_selected["stroke_color"], 
                             kw_style_selected["x_offset"], kw_style_selected["y_offset"]]
                    break  # Use the first keyword match found
            styled_subtitles.append(style)
        return styled_subtitles




