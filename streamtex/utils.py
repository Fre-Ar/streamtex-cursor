import os
import re
import base64
import requests
from requests.exceptions import ConnectionError, Timeout
from bs4 import BeautifulSoup as bs
import uuid
import textwrap

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
    """
    
    # 1. CSS
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
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.15s ease;
        }
        #streamtex-preview-card.visible { display: block; opacity: 1; }
        .st-card-row { display: flex; align-items: center; gap: 10px; }
        .st-card-favicon { width: 20px; height: 20px; border-radius: 4px; }
        .st-card-content { display: flex; flex-direction: column; overflow: hidden; }
        .st-card-title { font-size: 14px; font-weight: 600; color: #333; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
        .st-card-url { font-size: 11px; color: #1a73e8; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
    </style>
    """
    
    # 2. JS: DOM Construction Mode (No HTML strings)
    # We use textwrap.dedent to ensure clean indentation
    js = textwrap.dedent("""
    <script>
    (function() {
        console.log("StreamTeX: Init");

        // 1. Safe Card Creation using createElement (Avoids innerHTML parser issues)
        var existing = document.getElementById('streamtex-preview-card');
        if (!existing) {
            var card = document.createElement('div');
            card.id = 'streamtex-preview-card';
            
            var row = document.createElement('div');
            row.className = 'st-card-row';
            
            var img = document.createElement('img');
            img.className = 'st-card-favicon';
            
            var content = document.createElement('div');
            content.className = 'st-card-content';
            
            var titleSpan = document.createElement('span');
            titleSpan.className = 'st-card-title';
            titleSpan.textContent = 'Loading...';
            
            var urlSpan = document.createElement('span');
            urlSpan.className = 'st-card-url';
            
            // Assemble
            content.appendChild(titleSpan);
            content.appendChild(urlSpan);
            row.appendChild(img);
            row.appendChild(content);
            card.appendChild(row);
            
            document.body.appendChild(card);
        }

        // 2. References
        var card = document.getElementById('streamtex-preview-card');
        var cardImg = card.querySelector('.st-card-favicon');
        var cardTitle = card.querySelector('.st-card-title');
        var cardUrl = card.querySelector('.st-card-url');

        // 3. Listener Logic
        function attachListeners() {
            var links = document.querySelectorAll('a.streamtex-link');
            
            links.forEach(function(link) {
                if (link.dataset.hasListener) return;
                link.dataset.hasListener = "true";

                link.addEventListener('mouseenter', function() {
                    var href = link.href;
                    if (!href) return;

                    try {
                        var urlObj = new URL(href);
                        cardImg.src = 'https://www.google.com/s2/favicons?domain_url=' + href + '&sz=64';
                        cardTitle.textContent = urlObj.hostname;
                        cardUrl.textContent = href;

                        var rect = link.getBoundingClientRect();
                        var top = rect.bottom + 8;
                        var left = rect.left;

                        if (left + 280 > window.innerWidth) left = window.innerWidth - 300;
                        if (top + 80 > window.innerHeight) top = rect.top - 90;

                        card.style.top = top + 'px';
                        card.style.left = left + 'px';
                        card.classList.add('visible');
                    } catch (e) { console.log(e); }
                });

                link.addEventListener('mouseleave', function() {
                    card.classList.remove('visible');
                });
            });
        }

        // 4. Observer
        if (window.stxObs) window.stxObs.disconnect();
        window.stxObs = new MutationObserver(attachListeners);
        window.stxObs.observe(document.body, { childList: true, subtree: true });
        
        // Initial run
        setTimeout(attachListeners, 500);
        console.log("StreamTeX: Ready");
    })();
    </script>
    """)
    
    st.html(css)
    st.html(js, unsafe_allow_javascript=True)
    
    
def contain_link(html_content="", link="", no_link_decor=False, hover=True):
    """
    Wraps the given HTML content in an anchor tag, optionally adding a hover preview box.

    :param html: The HTML content to be wrapped in the anchor tag.
    :param link: The hyperlink to associate with the content. If empty, the function returns the original HTML.
    :param no_link_decor: If True, removes text decoration (like underline) from the link. Defaults to False.
    :param hover: If True, includes a hover preview box showing the page title and favicon. Defaults to True.
    :return: A string containing the original HTML wrapped in an anchor tag with optional hover content.
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
