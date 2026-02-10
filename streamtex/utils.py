import os
import re
import base64
import html as html_lib
import requests
from requests.exceptions import ConnectionError, Timeout
from bs4 import BeautifulSoup as bs
import uuid
from .toc import get_key_anchor

def _contain_link(html="", link="", no_link_decor=False, hover=True):
    """
    Wraps the given HTML content in an anchor tag, optionally adding a hover preview box.

    :param html: The HTML content to be wrapped in the anchor tag.
    :param link: The hyperlink to associate with the content. If empty, the function returns the original HTML.
    :param no_link_decor: If True, removes text decoration (like underline) from the link. Defaults to False.
    :param hover: If True, includes a hover preview box showing the page title and favicon. Defaults to True.
    :return: A string containing the original HTML wrapped in an anchor tag with optional hover content.

    Notes:
    - If `hover` is enabled, the function fetches a page preview using `get_page_preview` to display additional details.
    - If the page preview is unavailable, it falls back to displaying the link URL.
    """
    if not link:
        return html
    
    else:
        copy_link = link[:]
        if copy_link.strip().startswith("#"):
            # Internal link, no hover preview
            hover = False
            link =  "#" + get_key_anchor(link.strip()[1:])
        hover_content = ''
        data_preview = ""
        if hover:
            # Fetch the page title and icon using `get_page_preview`.
            # This provides contextual information about the link on hover.
            page_title, favicon_url, success = __get_page_preview(link)

            # Check if the page preview was successfully fetched. Fallback to the link if unsuccessful.
            fallback = page_title != 'Could not fetch page' 
            preview_title = page_title if fallback else link
            preview_favicon = favicon_url or 'https://www.google.com/s2/favicons?domain_url=' + link

            hover_content = f"""
            <div class="hide-hover-box">
                <img src="{favicon_url}" alt="favicon" style="vertical-align: middle; margin-right: 8px; width: 16px; height: 16px;">
                
                {f'<embed src="{link}" style="width:300px; height: 300px;">' if success else ''}
            </div>"""

            data_preview = f"""
            <div style="display: flex; align-items: center; margin-bottom: 8px; margin-top: 8px; font-size: 16px; font-weight: bold; color: #2e6ad2; width:300px; max-height: 300px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">
                <img src="{preview_favicon}" style="width:24px; height:24px; margin-right:16px;">
                <span style="width: 300px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;"><a href="{link}" style="font-weight: bold; color: #2e6ad2; text-decoration: none;">{preview_title}</a></span>
            </div>
            """

            if success:
                data_preview += f'<embed src="{link}" style="width:300px; max-height: 300px;">'
            data_preview = data_preview.strip()

        link_style = "text-decoration: none;" if no_link_decor else ""
        data_preview_escaped = html_lib.escape(data_preview)
        
        # Wrap the original HTML content in an anchor tag, optionally disabling the link decorations (underline).
        # The hover box is embedded within the anchor tag.
        # OLD AF - html = f'<a style="{'text-decoration: none;' if no_link_decor else ''} position: relative;" href="{link}">{html}</a>'
        # html = f"<a style=\"{'text-decoration: none;' if no_link_decor else ''} position: relative;\" href=\"{link}\">{html}</a>"
        html = f'<a href="{link}" style="{link_style}position:relative;" data-preview="{data_preview_escaped}">{html}</a>'
    return html

def strip_html(html_string):
    """
    Remove all HTML tags from a string and return plain text.
    
    :param html_string: The string containing HTML content.
    :return: A plain text string with HTML tags removed.
    """
    # Define a regex pattern to match HTML tags
    html_tag_pattern = re.compile(r'<.*?>')
    # Use re.sub to replace HTML tags with an empty string
    plain_text = re.sub(html_tag_pattern, '', html_string)
    return plain_text




def __get_page_preview(url: str):
    """
    Fetches the page title and favicon URL for the given link.
    If the connection is refused or times out, returns 'Could not fetch page' and None,
    preventing display of any preview.
    """
    title = url
    favicon = 'https://www.google.com/s2/favicons?domain_url=' + url
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = bs(response.content, 'html.parser')

        # Get the page title
        title = soup.title.string.strip() if soup.title else 'No title found'

        # Get the favicon
        favicon = None
        icon_link = soup.find('link', rel=lambda x: x and 'icon' in x.lower())
        if icon_link and icon_link.get('href'):
            favicon = icon_link['href']
            if favicon.startswith('//'):
                favicon = 'http:' + favicon
            elif favicon.startswith('/'):
                from urllib.parse import urljoin
                favicon = urljoin(url, favicon)
        else:
            # Default favicon if not found
            favicon = 'https://www.google.com/s2/favicons?domain_url=' + url

        return title, favicon, True
    
    except (ConnectionError, Timeout):
        # Specifically handle connection refusal or timeout
        return title, favicon, False

    except Exception as e:
        return 'Could not fetch page', None, False

def generate_key(prefix: str = "block"):
    return f"{prefix}-{uuid.uuid4().hex}"



def __get_base64_encoded_image(file_path: str):
    """Converts an image to a base64 encoded string."""
    try:
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def __is_url(path: str):
    """Checks if the given path is a URL."""
    return path.startswith(("http://", "https://", "www."))

