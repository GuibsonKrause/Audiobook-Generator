
# Universal Audiobook Generator

## Overview
This Python script is designed to transform any book into a series of audiobook chapters, with "Moby Dick" by Herman Melville serving as our primary example. Leveraging Amazon Polly's text-to-speech service, the script automates the synthesis of each chapter into individual audio files. These files are then organized and stored in an Amazon S3 bucket, with options to download them locally for offline listening.

## Features
- Automated extraction of book chapters from `.docx` format.
- High-quality, long-form network-based text-to-speech synthesis using Amazon Polly.
- Organized storage of audio files in Amazon S3, categorized by chapters.
- Easy local download of the generated audiobook chapters.

## Prerequisites
Before starting, you'll need:
- An AWS account with permissions for Amazon Polly and S3.
- Python 3.6 or later installed on your computer.
- Installation of required Python packages: `boto3`, `docx`, `re`, `os`.

## Configuration
First, configure your AWS credentials. This can be done via the AWS CLI or by manually editing your AWS credentials file.

## Usage
1. Clone this repository to your local environment.
2. Run `pip install boto3 python-docx` to install necessary Python libraries.
3. Place the `.docx` document of your book in the project's root directory.
4. Adapt the script configuration to include your AWS settings, the Polly voice ID of your choice, and the path for downloading the audio files.
5. Execute the script with `python main.py` to start generating your audiobook.

## Contributing
Contributions are welcome! Feel free to fork this repo, make your improvements, and propose changes through a pull request.

## License
This project is open-source under the MIT License. See LICENSE file for more details.

## Acknowledgements
- Thanks to Herman Melville for "Moby Dick", the example used to demonstrate this project's capabilities.
- Amazon Web Services for the Polly and S3 services that power our audiobook transformations.
