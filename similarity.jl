using SQLite

dbfilename = "word_vectors_.sqlite"
isfile(dbfilename) || error("Could not find database file")
db = SQLite.DB(dbfilename)

laeringsmaal = "anbringe eksempler på børnearbejde tidsmæssigt i forhold til hinanden"

ffm1 = "placere elementer fra historien tidsmæssigt i forhold til hinanden relativ kronologi"
ffm2 = "sammenligne tidlige tiders familie, slægt og fællesskaber med eget liv fællesskaber før og nu"
ffm3 = "bruge historiske spor i lokalområdet til at fortælle om fortiden identifikation af historiske spor i lokalområdet"

not_ffm = "Ukraine er i krig med rusland og Gandalf er meget sød"

function vectorize(text::AbstractString)
    words = split(text, " ")
    result = []
    
    for word in words
        sql = "SELECT * FROM word_vectors WHERE word = ? COLLATE NOCASE"
        r   = SQLite.query(db, sql, values=[word])
        size(r, 1) == 1 && push!(result, map(e -> e.value, convert(Array, r[1, 3:end])))
    end
    
    sum(result)
end

cossim(x, y) = 1 - dot(x, y) / (norm(x) * norm(y))

# --- test --- #
x = vectorize(laeringsmaal)
y1 = vectorize(ffm1)
y2 = vectorize(ffm2)
y3 = vectorize(ffm3)

z3 = vectorize(not_ffm)

println("Læringsmål: $laeringsmaal")

println("FFM1($ffm1): $(cossim(x, y1))")
println("FFM1($ffm2): $(cossim(x, y2))")
println("FFM1($ffm3): $(cossim(x, y3))")

println("NOT FFM($not_ffm): $(cossim(x, z3))")
