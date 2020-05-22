# error reporting helper routine
def report_error(error, line_num):
    print("Line " + str(line_num) + ": ")
    print(error)
    exit(1)


# parse the manifest part of the input file
def collect_manifest_code(file, line_num):
    manifest = file.readline()
    line_num += 1

    manifest = manifest.strip()
    manifest_code = ''
    if manifest != "_manifest:":
        report_error("_manifest: label not found!", line_num)

    while True:
        file_pos = file.tell()
        line = file.readline()
        line_num += 1
        if not line or "_tokens:" in line:
            file.seek(file_pos)
            break
        manifest_code += line

    return manifest_code, line_num


# parse the token definitions
def collect_tokens(file, line_num):
    tokens = file.readline().strip()
    line_num += 1
    if tokens != "_tokens:":
        report_error("_tokens: label not found!", line_num)

    token_list = []
    while True:
        file_pos = file.tell()
        line = file.readline()
        line_num += 1
        if not line or "_defines:" in line:
            file.seek(file_pos)
            break

        token_list.append(line.strip())

    return token_list, line_num

