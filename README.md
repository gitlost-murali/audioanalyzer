# AudioAnalyzer

Exploratory repo. Mix of  generic Video processing techniques for Indian TV series and Match highlights prediction.

```
videos_folder = 'videos/' 
bgm_folder = 'bgm/' 
img_dir ='gen_bgm_img/'
```
Place your videos (.mp4) in videos folder. `process_videos()` function will create BGM of the videos in `.mp3` format inside bgm folder. 

`process_bgms()` function will split the 'bgm/*.mp3' files and create small `gen_bgm_img/video_name/start2end.wav` and `gen_bgm_img/video_name/start2end.png` (Spectogram).