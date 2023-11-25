
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
# from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips

class VideoAssembler:
    def __init__(self, files, transition_duration=1):
        self.files = files
        self.transition_duration = transition_duration

    def _get_max_size(self, clips):
        max_width = max(clip.size[0] for clip in clips)
        max_height = max(clip.size[1] for clip in clips)
        return max_width, max_height

    def _resize_clip(self, clip, size):
        return clip.resize(newsize=size)

    def assemble_video(self, output_path):
        clips = [ImageClip(file).set_duration(5) if file.endswith(('png', 'jpg', 'jpeg')) else VideoFileClip(file) for file in self.files]
        max_size = self._get_max_size(clips)
        resized_clips = [self._resize_clip(clip, max_size) for clip in clips]
        fps = next((clip.fps for clip in resized_clips if isinstance(clip, VideoFileClip)), 24)

        final_clips = []
        for i, clip in enumerate(resized_clips):
            if i > 0:
                # Apply crossfade transition directly
                clip = clip.crossfadein(self.transition_duration)
            final_clips.append(clip)

        final_video = concatenate_videoclips(final_clips, method="compose", padding=-self.transition_duration)
        final_video.write_videofile(output_path, fps=fps, codec="libx264", audio_codec="aac")

# Example usage
# files = ['video1.mp4', 'video2.mp4', 'video3.mp4']
# video_assembler = VideoAssembler(files, transition_duration=1)
# video_assembler.assemble_video('final_video.mp4')




