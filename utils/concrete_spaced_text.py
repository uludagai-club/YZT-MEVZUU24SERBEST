def main(text):
    spaceFlag=True
    newText=""
    for char in text:
        if spaceFlag and char!=" ":
            spaceFlag=False
            newText+=char
        elif char==" ":
            spaceFlag=True
        else:
            return text
    return newText
        
# print(main("Ö D Ü L L E R"))        