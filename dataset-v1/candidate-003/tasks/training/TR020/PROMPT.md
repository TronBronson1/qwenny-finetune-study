Function contract: escape_html(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Escape &, <, >, double quote, and single quote as &amp;, &lt;, &gt;, &quot;, and &#x27; respectively. Do not recognize existing entities; escape their ampersands again.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import escape_html'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
