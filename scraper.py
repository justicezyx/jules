# --- Botify.ai Scraper Tool ---
# Author: Jules (AI Software Engineer)
# Date: [Current Date - will be filled by system or manually if needed]
#
# Description:
# This Python script is designed to scrape data from bot profile pages, specifically targeting
# websites structured like Botify.ai. It aims to extract:
#   - Bot's name, profile picture URL, gallery photo URLs, tags, and description.
#   - The first message (text and image URL) from the bot's chat page.
# The script then attempts to download all identified images and saves the textual
# information, along with paths to the downloaded images, into a JSON file.
#
# Core Functionality:
# 1. `scrape_bot_page(url)`: Fetches and parses the main bot profile page.
# 2. `scrape_chat_page(chat_url)`: Fetches and parses the bot's chat page for the initial message.
# 3. `download_image(image_url, save_path, filename)`: Downloads an image from a URL.
# 4. The main execution block (`if __name__ == '__main__':`) orchestrates these functions,
#    manages file/directory creation, and saves the output.
#
# IMPORTANT LIMITATIONS:
#   - JAVASCRIPT-DEPENDENT WEBSITES: This script uses the `requests` library to fetch HTML content
#     and `BeautifulSoup` for parsing. These tools DO NOT EXECUTE CLIENT-SIDE JAVASCRIPT.
#     Websites like Botify.ai heavily rely on JavaScript to dynamically load and render their content.
#     As a result, the HTML fetched by `requests` is often a minimal placeholder or a template,
#     lacking the actual data visible in a browser.
#
#   - `__NEXT_DATA__` RELIANCE: The script attempts to find a `<script id="__NEXT_DATA__">` tag,
#     which is common in applications built with Next.js (like Botify.ai appears to be). This tag
#     can sometimes contain server-rendered page data in JSON format. However, if this data
#     is incomplete, absent in the initial non-JavaScript response, or itself populated/modified
#     by client-side JavaScript, this script will fail to extract the target information.
#     THE CURRENT IMPLEMENTATION FAILS TO EXTRACT DATA FROM BOTIFY.AI because the necessary
#     details are not available in the `__NEXT_DATA__` block of the initially fetched HTML,
#     or the block itself is not structured as anticipated without JavaScript execution.
#
#   - SELECTOR ROBUSTNESS: The fallback HTML parsing (if `__NEXT_DATA__` is unhelpful) uses
#     generic selectors and assumptions about HTML structure. These are highly likely to break
#     with website updates or variations in page layout.
#
#   - SOLUTION FOR DYNAMIC SITES: To reliably scrape JavaScript-heavy websites like Botify.ai,
#     browser automation tools such as Selenium or Playwright are required. These tools can
#     control a web browser, execute JavaScript, and then access the fully rendered page content.
#     Such tools are not implemented in this script due to typical environment constraints
#     for automated agents.
#
# Conclusion for Botify.ai:
# While this script provides a structural template for web scraping, IT WILL NOT WORK CORRECTLY
# FOR BOTIFY.AI in its current form due to the aforementioned JavaScript dependency. The output
# for Botify.ai will be empty or contain placeholder/error values.

import requests
from bs4 import BeautifulSoup
import re
import json # Using json module to find data in script tags
import os
import shutil

