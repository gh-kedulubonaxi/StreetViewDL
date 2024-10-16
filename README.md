# StreetViewDL
Downloads all the tiles from a streetview scene and creates a 360-degree image that can be viewed offline.

Makes for a nice wallpaper
![image](https://github.com/gh-kedulubonaxi/StreetViewDL/blob/main/readme_assets/aSch6QZq6rdz9xDxI7uzkA_preview.png)
[Full size original example image (16384x8192, 86.39 MB)](https://github.com/gh-kedulubonaxi/StreetViewDL/blob/main/readme_assets/aSch6QZq6rdz9xDxI7uzkA.png)

Or you can view it in any player that supports 360-degree images/videos:

https://github.com/user-attachments/assets/b8af9c84-e058-419c-a2a4-c42bf7da3997

## Requirements
* [Python3](https://www.python.org/)
* [ImageMagick](https://imagemagick.org/index.php)
  
They have to be on the PATH so that their commands are available globally on the command line.

## Usage
Find a streetview scene you like, copy the URL and run the "StreetViewDL.py" script with the URL in quotation marks as a parameter:

```PowerShell
python StreetViewDL.py "https://www.google.com/maps/@35.6986805,139.7714552,3a,90y,263.12h,98.95t/data=!3m8!1e1!3m6!1saSch6QZq6rdz9xDxI7uzkA!2e0!5s20180401T000000!6shttps:%2F%2Fstreetviewpixels-pa.googleapis.com%2Fv1%2Fthumbnail%3Fcb_client%3Dmaps_sv.tactile%26w%3D900%26h%3D600%26pitch%3D-8.946818552644402%26panoid%3DaSch6QZq6rdz9xDxI7uzkA%26yaw%3D263.1164736151364!7i16384!8i8192?coh=205410&entry=ttu&g_ep=EgoyMDI0MTAwMi4xIKXMDSoASAFQAw%3D%3D"
```

![image](https://github.com/gh-kedulubonaxi/StreetViewDL/blob/main/readme_assets/powershell.png)

## Result
After it's done you should find a folder, named after the "panoid" of the streetview scene, containing the finished picture and [a folder with all the tiles.](https://raw.githubusercontent.com/gh-kedulubonaxi/StreetViewDL/refs/heads/main/readme_assets/tiles.png) 
![image](https://github.com/gh-kedulubonaxi/StreetViewDL/blob/main/readme_assets/description.png)

## Problems/solutions

I've encountered these problems on Ubuntu:
### convert-im6.q16: width or height exceeds limit

Change these lines in */etc/ImageMagick-6/policy.xml*:

```
<policy domain="resource" name="width" value="16KP"/>
<policy domain="resource" name="height" value="16KP"/>
```
to
```
<policy domain="resource" name="width" value="32KP"/>
<policy domain="resource" name="height" value="32KP"/>
```

### montage-im6.q16: cache resources exhausted

Change this line in */etc/ImageMagick-6/policy.xml*:

```
<policy domain="resource" name="disk" value="1GiB"/>
```
to
```
<policy domain="resource" name="disk" value="8GB"/>
```
