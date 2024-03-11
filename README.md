Gruyere - a web application with holes.

Copyright 2017 Google Inc. All Rights Reserved.

This code is licensed under the http://creativecommons.org/licenses/by-nd/3.0/us
Creative Commons Attribution-No Derivative Works 3.0 United States license.

DO NOT COPY THIS CODE!

This application is a small self-contained web application with numerous
security holes. It is provided for use with the Web Application Exploits and
Defenses codelab. You may modify the code for your own use while doing the
codelab but you may not distribute the modified code. Brief excerpts of this
code may be used for educational or instructional purposes provided this
notice is kept intact. By using Gruyere you agree to the Terms of Service
http://code.google.com/terms.html

---

# Security Updates - [11.03.2024]

- [Reflected XSS](#reflected-xss)
- [Stored XSS](#stored-xss)

## Reflected XSS

### Vulnerability Description

A security vulnerability was identified in the Gruyere web application that allows for potential Cross-Site Scripting (XSS) attacks. The issue arises from user input not being properly escaped when displayed in error messages.

### Exploitation Example

An attacker could craft a malicious URL, enticing a victim to click on it:

```html
https://google-gruyere.appspot.com/123/<script>alert(1)</script>
```

### Fix

To address this vulnerability, needs proper escaping of user input in the error messages template `(error.gtl)`. I add the `:text` modifier to escape user input:

```html
<!-- Example Fix in error.gtl -->
<div class="message">{{_message:text}}</div>
```

# Stored XSS

## Vulnerability Description

A potential Stored Cross-Site Scripting (XSS) vulnerability was identified in the Gruyere web application. The vulnerability exists within the snippet functionality, where user-provided data is served back to other users without proper sanitization.

## Exploitation Example

The following examples demonstrate different methods of exploiting the vulnerability:

1. `<a onmouseover="alert(1)" href="#">read this!</a>`
2. `<p <script>alert(1)</script>hello`
3. `</td <script>alert(1)</script>hello`

Multiple failures in sanitizing HTML allow these exploits to work.

## Fix

To address this vulnerability, I used a more robust approach to sanitizing HTML using the `bleach` library. The `_SanitizeTag` function in the `sanitize.py` file is replaced with the following `SanitizeHtml` function:

> Installation: `pip install bleach`

```python
# Fix - Using bleach library
import bleach

def SanitizeHtml(s):
    allowed_tags = [
        'a', 'b', 'big', 'br', 'center', 'code', 'em', 'h1', 'h2', 'h3',
        'h4', 'h5', 'h6', 'hr', 'i', 'img', 'li', 'ol', 'p', 's', 'small',
        'span', 'strong', 'table', 'td', 'tr', 'u', 'ul',
    ]
    
    allowed_attributes = {}

    # Use bleach to sanitize the HTML
    sanitized_html = bleach.clean(s, tags=allowed_tags, attributes=allowed_attributes)

    return sanitized_html
```