def __is_absolute_path(path: str):
    """Checks if the given path is an absolute path."""
    return os.path.isabs(path)

def __is_relative_path(path: str):
    """Checks if the given path is a relative path."""
    return path.startswith((".", "..", "/", "\\"))

def __get_mime_type(file_path: str):
    """Determine the MIME type based on the file extension."""
    extension = file_path.lower().split('.')[-1]
    if extension == "png":
        return "image/png"
    elif extension in ["jpg", "jpeg"]:
        return "image/jpeg"
    elif extension == "gif":
        return "image/gif"
    else:
        return None  # Unsupported format or no extension
    
    
import streamlit as st

def inject_link_preview_scaffold():
    """
    Injects the hidden Tooltip container and the JS event listeners.
    Call this ONCE at the start of your app.
    """
    
    # 1. CSS for the Hover Card (Google Docs style)
    css = """
    <style>
        #streamtex-preview-card {
            position: fixed;
            z-index: 999999;
            display: none;
            width: 280px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            border: 1px solid #e0e0e0;
            font-family: sans-serif;
            padding: 12px;
            pointer-events: none; /* Allows mouse to pass through to underlying elements */
            opacity: 0;
            transition: opacity 0.15s ease;
        }
        
        #streamtex-preview-card.visible {
            display: block;
            opacity: 1;
        }

        .st-card-row {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .st-card-favicon {
            width: 20px;
            height: 20px;
            border-radius: 4px;
        }
        
        .st-card-content {
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .st-card-title {
            font-size: 14px;
            font-weight: 600;
            color: #333;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .st-card-url {
            font-size: 11px;
            color: #1a73e8; /* Google Blue */
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
    </style>
    """
    
    # 2. JS: The "Lazy" Logic
    js = """
    <script>
        // A. Build the Card if it doesn't exist
        if (!document.getElementById('streamtex-preview-card')) {
            const card = document.createElement('div');
            card.id = 'streamtex-preview-card';
            card.innerHTML = `
                <div class="st-card-row">
                    <img class="st-card-favicon" src="" />
                    <div class="st-card-content">
                        <span class="st-card-title">Loading...</span>
                        <span class="st-card-url"></span>
                    </div>
                </div>
            `;
            document.body.appendChild(card);
        }

        const card = document.getElementById('streamtex-preview-card');
        const cardImg = card.querySelector('.st-card-favicon');
        const cardTitle = card.querySelector('.st-card-title');
        const cardUrl = card.querySelector('.st-card-url');

        // B. Event Logic
        function attachLinkListeners() {
            // We only target links with our special class
            const links = document.querySelectorAll('a.streamtex-link');
            
            links.forEach(link => {
                if (link.dataset.hasListener) return; 
                link.dataset.hasListener = "true";

                link.addEventListener('mouseenter', (e) => {
                    const urlStr = link.href;
                    if (!urlStr) return;
                    
                    try {
                        const urlObj = new URL(urlStr);
                        
                        // 1. Instant Data (No fetching required)
                        // We use Google's Favicon API which is super fast
                        cardImg.src = `https://www.google.com/s2/favicons?domain_url=${urlStr}&sz=64`;
                        cardTitle.textContent = urlObj.hostname; // Display Domain as title
                        cardUrl.textContent = urlStr;
                        
                        // 2. Position the Card near the mouse/element
                        const rect = link.getBoundingClientRect();
                        let top = rect.bottom + 8;
                        let left = rect.left;
                        
                        // Keep inside viewport
                        if (left + 280 > window.innerWidth) left = window.innerWidth - 300;
                        if (top + 80 > window.innerHeight) top = rect.top - 90;

                        card.style.top = `${top}px`;
                        card.style.left = `${left}px`;
                        card.classList.add('visible');
                        
                    } catch (err) { console.error(err); }
                });

                link.addEventListener('mouseleave', () => {
                    card.classList.remove('visible');
                });
            });
        }

        // C. Watch for new Streamlit elements (MutationObserver)
        const observer = new MutationObserver(attachLinkListeners);
        observer.observe(document.body, { childList: true, subtree: true });
        setTimeout(attachLinkListeners, 500); // Initial run
    </script>
    """
    
    st.html(css)
    st.html(js, unsafe_allow_javascript=True)
    
def contain_link(html_content="", link="", no_link_decor=False, hover=True):
    """
    Wraps content in an anchor tag. 
    Adds 'streamtex-link' class for JS-based lazy preview.
    Zero network requests.
    """
    if not link:
        return html_content
    
    # 1. Check for Internal Links (Anchors)
    # We strip spaces and check for '#'
    clean_link = link.strip()
    is_internal = clean_link.startswith("#")
    
    # 2. Determine Attributes
    # We only enable the hover preview for External links if hover=True
    css_classes = ""
    if hover and not is_internal:
        css_classes = ' class="streamtex-link"'
        
    style_attr = ""
    if no_link_decor:
        style_attr = ' style="text-decoration: none; color: inherit;"'
    
    # 3. Construct HTML
    # Note: We put the style/class on the <a> tag
    return f'<a href="{clean_link}"{css_classes}{style_attr}>{html_content}</a>'
