import os
import re
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from subtitle_parser import SubtitleParser
from gpt_tts import OpenAITTS
from edge_tts import EdgeTTS
from pydub import AudioSegment, silence


# class AudioSubtitleSync:
#     def __init__(self, audio_file, subtitles):
#         self.audio = AudioSegment.from_file(audio_file)
#         self.subtitles = subtitles
#         self.pause_duration = 1000  # Pause duration in milliseconds (1 second)

#     def _calculate_pause_position(self, start_time, end_time, text):
#         # Approximate where to insert pauses based on text content and subtitle timing
#         # This is a basic approximation and might need refinement
#         pause_positions = []

#         # Insert a pause at the start of each subtitle
#         pause_positions.append(start_time)

#         # Additional pauses for periods and commas within the subtitle
#         if '.' in text or ',' in text:
#             # Simple heuristic: split the duration equally for each sentence or clause
#             parts = text.count('.') + text.count(',')
#             part_duration = (end_time - start_time) / (parts + 1)
#             for i in range(1, parts + 1):
#                 pause_positions.append(start_time + i * part_duration)

#         return pause_positions

#     def sync_audio_with_subtitles(self):
#         synced_audio = self.audio
#         for subtitle in self.subtitles:
#             start = self._convert_time_to_seconds(subtitle['start'])
#             end = self._convert_time_to_seconds(subtitle['end'])
#             pause_positions = self._calculate_pause_position(start, end, subtitle['text'])

#             for pos in pause_positions:
#                 # Create a silence segment of specified duration
#                 pause_segment = AudioSegment.silent(duration=self.pause_duration)
#                 # Overlay the silence segment at the specified position
#                 synced_audio = synced_audio.overlay(pause_segment, position=pos)

#         return synced_audio

#     def _convert_time_to_seconds(self, time_str):
#         # Split the time string into hours, minutes, and seconds + milliseconds
#         h, m, s_ms = time_str.split(':')

#         # Accommodate both comma-separated and dot-separated formats
#         if ',' in s_ms:
#             s, ms = s_ms.split(',')
#         elif '.' in s_ms:
#             s, ms = s_ms.split('.')
#         else:
#             # Default to zero milliseconds if not provided
#             s = s_ms
#             ms = '0'

#         # Convert each part to milliseconds and sum them up
#         total_ms = int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)
#         return total_ms


class AudioSubtitleSync:
    def __init__(self, audio_file, subtitles):
        self.audio = AudioSegment.from_file(audio_file)
        self.subtitles = subtitles
        self.pause_durations = {
            "...": 1500,  # Longest pause for ellipsis
            ".": 1000,    # Slightly shorter pause for period
            ",": 500,     # Shorter pause for comma, parenthesis, exclamation, and question marks
            ")": 500,
            "!": 500,
            ";": 500,
            "?": 500
        }

    def _insert_pause_at_position(self, position, pause_duration):
        pause_segment = AudioSegment.silent(duration=pause_duration)
        return self.audio.overlay(pause_segment, position=position)

    def sync_audio_with_subtitles(self):
        synced_audio = self.audio
        for subtitle in self.subtitles:
            end_time = self._convert_time_to_seconds(subtitle['end'])
            last_char = subtitle['text'][-1]

            # Check for specific punctuation marks
            if last_char in self.pause_durations:
                pause_duration = self.pause_durations[last_char]
                synced_audio = self._insert_pause_at_position(end_time, pause_duration)
            elif subtitle['text'][-3:] == "...":
                # Check for ellipsis at the end
                pause_duration = self.pause_durations["..."]
                synced_audio = self._insert_pause_at_position(end_time, pause_duration)

        return synced_audio

    def _convert_time_to_seconds(self, time_str):
        h, m, s_ms = time_str.split(':')
        if ',' in s_ms:
            s, ms = s_ms.split(',')
        elif '.' in s_ms:
            s, ms = s_ms.split('.')
        else:
            s, ms = s_ms, '0'

        # Adjust milliseconds to ensure they are always in a three-digit format
        ms = ms.ljust(3, '0')

        total_ms = int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)
        return total_ms

# Example usage
# audio_sync = AudioSubtitleSync('audio_file.mp3', subtitles_data)
# synced_audio = audio_sync.sync_audio_with_subtitles()


# Example usage
# audio_sync = AudioSubtitleSync('audio_file.mp3', subtitles_data)
# synced_audio = audio_sync.sync_audio_with_subtitles()



