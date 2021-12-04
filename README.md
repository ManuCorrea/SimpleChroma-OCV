# SimpleChroma-OCV
 Chroma interface based on HSV values with postprocesing with erosion and dilation operations. 

 ## Instructions
For running it just run:
  ```
 python3 chroma.py
  ```

If OpenCV not installed:
```
pip install opencv-python
```

For making the chroma work you need to find out the range of values needed in the HSV ranges.

If you have little squares of noise they can be removed using erosion parameters. Then to compensate that erosion is recomended to also add the dilation.

If you want to play with another video just add it to the video folder and change the name of the readed video in the chroma.py script.

## Acknowledgments
* Base UI based on [Stack Overflow Answer](https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv/59906154#59906154)

Videos extracted from Pexels:
* [city.mp4](https://www.pexels.com/video/timelapse-video-of-a-city-5396823/)