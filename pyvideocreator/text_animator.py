from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip, ColorClip, ImageClip
import numpy as np
import textwrap


from functools import wraps

def fit_within_bounds(func):
    """
    A decorator to ensure that the generated TextClip fits within the video frame.
    """
    @wraps(func)
    def wrapper(animator, text, *args, **kwargs):
        max_width = animator.w - 60  # 20 pixels padding on each side
        max_height = animator.h - 60  # 20 pixels padding top and bottom

        # Generate a dummy clip to measure text dimensions
        dummy_clip = TextClip(text, fontsize=kwargs.get('fontsize', 70), font=kwargs.get('font', 'Gill-Sans-MT-Bold'))

        # Check if text width exceeds max_width
        if dummy_clip.size[0] > max_width:
            # Wrap the text
            wrapped_text = textwrap.fill(text, width=30)  # You might need to adjust the width based on your needs
            dummy_clip = TextClip(wrapped_text, fontsize=kwargs.get('fontsize', 70), font=kwargs.get('font', 'Gill-Sans-MT-Bold'))
            text = wrapped_text

        # Adjust x_offset and y_offset to ensure the text fits within the bounds
        x_offset = kwargs.get('x_offset', 0)
        y_offset = kwargs.get('y_offset', 0)

        if dummy_clip.size[0] + x_offset > max_width-10:
            x_offset = max_width - dummy_clip.size[0]
            kwargs['x_offset'] = x_offset
        
        if dummy_clip.size[1] + y_offset > max_height-10:
            y_offset = max_height - dummy_clip.size[1]
            kwargs['y_offset'] = y_offset

        return func(animator, text, *args, **kwargs)

    return wrapper


def split_text(text, format_type):
    # Define the max line length for each format type
    max_lengths = {
        'standard': 40,  # this is just a guess, adjust as needed
        'short': 25      # this is just a guess, adjust as needed
    }
    
    max_len = max_lengths.get(format_type, 25)
    wrapped_text = textwrap.fill(text, max_len)
    return wrapped_text


def adjust_clip_to_bounds(clip, video_format, margin=20):
    
    video_w, video_h = video_format
    
    # Estimate the clip size
    clip_w, clip_h = clip.size
    
    # Get current position (assuming the position is fixed and not a function)
    clip_x, clip_y = clip.pos(0)
    
    # Check and adjust the x position if it's too close to the edge
    if clip_x + clip_w > video_w - margin:
        clip_x = video_w - margin - clip_w
    elif clip_x < margin:
        clip_x = margin
    
    # Check and adjust the y position if it's too close to the edge
    if clip_y + clip_h > video_h - margin:
        clip_y = video_h - margin - clip_h
    elif clip_y < margin:
        clip_y = margin
    
    return clip.set_position((clip_x, clip_y))



def adjust_position(final_x_pos, final_y_pos, clip_size, format_type, margin=20):
    # Obtener las dimensiones del video
    
    if format_type == 'short':
    
        format_sizes = {
            'standard': (1920, 1080),
            'short': (1080, 1920)
        }
        
        video_w, video_h = format_sizes[format_type]
        clip_w, clip_h = clip_size  # Tamaño del clip/subtítulo
    
    
        # Ajustar x si el subtítulo se sale del margen derecho
        if final_x_pos + clip_w + margin > video_w:
            final_x_pos = video_w - clip_w - margin 
    
        # Ajustar x si el subtítulo se sale del margen izquierdo
        if final_x_pos < margin:
            final_x_pos = margin
        
        # Ajustar y si el subtítulo se sale del margen inferior
        if final_y_pos + clip_h + margin > video_h:
            final_y_pos = video_h - clip_h - margin 
    
        # Ajustar y si el subtítulo se sale del margen superior
        if final_y_pos < margin:
            final_y_pos = margin
            

    return final_x_pos, final_y_pos



