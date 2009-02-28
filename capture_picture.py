#!/usr/bin/python
#
# python-v4l2capture
#
# 2009 Fredrik Portstrom
#
# I, the copyright holder of this file, hereby release it into the
# public domain. This applies worldwide. In case this is not legally
# possible: I grant anyone the right to use this work for any
# purpose, without any conditions, unless such conditions are
# required by law.

import Image
import select
import time
import v4l2capture

# Open the video device.
video = v4l2capture.Video_device("/dev/video0")

# Suggest an image size to the device. The device may choose and
# return another size if it doesn't support the suggested one.
size_x, size_y = video.set_format(1280, 1024)

# Start the device. This lights the LED if it's a camera that has one.
video.start()

# Wait a little. Some cameras take a few seconds to get bright enough.
time.sleep(2)

# Create a buffer to store image data in.
video.create_buffers(1)

# Send the buffer to the device.
video.queue_all_buffers()

# Wait for the device to fill the buffer.
select.select((video,), (), ())

# The rest is easy :-)
image_data = video.read()
video.close()
image = Image.fromstring("RGB", (size_x, size_y), image_data)
image.save("image.jpg")
print "Saved image.jpg (Size: " + str(size_x) + " x " + str(size_y) + ")"
