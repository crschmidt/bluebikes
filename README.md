# Bluebikes hackery

This is a set of tools for generating point data to use with qgis to generate
an animated timeseries of bikeshare trips.

For more general tutorial, see:

   https://www.qgistutorials.com/en/docs/3/animating_time_series.html

##  Setup

 $ virtualenv env
 $ source env/bin/active
 $ pip install -r requirements.txt
 $ ./setup.sh
 $ python gen_activepoints.py

This will produce a .csv file with two days of trip data interpolated at 2
minute intervals. This data can then be loaded into qgis.

## qgis setup

### Temporal layer setup:

- Layer->Add Layer->Add Delimited Text Layer
- Choose your file, select Comma as a delimiter, and ensure that point coordinates are loaded with lon as X, lat as Y
- Once added, right click the layer and click "Properties"; select "Temporal" from the left sidebar.
- Check the "Temporal" box, change the Configuration dropdown to "Single Field with Date/Time", and select the "Timestamp" field. Set Event duration to 1 second.

### Styling:

- Click Symbology
- Click "Categorized" at the top; type "bikeid" for the Value.
- Click "Classify" at the bottom. This will assign a random color to each bike. (It will pop up a warning about a large number of colors. This is fine.)

## Animation

- Click the "Clock" icon in the main toolbar; this will open the Temporal Controller.
- Click the Play button in the temporal controller.
- Change the Step time to 119 seconds
- Next to the refresh icon (next to range), choose "Set to Single Layer's Range" to set the time window.
- Click the floppy disk icon to save a set of images for the animation. (Ensure that the width + height are divisible by 2.)

## Creating video

ffmpeg -r 30 -f image2 -s 1600x1600 -i imagename%04d.png   -vcodec libx264 -crf 25  -pix_fmt yuv420p myvid.mp4
