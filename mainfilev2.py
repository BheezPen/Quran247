import os
import random as rn
import datetime as dt
import textwrap
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
# You can move these to a config.ini or config.json later for easier customization
# For now, keeping them here as constants.

# Font files (ensure these paths are correct relative to your script)
MAIN_FONT_PATH = 'tahomabd.ttf'
FOOTER_FONT_PATH = './font/EngrvOs205.ttf' # Assuming EngrvOs205.ttf is in a 'font' subdirectory

# Text file paths
QURAN_VERSES_ENG_FILE = "quranverses_eng.txt"
QURAN_CHAPTERS_SURAH_FILE = "quran_chapters_surah.txt"

# Output directory
OUTPUT_DIR = "generated_images"

# Default image settings (can be made configurable)
BACKGROUND_IMAGE = 'bg_1.jpg' # Or 'bg_1a.jpg', or a random selection from a list
DEFAULT_TEXT_COLOR = 'Black'
DEFAULT_FOOTER_COLOR = 'green'
INSTAGRAM_ID_COLOR = 'red'
AUTOMATED_TEXT_COLOR = 'black'

# --- Helper Functions for Data Retrieval ---

def get_lines_from_file(file_path: str) -> list[str]:
    """
    Reads lines from a specified text file and returns them as a list of strings.
    Handles FileNotFoundError and general exceptions.
    """
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            content = f.read()
        # Filter out any empty strings that might result from extra newlines
        return [line for line in content.split("\n") if line.strip()]
    except FileNotFoundError:
        print(f"Error: Required file '{file_path}' not found. Please ensure it exists.")
        return []
    except Exception as e:
        print(f"An error occurred while reading '{file_path}': {e}")
        return []

# --- Verse and Surah/Ayah Parsing Logic (Corrected for pipe separator) ---

def parse_verse_line(verse_line: str) -> tuple[int, int, str]:
    """
    Parses a single verse string to extract Surah number, Ayah number,
    and the verse body based on the '|' (pipe) separator.

    Assumes format: "SURAH_NUM|AYAH_NUM|VERSE_TEXT"
    Example: "86|13|Verily, this is the Word that separates."
    """
    surah_num = 0
    ayah_num = 0
    verse_body = verse_line.strip()

    parts = verse_body.split('|', 2) # Split at most twice using '|'

    if len(parts) == 3: # Expecting 3 parts: Surah, Ayah, Verse_text
        try:
            surah_num = int(parts[0])
            ayah_num = int(parts[1])
            verse_body = parts[2].strip() # The rest is the actual verse text
        except ValueError:
            # If conversion to int fails, it means the parts weren't numbers.
            # Keep surah_num/ayah_num as 0 and use full line as fallback.
            pass
    else:
        # This handles cases where there aren't exactly two '|' separators.
        # Keep surah_num/ayah_num as 0 and use full line as fallback.
        pass

    if surah_num == 0 or ayah_num == 0:
        # If parsing failed, use the entire line as the verse body and default numbers
        print(f"Warning: Could not parse Surah/Ayah from line: '{verse_line}'. Using full line as verse body.")
        return 0, 0, verse_line.strip()

    return surah_num, ayah_num, verse_body

# --- Image Drawing Helper Functions ---

