from moviepy import VideoFileClip, vfx
import os


def convert_video_to_gif(
    input_path,
    output_path,
    start_time=None,
    end_time=None,
    speed_factor=1.0,
    resize_width=480,
    fps=12
):
    clip = None
    try:
        if not os.path.isfile(input_path):
            print(f"Error: Input file not found: {input_path}")
            return False

        if not output_path.lower().endswith(".gif"):
            print(f"Error: output_path must end with .gif (got {output_path})")
            return False

        if speed_factor <= 0:
            print(f"Error: speed_factor must be > 0 (got {speed_factor})")
            return False

        if start_time is not None and start_time < 0:
            print(f"Error: start_time must be >= 0 (got {start_time})")
            return False

        if end_time is not None and end_time < 0:
            print(f"Error: end_time must be >= 0 (got {end_time})")
            return False

        if start_time is not None and end_time is not None and start_time >= end_time:
            print("Error: start_time must be < end_time")
            return False

        out_dir = os.path.dirname(os.path.abspath(output_path))
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        clip = VideoFileClip(input_path)

        if start_time is not None or end_time is not None:
            clip = clip.subclipped(
                start_time if start_time is not None else 0,
                end_time
            )

        if speed_factor != 1.0:
            clip = clip.with_effects([vfx.MultiplySpeed(speed_factor)])

        if resize_width is not None:
            clip = clip.resized(width=resize_width)

        clip.write_gif(output_path, fps=fps, logger=None)

        print(f"Successfully converted to GIF: {output_path}")
        return True

    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

    finally:
        if clip is not None:
            try:
                clip.close()
            except Exception:
                pass
