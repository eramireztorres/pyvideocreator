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
1. Generating Images

Utilize the OpenAIImageGenerator for AI-generated images or PexelsRequester for sourcing images from Pexels.
```
from pyvideocreator import OpenAIImageGenerator, PexelsRequester

# For OpenAI images
openai_api_key = "YOUR_OPENAI_API_KEY"
image_generator = OpenAIImageGenerator(api_key=openai_api_key)

# For Pexels images
pexels_api_key = "YOUR_PEXELS_API_KEY"
pexels_image_generator = PexelsRequester(pexels_api_key)
```

2. Creating Video from Images

Create videos from images using ImageVideoCreator.
```
from pyvideocreator import ImageVideoCreator

image_dict = {
     'clip_1': {'clip': replace_with_some_image_path, 'duration': 15}
}

creator = ImageVideoCreator(output_video="output.mp4", width=1920, height=1080, fps=30)
creator.create_video(image_dict, anim_type='panning', panning_speed=0.6)

```

3. Adding Subtitles

Use VideoSubtitler to add subtitles to your video.
```
from pyvideocreator import VideoSubtitler, SubtitleStyler

video_info = {
    'clip': replace_with_some_mp4_video_path,
    'subtitles': replace_with_some_vtt_subtitles_path
}

subtitler = VideoSubtitler(video_info, styler=SubtitleStyler("subtitles_file.vtt"))
subtitler.add_subtitles_and_export("output_with_subtitles.mp4")

```

4. Adding Voice-Over

Generate voice-over for your video using VideoVoiceOver.
```
from pyvideocreator import VideoVoiceOver

clip_info = {
    'clip': replace_with_some_mp4_video_path,
    'subtitles': replace_with_some_vtt_subtitles_path,
    'voice': 'alloy'    
}

voice_over = VideoVoiceOver(clip_info)
voice_over.add_voice_over_with_pauses("final_video_with_voice.mp4")

```

5. Assembling the Final Video

Combine multiple video clips into a single video with VideoAssembler.
```
from pyvideocreator import VideoAssembler

video_assembler = VideoAssembler(files, transition_duration=0.5)
video_assembler.assemble_video("final_assembled_video.mp4")
```

## License

PyVideoCreator is licensed under the MIT License.