from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip, ImageClip
from pyvideocreator.text_animator import TextAnimator
from pyvideocreator.subtitle_parser import *
import os
import numpy as np


from moviepy.editor import *

def create_mask_for_green_screen(frame, color_key=[105, 220, 107], threshold=60):
    """Crea una máscara binaria para un color clave en un frame."""
    diff = np.abs(frame.astype(int) - np.array(color_key).astype(int))
    distance = np.sqrt(np.sum(diff ** 2, axis=2))
    mask = (distance > threshold).astype('uint8')
    return mask

def insert_banner(original_video_path, banner_video_path, output_video_path, start_second):
    # Cargar el video original
    clip_original = VideoFileClip(original_video_path)

    # Cargar el banner
    banner_clip = VideoFileClip(banner_video_path).resize(width=clip_original.size[0])

    # Si start_second es negativo, calcular la posición de inicio en relación con el final del video
    if start_second < 0:
        start_second = clip_original.duration + start_second
    
    def compose_frames(t):
        if t < start_second or t > start_second + banner_clip.duration:
            return clip_original.get_frame(t)
        
        main_frame = clip_original.get_frame(t)
        banner_frame = banner_clip.get_frame(t - start_second)
        mask = create_mask_for_green_screen(banner_frame)
        mask_3channel = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
        blended_frame = main_frame * (1 - mask_3channel) + banner_frame * mask_3channel
        return blended_frame

    composited_clip = (VideoClip(compose_frames, duration=clip_original.duration)
                       .set_fps(clip_original.fps)
                       .set_audio(clip_original.audio))

    # Escribir el archivo de salida
    composited_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")



import cv2
from PIL import Image

class ImageVideoComposer:
    
    def __init__(self, image_path, duration, video_format="standard", fps=30):
        
        self.image = Image.open(image_path)
        self.duration = duration
        if video_format=="standard":
            self.video_format = (1920, 1080)
        else:
            self.video_format = (1080, 1920)
        self.video_format_type = video_format
        self.fps = fps
        self.total_frames = int(fps * duration)
    
    def _apply_panning_effect(self, speed=0.5):
        width, height = self.video_format
        new_width = int(width * 1.1)
        frames = []

        for i in range(self.total_frames):
            img_resized = self.image.resize((new_width, height), Image.ANTIALIAS)
            offset = int(i * (new_width - width) / self.total_frames * speed)
            cropped_img = img_resized.crop((offset, 0, offset + width, height))
            frame = np.array(cropped_img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frames.append(frame)
            
            # print(f'append frame {i+1} of {self.total_frames}')

        return frames

    # Puedes agregar otros efectos aquí siguiendo una estructura similar

    def export_video(self, output_path, effect='panning'):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, self.video_format)

        if effect == 'panning':
            
            print('Applying panning...')
            
            frames = self._apply_panning_effect()

        # Añade otras condiciones para otros efectos
        
        print("Exporting image video...")

        for frame in frames:
            out.write(frame)

        out.release()


class VideoComposer:

    FORMATS = {
        'standard': (1920, 1080),
        'short': (1080, 1920) 
    }

    def __init__(self, media_files, subtitles_file, styler, voice_audio=None, 
                 bg_music=None, format_type='standard'):
        self.media_files = media_files
        self.subtitles_file = subtitles_file
        self.styler = styler
        self.voice_audio = voice_audio
        self.bg_music = bg_music
        self.format_type = format_type
        if self.format_type not in self.FORMATS:
            raise ValueError(f"Invalid format_type {self.format_type}. Available formats are {list(self.FORMATS.keys())}.")

    def compose(self, subtitle_style_function=None):
        target_size = self.FORMATS[self.format_type]
        clips = []

        # Si hay voice_audio, obtener su duración
        voice_duration = 0
        if self.voice_audio:
            voice_duration = AudioFileClip(self.voice_audio).duration

        # Primero, calcular la duración total de los clips de video
        video_duration = 0
        for f in self.media_files:
            if f.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_duration += VideoFileClip(f).duration
        
        # Calcula la duración total que deben tener las imágenes estáticas
        images_duration = voice_duration - video_duration if self.voice_audio else 8

        # Divide la duración entre el número de imágenes estáticas
        num_images = sum(1 for f in self.media_files if not f.endswith(('.mp4', '.avi', '.mov', '.mkv')))
        per_image_duration = images_duration / num_images if num_images != 0 else 0
        
        for j, f in enumerate(self.media_files):
            if f.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_clip = VideoFileClip(f).resize(newsize=target_size)
                clips.append(video_clip)
            else:
                # image_clip = ImageClip(f).set_duration(per_image_duration).resize(newsize=target_size)
                video_from_image = ImageVideoComposer(f, per_image_duration, video_format=self.format_type)
                f_vid = f'temp_image_video_{j*3 + 5}.mp4'
                
                print("Starting one image video...")
                video_from_image.export_video(f_vid)
                print("Finished one image video...")
                video_clip = VideoFileClip(f_vid)
                clips.append(video_clip)

        final_video = concatenate_videoclips(clips)
        
        # If voice audio is provided, set it as the video's audio
        if self.voice_audio:
            voice = AudioFileClip(self.voice_audio)
            final_video = final_video.set_audio(voice)

        # If background music is provided, mix it with the video's audio at a lower volume
        if self.bg_music:
            music = AudioFileClip(self.bg_music).volumex(0.5)
            final_audio = CompositeAudioClip([final_video.audio, music])
            final_video = final_video.set_audio(final_audio)

        # Add subtitles using the styler
        styled_subs = self.styler.style()  # Calling the styler's style method
        
        
        animator = TextAnimator(video_format=self.format_type)
        text_clips = []
        for index, sub in enumerate(self.styler.subtitles):
            start_time, end_time, text = sub['start'], sub['end'], sub['text']
            
            # print(f'subitle read in Video Composer: {text}')
            
            
            style = styled_subs[index]
            subtitle_animate, fontsize, font, color, stroke_color, x_offset, y_offset = style
            
            # print(f'y_offset before calling: {y_offset}')
            
            text_clip = subtitle_animate(text, start_time, end_time, fontsize=fontsize, 
                                          font=font, color=color, stroke_color=stroke_color, 
                                          x_offset=x_offset, y_offset=y_offset)
            text_clips.append(text_clip)
            
        
        print("Writing final video...")
        final_video = animator.overlay_on_video(final_video, *text_clips)
        

        return final_video


    def export(self, output_filename):
        final_video = self.compose()

        
        final_video.write_videofile(output_filename)

