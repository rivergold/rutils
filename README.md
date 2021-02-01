# rutils

Utils for computer vision

## Modules

### Common

#### str2path

```shell
from argparse import ArgumentParser
from rutils.common import str2path

opt_parser = ArgumentParser()
opt_parser.add_argument('--txt_path', type=str2path)
opt = opt_parser.parse_args()
print(type(opt.txt_path))
```

#### Run command

```python
from rutils.common import run_command

command = 'echo "Run command example"'
run_command(command)
```

### Video

#### Read video

```python
video_path = Path('./test.mp4')
video_reader = rutils.video.VideoReader(in_video_path=video_path)
print(video_reader.num_frames)
for _ in range(num_frames):
    frame = video_reader.get_next_frame()
```

#### Write video

Support two method:

- Use OpenCV

```python
video_writer = rutils.video.VideoWriter(
    out_path,
    video_w,
    video_h,
    fps=25,
    encoding='H264',
    video_bitrate='11M',
    mode='opencv'
)
video_writer.write_frame(frame)
video_writer.release()
```

- Use FFMpeg

```python
video_writer = rutils.video.VideoWriter(
    out_path,
    video_w,
    video_h,
    fps=25,
    encoding='H264',
    video_bitrate='11M',
    mode='ffmpeg'
)
video_writer.write_frame(frame)
video_writer.release()
```
