"""Declared contract-based candidate-007 additions; no model answers used as targets."""
LABELS = {
"TR001":"zero-items|partial-batch|exact-capacity|remainder|unit-capacity|large-integer",
"TR002":"remove-prefix|whole-prefix|absent-prefix|empty-text|remove-once|case-sensitive|start-only|space-prefix|unicode-prefix|long-prefix",
"TR003":"equal|left-larger|right-larger|mixed-sign|reverse-mixed-sign|both-negative|large",
"TR004":"below|lower-bound|inside|upper-bound|above|equal-bounds|negative-bounds",
"TR005":"zero|odd|even|negative-odd|negative-even|large",
"TR006":"zero-factorial|one|two|intermediate|upper-bound",
"TR007":"zero|single-digit|decimal-zero|internal-zero|repeated-digits|large",
"TR008":"zero|one|nonsquare|square|below-square|square-sixteen|above-square|large-square",
"TR009":"both-zero|left-zero|right-zero|ordinary|negative-left|negative-right|both-negative|coprime",
"TR010":"zero|one-bit|power-two|two-bits|byte-bits|higher-power|large-two-bits",
"TR011":"lower-bound|divisible-four|century-not-leap|century-leap|ordinary-not-leap|ordinary-leap|future-century|upper-bound",
"TR012":"identity|forward|wrap|negative-wrap|multiple-weeks|negative-weeks|forward-wrap",
"TR013":"zero|one|alphabetic-digit|carry|binary|ternary|hexadecimal|octal",
"TR014":"empty|unchanged|spaces-only|edges-and-run|preserve-tab|preserve-lf|unicode",
"TR015":"empty|whitespace-only|one-word|reverse-order|mixed-whitespace|unicode-whitespace",
"TR016":"empty|both-ascii-cases|no-vowels|mixed-text|exclude-accent-y|digits-punctuation",
"TR017":"both-empty|right-empty|left-empty|equal-length|left-remainder|right-remainder|unicode-space",
"TR018":"empty|one|two-equal|odd-palindrome|even-palindrome|not-palindrome|case-sensitive|literal-space|unicode",
"TR019":"empty|unchanged|crlf|cr|lf|mixed|adjacent-cr-crlf",
"TR020":"empty|unchanged|amp-angle|both-quotes|escape-existing-entity|unicode-combination",
"TR021":"both-empty|left-empty|equal|partial|shorter-right|case-sensitive|unicode",
"TR022":"empty-quoted|unquoted|comma|quote-doubled|cr|lf|preserve-space|unicode",
"TR023":"zero-plural|one-singular|ordinary-plural|literal-singular|literal-suffix|unicode-noun",
"TR024":"empty|ascii-case|punctuation-digits|nonascii-unchanged|newline",
"TR025":"empty|single|separated-runs|empty-strings|case-distinct|unicode",
"TR026":"empty|single|stable-order|zero-negative|already-unique",
"TR027":"empty|single|signed-differences|equal-pair|negative-values",
"TR028":"empty|single|ordinary|mixed-sign|zeros",
"TR029":"empty|partial-single|full-chunks|last-partial|unit-width|oversize-width",
"TR030":"empty|one-zero-column|several-zero-columns|square|one-row|one-column",
"TR031":"both-empty|right-empty|left-empty|multiplicity|count-limit|negative-order",
"TR032":"empty|zero|all-signs-stable|positive-only|negative-only",
"TR033":"only-item|first|middle|last|duplicates",
"TR034":"empty|full|middle|reversed-valid|end-empty",
"TR035":"empty|single|one-pair|long-run|separated-equals|several-runs",
"TR036":"single|even-lower|odd|even-unsorted|negative-duplicate",
"TR037":"zero|one|ordinary|maximum-length",
"TR038":"zero|decimal-digits|lowercase|mixed-case|byte-upper-bound|intermediate",
"TR039":"true|false",
"TR040":"ordinary|empty-value|first-equals-only|preserve-space|unicode",
"TR041":"zeros|negative-zero|signed-pair|maximum-length",
"TR042":"zeros|ordinary|upper-bound",
"TR043":"zero|one|leading-zeros|ordinary|maximum-length",
"TR044":"zero-width|full-boundaries|ordinary|equal-upper",
"TR045":"empty|separator-only|repeated-separators|literal-dot-segments|literal-backslash|space-unicode",
"TR046":"zero|negative-zero|positive-zero|leading-zeros|negative|maximum-length",
"TR047":"empty|first-overlap|second-overlap|third-overlap|missing-overlap|whole-string|absent|unicode",
"TR048":"lower-bound|last-single|first-double|double-boundary|last-double|first-triple|upper-bound",
"TR049":"single-cell|top-right|bottom-left|last-offset",
"TR050":"single-cell|origin|end-first-row|start-second-row|last-cell",
"TR051":"unit-length|positive-wrap|negative-one|negative-period|positive-period|large",
"TR052":"zero|last-second|minute|last-minute|hour|hours-over-day",
"TR053":"zero|fractional|negative-fractional|last-fraction|whole-unit|negative-whole|ordinary|large",
"TR054":"zero|single|last-ungrouped|first-grouped|negative|several-groups|large",
"TR055":"zero-components|maximum-components|ordinary|mixed-boundaries",
"TR056":"zero-components|maximum-components|ordinary|mixed-case",
"TR057":"empty|separators-only|lowercase|separator-runs|digits",
"TR058":"equal|less|greater-middle|lexicographic-major",
"TR059":"both-empty|right-empty|left-empty|interleaving|duplicates|negatives",
"TR060":"empty|ascii-letters-digits|mixed|unicode-other|whitespace-other",
"DV001":"empty-zero|empty-positive|single-negative|identity|right|left|wrap|duplicates|mutable-elements",
"DV002":"midnight|minute|hour|ordinary|last-minute",
"DV003":"lower-bound|iv|ix|xl|xc|cd|cm|combined|upper-bound",
"DV004":"empty|zero|maximum-byte|ordinary|duplicate-cancellation|repeated-cancellation",
"DV005":"empty|one-pair|nested|siblings|deep",
"DV006":"empty|first-group|ordinary|pqrs|wxyz|full-alphabet",
"DV007":"single-cell|top-left|interior-order|bottom-right|single-row|single-column",
"DV008":"both-empty|left-empty|right-empty|equal|substitution|two-edits|multistep|unicode-accent",
"DV009":"empty|before|equal|after|leftmost-duplicate|gap|negative",
"DV010":"zero|negative-zero|addition|subtraction|precedence-stack|negative-product",
"DV011":"empty|single|unordered-touching|nested|disjoint|negative-overlap",
"DV012":"empty|single-pair|nested-all-kinds|mismatched|unclosed|premature-close|reversed|concatenated"
}
VALID = {
"TR014":[(("a\u00a0 b",),"preserve-nbsp")],
"TR018":[(("a a!",),"literal-punctuation-and-space")],
"TR031":[(([2,1,2],[1,2]),"left-order-not-sorted")],
"TR032":[(([3,1,0,-1,-3],),"positive-negative-order")],
"TR041":[(("-999999999999,999999999999",),"both-components-max-length")],
"TR042":[(("0.999.999",),"later-components-upper-bound")],
"TR047":[(("Aa","a",1),"literal-case"),(("aA","a",2),"no-second-case-match")],
"TR053":[((-12345,),"negative-units-and-fraction")],
"DV008":[(("A","a"),"ascii-case-sensitive"),(("é","É"),"unicode-case-sensitive"),(("é","e\u0301"),"literal-codepoints-no-normalization")],
"DV010":[((["1"]*16+["+"]*15,),"long-valid-expression")],
"DV011":[(([(5,7),(1,3),(2,6)],),"transitive-unordered-union")]
}
INVALID = {
"TR037":[(("٣",),"ValueError","ascii-digits"),(("３",),"ValueError","ascii-digits")],
"TR038":[(("٣f",),"ValueError","ascii-digits"),(("３f",),"ValueError","ascii-digits")],
"TR041":[(("٣,4",),"ValueError","ascii-digits"),(("3,４",),"ValueError","ascii-digits"),(("0,1000000000000",),"ValueError","second-component-length")],
"TR042":[(("١.2.3",),"ValueError","ascii-digits"),(("1.２.3",),"ValueError","ascii-digits"),(("0.1000.0",),"ValueError","second-component-domain"),(("0.0.1000",),"ValueError","third-component-domain")],
"TR043":[(("١٠",),"ValueError","ascii-digits"),(("１０",),"ValueError","ascii-digits")],
"TR044":[(("[١:٣]",),"ValueError","ascii-digits"),(("[１:３]",),"ValueError","ascii-digits")],
"TR046":[(("+١",),"ValueError","ascii-digits"),(("-１",),"ValueError","ascii-digits")],
"TR056":[(("#١٢٣٤٥٦",),"ValueError","ascii-digits"),(("#１２３４５６",),"ValueError","ascii-digits")],
"TR057":[(("٣",),"ValueError","ascii-only"),(("Ａ",),"ValueError","ascii-only")],
"DV002":[(("٠١:٠٢",),"ValueError","ascii-digits"),(("０１:０２",),"ValueError","ascii-digits")],
"DV006":[(("Ａ",),"ValueError","uppercase-ascii-only")],
"DV007":[((0,0,1,0),"ValueError","columns-zero"),((0,0,1,-1),"ValueError","columns-negative"),((0,1,1,0),"ValueError","shape-before-bounds")],
"DV010":[((["٣"],),"ValueError","ascii-digits"),((["３"],),"ValueError","ascii-digits")]
}
RETURNS = {}
def assign(ids,text):
    for ident in ids.split(): assert ident not in RETURNS; RETURNS[ident]=text
