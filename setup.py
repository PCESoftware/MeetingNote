from setuptools import setup, find_packages

setup(
    name='meeting_note',
    version='1.0.0',
    description='A Whisper + ChatGPT Demo for meeting note recording and summarization',
    author='Scihacker',
    author_email='sjtuzlp@gmail.com',
    url='https://github.com/scihacker/MeetingNote',
    packages=find_packages(),
    install_requires=[
        "openai==1.25.0",
        "pyaudio",
        "wave",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)