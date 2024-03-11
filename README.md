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
- [XSRF Challenge](#xsrf-challenge)

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

## Stored XSS

### Vulnerability Description

A potential Stored Cross-Site Scripting (XSS) vulnerability was identified in the Gruyere web application. The vulnerability exists within the snippet functionality, where user-provided data is served back to other users without proper sanitization.

### Exploitation Example

The following examples demonstrate different methods of exploiting the vulnerability:

1. `<a onmouseover="alert(1)" href="#">read this!</a>`
2. `<p <script>alert(1)</script>hello`
3. `</td <script>alert(1)</script>hello`

Multiple failures in sanitizing HTML allow these exploits to work.

### Fix

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

## XSRF Challenge

### Vulnerability Description

The XSRF challenge presented a scenario where an attacker could perform an account-changing action on behalf of a logged-in Gruyere user without their knowledge. The vulnerability existed in the snippet deletion functionality, where a simple URL request could delete a snippet.

### Exploitation Example

To exploit the vulnerability, an attacker could craft a URL like the following and lure the user to visit it:

```
https://google-gruyere.appspot.com/123/deletesnippet?index=0
```

### Fix

To fix the vulnerability, I changed snippet deletion work via a `POST` request instead of a `GET` request. The HTML form for snippet deletion was updated to use `method='post'`. Additionally, an anti-CSRF token mechanism was introduced to ensure the authenticity of the request.

The replaced form in `snippets.gtl`:

```html
<form action='/{{_unique_id}}/deletesnippet' method='post'>
    <input type='hidden' name='index' value='{{_key}}'>
    <input type='hidden' name='csrf_token' value='{{ csrf_token }}'>
    <input type='submit' value='Delete Snippet'>
</form>
``` 

The `_DoDeletesnippet` in `gruyere.py` method in the server-side code was modified to check for the `POST` request and verify the `anti-CSRF` token before processing the deletion:

```python
# Add constructor to GruyereRequestHandler class
class GruyereRequestHandler(BaseHTTPRequestHandler):
    def __init__(self):
        self.csrf_token = secrets.token_urlsafe(16)
```

```python
def _VerifyCsrfToken(self, params):
    """Verify the anti-CSRF token."""
    return params.get('csrf_token') == self.csrf_token
```

```python
@staticmethod
def _IsPostRequest(params):
    """Check if the request method is POST."""
    return params.get('REQUEST_METHOD') == 'POST'
```

```python
def _DoDeletesnippet(self, cookie, specials, params):
    if self._IsPostRequest(params):
        if not self._VerifyCsrfToken(params):
            self._SendError('Invalid CSRF Token', cookie, specials, params)
            return

        index = self._GetParameter(params, 'index')
        snippets = self._GetSnippets(cookie, specials)

        try:
            del snippets[int(index)]
        except (IndexError, TypeError, ValueError):
            self._SendError('Invalid index (%s)' % (index,), cookie, specials, params)
            return

        self._SendRedirect('/snippets.gtl', specials[SPECIAL_UNIQUE_ID])
    else:
        self._SendError('Invalid Request Method', cookie, specials, params)
```