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