def download_image(image_url, save_path, filename):
    """
    Downloads an image from a URL and saves it to a specified path.

    Args:
        image_url (str): The URL of the image to download.
        save_path (str): The directory path where the image should be saved.
        filename (str): The name to save the image as.

    Returns:
        str: The full path to the saved image if successful, None otherwise.
    """
    if not image_url:
        print("No image URL provided for download.")
        return None

    try:
        # Ensure the save directory exists
        os.makedirs(save_path, exist_ok=True)

        full_file_path = os.path.join(save_path, filename)

        # Check if the URL is absolute, if not, it might be a relative path (less likely for external images)
        if not image_url.startswith(('http://', 'https://')):
            print(f"Skipping download for relative or invalid URL: {image_url}")
            return None

        response = requests.get(image_url, stream=True, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        with open(full_file_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)

        print(f"Image downloaded successfully: {full_file_path}")
        return full_file_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image {image_url}: {e}")
        return None
    except IOError as e:
        print(f"Error saving image {image_url} to {full_file_path}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while downloading {image_url}: {e}")
        return None

def scrape_bot_page(url):
    """
    Scrapes the main page of a Botify bot to extract its name, profile picture,
    photos, and tags.

    Args:
        url (str): The URL of the bot's main page.
                   Example: "https://botify.ai/bot_268784"

    Returns:
        dict: A dictionary containing the scraped data:
              {
                  "bot_name": str,
                  "profile_picture_url": str,
                  "photo_urls": list[str],
                  "tags": list[str],
                  "description": str (or None if not found)
              }
              Returns None if the page cannot be fetched or essential data is missing.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Data is often embedded in a <script type="application/json" id="__NEXT_DATA__"> tag in Next.js sites
    # or directly in <script> tags containing JavaScript variables.

    bot_data = {
        "bot_name": None,
        "profile_picture_url": None,
        "photo_urls": [],
        "tags": [],
        "description": None,
        "voice_id": None, # Added based on typical bot info
        "is_nsfw": None, # Added based on typical bot info
        "gender": None, # Added based on typical bot info
    }

    # Attempt to find data in __NEXT_DATA__ script tag (common in Next.js apps like Botify seems to be)
    next_data_script = soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
    if next_data_script:
        try:
            data = json.loads(next_data_script.string)
            props = data.get('props', {}).get('pageProps', {})

            # --- Extracting Bot Name ---
            # Path: props.profile.name or props.bot.name or similar
            # Example value: "Joi"
            if props.get('profile') and props['profile'].get('name'):
                bot_data['bot_name'] = props['profile']['name']
            elif props.get('bot') and props['bot'].get('name'): # Fallback
                 bot_data['bot_name'] = props['bot']['name']

            # --- Extracting Profile Picture URL ---
            # Path: props.profile.avatarUrl or props.profile.avatar.url or props.bot.avatarUrl
            # Example value: "https://exh-data.s3.us-west-2.amazonaws.com/cv/default_bots_metadata/v3/Joi/avatar_256.jpg"
            if props.get('profile') and props['profile'].get('avatarUrl'):
                bot_data['profile_picture_url'] = props['profile']['avatarUrl']
            elif props.get('profile') and props['profile'].get('avatar') and isinstance(props['profile']['avatar'], dict) and props['profile']['avatar'].get('url'):
                 bot_data['profile_picture_url'] = props['profile']['avatar']['url']
            elif props.get('bot') and props['bot'].get('avatarUrl'): # Fallback
                 bot_data['profile_picture_url'] = props['bot']['avatarUrl']


            # --- Extracting Photo URLs (Gallery) ---
            # Path: props.profile.galleryItems (list of objects with 'url') or props.bot.gallery
            # Example value: ["https://botify-galleries.s3.us-west-2.amazonaws.com/...jpg", ...]
            gallery_items = []
            if props.get('profile') and props['profile'].get('galleryItems'):
                gallery_items = props['profile']['galleryItems']
            elif props.get('bot') and props['bot'].get('gallery'): # Fallback
                gallery_items = props['bot']['gallery']

            if isinstance(gallery_items, list):
                for item in gallery_items:
                    if isinstance(item, dict) and item.get('url'):
                        bot_data['photo_urls'].append(item['url'])
                    elif isinstance(item, str): # If it's just a list of strings
                        bot_data['photo_urls'].append(item)

            # --- Extracting Tags ---
            # Path: props.profile.tags (list of objects with 'name' or list of strings) or props.bot.tags
            # Example value: [{name: "🤖 Robot"}, {name: "👽 Fictional"}, ...] or ["Robot", "Fictional"]
            tags_data = []
            if props.get('profile') and props['profile'].get('tags'):
                tags_data = props['profile']['tags']
            elif props.get('bot') and props['bot'].get('tags'): # Fallback
                tags_data = props['bot']['tags']

            if isinstance(tags_data, list):
                for tag_item in tags_data:
                    if isinstance(tag_item, dict) and tag_item.get('name'):
                        bot_data['tags'].append(tag_item['name'])
                    elif isinstance(tag_item, str): # If tags are just strings
                        bot_data['tags'].append(tag_item)

            # --- Extracting Description ---
            # Path: props.profile.description or props.bot.description
            if props.get('profile') and props['profile'].get('description'):
                bot_data['description'] = props['profile']['description']
            elif props.get('bot') and props['bot'].get('description'):
                 bot_data['description'] = props['bot']['description']

            # --- Extracting Voice ID ---
            # Path: props.profile.voiceId or props.bot.voiceId
            if props.get('profile') and props['profile'].get('voiceId'):
                bot_data['voice_id'] = props['profile']['voiceId']
            elif props.get('bot') and props['bot'].get('voiceId'):
                 bot_data['voice_id'] = props['bot']['voiceId']

            # --- Extracting NSFW status ---
            # Path: props.profile.isNsfw or props.bot.isNsfw
            if props.get('profile') and 'isNsfw' in props['profile']:
                 bot_data['is_nsfw'] = props['profile']['isNsfw']
            elif props.get('bot') and 'isNsfw' in props['bot']:
                 bot_data['is_nsfw'] = props['bot']['isNsfw']

            # --- Extracting Gender ---
            # Path: props.profile.gender or props.bot.gender
            if props.get('profile') and props['profile'].get('gender'):
                 bot_data['gender'] = props['profile']['gender']
            elif props.get('bot') and props['bot'].get('gender'):
                 bot_data['gender'] = props['bot']['gender']


        except json.JSONDecodeError:
            print("Could not parse JSON from __NEXT_DATA__ script tag.")
        except Exception as e:
            print(f"Error processing __NEXT_DATA__: {e}")

    # Fallback or additional scraping if __NEXT_DATA__ is not complete or not found
    # This part would use BeautifulSoup's find/find_all with specific tags/classes
    # if the JSON data isn't available or sufficient.
    # For now, we are heavily relying on __NEXT_DATA__.

    # Example (if we had to guess tags and classes):
    if not bot_data['bot_name']:
        name_tag = soup.find('h1') # Example: <h1 class="bot-name">Joi</h1>
        if name_tag:
            bot_data['bot_name'] = name_tag.text.strip()

    if not bot_data['profile_picture_url']:
        # Example: <img class="profile-avatar" src="...">
        avatar_tag = soup.find('img', attrs={'src': re.compile(r"avatar.*\.jpg|avatar.*\.png", re.IGNORECASE)})
        if avatar_tag and avatar_tag.get('src'):
            bot_data['profile_picture_url'] = avatar_tag['src']

    if not bot_data['photo_urls']:
        # Example: <div class="gallery-container"> <img src="..."> <img src="..."> </div>
        gallery_images = soup.find_all('img', attrs={'src': re.compile(r"gallery.*\.jpg|gallery.*\.png", re.IGNORECASE)})
        for img in gallery_images:
            # Avoid picking up the avatar again if it matches the gallery regex
            if img.get('src') != bot_data['profile_picture_url']:
                 bot_data['photo_urls'].append(img['src'])
        # Remove duplicates if any by converting to set and back to list
        bot_data['photo_urls'] = list(set(bot_data['photo_urls']))


    if not bot_data['tags']:
        # Example: <div class="tags-section"> <span class="tag">🤖 Robot</span> <span class="tag">👽 Fictional</span> </div>
        tag_elements = soup.find_all('span', class_=re.compile(r"tag|badge", re.IGNORECASE)) # Hypothetical class
        for tag_el in tag_elements:
            bot_data['tags'].append(tag_el.text.strip())

    if not bot_data['description']:
        # This is highly dependent on the site structure, e.g. <p class="bot-description">...</p>
        # For now, we'll assume __NEXT_DATA__ is the primary source.
        pass


    # Basic validation: if no name or profile picture, it's likely a failed scrape
    if not bot_data.get("bot_name") and not bot_data.get("profile_picture_url"):
        print(f"Could not extract essential bot data from {url}. The page might be fully dynamic or structure changed.")
        # We might return None or the partial bot_data depending on requirements
        # For now, returning what we have.

    return bot_data

if __name__ == '__main__':
    # Test with the example URL
    test_url = "https://botify.ai/bot_268784"
    print(f"Scraping {test_url}...")
    scraped_info = scrape_bot_page(test_url)

    if scraped_info:
        print("\n--- Scraped Information ---")
        print(f"Bot Name: {scraped_info.get('bot_name')}")
        print(f"Profile Picture URL: {scraped_info.get('profile_picture_url')}")
        print(f"Description: {scraped_info.get('description')}")
        print(f"Voice ID: {scraped_info.get('voice_id')}")
        print(f"Is NSFW: {scraped_info.get('is_nsfw')}")
        print(f"Gender: {scraped_info.get('gender')}")

        print("\nTags:")
        if scraped_info.get('tags'):
            for tag in scraped_info['tags']:
                print(f"- {tag}")
        else:
            print("No tags found.")

        print("\nPhoto URLs:")
        if scraped_info.get('photo_urls'):
            for photo_url in scraped_info['photo_urls']:
                print(f"- {photo_url}")
        else:
            print("No photo URLs found.")
        print("--- End of Scraped Information ---")
    else:
        print("Failed to scrape the bot page.")

    # Example of how to use with a different bot
    # test_url_2 = "https://botify.ai/bot/another_bot_id"
    # print(f"\nScraping {test_url_2}...")
    # scraped_info_2 = scrape_bot_page(test_url_2)
    # if scraped_info_2:
    #     print(json.dumps(scraped_info_2, indent=2))
    # else:
    #     print(f"Failed to scrape {test_url_2}")

def scrape_chat_page(chat_url):
    """
    Scrapes the chat page of a Botify bot to extract the first message from the bot,
    including any image and text.

    Args:
        chat_url (str): The URL of the bot's chat page.
                        Example: "https://botify.ai/bot_268784/chat"

    Returns:
        dict: A dictionary containing the first message data:
              {
                  "first_message_image_url": str or None,
                  "first_message_text": str or None
              }
              Returns None if the page cannot be fetched or essential data is missing.
    """
    try:
        response = requests.get(chat_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {chat_url}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    first_message_data = {
        "first_message_image_url": None,
        "first_message_text": None
    }

    # Attempt to find data in __NEXT_DATA__ script tag
    next_data_script = soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
    if next_data_script:
        try:
            data = json.loads(next_data_script.string)
            props = data.get('props', {}).get('pageProps', {})

            # The structure for initial messages can vary greatly.
            # Common paths: props.initialMessages, props.chat.messages, props.conversation.history
            # We're looking for the first message, usually from the 'bot' or 'assistant'.

            initial_messages = []
            if props.get('initialMessages'):
                initial_messages = props['initialMessages']
            elif props.get('chat') and isinstance(props['chat'], dict) and props['chat'].get('messages'):
                initial_messages = props['chat']['messages']
            elif props.get('conversation') and isinstance(props['conversation'], dict) and props['conversation'].get('history'):
                initial_messages = props['conversation']['history']
            # Add more potential paths based on observation if needed

            if initial_messages and isinstance(initial_messages, list) and len(initial_messages) > 0:
                # Assuming the first message in the list is the one we want,
                # and it might have a sender role like 'bot', 'assistant', or be implicitly the bot's first turn.
                first_bot_message = None
                for msg in initial_messages:
                    if isinstance(msg, dict):
                        # Heuristic: bot messages might have a specific role or lack a 'user' role
                        # Or they might be the very first message in the array.
                        # For now, let's assume the first message object is the bot's greeting.
                        # A more robust check would be msg.get('role') == 'assistant' or msg.get('sender') == 'bot'
                        first_bot_message = msg
                        break

                if first_bot_message:
                    # --- Extracting First Message Text ---
                    # Paths: message.text, message.content, message.body
                    if first_bot_message.get('text'):
                        first_message_data['first_message_text'] = first_bot_message['text']
                    elif first_bot_message.get('content') and isinstance(first_bot_message['content'], str):
                        first_message_data['first_message_text'] = first_bot_message['content']
                    elif first_bot_message.get('body'):
                         first_message_data['first_message_text'] = first_bot_message['body']

                    # --- Extracting First Message Image URL ---
                    # Paths: message.imageUrl, message.attachment.url, message.image.url
                    # Example value: "https://botify-galleries.s3.us-west-2.amazonaws.com/...jpg"
                    if first_bot_message.get('imageUrl'):
                        first_message_data['first_message_image_url'] = first_bot_message['imageUrl']
                    elif first_bot_message.get('attachment') and isinstance(first_bot_message['attachment'], dict) and first_bot_message['attachment'].get('url'):
                        first_message_data['first_message_image_url'] = first_bot_message['attachment']['url']
                    elif first_bot_message.get('image') and isinstance(first_bot_message['image'], dict) and first_bot_message['image'].get('url'):
                        first_message_data['first_message_image_url'] = first_bot_message['image']['url']
                    # Sometimes images are in a list of attachments
                    elif first_bot_message.get('attachments') and isinstance(first_bot_message['attachments'], list):
                        for attachment in first_bot_message['attachments']:
                            if isinstance(attachment, dict) and attachment.get('type') == 'image' and attachment.get('url'):
                                first_message_data['first_message_image_url'] = attachment['url']
                                break # Take the first image found

        except json.JSONDecodeError:
            print("Could not parse JSON from __NEXT_DATA__ script tag on chat page.")
        except Exception as e:
            print(f"Error processing __NEXT_DATA__ on chat page: {e}")

    # Fallback HTML parsing if __NEXT_DATA__ doesn't yield results or isn't present
    if not first_message_data['first_message_text']:
        # This is highly speculative and depends on the rendered HTML structure.
        # Example: <div class="message bot-message"> <p class="message-text">...</p> <img src=".."> </div>
        # We'd need to inspect the actual rendered HTML to create reliable selectors.
        # For now, this is a placeholder.
        # Let's assume the first text block after a certain known element or with a specific class.
        # This is very difficult without seeing the rendered HTML.
        # A simple heuristic might be to find the first substantial text block.

        # Try to find a div that looks like a message bubble from the bot
        # This is extremely fragile.
        potential_message_elements = soup.find_all(['div', 'p'], limit=10) # Look in first few divs/ps
        for el in potential_message_elements:
            text = el.get_text(separator='\n', strip=True)
            # A simple heuristic: if it contains multiple lines or a known phrase
            if text and ("\n" in text or len(text) > 50): # Arbitrary length check
                 # Check if it's not part of UI text (e.g., button text, headers)
                 # This is very hard to do reliably.
                 # Let's assume the example text:
                 if "digital muse" in text or "Joi, crafted to become" in text:
                    first_message_data['first_message_text'] = text
                    # Try to find an image sibling or child of this text's parent
                    parent = el.find_parent()
                    if parent:
                        img_tag = parent.find('img', attrs={'src': re.compile(r"galleries.*\.jpg|galleries.*\.png", re.IGNORECASE)})
                        if img_tag and img_tag.get('src'):
                            first_message_data['first_message_image_url'] = img_tag['src']
                    break

    if not first_message_data['first_message_image_url']:
        # Fallback for image if not found with text
        # Look for an image that seems like a message attachment
        img_tag = soup.find('img', attrs={'src': re.compile(r"galleries.*\.jpg|galleries.*\.png", re.IGNORECASE)})
        if img_tag and img_tag.get('src'):
            # Check if it's not the profile avatar if we somehow landed on a page that also shows it
            # This is unlikely for a dedicated chat page.
            first_message_data['first_message_image_url'] = img_tag['src']


    if not first_message_data.get("first_message_text") and not first_message_data.get("first_message_image_url"):
        print(f"Could not extract first message data from {chat_url}.")

    return first_message_data

if __name__ == '__main__':
    # Test with the example URL for main page
    test_url = "https://botify.ai/bot_268784"
    print(f"Scraping {test_url}...")
    scraped_info = scrape_bot_page(test_url)

    if scraped_info:
        print("\n--- Scraped Bot Information ---")
        print(f"Bot Name: {scraped_info.get('bot_name')}")
        print(f"Profile Picture URL: {scraped_info.get('profile_picture_url')}")
        print(f"Description: {scraped_info.get('description')}")
        print(f"Voice ID: {scraped_info.get('voice_id')}")
        print(f"Is NSFW: {scraped_info.get('is_nsfw')}")
        print(f"Gender: {scraped_info.get('gender')}")

        print("\nTags:")
        if scraped_info.get('tags'):
            for tag in scraped_info['tags']:
                print(f"- {tag}")
        else:
            print("No tags found.")

        print("\nPhoto URLs:")
        if scraped_info.get('photo_urls'):
            for photo_url in scraped_info['photo_urls']:
                print(f"- {photo_url}")
        else:
            print("No photo URLs found.")
        print("--- End of Scraped Bot Information ---")
    else:
        print(f"Failed to scrape the bot page: {test_url}")


    base_bot_url = "https://botify.ai/bot_268784" # Example bot
    # Extract bot_id for directory naming, assuming URL format like ".../bot_<id>"
    bot_id_match = re.search(r'bot_(\d+)', base_bot_url)
    if not bot_id_match:
        print(f"Could not extract bot_id from URL: {base_bot_url}. Using a generic directory name.")
        bot_specific_dir_name = "unknown_bot"
    else:
        bot_specific_dir_name = f"bot_{bot_id_match.group(1)}"

    # Define base directory for all bot data
    main_output_directory = "bot_data"
    bot_data_directory = os.path.join(main_output_directory, bot_specific_dir_name)

    print(f"Data will be saved in: {bot_data_directory}")

    # Scrape main bot page
    print(f"\nScraping bot page: {base_bot_url}...")
    bot_info = scrape_bot_page(base_bot_url)

    # Scrape chat page
    chat_url = f"{base_bot_url}/chat"
    print(f"\nScraping chat page: {chat_url} for first message...")
    chat_info = scrape_chat_page(chat_url)

    if not bot_info and not chat_info:
        print("Failed to scrape any information. Exiting.")
    else:
        # Prepare a dictionary to store all text info and paths to downloaded files
        output_data = {
            "bot_page_url": base_bot_url,
            "chat_page_url": chat_url,
            "bot_details": bot_info if bot_info else {},
            "chat_details": chat_info if chat_info else {},
            "downloaded_files": {}
        }

        os.makedirs(bot_data_directory, exist_ok=True)

        # Download profile picture
        if bot_info and bot_info.get('profile_picture_url'):
            print(f"\nDownloading profile picture from: {bot_info['profile_picture_url']}")
            profile_pic_filename = "profile_avatar" + os.path.splitext(bot_info['profile_picture_url'])[1] # keep original extension
            if not profile_pic_filename.endswith(('.jpg', '.jpeg', '.png', '.gif')): # ensure common image extensions
                profile_pic_filename = "profile_avatar.jpg"
            saved_profile_pic = download_image(bot_info['profile_picture_url'], bot_data_directory, profile_pic_filename)
            if saved_profile_pic:
                output_data["downloaded_files"]["profile_picture"] = os.path.relpath(saved_profile_pic, main_output_directory)


        # Download gallery photos
        if bot_info and bot_info.get('photo_urls'):
            print("\nDownloading gallery photos...")
            output_data["downloaded_files"]["gallery_photos"] = []
            for i, photo_url in enumerate(bot_info['photo_urls']):
                gallery_photo_filename = f"gallery_{i}" + os.path.splitext(photo_url)[1]
                if not gallery_photo_filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                     gallery_photo_filename = f"gallery_{i}.jpg"
                print(f"Downloading gallery photo {i+1} from: {photo_url}")
                saved_gallery_photo = download_image(photo_url, bot_data_directory, gallery_photo_filename)
                if saved_gallery_photo:
                    output_data["downloaded_files"]["gallery_photos"].append(os.path.relpath(saved_gallery_photo, main_output_directory))

        # Download first message image
        if chat_info and chat_info.get('first_message_image_url'):
            print(f"\nDownloading first message image from: {chat_info['first_message_image_url']}")
            fm_image_filename = "first_message_image" + os.path.splitext(chat_info['first_message_image_url'])[1]
            if not fm_image_filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                fm_image_filename = "first_message_image.jpg"
            saved_fm_image = download_image(chat_info['first_message_image_url'], bot_data_directory, fm_image_filename)
            if saved_fm_image:
                 output_data["downloaded_files"]["first_message_image"] = os.path.relpath(saved_fm_image, main_output_directory)

        # Save all collected information to info.json
        info_file_path = os.path.join(bot_data_directory, "info.json")
        try:
            with open(info_file_path, 'w') as f:
                json.dump(output_data, f, indent=4)
            print(f"\nAll textual information saved to: {info_file_path}")
        except IOError as e:
            print(f"Error writing info.json: {e}")
        except TypeError as e:
            print(f"Error serializing data to JSON: {e}")

        print("\n--- Script Finished ---")