class TextAnimator:

    FORMATS = {
        'short': (1080, 1920),
        'standard': (1920, 1080)
    }

    def __init__(self, video_format='standard'):
        self.format_type = video_format
        self.format = self.FORMATS[video_format]
        self.w, self.h = self.format

    # @fit_within_bounds
    def standard_subtitle(self, text, start_time, end_time, fontsize=80,
                          font='Gill-Sans-MT-Bold',
                          color='yellow', stroke_color='black',
                          x_offset=0, y_offset=300,
                          stroke_width=2):
        """Display a standard subtitle at the bottom."""
        
        text = split_text(text, self.format_type)
        
               
        clip = TextClip(text, fontsize=fontsize, color=color, size=self.format, font=font, 
                        stroke_color=stroke_color, stroke_width=stroke_width)
        
        # Calculate the true center position for the text
        text_width, text_height = clip.size
        center_x = (self.w - text_width) / 2
        center_y = (self.h - text_height) / 2
        
        final_x_pos = center_x + x_offset
        final_y_pos = center_y + y_offset
        
       
        # final_x_pos, final_y_pos = adjust_position(final_x_pos, final_y_pos, clip.size, self.format_type)
        
        # print(f'final_y_pos: {final_y_pos}')
        clip = clip.set_position((final_x_pos, final_y_pos)).set_start(start_time).set_end(end_time)
        return clip
    
    # @fit_within_bounds
    def animated_text(self, text, start_time, end_time, fontsize=80,
                      font='Gill-Sans-MT-Bold',
                      color='black', stroke_color='blue',                           
                      x_offset=300, y_offset=-100, 
                      stroke_width=2):
        """Display an animated text moving vertically."""
        
        text = split_text(text, self.format_type)
        
        
        clip = TextClip(text, fontsize=fontsize, color=color, size=self.format, font=font, 
                        stroke_color=stroke_color, stroke_width=stroke_width)
        
        # Calculate the true center position for the text
        text_width, text_height = clip.size
        center_x = (self.w - text_width) / 2 
        center_y = (self.h - text_height) / 2 
        
        final_x_pos = center_x + x_offset
        final_y_pos = center_y + y_offset
        
        
        final_x_pos, final_y_pos = adjust_position(final_x_pos, final_y_pos, clip.size, self.format_type)


        clip = clip.set_position(lambda t: (final_x_pos, final_y_pos + 20*t)).set_start(start_time).set_end(end_time)
        clip = adjust_clip_to_bounds(clip, self.format, margin=20)
        return clip

    # @fit_within_bounds
    def fading_text(self, text, start_time, end_time, fontsize=90,
                    font='Gill-Sans-MT-Bold',
                    color='white', stroke_color='red',                       
                    x_offset=-400, y_offset=-200,
                    stroke_width=2, fade_duration=0.5):
        """Display a text with fade in and fade out effects, aligned to the right."""
        
        text = split_text(text, self.format_type)
        
        
        clip = TextClip(text, fontsize=fontsize, color=color, size=self.format, font=font,
                        stroke_color=stroke_color, stroke_width=stroke_width)
    
        # Calculate the right-aligned position for the text
        text_width, text_height = clip.size
        pos_x = self.w - text_width + x_offset  
        pos_y = (self.h - text_height) / 2 + y_offset
        
        final_x_pos = pos_x
        final_y_pos = pos_y
        
        final_x_pos, final_y_pos = adjust_position(final_x_pos, final_y_pos, clip.size, self.format_type)
      

        clip = (clip.set_position((pos_x, pos_y))
                .set_start(start_time)
                .set_end(end_time)
                .crossfadein(fade_duration)
                .crossfadeout(fade_duration))
    
        clip = adjust_clip_to_bounds(clip, self.format, margin=20)
        return clip


    # @fit_within_bounds
    def text_with_background(self, text, start_time, end_time, fontsize=80, 
                             font='Lucida-Bright-Demibold',
                             color='white', bg_color='blue',
                             x_offset=0, y_offset=0, 
                             stroke_width=2):
        """Display a text with a colored background."""
        
        text = split_text(text, self.format_type)
        
        
        clip = TextClip(text, fontsize=fontsize, color=color, bg_color=bg_color, font=font,
                            size=self.format, align='center')
        
        # Calculate the true center position for the text
        text_width, text_height = clip.size
        center_x = (self.w - text_width) / 2
        center_y = (self.h - text_height) / 2
        
        final_x_pos = center_x
        final_y_pos = center_y
        
        
        final_x_pos, final_y_pos = adjust_position(final_x_pos, final_y_pos, clip.size, self.format_type)
        
        # Set the position, duration, and time of appearance.
        clip = clip.set_position((final_x_pos, final_y_pos)).set_duration(end_time - start_time).set_start(start_time)
        return clip          

    # @fit_within_bounds
    def text_with_tight_background(self, text, start_time, end_time, fontsize=80,
                                   font='Book-Antiqua-Bold',
                                   color='white', bg_color='blue', 
                                   x_offset=0, y_offset=300, 
                                   padding=10, fade_duration=0.5):
        """Display a text with a tight colored background with a fade-in effect."""
        
        text = split_text(text, self.format_type)
        
        # Map of common colors to their RGB values
        color_map = {
            'blue': (0, 0, 255),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            # ... add more as needed
        }
        
        # Ensure the bg_color is in RGB format
        bg_color_rgb = color_map.get(bg_color, bg_color)
    
        # Create a TextClip. You can customize the font, color, etc.
        clip = TextClip(text, fontsize=fontsize, color=color, font=font)
        
        # Calculate the true center position for the text
        text_width, text_height = clip.size
        center_x = (self.w - text_width) / 2 
        center_y = (self.h - text_height) / 2 
        
        txt_w, txt_h = clip.size
        canvas = np.ones((txt_h + 2*padding, txt_w + 2*padding, 3), np.uint8) * np.array(bg_color_rgb, np.uint8)
        
        # Create a ColorClip for the background
        bg_clip = ImageClip(canvas, ismask=False)
        
        final_x_pos = center_x + x_offset
        final_y_pos = center_y + y_offset
        
        # print("Before adjust_position:")
        # print(f"final_x_pos: {final_x_pos}, final_y_pos: {final_y_pos}, text_width: {text_width}, text_height: {text_height}")

        
        final_x_pos, final_y_pos = adjust_position(final_x_pos, final_y_pos, clip.size, self.format_type)

        # print("After adjust_position:")
        # print(f"final_x_pos: {final_x_pos}, final_y_pos: {final_y_pos}")
        
        # Composite both clips
        comp_clip = CompositeVideoClip([
            bg_clip.set_position((final_x_pos, final_y_pos)),
            clip.set_position((final_x_pos, final_y_pos))
        ], size=self.format).set_duration(end_time - start_time).set_start(start_time)
        
        # Apply the crossfadein effect
        comp_clip = comp_clip.crossfadein(fade_duration)
        return comp_clip



    def overlay_on_video(self, video_clip, *text_clips):
        """Overlay the text clips on a video."""
        
        print("Overlaying text clips on video...")
        
        return CompositeVideoClip([video_clip] + list(text_clips))
    

