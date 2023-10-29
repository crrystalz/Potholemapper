import os
from moviepy.editor import VideoFileClip, clips_array

def concatenate_videos(input_dir, output_file):
    video_files = [f for f in os.listdir(input_dir) if f.endswith('.mp4')]
    video_clips = [VideoFileClip(os.path.join(input_dir, file)) for file in video_files]

    final_video = clips_array([[clip] for clip in video_clips])
    final_video.write_videofile(output_file, codec="libx264")

if __name__ == "__main__":
    input_directory = f"C:\Users\rrishi\Desktop\Newfolder"
    output_file = "output.mp4"

    concatenate_videos(input_directory, output_file)
