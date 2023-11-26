# pyvideocreator
PyVideoCreator simplifies video production with tools for assembling clips, adding subtitles, integrating AI-generated images, and creating voice-overs. Perfect for content creators and developers, it's a versatile toolkit for enhancing and streamlining video editing tasks across platforms.


## Installation

Make sure you use python 3.11 or higher.
Since PyPI is temporarily not accepting new user registrations, you can install PyVideoCreator directly from the source using the following steps:
1. Clone the GitHub repository:
```
git@github.com:eramireztorres/pyvideocreator.git
cd pyvideocreator
```
2. Clone the GitHub repository:
```
python setup.py install
```

This method will install PyVideoCreator and its dependencies on your system.

## Usage

Here's a step-by-step guide to using PyVideoCreator:

1. **Generating Images**

Utilize OpenAIImageGenerator for AI-generated images or PexelsRequester for sourcing images from Pexels.

```python
import os
from pyvideocreator.gpt_image import OpenAIImageGenerator
from pyvideocreator.pxls import PexelsRequester

# For OpenAI images
openai_api_key = os.getenv("OPENAI_API_KEY")
image_generator = OpenAIImageGenerator(api_key=openai_api_key)
image_path = some_output_image_path
image_url = image_generator.generate_image("A  Dendrobatidae frog")
download_status = image_generator.download_image(image_url, image_path)

# For Pexels images
pexels_api_key = "YOUR_PEXELS_API_KEY"
pexels_image_generator = PexelsRequester(pexels_api_key)
image_path = some_output_image_path
folder_path='pexels_images'
image_data = pexels_image_generator.get_images_by_query(query='Terrier Dog')
filtered_images = filter_by_aspect_ratio('standard', image_data, filetype="photos")
first_image_url = filtered_images[0]['src']['original'] 
pexels_image_generator.save_image(first_image_url, folder_path=folder_path, filename=image_path)
```

2. Creating Video from Images

Create videos from images using ImageVideoCreator.
```
from pyvideocreator.image_to_clip import ImageVideoCreator

image_dict = {
     'clip_1': {'clip': 'path_to_some_image.jpg', 'duration': 15}
}

creator = ImageVideoCreator(output_video="output.mp4", width=1920, height=1080, fps=30)
creator.create_video(image_dict, anim_type='panning', panning_speed=0.6)

```

3. Adding Subtitles

Use VideoSubtitler to add subtitles to your video.
```
from pyvideocreator.video_subtitler import VideoSubtitler, SubtitleStyler

video_info = {
    'clip': 'path_to_some_video.mp4',
    'subtitles': 'path_to_subtitles.vtt'
}

styler = SubtitleStyler('path_to_subtitles.vtt')
subtitler = VideoSubtitler(video_info, styler=styler)
subtitler.add_subtitles_and_export("output_with_subtitles.mp4")
```

4. Adding Voice-Over

Generate voice-over for your video using VideoVoiceOver.
```
from pyvideocreator.video_voicer import VideoVoiceOver

clip_info = {
    'clip': 'path_to_video_with_subtitles.mp4',
    'subtitles': 'path_to_subtitles.vtt',
    'voice': 'alloy'
}

voice_over = VideoVoiceOver(clip_info)
voice_over.add_voice_over_with_pauses("final_video_with_voice.mp4")

```

5. Assembling the Final Video

Combine multiple video clips into a single video with VideoAssembler.
```
from pyvideocreator.video_assembler import VideoAssembler

files = ['video_clip_1.mp4', 'video_clip_2.mp4', 'video_clip_3.mp4']
video_assembler = VideoAssembler(files, transition_duration=0.5)
video_assembler.assemble_video("final_assembled_video.mp4")

```

## License

PyVideoCreator is licensed under the MIT License.