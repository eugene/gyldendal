using SQLite

dbfilename = "word_vectors_.sqlite"
isfile(dbfilename) || error("Could not find database file")
db = SQLite.DB(dbfilename)

laeringsmaal = "fortælle, hvornår en bestemt slags mad og måder at spise på var almindelige"

ffm1 = "Eleven kan placere elementer fra historien tidsmæssigt i forhold til hinanden. "
ffm2 = "Eleven har viden om relativ kronologi"
ffm3 = "Eleven har viden om særtræk ved historiske fortællinger"

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

# cosine betweeen all combinations  
# average distance between combinations

