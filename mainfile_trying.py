from PIL import Image, ImageDraw, ImageFont
import textwrap
import random as rn
import datetime as ds
import requests
import json

def get_verse():
    """A Function that will help get the verses from the verse.txt file and convert them into a list datatype"""
    verses_to_use = open("quranverses_eng.txt", "r", encoding='utf-8') #Open the verse.txt file in read mode
    single_verse = verses_to_use.read()
    verses_to_list = single_verse.split("\n") #TO split with new lines
    verses_in_list = verses_to_list
    verses_to_use.close()
    global verse_to_use
    verse_to_use = verses_in_list[rn.randint(1,6200)]

def surah_pick():
    '''This pick out the Surah Number from the Qranverses_eng.txt file as per the line selected randomly'''
    try:
        global surah_str
        surah_str = verse_to_use[0:3]
        surah = int(surah_str)
        return surah
    except ValueError:
        try:
            surah_str = verse_to_use[0:2]
            surah = int(surah_str)
            return surah
        except ValueError:
            surah_str = verse_to_use[0]
            surah = int(surah_str)
            return surah

def three_ayah_pick():
    '''This pick out the Ayah Number for surah between 100 to 114 from the Qranverses_eng.txt file as per the line selected randomly'''
    try:
        ayah_str = verse_to_use[4:7]
        global ayah
        ayah = int(ayah_str)
        return ayah
    except ValueError:
        try:
            ayah_str = verse_to_use[4:6]
            #global ayah
            ayah = int(ayah_str)
            return ayah
        except ValueError:
            ayah_str = verse_to_use[4]
            #global ayah
            ayah = int(ayah_str)
            return ayah

def two_ayah_pick():
    '''This pick out the Ayah Number for surah between 10 to 99 from the Qranverses_eng.txt file as per the line selected randomly'''
    try:
        ayah_str = verse_to_use[3:6]
        global ayah
        ayah = int(ayah_str)
        return ayah
    except ValueError:
        try:
            ayah_str = verse_to_use[3:5]
            #global ayah
            ayah = int(ayah_str)
            return ayah
        except ValueError:
            ayah_str = verse_to_use[3]
            #global ayah
            ayah = int(ayah_str)
            return ayah

def one_ayah_pick():
    '''This pick out the Ayah Number for surah between 1 to 9 from the Qranverses_eng.txt file as per the line selected randomly'''
    try:
        ayah_str = verse_to_use[2:5]
        global ayah
        ayah = int(ayah_str)
        return ayah
    except ValueError:
        try:
            ayah_str = verse_to_use[2:4]
            #global ayah
            ayah = int(ayah_str)
            return ayah
        except ValueError:
            ayah_str = verse_to_use[2]
            #global ayah
            ayah = int(ayah_str)
            return ayah

def ayah_pick():
    '''This tell which of three Ayah Picker function should be called'''
    try:
        if len(surah_str) == 3:
            print(surah_str)
            three_ayah_pick()
            global ayah_num
            ayah_num = ayah
            return ayah_num
        elif len(surah_str) == 2:
            two_ayah_pick()
            ayah_num = ayah
            return ayah_num
        elif len(surah_str) == 1:
            one_ayah_pick()
            ayah_num = ayah
            return ayah_num
        else:
            return "Error Somewhere"
    except:
        return "Error Somewhere"

def get_chapter():
    """A Function that will help get the quran chapters (surah) from the quran_chapters_surah.txt file and convert them into a list datatype"""
    chapter_to_use = open("quran_chapters_surah.txt", "r", encoding='utf-8') #Open the quran_chapters_surah.txt file in read mode
    single_chapter = chapter_to_use.read()
    chapter_to_list = single_chapter.split("\n") #TO split with new lines
    chapter_in_list = chapter_to_list
    chapter_to_use.close()
    chapter_to_use = chapter_in_list[int(surah_pick()) -1]
    return chapter_to_use


def image_name_generator():
    '''This function held generate the name for every images generated so as to name of image when saving'''
    date = str(ds.datetime.now(None))
    image_suffix = date[5:7] + date[8:10] + date[11:13] + date[14:16] + date[17]#date[17:19]
    image_name = f"img_for_{image_suffix}"
    return image_name

