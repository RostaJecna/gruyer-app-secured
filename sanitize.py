"""HTML sanitizer for Gruyere, a web application with holes.

Copyright 2017 Google Inc. All rights reserved.

This code is licensed under the https://creativecommons.org/licenses/by-nd/3.0/us/
Creative Commons Attribution-No Derivative Works 3.0 United States license.

DO NOT COPY THIS CODE!

This application is a small self-contained web application with numerous
security holes. It is provided for use with the Web Application Exploits and
Defenses codelab. You may modify the code for your own use while doing the
codelab but you may not distribute the modified code. Brief excerpts of this
code may be used for educational or instructional purposes provided this
notice is kept intact. By using Gruyere you agree to the Terms of Service
https://www.google.com/intl/en/policies/terms/
"""

__author__ = 'Bruce Leban'

# system modules
import re
import bleach


def SanitizeHtml(s):
    """Makes html safe for embedding in a document.

    Filters the html to exclude all but a small subset of html by
    removing script tags/attributes.

    Args:
      s: some html to sanitize.

    Returns:
      The html with all unsafe html removed.
    """

    # Define a whitelist of allowed tags and attributes
    allowed_tags = [
        'a', 'b', 'big', 'br', 'center', 'code', 'em', 'h1', 'h2', 'h3',
        'h4', 'h5', 'h6', 'hr', 'i', 'img', 'li', 'ol', 'p', 's', 'small',
        'span', 'strong', 'table', 'td', 'tr', 'u', 'ul',
    ]
    allowed_attributes = {}

    # Use bleach to sanitize the HTML
    sanitized_html = bleach.clean(s, tags=allowed_tags, attributes=allowed_attributes)

    return sanitized_html
