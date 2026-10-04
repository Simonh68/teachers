"""Build Boost Simulation from supplied practice, preserving question/reveal pairs."""
import json,html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'grade6/boost-simulation'
slides=[];clips={};sets=[]
def add(kind,title,**kw):
 slides.append(dict(kind=kind,title=title,**kw))
def pair(title,q,options,correct,explain,audio=None):
 for reveal in [False,True]:add('mcq',title,q=q,options=options,correct=correct,explain=explain,reveal=reveal,audio=audio)
def listen(key,text):clips[key]=text;return key
responses=[
 [('Can I help you?',['Congratulations!','No, thank you.','Pleasant dreams!'],1,'מציעים עזרה. No, thank you היא דרך מנומסת לסרב. Congratulations מברך על הצלחה, ו־Pleasant dreams מתאים לפני השינה.'),
 ('How are you doing today?',['Pretty good, thank you.','See you later.',"It’s my mistake."],0,'שואלים לשלומכם. Pretty good פירושו די טוב. See you later היא פרידה, ו־It’s my mistake מציין טעות.'),
 ('Excuse me, where is the library?',["It’s at 5 o’clock.","It’s next to the cafeteria.",'Yes, I do.'],1,'Where שואל על מקום. next to פירושו ליד. שעה אינה מקום, ו־Yes, I do אינו עונה לשאלה היכן.'),
 ('Have a nice weekend!',['You too!',"I’m sorry.","That’s correct."],0,'מאחלים לכם סוף שבוע נעים. You too מחזיר את האיחול: גם לך!'),
 ('Would you like some coffee or tea?',['Yes, please.','Not at all.',"It’s next to the door."],0,'מציעים משקה. Yes, please מקבל את ההצעה בנימוס. Not at all אינו תשובה טבעית כאן.')],
 [('Thank you so much for your help!',["You’re welcome.","It’s too late.","I don’t know."],0,'מודים לכם על עזרה. You’re welcome פירושו בבקשה, בתגובה לתודה.'),
 ('What time does the movie start?',['On the table.','At 7:00 PM.','Yes, I do.'],1,'What time שואל באיזו שעה. At 7:00 PM פירושו בשבע בערב. On the table מציין מקום.'),
 ("I’m sorry I am late.",['Never mind.','See you later.',"That’s terrible."],0,'הדובר מתנצל על איחור. Never mind מרגיע: לא נורא. See you later היא פרידה.'),
 ('Can you pass me the salt, please?',['Of course, here you go.','I am fine, thank you.','The salt is expensive.'],0,'מבקשים להעביר מלח. Of course, here you go פירושו כמובן, בבקשה.'),
 ('How was your English exam?',['It was easy, thank you.','It is far away.','Yes, it is.'],0,'שואלים איך היה המבחן. It was easy מתאר את המבחן בעבר: הוא היה קל. זו אינה שאלת כן או לא.')]
]
passages=[
[("Hi, I'm Sarah. This weekend, I’m planning to visit my grandparents in the city. They just moved into a new apartment near the park, so I’m really excited to see it.",
 [('Where is Sarah going this weekend?',['To the beach.','To visit her grandparents.','To a movie.'],1,'Sarah אומרת: visit my grandparents. היא נוסעת לבקר את סבא וסבתא שלה.'),('Where is her grandparents’ new apartment?',['Near the park.','Near the school.','In the countryside.'],0,'הביטוי near the park מציין שהדירה החדשה ליד הפארק. הם גרים בעיר.'),('How does Sarah feel about visiting?',['She is tired.','She is bored.','She is excited.'],2,'Sarah אומרת I’m really excited: אני ממש מתרגשת. שאלה עם How does ... feel מבקשת לזהות רגש.')]),
 ("My name is David. Every Tuesday afternoon, I go to the community center to play basketball with my friends. We usually play for an hour, and then we have pizza together.",
 [('When does David play basketball?',['On Monday morning.','On Tuesday afternoon.','On Friday night.'],1,'When שואל מתי. David אומר Every Tuesday afternoon: בכל יום שלישי אחר הצהריים.'),('Where does he play?',['At school.','At a park.','At the community center.'],2,'Where שואל היכן. community center הוא מרכז קהילתי.'),('What do David and his friends do after basketball?',['They go home.','They have pizza together.','They play video games.'],1,'and then פירושו ואז. אחרי המשחק הם אוכלים פיצה יחד.')])],
[("Tomorrow is my mother's birthday. I bought her a beautiful bouquet of red roses and a card. In the evening, we are going to have a special dinner at a fancy restaurant.",
 [('What is tomorrow?',["The speaker’s father’s birthday.",'A national holiday.',"The speaker’s mother’s birthday."],2,'הדובר או הדוברת אומרים my mother’s birthday: יום ההולדת של אמא שלי. מין הדובר אינו מצוין בקטע.'),('What did the speaker buy?',['A new book and a pen.','A bouquet of red roses and a card.','A cake and a gift.'],1,'bought הוא העבר של buy. bouquet of red roses פירושו זר ורדים אדומים. card הוא כרטיס ברכה.'),('What will they do in the evening?',['Cook dinner at home.','Have a special dinner at a restaurant.','Go to the cinema.'],1,'In the evening מציין בערב. are going to מציין תוכנית: לאכול ארוחה מיוחדת במסעדה.')]),
 ("My dog, Max, loves to run in the backyard. Every morning before school, I throw a ball and he brings it back. He is a very energetic dog.",
 [('What is the name of the dog?',['Rex.','Max.','Buddy.'],1,'הקטע נפתח ב־My dog, Max: לכלב קוראים Max.'),('When does the speaker play with the dog?',['Every morning before school.','Every afternoon after sports.','In the evenings.'],0,'Every morning before school פירושו בכל בוקר לפני בית הספר. before פירושו לפני.'),('What game do they play?',['Hide and seek.','Tag.','Throwing a ball.'],2,'הדובר זורק כדור והכלב מחזיר אותו. throw = לזרוק, brings it back = מחזיר אותו.')])]
]
speaking=[
[("Tell us about a person that you like very much. Explain why you like this person.",
 ["A person I like very much is my older brother. His name is Daniel. He is eighteen years old. He is kind and funny. We live in the same house, so I see him every day.","We often play basketball together in the afternoon. Sometimes we watch a film or make dinner. When I have a problem with my homework, he helps me. He listens to me and explains things slowly.","I like him because I can talk to him about anything. Last week, I was worried about a test. He helped me study and made me feel better. I want to be kind and helpful like him."],
 ['פותחים בזיהוי האדם ובכמה פרטים פשוטים: שם, גיל והקשר אליכם. התשובה כאן היא דוגמה; התאימו את הפרטים לעצמכם.','מוסיפים פעילויות משותפות ודוגמה לעזרה. משפטים פשוטים וברורים מאפשרים להמשיך לדבר.','because מציג סיבה. דוגמה מהשבוע האחרון מוסיפה פרטים. מסיימים במחשבה אישית.']),
 ("Tell us about a subject that you like to study at school and explain why you like to study it.",
 ["My favorite subject at school is English. We study English several times a week. In class, we read short stories, learn new words, and practice speaking. I especially enjoy speaking activities with a partner.","I like English because it helps me understand songs and films. I also want to speak to people from other countries. Last month, we read a story about a boy and his dog. I enjoyed it very much.","Some words are difficult for me, but I practice at home. I listen to short texts and say the words aloud. My goal is to speak more clearly. I feel happy when I understand something new."],
 ['מציינים את המקצוע ומתארים מה עושים בשיעור. אין צורך להשתמש בשפה גבוהה.','מסבירים למה אוהבים את המקצוע ומוסיפים דוגמה משיעור. because = מפני ש־.','אפשר לתאר קושי, דרך לתרגול ומטרה אישית. קראו את כל שלושת החלקים ברצף ותזמנו את הדיבור.'])],
[("Tell us about a favorite hobby or activity that you like to do in your free time.",
 ["My favorite hobby is playing basketball. I usually play after school with my friends. We meet at a court near my home. I play two or three times a week. We do not need much equipment, just a ball.","I like basketball because it is fun and it keeps me active. I enjoy working with a team. My friends and I help each other and try to improve. Sometimes we play a short match against another team.","Last week, our team won a game. I scored a basket near the end, and I felt very happy. I am not the best player, but I practice often. In the future, I want to play better."],
 ['מציינים תחביב, מקום, תדירות ועם מי עוסקים בו. usually = בדרך כלל.','מסבירים למה אוהבים את הפעילות. הוסיפו פרטים על מה שקורה בזמן הפעילות.','סיפור קצר מהעבר נותן דוגמה אישית. מסיימים במטרה לעתיד. התאימו את התשובה לתחביב שלכם.']),
 ("Tell us about a meal you really like to eat and explain why it is your favorite.",
 ["My favorite meal is chicken with rice and a salad. We usually eat this meal at home on Friday evening. My mother makes the chicken, and I sometimes help her prepare the salad. I wash and cut the vegetables.","I like this meal because it tastes good and it reminds me of my family. The chicken is warm, and the salad is fresh. We sit around the table and talk about our week. This makes the meal special.","Last Friday, I helped cook the rice for the first time. It was easy, and everyone liked it. I felt proud. I would like to learn how to make the whole meal by myself one day."],
 ['מציינים את המאכל ומתי ואיפה אוכלים אותו. אפשר גם להסביר מי מכין אותו.','מסבירים למה אוהבים את הארוחה. tastes good = טעים. אפשר להזכיר טעם, משפחה או זיכרון.','מוסיפים אירוע מסוים ומחשבה אישית. זו תשובה אפשרית, ולא טקסט שחייבים לשנן.'])]
]
stories=[
 [('A boy is packing his backpack. He is getting ready for a walk.','הילד אורז את תיק הגב ומתכונן לטיול. is packing מתאר פעולה שמתרחשת בתמונה.'),('Next, he is walking into the forest. He is carrying his backpack.','Next = אחר כך. מוסיפים פרט שנראה בתמונה: הוא נושא את התיק.'),('Then, he is looking at a map. He looks lost and worried.','Then = ואז. looking at = מסתכל על. looks lost = נראה אבוד. אפשר להסיק רגש, בלי להמציא פרטים רחוקים מהתמונה.'),('Finally, he finds a path and smiles. He can continue his walk.','Finally = לבסוף. סוף הסיפור פותר את הבעיה: הוא מוצא שביל ומחייך.')],
 [('A girl is making a cake in the kitchen. She is mixing the ingredients.','הילדה מכינה עוגה במטבח. is mixing = מערבבת. מתחילים בתיאור הפעולה הראשונה.'),('Next, she is taking the cake out of the oven. The cake looks good.','Next = אחר כך. taking ... out of = מוציאה מתוך. מתארים מה רואים בתמונה.'),('Then, she is setting the table. She puts plates and forks on it.','setting the table = עורכת את השולחן. Then מחבר את האירוע לשלבים הקודמים.'),('Finally, the family is sitting around the table. They are eating the cake together.','לבסוף המשפחה יושבת ואוכלת יחד. are eating מתאר פעולה של כמה אנשים.')]
]
add('cover','Boost Simulation',text='כיתה ו׳',he='תרגול דיבור והאזנה באנגלית')
add('intro','שני סטים של תרגול',he='בכל סט ארבעה חלקים: תגובות למצבים, הבנת הנשמע, דיבור על עצמכם וסיפור בתמונות. תחילה עונים, ורק בשקף הבא רואים תשובה והסבר.',text='A2 · BOOST practice',note='חומר תרגול מקורי לפי הדגם שסופק. אינו שאלון רשמי.')
for si in range(2):
 s=si+1
 add('cover',f'Set {s}',text='Boost Simulation',he='ארבעה חלקים · שאלה ואחריה תשובה')
 add('intro','Part 1 · Situation Responses',he='האזינו למשפט ובחרו תגובה מתאימה מתוך שלוש אפשרויות. בכל פעם מוצגת שאלה אחת. עברו לשקף הבא רק אחרי שבחרתם.',text='Listen and choose the best response.')
 for qi,(q,opts,c,h) in enumerate(responses[si],1):
  pair(f'Set {s} · Part 1 · {qi}/5',q,opts,c,h,listen(f's{s}-response-{qi}',q))
 add('break','הפוגה קצרה',text='Can I help you? — No, thank you.',he='אמרו לבן הזוג משפט מהחלק הקודם. הוא יענה בלי להסתכל. אחר כך החליפו תפקידים.')
 add('intro','Part 2 · Listening Comprehension',he='האזינו לקטע קצר, ואז ענו על שלוש שאלות. אפשר להאזין שוב. הטקסט המלא נמצא במדריך למורה, כדי שלא יגלה את התשובות מראש.',text='Listen for people, places, times and feelings.')
 for pi,(text,qs) in enumerate(passages[si],1):
  key=listen(f's{s}-passage-{pi}',text)
  add('listen',f'Set {s} · Passage {pi}',audio=key,he='האזינו בלי לקרוא תמליל. נסו לזכור מי מדבר, מה הוא עושה, היכן ומתי.',text='Listen to the short passage.')
  for qi,(q,opts,c,h) in enumerate(qs,1):pair(f'Set {s} · Passage {pi} · {qi}/3',q,opts,c,h,key)
 add('intro','Part 3 · Talking About Yourself',text='Choose one topic. Speak for at least one minute.',he='בחרו אחת משתי האפשרויות ותרגלו דיבור במשך דקה לפחות. אמרו מה בחרתם, למה, והוסיפו פרטים ודוגמה אישית. אין תשובה נכונה אחת.')
 for oi,(q,parts,hs) in enumerate(speaking[si],1):
  add('speak',f'Set {s} · Option {oi}',q=q,he='ענו בעצמכם תחילה. בשקפים הבאים תופיע תשובה אפשרית בשלושה חלקים. לדקת תרגול חברו את כל החלקים והתאימו אותם לחיים שלכם.')
  for n,(p,h) in enumerate(zip(parts,hs),1):add('model',f'Option {oi} · Model {n}/3',q=q,text=p,he=h)
 add('break','לפני הסיפור בתמונות',text='First · Next · Then · Finally',he='המילים האלה יעזרו לחבר את התמונות לסיפור. אמרו אותן בסדר הנכון בלי להסתכל.')
 add('intro','Part 4 · Picture Story',text='Describe the four pictures as one story.',he='התבוננו בכל ארבע התמונות לפי המספרים. תארו את הפעולות וחברו אותן לסיפור. אחר כך בדקו דוגמה אפשרית לכל תמונה.')
 add('story',f'Set {s} · Picture Story',row=si,he='ספרו את הסיפור כולו לפני החשיפה. התחילו בתמונה 1 וסיימו בתמונה 4.')
 for pi,(p,h) in enumerate(stories[si]):
  for rev in [False,True]:add('picture',f'Set {s} · Picture {pi+1}/4',row=si,col=pi,text=p,he=h,reveal=rev)
 add('storymodel',f'Set {s} · A complete story',row=si,text=' '.join(p for p,h in stories[si]),he='זו דוגמה אפשרית. גם תיאור אחר יכול להתאים אם הוא ברור, נכון לתמונות ומחובר ברצף.')
