camel_case= input("Enter string:")

kebab_case= ""

for char in camel_case:
    if char.isupper():
      kebab_case += '-' + char.lower()
    else:
      kebab_case += char

print(kebab_case)