def wrap_and_draw_text(image: Image.Image, text: str, font_path: str, base_fontsize: int,
                       text_color: tuple[int, int, int] | str, start_height: int,
                       line_height_multiplier: float, wrap_width: int, align: str = "left"):
    """
    Wraps text and draws it on the image, adjusting font size and line height.

    Args:
        image: PIL Image object to draw on.
        text: The text string to draw.
        font_path: Path to the font file.
        base_fontsize: The initial font size.
        text_color: Color of the text (e.g., 'Black', or (0,0,0)).
        start_height: Starting Y-coordinate for the first line of text.
        line_height_multiplier: Multiplier for line height based on font size.
        wrap_width: Character width for text wrapping.
        align: Text alignment ('left', 'center', 'right').
    Returns:
        The final Y-coordinate after drawing all lines.
    """
    try:
        font = ImageFont.truetype(font_path, base_fontsize)
    except IOError:
        print(f"Error: Font file not found at {font_path}. Using default font.")
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(image)
    lines = textwrap.wrap(text, width=wrap_width)
    y_text = start_height
    image_width, _ = image.size # Get image width for alignment calculations

    for line in lines:
        # Use textbbox to get the bounding box, then calculate width
        # textbbox returns (left, top, right, bottom)
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0] # right - left

        x_pos = 0 # Initialize x_pos

        if align == "right":
            x_pos = image_width - line_width - 80 # 80px padding from right
        elif align == "center":
            x_pos = (image_width - line_width) / 2
        else: # default left
            x_pos = 80 # 80px padding from left

        draw.text((x_pos, y_text), line, font=font, fill=text_color)
        y_text += base_fontsize * line_height_multiplier # Use fontsize for consistent line height

    return y_text

def draw_footer_text(image: Image.Image, text: str, fontsize: int, text_color: tuple[int, int, int] | str,
                     y_pos: int, font_path: str, align: str = "center"):
    """
    Helps write general footer text on the background image.
    Automatically centers text horizontally based on image width.
    """
    try:
        font = ImageFont.truetype(font_path, fontsize)
    except IOError:
        print(f"Error: Footer font file not found at {font_path}. Using default font.")
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(image)
    image_width, _ = image.size

    # Use textbbox to get the bounding box, then calculate width
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]

    x_pos = (image_width - text_width) / 2 # Center calculation

    # You could add logic for other alignments here too if needed for footer
    if align == "left":
        x_pos = 80
    elif align == "right":
        x_pos = image_width - text_width - 80

    draw.text((x_pos, y_pos), text, font=font, fill=text_color)


# --- Main Image Generation Logic ---

