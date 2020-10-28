from pathlib import Path
import rutils

if __name__ == '__main__':
    in_video_path = Path('./test.mp4')
    out_video_path = Path('./test-out.mp4')
    video_reader = rutils.video.VideoReader(in_video_path)
    video_writer = rutils.video.VideoWriter(out_video_path,
                                            video_reader.w,
                                            video_reader.h,
                                            mode='opencv')
    print(video_reader.num_frames)
    for idx in range(video_reader.num_frames):
        frame = video_reader.get_next_frame()
        video_writer.write_frame(frame)