def draw_multiple_line_text(image, text, fontsize, text_color, text_start_height):
    '''Helps write the verses (ayah) text on the background'''
    font = ImageFont.truetype('tahomabd.ttf', fontsize)
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    global y_text
    y_text = text_start_height
    lines = textwrap.wrap(text, width=25)
    for line in lines:
        draw.text((80, y_text), line, font=font, fill=text_color, align="center")
        y_text += 70  * 1.2

def draw_multiple_line_text1(image, text, fontsize, text_color, text_start_height):
    '''Helps write the verses (ayah) text on the background'''
    font = ImageFont.truetype('tahomabd.ttf', fontsize)
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    global y_text
    y_text = text_start_height
    lines = textwrap.wrap(text, width=35)
    for line in lines:
        draw.text((80, y_text), line, font=font, fill=text_color, align="center")
        y_text += 50  * 1.2

def draw_multiple_line_text2(image, text, fontsize, text_color, text_start_height):
    '''Helps write the verses (ayah) text on the background'''
    font = ImageFont.truetype('tahomabd.ttf', fontsize)
    draw = ImageDraw.Draw(image)
    global y_text
    y_text = text_start_height
    lines = textwrap.wrap(text, width=45)
    for line in lines:
        draw.text((80, y_text), line, font=font, fill=text_color, align="right")
        y_text += 40  * 1.2

def draw_multiple_line_text3(image, text, fontsize, text_color, text_start_height):
    '''Helps write the verses (ayah) text on the background'''
    font = ImageFont.truetype('tahomabd.ttf', fontsize)
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    global y_text
    y_text = text_start_height
    lines = textwrap.wrap(text, width=50)
    for line in lines:
        draw.text((80, y_text), line, font=font, fill=text_color, align="right")
        y_text += 38  * 1.2

def draw_multiple_line_text4(image, text, fontsize, text_color, text_start_height):
    '''Helps write the verses (ayah) text on the background'''
    font = ImageFont.truetype('tahomabd.ttf', fontsize)
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    global y_text
    y_text = text_start_height
    lines = textwrap.wrap(text, width=58)
    for line in lines:
        draw.text((80, y_text), line, font=font, fill=text_color, align="right")
        y_text += 34  * 1.2

def draw_multiple_line_text5(image, text, fontsize, text_color, text_start_height):
    '''Helps write the verses (ayah) text on the background'''
    font = ImageFont.truetype('tahomabd.ttf', fontsize)
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    global y_text
    y_text = text_start_height
    lines = textwrap.wrap(text, width=63)
    for line in lines:
        draw.text((80, y_text), line, font=font, fill=text_color, align="right")
        y_text += 29  * 1.2

def draw_footer_text(image, text, fontsize, text_color, text_start_height,):
    '''Helps write the footer text on the background'''
    font = ImageFont.truetype('./font/EngrvOs205.ttf', fontsize)
    draw = ImageDraw.Draw(image)
    y_text = text_start_height
    draw.text((80, y_text), text, font=font, fill=text_color)

def generate_verse_to_image():
    '''Helps assemble all text and background needed to generate the image '''
    line2 = f'{get_verse()}'
    to_remove1,to_remove2 = surah_pick(),ayah_pick()
    to_remove11,to_remove22 = str(to_remove1),str(to_remove2)
    total_remove = len(to_remove11) + len(to_remove22) + 2
    global ayah_body
    ayah_body = f'"{verse_to_use[total_remove:]}"'

    #post_width, post_height = 1080, 1080
    image = Image.open('bg_1.jpg', mode='r' )
    #image = Image.new('RGB', (post_width, post_height), color = (rn.randint(1,255), 70, 20))
    text2 = ayah_body
    fontsize = 55
    text2_color = 'Black'
    text3 = f'Quran {get_chapter()}, Verse {ayah_pick()}'
    global ayah_caption
    ayah_caption = text3
    text3_color = 'green'
    text4 = '@InstagramID' #Change this afterwards
    text4_color = 'red'

    #The condition below help specify which of the function to call base on the lenght of the Verse (text)
    #This is because the mode of writiing for the function is kinda different base on line spacing, font size, starting_point etc
    if 0 <= len(text2) <= 200:
        draw_multiple_line_text(image, text2.upper(), fontsize, text2_color, 220)
    elif 200 <= len(text2) <= 400:
        fontsize = 44
        draw_multiple_line_text1(image, text2.upper(), fontsize, text2_color, 150)
    elif 400 <= len(text2) <= 700:
        fontsize = 33
        draw_multiple_line_text2(image, text2.upper(), fontsize, text2_color, 150)
    elif 700 <= len(text2) <= 850:
        fontsize = 30
        draw_multiple_line_text3(image, text2.upper(), fontsize, text2_color, 150)
    elif 840 <= len(text2) <= 1000:
        fontsize = 27
        draw_multiple_line_text4(image, text2.upper(), fontsize, text2_color, 150)
    else:
        fontsize = 25
        draw_multiple_line_text5(image, text2.upper(), fontsize, text2_color, 150)
    
    draw_footer_text(image, text3.upper(), 25, text3_color, y_text + 5  )
    draw_footer_text(image, text4, 30, text4_color, 1000)
    draw_footer_text(image, 'Built By H.A.O. Bheez, @horladipupo', 20, "black", 1040)
    print(len(text2),fontsize) #Comment or Change this afterwards, here for testign purpose only
    global image_to_post
    image_to_post = image.save(f'./generated_images/{image_name_generator()}.png')
    #image.show()


