
# from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip, concatenate_audioclips
# # from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips

# class VideoAssembler:
#     def __init__(self, files, transition_duration=1):
#         self.files = files
#         self.transition_duration = transition_duration

#     def _get_max_size(self, clips):
#         max_width = max(clip.size[0] for clip in clips)
#         max_height = max(clip.size[1] for clip in clips)
#         return max_width, max_height

#     def _resize_clip(self, clip, size):
#         return clip.resize(newsize=size)

#     def assemble_video(self, output_path):
#         clips = [ImageClip(file).set_duration(5) if file.endswith(('png', 'jpg', 'jpeg')) else VideoFileClip(file) for file in self.files]
#         max_size = self._get_max_size(clips)
#         resized_clips = [self._resize_clip(clip, max_size) for clip in clips]
#         fps = next((clip.fps for clip in resized_clips if isinstance(clip, VideoFileClip)), 24)

#         final_clips = []
#         for i, clip in enumerate(resized_clips):
#             if i > 0:
#                 # Apply crossfade transition directly
#                 clip = clip.crossfadein(self.transition_duration)
#             final_clips.append(clip)

#         # final_video = concatenate_videoclips(final_clips, method="compose", padding=-self.transition_duration)
#         # final_video.write_videofile(output_path, fps=fps, codec="libx264", audio_codec="aac")
        
#         video_clip = concatenate_videoclips(final_clips, method='compose')
#         audio_concatenation = concatenate_audioclips(final_clips)
#         video_clip = video_clip.set_audio(audio_concatenation)
#         video_clip.write_videofile(output_path, fps=fps, codec="libx264", audio_codec="aac")
        

# Example usage
# files = ['video1.mp4', 'video2.mp4', 'video3.mp4']
# video_assembler = VideoAssembler(files, transition_duration=1)
# video_assembler.assemble_video('final_video.mp4')


# import os
# from typing import List
# from moviepy.editor import ImageClip, VideoFileClip

# class VideoAssembler:
#     def __init__(self, files, transition_duration=1, temporary_process_folder='Temp'):
#         self.files = files
#         self.transition_duration = transition_duration
#         self.temporary_process_folder = temporary_process_folder
#         os.makedirs(self.temporary_process_folder, exist_ok=True)

#     def _get_max_size(self, clips):
#         max_width = max(clip.size[0] for clip in clips)
#         max_height = max(clip.size[1] for clip in clips)
#         return max_width, max_height

#     def _resize_clip(self, clip, size):
#         return clip.resize(newsize=size)

#     def _concat_videos_ffmpeg(self, input_video_path_list: List[str], output_video_path: str) -> str:
#         concat_file_list: List[str] = []
#         for idx, input_video_path in enumerate(input_video_path_list, start=1):
#             temp_file_ts = f'{self.temporary_process_folder}/concat_{idx}.ts'
#             os.system(f'ffmpeg -y -loglevel error -i {input_video_path} -c copy -bsf:v h264_mp4toannexb -f mpegts {temp_file_ts}')
#             concat_file_list.append(temp_file_ts)

#         concat_string = '|'.join(concat_file_list)
#         os.system(f'ffmpeg -y -loglevel error -i "concat:{concat_string}" -c copy {output_video_path}')
#         return output_video_path

#     def assemble_video(self, output_path):
#         clips = [ImageClip(file).set_duration(5) if file.endswith(('png', 'jpg', 'jpeg')) else VideoFileClip(file) for file in self.files]
#         max_size = self._get_max_size(clips)
#         resized_clips = [self._resize_clip(clip, max_size) for clip in clips]

#         # Save temporary resized clips
#         temp_files = []
#         for i, clip in enumerate(resized_clips):
#             temp_file_path = f"{self.temporary_process_folder}/temp_clip_{i}.mp4"
#             clip.write_videofile(temp_file_path, codec="libx264", audio_codec="aac")
#             temp_files.append(temp_file_path)

#         # Use FFmpeg to concatenate videos
#         self._concat_videos_ffmpeg(temp_files, output_path)

#         # Clean up temporary files
#         for file in temp_files:
#             os.remove(file)

# import os
# from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
# from pydub import AudioSegment

# class VideoAssembler:
#     def __init__(self, files, transition_duration=1, temporary_process_folder='Temp'):
#         self.files = files
#         self.transition_duration = transition_duration
#         self.temporary_process_folder = temporary_process_folder
#         os.makedirs(self.temporary_process_folder, exist_ok=True)

#     def _get_max_size(self, clips):
#         max_width = max(clip.size[0] for clip in clips)
#         max_height = max(clip.size[1] for clip in clips)
#         return max_width, max_height

#     def _resize_clip(self, clip, size):
#         return clip.resize(newsize=size)

#     def _concatenate_audio(self, audio_segments):
#         concatenated_audio = AudioSegment.empty()
#         for segment in audio_segments:
#             concatenated_audio += segment
#         return concatenated_audio

#     def assemble_video(self, output_path):
#         video_clips = [VideoFileClip(file) for file in self.files]
#         max_size = self._get_max_size(video_clips)
#         resized_video_clips = [self._resize_clip(clip, max_size) for clip in video_clips]

