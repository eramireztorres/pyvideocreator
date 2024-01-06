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

## Dependencies

Apart from the Python packages installed by default, this project also depends on `edge-tts`. 

To install `edge-tts`, run the following command:

```bash
pip install edge-tts
```

## Additional Dependency: FFmpeg

PyVideoCreator requires FFmpeg for video processing. Please ensure that FFmpeg is installed on your system.
Windows:

1. Download FFmpeg from FFmpeg's official website.
2. Extract the downloaded ZIP file.
3. Add the path to the extracted FFmpeg bin folder (e.g., C:\ffmpeg\bin) to your system's PATH environment variable.

macOS:
    
1. Install Homebrew if it's not already installed.
2. Install FFmpeg using Homebrew:

```
brew install ffmpeg
```

Linux:

FFmpeg can be installed from the default repositories on most Linux distributions:

```
sudo apt-get update
sudo apt-get install ffmpeg
```
(Note: The above commands are for Debian/Ubuntu. Please adjust for other distributions.)

After installing FFmpeg, you can verify the installation by running ffmpeg -version in your command line or terminal.

## Additional Requirement for Windows Users: PowerShell

PyVideoCreator requires PowerShell to be installed on Windows systems for certain functionalities. Follow these steps to install and configure PowerShell:

1. **Checking PowerShell Version:**
   - First, check if you have PowerShell installed and its version. PowerShell 5.1 or higher is recommended for optimal compatibility.
   - Open a Command Prompt and type `powershell` followed by `$PSVersionTable.PSVersion`. This will display the PowerShell version.

2. **Installing or Updating PowerShell:**
   - If PowerShell is not installed or you need to update it, download the latest version from the [official PowerShell GitHub repository](https://github.com/PowerShell/PowerShell).
   - Choose the appropriate installer for your version of Windows (Windows 7/8/10/11).

3. **Installing PowerShell via Windows Features (Optional):**
   - For Windows 10 and later, PowerShell can also be installed via Windows Features.
   - Navigate to 'Control Panel' > 'Programs' > 'Turn Windows features on or off'.
   - Check the box for 'Windows PowerShell' and click 'OK'. Follow the prompts to complete the installation.

4. **Setting Execution Policy (If Required):**
   - Some PowerShell scripts require setting the execution policy.
   - Open PowerShell as an administrator and run `Set-ExecutionPolicy RemoteSigned` or a policy level that suits your security needs.

5. **Verifying Installation:**
   - After installation, verify by opening PowerShell and typing `$PSVersionTable.PSVersion`.

Please ensure that PowerShell is properly installed and configured on your Windows system to utilize all features of PyVideoCreator.


## Usage

Here's a step-by-step guide to using PyVideoCreator:

1. **Generating Images**

Utilize OpenAIImageGenerator for AI-generated images or PexelsRequester for sourcing images from Pexels.

```python
import os
from pyvideocreator.gpt_image import OpenAIImageGenerator
from pyvideocreator.pxls import PexelsRequester

# For OpenAI images
openai_api_key = os.getenv("OPENAI_API_KEY") #Write your API key manually if not in the environment
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