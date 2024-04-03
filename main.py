import boto3
import docx
import time
import re  # Required for cleaning special characters from chapter titles
import os  # Needed for file path operations

# Configuration section for AWS and local setup
output_bucket = 'echotales'  # Specify your S3 output bucket name
voice_id = 'Danielle'  # Specify the voice ID for text-to-speech
engine = 'long-form'  # Use long form engine for high-quality speech synthesis
output_format = 'mp3'  # Set the output format of synthesized audio
local_directory = r'C:\Users\Guibson\Documents\AudioBooks\MobyDick\audiosBrutos'  # Local directory to save audio files


def clean_title(title):
    """
    Cleans the chapter title to be used as S3 key prefix.

    Args:
        title (str): The original chapter title.

    Returns:
        str: A cleaned version of the chapter title suitable for S3 keys.
    """
    cleaned_title = re.sub(r"[^0-9a-zA-Z!\-_.*'()]+", '_', title)
    return cleaned_title.strip('_')


def extract_chapters(docx_path):
    """
    Extracts chapters from a .docx file based on chapter titles.

    Args:
        docx_path (str): Path to the .docx file containing the book text.

    Returns:
        dict: A dictionary with chapter titles as keys and their texts as values.
    """
    doc = docx.Document(docx_path)
    full_text = [paragraph.text for paragraph in doc.paragraphs]
    chapters = {}
    current_chapter = None
    for text in full_text:
        if text.startswith('CHAPTER'):
            current_chapter = text.strip()
            chapters[current_chapter] = text
        elif current_chapter:
            chapters[current_chapter] += ' ' + text
    return chapters


def download_audio(s3_client, bucket, s3_key, local_path):
    """
    Downloads an audio file from S3 to a local file.

    Args:
        s3_client: The boto3 S3 client.
        bucket (str): The name of the S3 bucket.
        s3_key (str): The S3 key for the audio file.
        local_path (str): The local path where the audio file should be saved.
    """
    try:
        s3_client.download_file(bucket, s3_key, local_path)
        print(f"Downloaded audio to {local_path}")
    except boto3.exceptions.Boto3Error as e:
        print(f"An error occurred while downloading {s3_key}: {e}")


def synthesize_chapter(chapter_text, chapter_title, s3_client):
    """
    Synthesizes speech from the provided chapter text and saves it in S3.

    Args:
        chapter_text (str): The text of the chapter to synthesize.
        chapter_title (str): The title of the chapter.
        s3_client: The boto3 S3 client used for downloading the audio file.

    Returns:
        str: The S3 URI of the generated audio file.
    """
    session = boto3.Session()
    polly_client = session.client('polly')
    clean_chapter_title = clean_title(chapter_title)

    try:
        response = polly_client.start_speech_synthesis_task(
            Text=chapter_text,
            VoiceId=voice_id,
            Engine=engine,
            OutputFormat=output_format,
            OutputS3BucketName=output_bucket,
            OutputS3KeyPrefix=f"{clean_chapter_title}/",
        )

        task_status = 'inProgress'
        task_id = response['SynthesisTask']['TaskId']
        while task_status not in ['completed', 'failed']:
            time.sleep(5)
            task = polly_client.get_speech_synthesis_task(TaskId=task_id)
            task_status = task['SynthesisTask']['TaskStatus']

        if task_status == 'completed':
            time.sleep(10)
            print(f"Audio for {chapter_title} successfully generated and saved in S3.")
            s3_key = task['SynthesisTask']['OutputUri'].split('/')[-1]
            local_path = os.path.join(local_directory, f"{clean_chapter_title}.mp3")
            download_audio(s3_client, output_bucket, f"{clean_chapter_title}/{s3_key}", local_path)
            return task['SynthesisTask']['OutputUri']
        else:
            print(f"Task for {chapter_title} not completed due to: {task_status}")
            return None
    except boto3.exceptions.Boto3Error as e:
        print(f"An error occurred for {chapter_title}: {e}")
        return None


# Main execution process
s3_client = boto3.client('s3')  # Initialize an S3 client for downloading files
docx_path = 'mobyDick.docx'  # Update this path to your .docx file location
chapters = extract_chapters(docx_path)

for chapter_title, chapter_text in chapters.items():
    audio_url = synthesize_chapter(chapter_text, chapter_title, s3_client)
    if audio_url:
        print(f"Audio for {chapter_title} generated and saved in S3. URL: {audio_url}")
    else:
        print(f"Failed to generate audio for {chapter_title}")
