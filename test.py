with open("test.md", "w") as f:
    f.write("```ansi\n")
    f.write("\033[31mRed text\033[0m\n")
    f.write("\033[32mGreen text\033[0m\n")
    f.write("\033[34mBlue text\033[0m\n")
    f.write("```\n")
