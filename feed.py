import feedparser
import pygame
import urllib

from PIL import Image
from io import BytesIO


#Returns the image at url as a pygame surface
def get_image_from_url(url):
    
    #Open image from url
    img_url = urllib.request.urlopen(url)
    img = BytesIO(img_url.read())
    img = Image.open(img)

    mode = img.mode
    size = img.size
    data = img.tostring()

    assert mode in "RGB", "RGBA"

    #Convert image url to pygame surface
    surface = pygame.image.fromstring(data, size, mode)
    return surface


#Returns thumbnail from entry as pygame surface
def get_thumb(entry, big=1):

    if len(entry) == 1:
        big = 0
    url = entry[big]['url']

    return get_image_from_url(url)


#Splits a string into maximum length substrings for wrapping
def split_text(text, rect, font):

    rect = pygame.Rect(rect)
    i = 1
    lines = []

    #Iterate the string. If it's over max width, split at most recent space. Repeat
    while text:
        
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1
        lines.append(text[:i])
        text = text[i:]

    return lines


#Calls split_text on a string then render and blits
def draw_text(text, rect, font):

    lines = split_text(text, rect, font)
    y = 0
    spacing = 3
    font_height = font.size("Tg")[1]

    #blit to screen one line at a time
    for line in lines:
        line = font.render(line, 1, colour)
        screen.blit(line, (rect[0], rect[1]+y))
        y += font_height + spacing


#Commits retrieved data to screen
#Causes flickering of pictures except top 2
def update_screen(offset):

    count = 0
    for entry in data.entries:
    
        title = entry['title']
        summary = entry['summary']
        #thumb = entry['media_thumbnail']
        #thumbs.append(get_thumb(entry))

        #Render and blit to screen
        screen.blit(thumbs[count], (MARGIN, (thumb_height + SPACING)*count + MARGIN + offset))
        draw_text(title, (text_left,(thumb_height + SPACING)*count + offset, WIDTH - MARGIN - text_left, HEIGHT), title_font)
        #need to calculate actual value, 40 is ballpark
        draw_text(summary, (text_left,(thumb_height + SPACING)*count + 40 + offset, WIDTH - MARGIN - text_left,50), sum_font)

        #Only draw as many as you can have on screen
        if count < 6:
            pygame.display.flip()
        else:
            break
                    
        count +=1
      
    
################################
#
#   Main body of program
#
################################


pygame.init()
pygame.display.set_caption('Feed Me')

WIDTH=640
HEIGHT=480
MARGIN = 5      #Pixels between content and window border
SPACING = 3

title_font = pygame.font.SysFont("arial", 30)
sum_font = pygame.font.SysFont("arial", 16)

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

colour = (10,10,10)
bg_colour = (255,255,255)
screen.fill(bg_colour)
pygame.display.flip()

url = "http://feeds.bbci.co.uk/news/rss.xml"

data = feedparser.parse(url)    #need to add exception handling

#useful ones:
#media_thumbnail, title, link, published, summary
big = 1
if len(data.entries[0]['media_thumbnail']) == 1:
    big = 0
thumb_width = int(data.entries[0]['media_thumbnail'][big]['width'])
thumb_height = int(data.entries[0]['media_thumbnail'][big]['height'])
text_left = MARGIN + thumb_width + SPACING

count = 0
offset = 0

thumbs = []

    #move to fetch_data function
for entry in data.entries:
    
    title = entry['title']
    summary = entry['summary']
    #thumb = entry['media_thumbnail']
    thumbs.append(get_thumb(entry['media_thumbnail']))

    #Render and blit to screen
    screen.blit(thumbs[count], (MARGIN, (thumb_height + SPACING)*count + MARGIN + offset))
    draw_text(title, (text_left,(thumb_height + SPACING)*count + offset, WIDTH - MARGIN - text_left, HEIGHT), title_font)
    #need to calculate actual value, 40 is ballpark
    draw_text(summary, (text_left,(thumb_height + SPACING)*count + 40 + offset, WIDTH - MARGIN - text_left,50), sum_font)

    #Only draw as many as you can have on screen
    if count < 6:
        pygame.display.flip()
    else:
        break
                
    count +=1



################################
#
#   Main event loop
#
################################

scrolling = False

while True:

    event = pygame.event.wait()

    if event.type == pygame.MOUSEMOTION and scrolling:
        screen.fill(bg_colour)
        if event.rel[1] != 0:   #add some tolerance?
            offset += event.rel[1]    #add some fluidity to the effect
                                            #velocity = rel[1]?
            update_screen(offset)

    elif event.type == pygame.MOUSEBUTTONDOWN:
        scrolling = True

    elif event.type == pygame.MOUSEBUTTONUP:
        scrolling = False