# class VideoVoiceOver:
#     def __init__(self, clip_info, openai_api_key=None):
#         self.clip_info = clip_info
#         self.openai_api_key = openai_api_key
#         self.subtitle_parser = SubtitleParser(clip_info['subtitles'])
#         self.subtitles = self.subtitle_parser.parse()
#         self.openai_voices = {'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'}

#     def _get_tts_service(self, voice):
#         if voice in self.openai_voices:
#             return OpenAITTS(api_key=self.openai_api_key)
#         else:
#             return EdgeTTS()
        
#     def _generate_complete_audio(self):
#         full_text = ' '.join([sub['text'] for sub in self.subtitles])
#         temp_audio_filename = "complete_audio.mp3"

#         tts_service = self._get_tts_service(self.clip_info['voice'])
#         if isinstance(tts_service, OpenAITTS):
#             tts_service.generate_audio(full_text, voice=self.clip_info['voice'], output_path=temp_audio_filename)
#         else:
#             tts_service.convert_text_to_audio(full_text, output_filename=temp_audio_filename, voice=self.clip_info['voice'])
        
#         return temp_audio_filename
    
#     def _insert_pauses_in_audio(self, audio_file):        
#         audio_sync = AudioSubtitleSync(audio_file, self.subtitles)
#         synced_audio = audio_sync.sync_audio_with_subtitles()
    
#         return synced_audio

#     def add_voice_over_with_pauses(self, output_filename):
#         video_clip = VideoFileClip(self.clip_info['clip'])
#         complete_audio_file = self._generate_complete_audio()
#         audio_with_pauses = self._insert_pauses_in_audio(complete_audio_file)

#         # Save the modified audio
#         modified_audio_file = "modified_audio.mp3"
#         audio_with_pauses.export(modified_audio_file, format="mp3")

#         # Load the modified audio as an AudioFileClip
#         modified_audio_clip = AudioFileClip(modified_audio_file)

#         # Set the modified audio to the video clip
#         final_video = video_clip.set_audio(modified_audio_clip)
#         final_video.write_videofile(output_filename, codec="libx264", audio_codec="aac")
        
#         # Clean up temporary files
#         os.remove(complete_audio_file)
#         os.remove(modified_audio_file)

class VideoVoiceOver:
    def __init__(self, clip_info, openai_api_key=None):
        self.clip_info = clip_info
        self.openai_api_key = openai_api_key
        self.subtitle_parser = SubtitleParser(clip_info['subtitles'])
        self.subtitles = self.subtitle_parser.parse()
        self.openai_voices = {'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'}

    def _get_tts_service(self, voice):
        if voice in self.openai_voices:
            return OpenAITTS(api_key=self.openai_api_key)
        else:
            return EdgeTTS()
        
    def _generate_complete_audio(self):
        full_text = ' '.join([sub['text'] for sub in self.subtitles])
        temp_audio_filename = "complete_audio.mp3"
        
        tts_service = self._get_tts_service(self.clip_info['voice'])
        if isinstance(tts_service, OpenAITTS):
            tts_service.generate_audio(full_text, voice=self.clip_info['voice'], output_path=temp_audio_filename)
        else:
            tts_service.convert_text_to_audio(full_text, output_filename=temp_audio_filename, voice=self.clip_info['voice'])
        
        return temp_audio_filename

    def _insert_pauses_in_audio(self, audio_file):
        audio_sync = AudioSubtitleSync(audio_file, self.subtitles)
        synced_audio = audio_sync.sync_audio_with_subtitles()
        return synced_audio

    def _extract_audio_from_video(self, video_path, output_audio_path):
        command = f"ffmpeg -i {video_path} -q:a 0 -map a {output_audio_path}"
        subprocess.run(command, shell=True, check=True)

    def _merge_audio_with_video(self, video_path, audio_path, output_path):
        command = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac -strict experimental {output_path}"
        subprocess.run(command, shell=True, check=True)

    def add_voice_over_with_pauses(self, output_filename):
        original_video_path = self.clip_info['clip']
        complete_audio_file = self._generate_complete_audio()
        audio_with_pauses = self._insert_pauses_in_audio(complete_audio_file)

        # Save the modified audio
        modified_audio_file = "modified_audio.mp3"
        audio_with_pauses.export(modified_audio_file, format="mp3")

        # Merge the modified audio with the original video
        self._merge_audio_with_video(original_video_path, modified_audio_file, output_filename)

        # Clean up temporary files
        os.remove(complete_audio_file)
        os.remove(modified_audio_file)


