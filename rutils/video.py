import subprocess, math
from pathlib import Path
import cv2
from PIL import Image
import pymediainfo


class VideoReader(object):
    def __init__(self, in_video_path: Path = None):
        self.video_path = in_video_path
        self._video = None
        self.fps = None
        self.w = None
        self.h = None
        self.fps_mode = None
        self.video_bitrate = None
        self.encode_format = None
        self.num_frame = None
        self.frame_id = None

        if in_video_path:
            self.load(in_video_path)

    def load(self, in_video_path):
        self.release()
        self.video_path = in_video_path
        if not Path(in_video_path).exists():
            raise IOError(
                'There is no {}, please check again'.format(in_video_path))
        self._video = cv2.VideoCapture(in_video_path)

        self.fps = self._video.get(cv2.CAP_PROP_FPS)
        self.w = int(self._video.get(3))
        self.h = int(self._video.get(4))
        self.num_frame = int(self._video.get(cv2.CAP_PROP_FRAME_COUNT))

    def parse_mediainfo(self):
        # TODO: pymediainfo has multi threading bug, cannot use in multi threading!
        video_info = pymediainfo.MediaInfo.parse(self.video_path)
        for track in video_info.tracks:
            if track.track_type == 'Video':
                self.fps_mode = track.frame_rate_mode
                self.video_bitrate = track.bit_rate
                self.encode_format = track.format

    def set_start_frame(self, frame_id):
        self._video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)

    def get_next_frame(self):
        rev, frame = self._video.read()
        if rev:
            return frame
        else:
            return None

    def release(self):
        if self._video:
            self._video.release()
            self._video = None


class VideoWriter(object):
    """[summary]

    Arguments:
        object {[type]} -- [description]
    """
    def __init__(self,
                 out_path,
                 video_w,
                 video_h,
                 fps=25,
                 encoding='H264',
                 video_bitrate='11M',
                 mode='ffmpeg'):
        self._mode = mode
        self._w = video_w
        self._h = video_h
        self._fps = fps
        if mode == 'opencv':
            self._video = cv2.VideoWriter(out_path,
                                          cv2.VideoWriter_fourcc(*encoding),
                                          self._fps, (self._w, self._h))
        else:
            self._pipeline = subprocess.Popen(
                'ffmpeg -loglevel warning -y -f image2pipe -vcodec png -r {fps} -i - -vcodec h264 -profile:v high -level:v 5 -refs 6 -q:v 0 -r {fps} -b:v {bitrate} -pix_fmt yuv420p {out_path}'
                .format(fps=self._fps,
                        bitrate=video_bitrate,
                        out_path=out_path),
                stdin=subprocess.PIPE,
                shell=True)

    def write_frame(self, frame):
        assert (frame.shape[1] == self._w and frame.shape[0] == self._h)
        if self._mode == 'opencv':
            self._video.write(frame)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame.save(self._pipeline.stdin, 'PNG')

    def release(self):
        if self._mode == 'opencv':
            self._video.release()
        else:
            self._pipeline.stdin.close()
            self._pipeline.wait()


class FrameReader(object):
    def __init__(self, frame_dir):
        self._frame_dir = Path(frame_dir)

    def get_frame(self, frame_id):
        img_path = self._frame_dir / 'frm_{}.jpg'.format(frame_id)
        if not img_path.exists():
            return None
        frame = cv2.imread(img_path.as_posix())
        return frame


# def split_video_frame_sequence(start_frame_id, end_frame_id, num_parts):
#     num_frames = end_frame_id - start_frame_id + 1
#     num_each_part = math.floor(num_frames / num_parts)
#     start_end_frame_ids = [[
#         start_frame_id + i * num_each_part,
#         start_frame_id + (i + 1) * num_each_part
#     ] for i in range(num_parts - 1)]
#     start_end_frame_ids.append([
#         start_frame_id + (num_parts - 1) * num_each_part,
#         start_frame_id + num_frames
#     ])
#     return start_end_frame_ids

# def concat_video(video_paths, tmp_dir, out_video_path):
#     concat_txt = Path(tmp_dir) / '{}.txt'.format(get_current_strtime())
#     with concat_txt.open('w', encoding='utf-8') as f:
#         for video_path in video_paths:
#             f.write('file {}\n'.format(video_path))
#     command = 'ffmpeg -loglevel warning -y -f concat -safe 0 -i {} -c copy {}'.format(
#         concat_txt.as_posix(), out_video_path)
#     run_command(command)
#     concat_txt.unlink()
