Function contract: count_vowels(text).

- text: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Return the number of ASCII vowels a,e,i,o,u in either ASCII case. Accented letters and y do not count.

Return type: exact built-in int.

Coverage expectations: include normal cases for empty, both-ascii-cases, no-vowels, mixed-text, exclude-accent-y, digits-punctuation. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import count_vowels'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