def generate_verse_image():
    """
    Main function to generate an image with a random Quranic verse.
    It reads a verse, parses its details, loads a background, and
    draws the text onto it before saving the image.
    """
    verses_list = get_lines_from_file(QURAN_VERSES_ENG_FILE)
    if not verses_list:
        print("Exiting: No verses found or file could not be read.")
        return

    # Randomly select a verse line
    selected_verse_line = rn.choice(verses_list)
    surah_num, ayah_num, ayah_body_text = parse_verse_line(selected_verse_line)

    # Initialize surah_name and ayah_caption_text with defaults
    # This prevents UnboundLocalError if parsing fails for some reason
    surah_name = "Unknown Surah"
    ayah_caption_text = "A beautiful Quranic verse for reflection."

    # If parsing failed to get valid numbers, fallback to a generic display or skip
    if surah_num == 0 or ayah_num == 0:
        print(f"Warning: Failed to parse Surah/Ayah from line: '{selected_verse_line}'. Displaying raw line and generic info.")
        ayah_body_text_display = selected_verse_line.strip()
        ayah_info_text = "QURAN: VERSE" # Generic placeholder
        ayah_caption_text = f"A Quranic verse for reflection: {ayah_body_text_display}"
    else:
        # Prepare chapter name
        chapter_names = get_lines_from_file(QURAN_CHAPTERS_SURAH_FILE)
        if 0 < surah_num <= len(chapter_names):
            surah_name = chapter_names[surah_num - 1]
        else:
            print(f"Warning: Surah number {surah_num} out of bounds for chapter names list. Using 'Unknown Surah'.")

        ayah_body_text_display = f'"{ayah_body_text}"'
        ayah_info_text = f'QURAN {surah_num}: {surah_name.upper()}, VERSE {ayah_num}'
        ayah_caption_text = f"A beautiful reminder from Surah {surah_name} ({surah_num}), Verse {ayah_num}. Let's reflect on Allah's words. #Quran #Islam #DailyReminder #VerseOfTheDay #Allah #Quran247"


    # --- Image & Text Preparation ---
    try:
        image = Image.open(BACKGROUND_IMAGE).convert("RGB") # Ensure RGB mode for consistency
    except FileNotFoundError:
        print(f"Error: Background image '{BACKGROUND_IMAGE}' not found. Exiting.")
        return
    except Exception as e:
        print(f"Error loading background image: {e}. Exiting.")
        return

    # Determine font size and wrapping parameters based on text length
    text_len = len(ayah_body_text_display) # Use the display version for length calculation

    # These ranges and values are derived from your original logic.
    # You might want to fine-tune them for optimal appearance.
    if 0 <= text_len <= 200:
        fontsize = 55
        wrap_width = 25
        line_height_mult = 1.2
        text_start_y = 220
        align = "center"
    elif 200 < text_len <= 400:
        fontsize = 42
        wrap_width = 35
        line_height_mult = 1.2
        text_start_y = 150
        align = "center"
    elif 400 < text_len <= 700:
        fontsize = 33
        wrap_width = 45
        line_height_mult = 1.2
        text_start_y = 150
        align = "right"
    elif 700 < text_len <= 850:
        fontsize = 30
        wrap_width = 50
        line_height_mult = 1.2
        text_start_y = 150
        align = "right"
    elif 840 < text_len <= 1000:
        fontsize = 27
        wrap_width = 58
        line_height_mult = 1.2
        text_start_y = 150
        align = "right"
    else: # For very long verses
        fontsize = 25
        wrap_width = 63
        line_height_mult = 1.2
        text_start_y = 150
        align = "right"

    # Draw the main verse text
    # final_y_after_verse from `wrap_and_draw_text` is the end position of the last line
    final_y_after_verse = wrap_and_draw_text(
        image, ayah_body_text_display.upper(), MAIN_FONT_PATH, fontsize,
        DEFAULT_TEXT_COLOR, text_start_y, line_height_mult, wrap_width, align=align
    )

    # Draw footer text
    instagram_id_text = '@YOUR_INSTAGRAM_ID' # <-- REMEMBER TO CHANGE THIS!
    automated_text = 'This is AUTOMATED and built By H.A.O. Bheez, @horladipupo'

    draw_footer_text(image, ayah_info_text.upper(), 25, DEFAULT_FOOTER_COLOR, final_y_after_verse + 5, FOOTER_FONT_PATH)
    draw_footer_text(image, instagram_id_text, 30, INSTAGRAM_ID_COLOR, 1000, FOOTER_FONT_PATH) # Fixed Y for bottom
    draw_footer_text(image, automated_text, 20, AUTOMATED_TEXT_COLOR, 1040, FOOTER_FONT_PATH) # Fixed Y for bottom

    # --- Save and Show Image ---
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate unique filename
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S_%f") # Includes microseconds for uniqueness
    image_filename = f"quran_verse_{surah_num}_{ayah_num}_{timestamp}.png"
    output_path = os.path.join(OUTPUT_DIR, image_filename)

    #image.save(output_path)
    #print(f"Generated image: {output_path}")

    # For development/testing, you can show the image immediately.
    # For production, especially automated runs, comment this out.
    image.show() # This opens the image, might be annoying in loops.

    # Return structured information about the generated image for external use
    return {
        "image_path": output_path,
        "verse_text": ayah_body_text, # The raw verse text without quotes
        "surah_name": surah_name,
        "surah_num": surah_num,
        "ayah_num": ayah_num,
        "suggested_caption": ayah_caption_text # Use the generated caption
    }

# --- Execution ---
if __name__ == "__main__":
    # Ensure the 'generated_images' directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate a single image (you can put this in a loop for multiple images)
    generated_info = generate_verse_image()

    if generated_info:
        print(f"\n--- Generation Summary ---")
        print(f"Image saved to: {generated_info['image_path']}")
        print(f"Verse Text: {generated_info['verse_text'][:70]}...") # Show beginning of verse
        print(f"Surah: {generated_info['surah_name']} ({generated_info['surah_num']}), Ayah: {generated_info['ayah_num']}")
        print(f"Suggested Caption: {generated_info['suggested_caption']}")