#encoding "utf-8"

Person -> AnyWord<gram="имя">;
Born -> Verb<kwtype=born>;
Dead -> Verb<kwtype=dead>;
Live -> Verb<kwtype=live>;
Family -> Noun<kwtype=family>;


S -> Person interp(BasicFact.Person) Dead;
S -> Dead interp(BasicFact.Person) Person;

S -> Person interp(BasicFact.Person) Born;
S -> Born interp(BasicFact.Person) Person;

S -> Person interp(BasicFact.Person) Live;
S -> Live interp(BasicFact.Person) Person;

S -> Family interp(BasicFact.Person) Person;

S -> Person interp(BasicFact.Person) Hyphen;

S -> Born interp(BasicFact.Person);