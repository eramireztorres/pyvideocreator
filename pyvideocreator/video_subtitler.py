from video_composer import VideoComposer
from subtitle_parser import KeyWordStyler, SubtitleStyler

class VideoSubtitler:
    def __init__(self, video_info, styler, voice_audio=None, bg_music=None, format_type='standard'):
        self.video_info = video_info
        self.styler = styler
        self.voice_audio = voice_audio
        self.bg_music = bg_music
        self.format_type = format_type

    def add_subtitles_and_export(self, output_filename):
        media_files = [self.video_info['clip']]  # List of media files (currently only the main video clip)
        subtitles_file = self.video_info['subtitles']

        # Initialize the VideoComposer with the necessary parameters
        composer = VideoComposer(media_files, subtitles_file, self.styler, 
                                 voice_audio=self.voice_audio, bg_music=self.bg_music, 
                                 format_type=self.format_type)

        # Use the VideoComposer to create the final video
        final_video = composer.compose()

        # Export the final video with subtitles
        composer.export(output_filename)

