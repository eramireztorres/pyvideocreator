import cv2
from PIL import Image
import numpy as np

class ImageVideoCreator:
    def __init__(self, output_video, width, height, fps):
        self.output_video = output_video
        self.width = width
        self.height = height
        self.fps = fps

    def _apply_panning(self, img, total_frames, panning_speed):
        new_width = int(self.width * 1.1)
        img_resized = img.resize((new_width, self.height), Image.ANTIALIAS)
        for i in range(total_frames):
            offset = int(i * (new_width - self.width) / total_frames * panning_speed)
            yield img_resized.crop((offset, 0, offset + self.width, self.height))

    def _apply_zoom(self, img, total_frames, zoom_factor, zoom_in=True):
        for i in range(total_frames):
            zoom = 1 + i * (zoom_factor - 1) / total_frames if zoom_in else zoom_factor - i * (zoom_factor - 1) / total_frames
            new_size = (int(self.width * zoom), int(self.height * zoom))
            img_resized = img.resize(new_size, Image.ANTIALIAS)
            offset_x = (img_resized.width - self.width) // 2
            offset_y = (img_resized.height - self.height) // 2
            yield img_resized.crop((offset_x, offset_y, offset_x + self.width, offset_y + self.height))

    def _fade_transition(self, frame, prev_frame, i, fade_frames):
        if prev_frame is not None and i < fade_frames:
            alpha = i / fade_frames
            return cv2.addWeighted(prev_frame, 1 - alpha, frame, alpha, 0)
        return frame

    def create_video(self, image_dict, anim_type='panning', panning_speed=0.2, zoom_factor=1.1, fade_duration=1):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.output_video, fourcc, self.fps, (self.width, self.height))

        prev_frame = None
        fade_frames = int(self.fps * fade_duration)

        for image_info in image_dict.values():
            img = Image.open(image_info['clip'])
            frames_for_image = int(self.fps * image_info['duration'])

            if anim_type == 'panning':
                frame_generator = self._apply_panning(img, frames_for_image, panning_speed)
            elif anim_type == 'zoom_in':
                frame_generator = self._apply_zoom(img, frames_for_image, zoom_factor, zoom_in=True)
            elif anim_type == 'zoom_out':
                frame_generator = self._apply_zoom(img, frames_for_image, zoom_factor, zoom_in=False)
            else:
                frame_generator = [img.resize((self.width, self.height), Image.ANTIALIAS)] * frames_for_image

            for i, cropped_img in enumerate(frame_generator):
                frame = np.array(cropped_img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                frame = self._fade_transition(frame, prev_frame, i, fade_frames)
                prev_frame = frame.copy()
                out.write(frame)

        out.release()
        cv2.destroyAllWindows()

# # Usage example
# image_dict = {
#     # 'clip1': {'clip': 'C:/Users/Erick/trabajo/_ trabajo alcala/ML/python/ai_channel/trivia_images/imagen_generada_4 (4).png', 'duration': 15},
#     'clip2': {'clip': 'C:/Users/Erick/trabajo/_ trabajo alcala/ML/python/ai_channel/trivia_images/imagen_generada_1 (4).png', 'duration': 10}
# }

# creator = ImageVideoCreator(output_video='output_3.mp4', width=1920, height=1080, fps=30)
# creator.create_video(image_dict, anim_type='panning', panning_speed=0.6)
