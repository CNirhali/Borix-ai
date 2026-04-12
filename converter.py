import sys
import os
from PIL import Image
import imageio
import numpy as np

def convert_webp_to_mp4(webp_path, output_path, fps=5):
    """
    Converts an animated .webp file to an .mp4 video.
    Note: FPS is set to 5 by default as webp animations from agents are usually low framerate.
    """
    print(f"Converting {webp_path} to {output_path}...")
    try:
        img = Image.open(webp_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return
        
    frames = []
    try:
        while True:
            # We must convert the frame to RGB because mp4/h264 usually drops alpha channels
            frame = img.convert('RGB')
            frames.append(np.array(frame))
            img.seek(img.tell() + 1)
    except EOFError:
        pass # Reached the end of the webp frames
    
    if not frames:
        print("No frames found or not an animated webp!")
        return
        
    print(f"Extracted {len(frames)} frames. Encoding to MP4...")
    
    try:
        writer = imageio.get_writer(output_path, fps=fps, macro_block_size=None)
        for frame_data in frames:
            writer.append_data(frame_data)
        writer.close()
        print(f"Successfully created: {output_path}!")
    except Exception as e:
        print(f"Error writing MP4: {e}")

def convert_webp_to_png(webp_path, output_path):
    """
    Extracts the first frame of a .webp file and saves it as a high-quality .png.
    """
    print(f"Converting {webp_path} to {output_path}...")
    try:
        img = Image.open(webp_path)
        img.convert('RGBA').save(output_path, 'PNG')
        print(f"Successfully created: {output_path}!")
    except Exception as e:
        print(f"Error creating PNG: {e}")

def convert_webp_to_gif(webp_path, output_path, fps=5):
    """
    Converts an animated .webp file to a .gif video.
    """
    print(f"Converting {webp_path} to {output_path}...")
    try:
        img = Image.open(webp_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return
        
    frames = []
    try:
        while True:
            # Convert to RGB to ensure clean gif palette compilation 
            frames.append(img.convert('RGB'))
            img.seek(img.tell() + 1)
    except EOFError:
        pass # Reached the end
        
    if not frames:
        print("No frames found!")
        return
        
    print(f"Extracted {len(frames)} frames. Encoding to GIF...")
    duration = int(1000 / fps)
    
    try:
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0
        )
        print(f"Successfully created: {output_path}!")
    except Exception as e:
        print(f"Error writing GIF: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python converter.py <input.webp> <output>")
        print("Example 1: python converter.py demo.webp output.mp4")
        print("Example 2: python converter.py demo.webp output.png")
        print("Example 3: python converter.py demo.webp output.gif")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)
    
    if output_file.lower().endswith('.mp4'):
        convert_webp_to_mp4(input_file, output_file)
    elif output_file.lower().endswith('.png'):
        convert_webp_to_png(input_file, output_file)
    elif output_file.lower().endswith('.gif'):
        convert_webp_to_gif(input_file, output_file)
    else:
        print("Error: Unsupported output format. Please use an extension of '.mp4', '.gif', or '.png'.")
