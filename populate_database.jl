# Pkg.add("SQLite")

using SQLite

# db = SQLite.DB("word_vectors.sqlite")
dbfilename = "word_vectors_.sqlite"
isfile(dbfilename) && rm(dbfilename)
db = SQLite.DB(dbfilename)

create_statement = """
CREATE TABLE `word_vectors` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`word`	TEXT,
    $(join(map(i -> "`coordinate_$i` REAL",1:300), ","))
);
"""

index_statement = """
CREATE INDEX word_index ON word_vectors (
    word
);
"""

SQLite.query(db, create_statement)
SQLite.query(db, index_statement)

f = open("/Users/eugene/Git/fastText/models/wiki.da.vec")

i = 0
for ln in eachline(f)
    i+=1

    # skip the first line
    if i == 1
        continue 
    end

    # print("$i $(length(ln)), $ln")
    line_array = split(ln, ' ', keep = false)
    word = replace(line_array[1], "'", "\\'")
    coordinates = filter(e -> e != "\n", line_array[2:end])
    coordinates = map(c -> parse(Float64, c), coordinates)

    SQLite.query(db, "INSERT INTO word_vectors (word, $(join(map(i -> "coordinate_$i",1:300), ","))) VALUES ($(join(map(e -> '?', 1:301), ",")))"; values=cat(1, word, coordinates))

    i % 1000 == 0 && println("Inserted $i entries")
end
 