def post_on_ig(necessary_function):

    # Post the Image
    ig_user_id = 17841454897586133 #9294009310
    user_access_token = "IGQVJYWDBPYXdjaTNIMExBMUJaRDV3M1ZA5X1JzR1MyeEluLVlPV3lSM3pOaF9SdEJLY056VGE4RlNXNk04cjJSRFhNMnVwNXRwYUhINllFWjlMdUhGWHdicksydWhkQzVucUpXTEZAoMVZAaWkxNSmVpSQZDZD"
    image_location = image_to_post#f'./generated_images/{image_name_generator()}.png' #f'https://828naija.by-friday.xyz/posts/{image_name_generator()}.png'
    post_url = f'https://graph.facebook.com/v10.0/{ig_user_id}/media'

    payload = {
        'image_url': image_location,
        'caption': f'{ayah_body}.{ayah_caption} Read more from Quran {get_chapter()}, Verse {ayah_pick()} - @247Quran #247Quran',
        'access_token': user_access_token
    }
    r = requests.post(post_url, data=payload)
    print(r.text)

    result = json.loads(r.text)

    if 'id' in result:
        creation_id = result['id']
        second_url = f'https://graph.facebook.com/v10.0/{ig_user_id}/media_publish'
        second_payload = {
            'creation_id': creation_id,
            'access_token': user_access_token
        }
        r = requests.post(second_url, data=second_payload)
        print('Posted to IG')
        print(r.text)
        print(f'Last posted image on Instagram = {image_name_generator()}')
        print(f'Last posted image on Instagram = {image_name_generator()}')
        print(f'Time last posted is {(ds.datetime.now(None))}')

    else:
        print('Unable to Submit Post to IG')


#generate_verse_to_image()
post_on_ig(generate_verse_to_image())

'''

import requests
import json

# Set the Instagram API endpoint
API_ENDPOINT = "https://www.instagram.com/graphql/query/"

# Set the access token for the Instagram API
ACCESS_TOKEN = "your_access_token_here"

# Set the message to be posted on Instagram
MESSAGE = "Hello, Instagram!"

# Set the Instagram API parameters
params = {
    "query_hash": "your_query_hash_here",
    "variables": {
        "input": {
            "text": MESSAGE
        }
    }
}

# Make the POST request to the Instagram API
response = requests.post(API_ENDPOINT, json=params, headers={ "Authorization": "Bearer " + ACCESS_TOKEN })

# Print the response from the Instagram API
print(response.text)

This script uses the requests library to send a POST request to the Instagram GraphQL API. 
You will need to replace your_access_token_here with a valid access token and your_query_hash_here with the appropriate query hash. 
You can also modify the MESSAGE variable to specify the message that you want to post.

Note that this script is just an example and may not work out of the box. 
You may need to make additional modifications or perform additional setup in order to use it successfully.'''



'''
Instagram token gotten is 
IGQVJYWDBPYXdjaTNIMExBMUJaRDV3M1ZA5X1JzR1MyeEluLVlPV3lSM3pOaF9SdEJLY056VGE4RlNXNk04cjJSRFhNMnVwNXRwYUhINllFWjlMdUhGWHdicksydWhkQzVucUpXTEZAoMVZAaWkxNSmVpSQZDZD

generated in the 19th april 2023'''