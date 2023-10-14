import cv2
import os
# from esrgan_pytorch import ESRGAN


class Frames():
    PATH_TO_SAVE = R"C:\Users\Dima\Desktop\Repositories\HackathonAI\web\user-tmp-files"
    dir_id = 0
    # def __init__(self) -> None:
    #     self.model = ESRGAN()

    def get_dir_name():
        Frames.dir_id += 1
        return f"frames_{Frames.dir_id:05d}"
    
    def save_frames(self, video_path, start_time, end_time) -> str:
        """
            Возвращает путь до папки извлеченных изображений
        """
        # Откройте видеофайл
        video_capture = cv2.VideoCapture(video_path)

        # Убедитесь, что начальное и конечное время находятся в пределах длительности видео
        video_length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_rate = int(video_capture.get(cv2.CAP_PROP_FPS))
        if start_time < 0:
            start_time = 0
        print(video_length, frame_rate)
        if end_time >= video_length / frame_rate:
            end_time = video_length / frame_rate

        # Переместитесь к начальному времени
        video_capture.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)

        # Извлеките 5 кадров с равным интервалом
        interval = (end_time - start_time) / 4
        frame_number = 0

        res_dir = Frames.get_dir_name()
        os.mkdir(Frames.PATH_TO_SAVE+fR'\{res_dir}')
        while frame_number < 5:
            ret, frame = video_capture.read()

            if not ret:
                break

            # Здесь можно сохранить кадр в файл или выполнять другую обработку
            # Например, сохранить кадр в файл формата .jpg
            frame_filename = Frames.PATH_TO_SAVE+fR'\{res_dir}\frame_{frame_number:05d}.jpg'
            # enhanced_image = self.model.enhance(frame)
            cv2.imwrite(frame_filename, frame)

            frame_number += 1

            # Переместитесь к следующему кадру с заданным интервалом
            start_time += interval
            video_capture.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)

        # Освободите ресурсы и закройте видеофайл
        video_capture.release()
        cv2.destroyAllWindows()
        os.remove(video_path)
        return res_dir
