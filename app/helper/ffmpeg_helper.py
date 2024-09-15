from app.utils import SystemUtils


def resolution_to_format(width, height):
    # 根据分辨率宽度返回常见格式名称
    if width <= 640:
        return "480p"
    elif width <= 1280:
        return "720p"
    elif width <= 1920:
        return "1080p"
    elif width <= 2560:
        return "2K"
    elif width <= 3840:
        return "4K"
    elif width <= 7680:
        return "8K"
    else:
        return "Unknown resolution"


class FfmpegHelper:
    def get_thumb_image_from_video(video_path, image_path, frames="00:03:01"):
        """
        使用ffmpeg从视频文件中截取缩略图
        """
        if not video_path or not image_path:
            return False
        cmd = 'ffmpeg -i "{video_path}" -ss {frames} -vframes 1 -f image2 "{image_path}"'.format(video_path=video_path,
                                                                                                 frames=frames,
                                                                                                 image_path=image_path)
        result = SystemUtils.execute(cmd)
        if result:
            return True
        return False

    @staticmethod
    def get_audio_video_codec(video_path):
        if not video_path:
            return {
                'audio_codec': 'aac',
                'video_codec': 'h264',
                'resource_pix': ""
            }

        video_cmd = ('ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of '
                     'default=noprint_wrappers=1:nokey=1 "{input_file}"').format(input_file=video_path)
        audio_cmd = ('ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of '
                     'default=noprint_wrappers=1:nokey=1 "{input_file}"').format(
            input_file=video_path)
        resolution_cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
        'stream=width,height', '-of', 'json', video_path
    ]

        video_result = SystemUtils.execute(video_cmd)
        audio_result = SystemUtils.execute(audio_cmd)
        resource_result = SystemUtils.execute_get_json(resolution_cmd)
        width = resource_result['streams'][0]['width']
        height = resource_result['streams'][0]['height']
        resource_pix = resolution_to_format(width, height)

        if video_result and audio_result:
            return {
                'audio_codec': audio_result,
                'video_codec': video_result,
                'resource_pix': resource_pix
            }

        return {
            'audio_codec': 'aac',
            'video_codec': 'h264',
            'resource_pix': resource_pix
        }

