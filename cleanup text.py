import unicodedata

input_file = "C:/Data Projects/Portfolio/bhara033.github.io/hugo.yaml"
output_file = "C:/Data Projects/Portfolio/bhara033.github.io/cleaned hugo.yaml"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# Normalize Unicode characters
# Converts LinkedIn-style characters (when possible) to standard equivalents
cleaned = unicodedata.normalize("NFKC", text)

# Remove common formatting artifacts
replacements = {
    "•": "-",
    "<br>": "\n",
    "<br/>": "\n",
    "<br />": "\n",
    "<strong>": "",
    "</strong>": "",
    "<b>": "",
    "</b>": "",
    "**": "",
    "__": "",
}

for old, new in replacements.items():
    cleaned = cleaned.replace(old, new)

# Remove trailing whitespace on each line
cleaned = "\n".join(line.rstrip() for line in cleaned.splitlines())

# Write cleaned output
with open(output_file, "w", encoding="utf-8") as f:
    f.write(cleaned)

print(f"Cleanup complete. Saved as: {output_file}")
