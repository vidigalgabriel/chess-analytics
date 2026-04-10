# cortar_pre2013.py
pgn_path = "data/caissapng.pgn"
output_pgn = "data/caissapng_pre2013.pgn"

with open(pgn_path, "r", encoding="utf-8", errors="ignore") as infile, \
     open(output_pgn, "w", encoding="utf-8") as outfile:

    buffer = []
    copy_game = False

    for line in infile:
        if line.startswith("[Event"): 
            if buffer:
                if copy_game:
                    outfile.writelines(buffer)
                buffer = []
            buffer.append(line)
            copy_game = False
        elif line.startswith("[Date "):
            try:
                year = int(line.split('"')[1].split(".")[0])
                if year < 2013:
                    copy_game = True
            except:
                copy_game = False
            buffer.append(line)
        else:
            buffer.append(line)

    if buffer and copy_game:
        outfile.writelines(buffer)