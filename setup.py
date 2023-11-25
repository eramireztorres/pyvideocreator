from setuptools import setup, find_packages

setup(
    name='pyvideocreator',
    version='0.1.0',
    author='Erick Eduardo Ramirez Torres',
    author_email='erickeduardoramireztorres@gmail.com',
    description='PyVideoCreator simplifies video production with tools for assembling clips, adding subtitles, integrating AI-generated images, and creating voice-overs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eramireztorres/pyvideocreator',
    packages=find_packages(),
    install_requires=[
        'moviepy==1.0.3',
        'openai==1.3.3',
        'opencv-python',
        'Pillow==9.4.0',
        'joblib',
        'pydub==0.25.1',
        'decorator==4.4.2'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Multimedia :: Video :: Editing',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.7',
    keywords='video editing, moviepy, openai, computer vision, python'
)