add('intro','סיום התרגול',text='Listen. Choose. Speak. Tell a story.',he='חזרו לשאלות שבהן טעיתם וענו שוב לפני החשיפה. בחלקי הדיבור השתמשו בפרטים שלכם. אפשר לחזור לכל חלק באמצעות רשימת השקפים.')
(OUT/'lesson.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2))
(OUT/'audio-texts.json').write_text(json.dumps(clips,ensure_ascii=False,indent=2))
sections=[]
for si in range(2):
 body=f'<h2>Set {si+1}</h2><h3>חלק 1</h3>'
 for q,o,c,h in responses[si]:body+=f'<p dir="ltr"><b>{html.escape(q)}</b><br>{html.escape(o[c])}</p><p>{h}</p>'
 body+='<h3>חלק 2 — תמלילים ומפתח</h3>'
 for text,qs in passages[si]:
  body+=f'<blockquote dir="ltr">{html.escape(text)}</blockquote>'
  for q,o,c,h in qs:body+=f'<p dir="ltr">{html.escape(q)}<br><b>{html.escape(o[c])}</b></p><p>{h}</p>'
 body+='<h3>חלק 3 — דוגמאות לדקת דיבור</h3><p>תזמנו דיבור בפועל. דוגמאות אינן הבטחה לאורך קבוע: הקצב משתנה בין תלמידים. אם מסיימים מוקדם, מוסיפים פרט אישי או דוגמה נוספת. אין לשנן פרטים שאינם נכונים לתלמיד.</p>'
 for q,ps,hs in speaking[si]:body+=f'<h4 dir="ltr">{html.escape(q)}</h4><p dir="ltr">{html.escape(" ".join(ps))}</p>'
 body+='<h3>חלק 4 — סיפור אפשרי</h3><p dir="ltr">'+html.escape(' '.join(x[0] for x in stories[si]))+'</p>'
 sections.append(body)
(OUT/'teacher.html').write_text('''<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Boost Simulation — מדריך למורה</title><style>body{background:#050b14;color:#f4f8ff;font:20px/1.65 Arial;margin:0;padding:30px}main{max-width:900px;margin:auto}h1,h2,a{color:#53e4ff}h3,b{color:#dfff5b}blockquote{margin:20px 0;padding:20px;border-inline-start:3px solid #53e4ff}p[dir=ltr],blockquote{text-align:left}a{display:inline-block;margin-bottom:20px}</style><main><a href="./">חזרה למצגת</a><h1>Boost Simulation — מדריך למורה</h1><p>כיתה ו׳ · רמת A2 · שני סטים לפי הפרומפט שסופק. תרגול לפי דגם BOOST, ללא טענה שזהו שאלון רשמי. שאלה ותשובה בשקפים נפרדים. הפעלת שמע בלחיצה, עצירה במעבר שקף.</p><p>תיקוני בהירות: בסט 1 שאלה 5 הוחלפה האפשרות Sounds good; בסט 2 שאלה 4 הוחלפה האפשרות No problem at all. שתיהן יכולות להיות תגובות סבירות במקור. בשאלת יום ההולדת מין הדובר אינו ידוע ולכן האפשרויות מציינות the speaker.</p><p>בחלק 1: השמיעו, המתינו לבחירה, ואז חשפו והסבירו. בחלק 2: השמיעו את הקטע, הציגו שאלות בזו אחר זו, ורק לאחר תשובה עצמאית חשפו. בחלק 3: כל תלמיד בוחר אפשרות אחת, מתרגל דקה ומוסיף סיבה ודוגמה. בחלק 4: תנו קודם לספר את כל הסיפור, אחר כך חשפו את הדוגמאות.</p>'''+''.join(sections)+'</main></html>')
print(f'Built {len(slides)} slides and {len(clips)} audio scripts')
