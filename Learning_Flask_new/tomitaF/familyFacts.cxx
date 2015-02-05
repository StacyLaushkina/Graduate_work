#encoding "utf-8"

Person -> AnyWord<gram="имя">;
Marry -> Verb<kwtype=marry>;
Marry -> Adv<kwtype=marry>;
Full_family -> Noun<kwtype=full_family>;

S -> Person interp(FamilyFact.Person) Marry;

S -> Person interp(FamilyFact.Person) Full_family;

S -> Full_family interp(FamilyFact.Person) Person;

S -> Adj interp(FamilyFact.Person) Full_family;

S -> Full_family interp(FamilyFact.Person) Adj;