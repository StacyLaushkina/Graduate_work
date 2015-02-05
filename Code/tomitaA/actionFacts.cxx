#encoding "utf-8"

Person -> AnyWord<gram="имя">;
Action -> Verb<kwtype=action>;
Member -> Noun<kwtype=member>;
StartEnd -> Verb<kwtype=startend>;

S -> Person Prep interp(ActionFact.Person) Action;
S -> Person interp(ActionFact.Person) Action;
S -> Prep Adj interp(ActionFact.Person) Action;

S -> Person Prep StartEnd interp(ActionFact.Person) Action;
S -> Person interp(ActionFact.Person) StartEnd Action;
S -> Prep Adj StartEnd interp(ActionFact.Person) Action;

//how?

S -> Person interp(ActionFact.Person) Member;
S -> Person Verb interp(ActionFact.Person) Member;
S -> Person Verb Prep interp(ActionFact.Person) Member;