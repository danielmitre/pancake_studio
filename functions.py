from PIL import Image, ExifTags, ImageFont, ImageDraw
import numpy as np
import random
from blend_modes import soft_light as sfl


# Applies grain effect to image
def grain_img(img, percentage):
	img_aux = img
	img_arr = np.array(img_aux)
	for i in range(len(img_arr)):
		grain_line(img_arr[i], percentage)
	return img_aux


# Applies grains on one line of image matrix
def grain_line(arr, percentage):
	pixels = random_pixels(len(arr), percentage)
	for p in range (len(arr)):
		if p in pixels:
			bright_pixel(arr[p], 10, 40)


# Determines the pixels that will be brighter
def random_pixels(size, percentage):
	pixels = []
	for i in range(int(size*percentage)):
		pixels.append(random.randint(0, size-1))
	return pixels


# Makes a pixels brighter in a random way
def bright_pixel(arr, min_br, max_br):
	br = random.randint(min_br, max_br)
	for i in range(len(arr)):
		arr[i] = min(arr[i] + br, 255)


# Resizes image
def resize(img, max_height, max_width):
	img_aux = img
	img_arr = np.array(img_aux)
	height = len(img_arr)
	width = len(img_arr[0])
	ratio = 1

	if height > max_height or width > max_width:
		if max_width > max_height:
			ratio = max_height / height
		else:
			ratio = max_width / width

	new_height = height * ratio
	new_width = width * ratio

	size = new_height, new_width
	img_aux.thumbnail(size)

	return img_aux


# Crops image
def crop(img, height, width):
	img_arr = np.array(img)
	img_width = len(img_arr[0])
	img_height = len(img_arr)
	center_width = img_width / 2
	center_height = img_height / 2

	if width > img_width:
		width = img_width
	if height > img_height:
		height = img_height

	init_width = int(center_width - (width/2))
	end_width = int(init_width + width)
	init_height = int(center_height - (height/2))
	end_height = int(init_height + height)

	img_arr = img_arr[init_height:end_height, init_width:end_width]
	img = Image.fromarray(img_arr)
	print(height, len(img_arr), width, len(img_arr[0]))

	return img


# Overlays RGBA images
def soft_light(background, overlay, opacity):
	# Converts images to arrays of float type so
	# the blend modes module can work
	background_arr = np.array(background).astype(float)
	overlay_arr = np.array(overlay).astype(float)

	# Blend the images using soft light mode
	final_img_arr = sfl(background_arr, overlay_arr, opacity)

	# Transforms array of floats to array of unsigned integer
	# between 0 and 255
	final_img_arr = np.uint8(final_img_arr)
	# Transforms array to image
	final_img = Image.fromarray(final_img_arr)

	return final_img


def size(img):
	img_arr = np.array(img)
	height = len(img_arr)
	width = len(img_arr[0])
	return (height, width)


def get_exif(im):
    im_exif = im._getexif().items()
    exif = {}
    
    for (tag, value) in im_exif:
        if tag in ExifTags.TAGS:
            exif[ExifTags.TAGS[tag]] = value

    return exif


def get_img_date(im):
    exif = get_exif(im)
    date = exif['DateTime'].split(' ')[0]
    year = str(date[2:4])
    month = str(date[5:7])
    day = str(date[8:10])
    return {'day': day, 'month': month, 'year': year}


def write_on_img(im, text, font, size, position, color):
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(font, size)
    draw.text(position, text, color, font=font)
    return im


def blank_img(size, color):
    im = Image.new('RGBA', size, color)
    return im


def black_img(size):
    color = (0, 0, 0, 255)
    im = blank_img(size, color)
    return im


def transparent_img(size):
	color = (0, 0, 0, 0)
	im = blank_img(size, color)
	return im


def brazilian_date_format(date):
    text = date['day'] + ' ' + date['month'] + " '" + date['year']
    return text

def write_date_img_black(im):
    size = im.size
    black_im = black_img(size)
    date = get_img_date(im)
    text = brazilian_date_format(date)
    font_color = (255, 255, 255)
    position = (0, 0)
    write_on_img(black_im, text, 'digital-7.ttf', 50, position, font_color)
    return black_im