#         # Extract and concatenate audio segments
#         audio_segments = [AudioSegment.from_file(file) for file in self.files]
#         concatenated_audio = self._concatenate_audio(audio_segments)
#         final_audio_file_path = os.path.join(self.temporary_process_folder, "final_audio.mp3")
#         concatenated_audio.export(final_audio_file_path, format="mp3")

#         # Concatenate video clips
#         final_video = concatenate_videoclips(resized_video_clips, method="compose")
        
#         # Set the concatenated audio to the final video
#         final_video.audio = AudioFileClip(final_audio_file_path)
#         final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

#         # Clean up temporary files
#         os.remove(final_audio_file_path)
#         for clip in resized_video_clips:
#             clip.close()

#         return output_path

# import os
# import subprocess
# from moviepy.editor import VideoFileClip

# class VideoAssembler:
#     def __init__(self, files, temporary_process_folder='Temp'):
#         self.files = files
#         self.temporary_process_folder = temporary_process_folder
#         os.makedirs(self.temporary_process_folder, exist_ok=True)

#     def _get_max_size(self, clips):
#         max_width = max(clip.size[0] for clip in clips)
#         max_height = max(clip.size[1] for clip in clips)
#         return max_width, max_height

#     def _resize_clip(self, clip, size):
#         return clip.resize(newsize=size)

#     def _concat_videos_ffmpeg(self, input_video_path_list, output_video_path):
#         with open(os.path.join(self.temporary_process_folder, 'input.txt'), 'w') as f:
#             for file in input_video_path_list:
#                 f.write(f"file '{file}'\n")

#         concat_list_path = os.path.join(self.temporary_process_folder, 'input.txt')
#         subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_list_path, 
#                         '-c', 'copy', output_video_path], check=True)

#     def assemble_video(self, output_path):
#         video_clips = [VideoFileClip(file) for file in self.files]
#         max_size = self._get_max_size(video_clips)
#         resized_clips_paths = []

#         for i, clip in enumerate(video_clips):
#             resized_clip = self._resize_clip(clip, max_size)
#             temp_file_path = os.path.join(self.temporary_process_folder, f"temp_clip_{i}.mp4")
#             resized_clip.write_videofile(temp_file_path, codec="libx264", audio_codec="aac")
#             resized_clips_paths.append(temp_file_path)
#             clip.close()

#         self._concat_videos_ffmpeg(resized_clips_paths, output_path)

#         # Clean up temporary files
#         for file in resized_clips_paths:
#             os.remove(file)
#         os.remove(os.path.join(self.temporary_process_folder, 'input.txt'))

#         return output_path

# import os
# import subprocess
# from moviepy.editor import VideoFileClip

# class VideoAssembler:
#     def __init__(self, files):
#         self.files = files

#     def _get_max_size(self, clips):
#         max_width = max(clip.size[0] for clip in clips)
#         max_height = max(clip.size[1] for clip in clips)
#         return max_width, max_height

#     def _resize_clip(self, clip, size):
#         return clip.resize(newsize=size)

#     def assemble_video(self, output_path):
#         clips = [VideoFileClip(file) for file in self.files]
#         max_size = self._get_max_size(clips)

#         # Resize clips to match the size of the largest clip
#         resized_clips = [self._resize_clip(clip, max_size) for clip in clips]

#         # Save temporary resized clips
#         temp_files = []
#         for i, clip in enumerate(resized_clips):
#             temp_file_path = f"temp_clip_{i}.mp4"
#             clip.write_videofile(temp_file_path, codec="libx264", audio_codec="aac")
#             temp_files.append(temp_file_path)

#         # Construct FFmpeg command for concatenation
#         input_str = ' '.join([f"-i {file}" for file in temp_files])
#         filter_complex_str = ' '.join([f"[{i}:v][{i}:a]" for i in range(len(temp_files))])
#         filter_complex_str += f"concat=n={len(temp_files)}:v=1:a=1"

#         # Use subprocess to execute FFmpeg command
#         subprocess.run(f"ffmpeg {input_str} -filter_complex \"{filter_complex_str}\" -vsync vfr {output_path}", shell=True, check=True)

#         # Clean up temporary files
#         for file in temp_files:
#             os.remove(file)

# Example usage
# files = ['video1.mp4', 'video2.mp4', ...]
# video_assembler = VideoAssembler(files)
# video_assembler.assemble_video('final_video.mp4')

import subprocess
import os

class VideoAssembler:
    def __init__(self, files):
        self.files = files

    def assemble_video(self, output_path):
        # Check if output_path has a directory part and create it if necessary
        directory = os.path.dirname(output_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        # Construct and execute the FFmpeg command
        print("Creating final video...")
        input_str = ' '.join([f"-i {file}" for file in self.files])
        filter_complex_str = ' '.join([f"[{i}:v][{i}:a]" for i in range(len(self.files))])
        filter_complex_str += f"concat=n={len(self.files)}:v=1:a=1"
        
        

        command = f"ffmpeg {input_str} -filter_complex \"{filter_complex_str}\" -vsync vfr {output_path}"
        
        print(f'Executing: {command}')
        
        subprocess.run(command, shell=True, check=True)


# Example usage:
# files = ['video1.mp4', 'video2.mp4', ...]
# video_assembler = VideoAssembler(files)
# video_assembler.assemble_video('final_output.mp4')


