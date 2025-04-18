Detta är ett rekommendationssystem för filmer. Systemet kombinerar genrer och taggar för att kunna ge förslag på flera iknande filmer och bygger på TF-IDF för textanalys och cosine similarity för att räkna ut hur lika filmerna är.

Först görs en förbehandling av datan där filmernas genrer delas upp i listor vilket gör det möjligt att hantera filmer med flera genrer. Genrerna omvandlas sedan till binär form med så kallad one-hot encoding vilket innebär att varje genre får sin egen kolumn där en film får ett värde på 1 om den tillhör genren eller 0 om den inte gör det. Taggarna från användare samlas ihop till en sammanhängande text per film och för att säkerställa att taggarna innehåller tillräckligt med information filtreras filmer som har färre än tre taggar bort vilket förbättrar rekommendationerna.

Efteråt sker en vektorisering av taggarna. Här används TF-IDF som är en metod för att vikta ord efter hur viktiga de är för ett specifikt dokument, i detta fall en film. Vanliga ord som förekommer i många filmer får låg vikt medan unika eller ovanliga ord får högre vikt. Genrerna viktas upp ytterligare genom att multipliceras med en faktor två och detta görs eftersom genrer ofta har större betydelse än taggar när det gäller att avgöra hur lika filmer är.

Därefter beräknas likheten mellan filmerna med hjälp av cosine similarity. Denna metod mäter vinkeln mellan två vektorer, ju mindre vinkel desto mer lika är filmerna. Kombinationen av genrer och TF-IDF-viktade taggar gör att systemet kan identifiera filmer som liknar varandra genom både genrer och taggar.

Systemet tar inte hänsyn till användarbetyg utan bygger helt på innehållet i filmerna. Det gör det särskilt användbart när man vill rekommendera filmer till nya användare eller när man saknar tillgång till betygsdata därför är genrer mer prioriterade än taggar.

Sammanfattningsvis erbjuder detta system ett enkelt sätt att hitta liknande filmer baserat på vad de handlar om och hur de beskrivs.