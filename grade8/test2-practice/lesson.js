/* Exact task IDs and source prompts: Grade8_Test2_Practice_60_Exercises.pdf. */
window.LESSON = {
 version:'2026-11-16.1',
 sections:[
  ['A','Word meanings','פירושי מילים','Choose the Hebrew meaning.','בחרו את הפירוש בעברית.'],
  ['B','Words in sentences','מילים במשפטים','Complete the sentence. Type a word or tap the word bank.','השלימו את המשפט. אפשר להקליד או לבחור ממחסן המילים.'],
  ['C','Grammar choices','בחירה דקדוקית','Choose the correct word.','בחרו את המילה הנכונה.'],
  ['D','Spelling repair','תיקון איות','Correct the spelling. Write the word in English.','תקנו את האיות. כתבו את המילה באנגלית.'],
  ['E','Sentence builder','בניית משפטים','Tap the parts in order. Tap a selected part to return it.','לחצו על החלקים לפי הסדר. לחיצה על חלק שנבחר מחזירה אותו.'],
  ['F','Translate','תרגום משפטים','Translate into English. More than one answer may be possible.','תרגמו לאנגלית. ייתכנו כמה תשובות נכונות.'],
  ['G','Grammar repair','תיקון דקדוק','Fix one grammar mistake. Write the whole sentence.','תקנו שגיאה דקדוקית אחת. כתבו את המשפט השלם.'],
  ['H','Your own sentences','כתיבה עצמאית','Write two original sentences. Use the checklist, then ask your teacher to review.','כתבו שני משפטים משלכם. בדקו לפי הרשימה והראו למורה.']
 ],
 bank:['beach','candles','cooler','opal','sand','time','underground','vacation'],
 tasks:[]
};
(function(L){
const add=(s,n,l,p,a,h,hh,extra={})=>L.tasks.push({id:s+n,s,level:l,p,answers:a,h,hh,...extra});
const vocab=[
 ['watch','שעון יד',1,'You wear it to see the time.','עונדים אותו כדי לדעת מה השעה.'],
 ['beach','חוף ים',1,'A place with sea and sand.','מקום עם ים וחול.'],
 ['summer','קיץ',1,'The hot season.','העונה החמה.'],
 ['winter','חורף',1,'The cold season.','העונה הקרה.'],
 ['towel','מגבת',2,'You use it after a swim.','משתמשים בה לאחר שחייה.'],
 ['candle','נר',2,'You light it at Hanukkah.','מדליקים אותו בחנוכה.'],
 ['ground','קרקע',2,'The surface under your feet.','המשטח שעליו עומדים.'],
 ['visitor','מבקר',2,'A person who comes to a place for a visit.','אדם שמגיע לביקור במקום.'],
 ['underground','תת־קרקעי',3,'Under + ground.','מתחת לקרקע.'],
 ['temperature','טמפרטורה',3,'It tells us how hot or cold something is.','מדד לחום או לקור.'],
 ['dugout','בית החצוב בסלע',3,'A home dug into the ground or rock.','בית שחופרים באדמה או בסלע.'],
 ['comfortable','נוח',3,'A place where you feel good and relaxed.','מקום שבו מרגישים בנוח.']
];
vocab.forEach((v,i)=>{const opts=[v[1],vocab[(i+3)%12][1],vocab[(i+7)%12][1],vocab[(i+9)%12][1]];let target=i%4;[opts[0],opts[target]]=[opts[target],opts[0]];add('A',i+1,v[2],v[0],[v[1]],v[3],v[4],{options:opts,explain:v[0]+' = '+v[1],explainHe:v[0]+' = '+v[1]});});
[
 [1,"Daniel's watch shows the ________ in Israel.",'time','A watch tells you this.','השעון מראה את השעה.'],
 [1,'Ben is on summer ________.','vacation','Time away from school.','זמן חופשי מבית הספר.'],
 [1,'They swim at the ________.','beach','Where can people swim in the sea?','איפה שוחים בים?'],
 [2,'Daniel has ________ on his feet.','sand','You find it on the beach.','חומר שנמצא על החוף.'],
 [2,'The family lights ________ for Hanukkah.','candles','Use the plural: more than one.','השתמשו בצורת רבים.'],
 [2,'A dugout is an ________ home.','underground','Where is a dugout?','איפה נמצא הבית החצוב?'],
 [3,'It is ________ inside a dugout than outside.','cooler','Look for a comparison with than.','חפשו מילת השוואה המתאימה ל־than.'],
 [3,'Visitors look for small pieces of ________.','opal','A stone mentioned in the text.','אבן המוזכרת בטקסט.']
].forEach((v,i)=>add('B',i+1,v[0],v[1],[v[2]],v[3],v[4],{explain:v[1].replace(/_+/g,v[2]),explainHe:'קראו שוב את המשפט השלם ובדקו את משמעותו.'}));
[
 [1,'Daniel ________ a watch.','has','have','Daniel = he. Use has.','דניאל הוא יחיד: משתמשים ב־has.'],
 [1,'The towels ________ wet.','are','is','Towels is plural. Use are.','מגבות הן ברבים: משתמשים ב־are.'],
 [1,'It ________ hot in summer.','is','are','Use is with it.','אחרי it משתמשים ב־is.'],
 [1,'I ________ in Australia.','am','is','I goes with am.','אחרי I משתמשים ב־am.'],
 [2,'Visitors can ________ here.','sleep','sleeps','After can, use the base verb: can sleep.','אחרי can משתמשים בצורת הבסיס, ללא s.'],
 [2,'________ Ben swim?','Can','Is','Can + subject + base verb asks about ability.','שאלת יכולת: Can, נושא ופועל בסיסי.'],
 [2,"He ________ wear a coat.","doesn't","don't","He / she / it: doesn't + base verb.",'עם he משתמשים ב־doesn’t ולאחריו פועל בסיסי.'],
 [2,'The photo ________ two towels.','shows','show','The photo is singular: add s in the present simple.','התמונה היא יחידה: מוסיפים s לפועל בהווה פשוט.'],
 [3,'Yesterday, Daniel ________ to the beach.','went','go','Yesterday tells us to use the past: go → went.','Yesterday מציין עבר: go הופך ל־went.'],
 [3,'It is ________ inside than outside.','cooler','cool','Compare two places: cooler than.','השוואה בין שני מקומות: cooler than.'],
 [3,'These are visitors ________ like opals.','who','when','Who describes people.','Who מתייחס לאנשים.'],
 [3,'________ it is winter in Israel, it is summer in Australia.','When','Who','When connects two things happening at the same time.','When מחבר בין שני מצבים המתרחשים באותו זמן.']
].forEach((v,i)=>add('C',i+1,v[0],v[1],[v[2]],'Check the subject and the words around the gap.','בדקו את הנושא ואת המילים ליד החסר.',{options:i%2?[v[2],v[3]]:[v[3],v[2]],explain:v[4],explainHe:v[5]}));
[
 [1,'wotch','watch','שעון יד','The vowel is a.','התנועה במילה היא a.'],
 [1,'bech','beach','חוף ים','There are two vowels together: ea.','יש שתי אותיות תנועה ברצף: ea.'],
 [1,'sumer','summer','קיץ','Double the m.','יש שתי אותיות m.'],
 [2,'towle','towel','מגבת','Check the order of the last two letters.','בדקו את סדר שתי האותיות האחרונות.'],
 [2,'candels','candles','נרות','The ending is -les.','המילה מסתיימת ב־les.'],
 [2,'visiters','visitors','מבקרים','The ending is -ors.','המילה מסתיימת ב־ors.'],
 [3,'undergraund','underground','תת־קרקעי','Under + ground. Ground contains ou.','ground נכתב עם ou.'],
 [3,'temprature','temperature','טמפרטורה','There is an e after p.','יש e אחרי p.']
].forEach((v,i)=>add('D',i+1,v[0],v[1],[v[2]],v[4],v[5],{cue:v[3],explain:v[2],explainHe:'השוו את האיות שלכם למילה הנכונה.'}));
[
 [1,['a watch','has','Daniel'],['Daniel has a watch.'],'Subject → verb → object.','נושא, פועל, מושא.'],
 [1,['in summer','It','hot','is'],['It is hot in summer.','In summer it is hot.'],'It → is → adjective → time.','It, הפועל is, תיאור ומילת זמן.'],
 [2,['in an underground hotel','can','Visitors','sleep'],['Visitors can sleep in an underground hotel.','In an underground hotel visitors can sleep.'],'Visitors → can → base verb → place.','נושא, can, פועל בסיסי ותיאור מקום.'],
 [2,['a coat',"doesn't",'Ben','in summer','wear'],["Ben doesn't wear a coat in summer.","In summer Ben doesn't wear a coat."],'Ben → doesn’t → wear → object → time.','Ben, אחריו doesn’t, הפועל wear, מושא וזמן.'],
 [3,['is summer in Australia','When','it','in Israel,','is winter','it'],['When it is winter in Israel, it is summer in Australia.','It is summer in Australia when it is winter in Israel.'],'When + one sentence, then the other sentence.','When, משפט על ישראל, ואז המשפט על אוסטרליה.'],
 [3,['for opals','who visit Coober Pedy','can look','People'],['People who visit Coober Pedy can look for opals.'],'People → who describes them → can look → for opals.','People, אחריו תיאור עם who, ואז can look for opals.']
].forEach((v,i)=>add('E',i+1,v[0],'Build the sentence.',v[2],v[3],v[4],{parts:v[1],explain:v[2][0],explainHe:'בדקו את סדר החלקים. ייתכנו גם סדרים תקינים אחרים.'}));
[
 [1,'חם בקיץ.',['It is hot in summer.','It is hot in the summer.','In summer it is hot.','In the summer it is hot.'],'Start with It is...','אפשר להתחיל ב־It is.'],
 [1,'לדניאל יש שעון יד.',['Daniel has a watch.','Daniel has got a watch.','Daniel owns a watch.','Daniel has a wristwatch.'],'Daniel = he.','חשבו על הצורה המתאימה ל־he.'],
 [2,'המבקרים יכולים לישון במלון תת־קרקעי.',['Visitors can sleep in an underground hotel.','The visitors can sleep in an underground hotel.','Visitors are able to sleep in an underground hotel.','The visitors are able to sleep in an underground hotel.','The visitors can sleep at an underground hotel.','Visitors can sleep at an underground hotel.'],'can + base verb; an underground hotel.','אחרי can בא פועל בסיסי. שימו לב ל־an.'],
 [2,'בן אינו לובש מעיל בקיץ.',["Ben doesn't wear a coat in summer.","Ben doesn't wear a coat in the summer.","In summer Ben doesn't wear a coat.","In the summer Ben doesn't wear a coat."],'doesn’t + base verb.','אחרי doesn’t הפועל נשאר בצורת הבסיס.'],
 [3,'כשבישראל חורף, באוסטרליה קיץ.',['When it is winter in Israel, it is summer in Australia.','It is summer in Australia when it is winter in Israel.','When Israel has winter, Australia has summer.'],'When + sentence, sentence.','When מחבר בין שני משפטים.'],
 [3,'הבית התת־קרקעי קריר יותר מהמדבר שבחוץ.',['The underground home is cooler than the desert outside.','The underground house is cooler than the desert outside.','The dugout is cooler than the desert outside.','The underground home is cooler than the desert outdoors.'],'cool → cooler than.','בהשוואה משתמשים ב־cooler than.']
].forEach((v,i)=>add('F',i+1,v[0],v[1],v[2],v[3],v[4],{explain:v[2][0],explainHe:'זו תשובה אפשרית, לא האפשרות היחידה. שימו לב לסדר המילים ולצורת הפועל.'}));
[
 [1,'Daniel have a watch.',['Daniel has a watch.'],'Daniel = he.','בדקו את הפועל אחרי נושא יחיד.','Use has with Daniel.','עם Daniel משתמשים ב־has.'],
 [1,'The rooms is cool.',['The rooms are cool.'],'Rooms is plural.','Rooms היא צורת רבים.','Use are with a plural subject.','עם נושא ברבים משתמשים ב־are.'],
 [2,'Visitors can to sleep underground.',['Visitors can sleep underground.'],'Check the word after can.','בדקו מה בא אחרי can.','After can, use the base verb without to.','אחרי can אין to.'],
 [2,"Ben doesn't wears a coat.",["Ben doesn't wear a coat."],'Check the verb after doesn’t.','בדקו את הפועל אחרי doesn’t.','After doesn’t, use wear, not wears.','אחרי doesn’t משתמשים ב־wear ללא s.'],
 [3,'Yesterday, Daniel go to the beach.',['Yesterday, Daniel went to the beach.','Daniel went to the beach yesterday.'],'Yesterday = past.','Yesterday מציין עבר.','The past of go is went.','צורת העבר של go היא went.'],
 [3,'This room is more cooler than the desert.',['This room is cooler than the desert.'],'Use one comparative form, not two.','אין צורך בשתי צורות השוואה.','Cooler already means more cool. Do not add more.','cooler כבר מבטא השוואה. אין להוסיף more.']
].forEach((v,i)=>add('G',i+1,v[0],v[1],v[2],v[3],v[4],{explain:v[5],explainHe:v[6]}));
add('H',1,2,'Write two sentences about Daniel: one with has and one with can.',[], 'Write one idea in each sentence.','כתבו רעיון אחד בכל משפט.',{promptHe:'כתבו שני משפטים על דניאל: אחד עם has ואחד עם can.',required:['has','can'],models:['Daniel has a watch.','Daniel can swim at the beach.']});
add('H',2,3,'Write two sentences about Coober Pedy: one with who and one with when.',[],'Use who for people and when for time.','Who מתייחס לאנשים; when מתייחס לזמן.',{promptHe:'כתבו שני משפטים על Coober Pedy: אחד עם who ואחד עם when.',required:['who','when'],models:['People who visit Coober Pedy can look for opals.','When it is hot outside, people can stay underground.']});
})(window.LESSON);