# font = 'DejaVu-Sans-Condensed-Bold-Oblique'
# font = 'Comic-Sans-MS-Bold'
# font_0 = 'DejaVu-Sans' #Bad
# font_1 = 'DejaVu-Sans-Mono' #Malo
# font_2 = 'Gill-Sans-MT-Bold' #Bueno
# font_3 = 'Lucida-Sans-Regular' #Mas o menos
# font_4 = 'Berlin-Sans-FB-Demi-Bold' #Interesante, bonito
# font_5 = 'Tempus-Sans-ITC' #Interesante, 

# font_5 = 'Century' #Bad
# font_0 = 'DejaVu-Sans' #Bad
# font_2 = 'Garamond-Bold' #Usable maquina de escribir
# font_3 = 'Niagara-Solid' #Poco legible
# font_4 = 'Playbill' #Usable West title

# font_5 = 'Agency-FB-Bold' #Usable historieta
# font_0 = 'Bell-MT-Bold' #Malo
# font_2 = 'Blackadder-ITC' #Usar en casos excepcionales Cursiva artístico
# font_3 = 'Bodoni-MT-Bold' #Malo
# font_4 = 'Book-Antiqua-Bold' #Bueno para recuadro

# font_5 = 'Bookman-Old-Style-Bold' #Malo, rígido
# font_0 = 'Broadway' #Malo, bueno para cartel
# font_2 = 'Caladea-Bold' #Regular
# font_3 = 'Californian-FB-Bold' #Aceptable
# font_4 = 'Cambria-Bold' #Bueno

# font_5 = 'Gill-Sans-MT-Bold' 
# font_0 = 'Gill-Sans-MT-Bold' 
# font_2 = 'Gill-Sans-MT-Bold' 
# font_3 = 'Lucida-Bright-Demibold' 
# font_4 = 'Book-Antiqua-Bold' 

# video = VideoFileClip("news_2023-10-06_final_1.mp4")
# animator = TextAnimator(video_format='standard')

# subtitle = animator.standard_subtitle("This is a subtitle.", 5, 10, font=font_5)
# animated = animator.animated_text("Animated text!", 12, 18, font=font_0)
# fading = animator.fading_text("Text with Fades", 20, 24, font=font_2)
# bg_text = animator.text_with_background("Text with background", 26, 30, font=font_3)
# bg_text_t = animator.text_with_tight_background("Text with tight background", 32, 40, font=font_4)


# final_video = animator.overlay_on_video(video, subtitle, animated, fading, bg_text, bg_text_t)
# final_video.write_videofile("output.mp4")