assign("TR001 TR003 TR004 TR006 TR007 TR009 TR010 TR012 TR016 TR035 TR036 TR037 TR038 TR043 TR046 TR047 TR049 TR051 TR058 DV002 DV004 DV005 DV008 DV009 DV010","exact built-in int")
assign("TR008 TR011 TR018 TR039 DV012","exact built-in bool")
assign("TR002 TR005 TR013 TR014 TR015 TR017 TR019 TR020 TR021 TR022 TR023 TR024 TR048 TR053 TR054 TR055 TR057 DV003 DV006","exact built-in str")
assign("TR026 TR027 TR028 TR031 TR033 TR034 TR059","exact built-in list of exact built-in ints")
assign("TR045","exact built-in list of exact built-in strings")
assign("TR029 TR030","exact built-in list of exact built-in lists of exact built-in ints")
assign("TR025","exact built-in list of exact two-item tuples (exact str label, exact int count)")
assign("TR032","exact built-in three-item tuple of exact lists of exact ints")
assign("TR041 TR044 TR050","exact built-in two-item tuple of exact built-in ints")
assign("TR042 TR052 TR056 TR060","exact built-in three-item tuple of exact built-in ints")
assign("TR040","exact built-in two-item tuple of exact built-in strings")
assign("DV007 DV011","exact built-in list of exact two-item tuples of exact built-in ints")
assign("DV001","exact built-in tuple containing the original element objects, preserving their identities")
assert len(RETURNS)==72 and set(RETURNS)==set(LABELS)

