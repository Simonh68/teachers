from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[2] / 'grade7/the-same-way'
# Each item is exactly one reading step; dialogue remains with its speaker.
parts=[
[
('My name is Dan, and I am in Grade 7.','קוראים לי דן, ואני בכיתה ז׳.'),
('My new school is far from home, but I chose it because I love its science lessons.','בית הספר החדש שלי רחוק מהבית, אבל בחרתי בו כי אני אוהב את שיעורי המדעים שלו.'),
('Every morning, I leave home with a heavy blue bag.','בכל בוקר אני יוצא מהבית עם תיק כחול כבד.'),
('My little brother is still in bed when I close the door.','אחי הקטן עדיין במיטה כשאני סוגר את הדלת.')
],[
('First, I walk to the bus stop and take a bus to the train station.','ראשית, אני הולך לתחנת האוטובוס ונוסע באוטובוס לתחנת הרכבת.'),
('Then I take a train and another bus.','לאחר מכן אני נוסע ברכבת ובאוטובוס נוסף.'),
('Finally, I walk for ten minutes to school.','לבסוף, אני הולך עשר דקות לבית הספר.'),
('I lift my bag onto my back and look at the time again.','אני מרים את התיק אל הגב ומסתכל שוב מה השעה.'),
('There are two boys near me, but we do not talk.','יש שני בנים לידי, אבל אנחנו לא מדברים.'),
('One has a green bag, and the other has a red cap.','לאחד יש תיק ירוק, ולאחר יש כובע אדום.')
],[
('Today the sky is blue, but I think about winter.','היום השמיים כחולים, אבל אני חושב על החורף.'),
('What will I do when it rains?','מה אעשה כשירד גשם?'),
('My books will be wet, and I will be cold.','הספרים שלי יהיו רטובים, ויהיה לי קר.'),
('I do not know the answer.','אני לא יודע את התשובה.'),
('I take my phone out of my bag, but I do not call home.','אני מוציא את הטלפון מהתיק, אבל לא מתקשר הביתה.')
],[
('At school, I open the classroom door and stop.','בבית הספר אני פותח את דלת הכיתה ועוצר.'),
('The green bag and the red cap are there!','התיק הירוק והכובע האדום שם!'),
('The boys from the journey are in my class.','הבנים מהדרך נמצאים בכיתה שלי.'),
('At break, I walk over to meet them.','בהפסקה אני ניגש להכיר אותם.'),
('“Are you tired too?” I ask.','״גם אתם עייפים?״ אני שואל.'),
('“Yes, and I worry about the rain,” says Ben.','״כן, ואני דואג מהגשם,״ אומר בן.'),
('“Me too,” says Noam.','״גם אני,״ אומר נועם.'),
('“I look at the time all the way to school!”','״אני מסתכל מה השעה כל הדרך לבית הספר!״')
],[
('I smile and put my phone away.','אני מחייך ומניח את הטלפון בצד.'),
('“Can I join you tomorrow?” I ask.','״אפשר להצטרף אליכם מחר?״ אני שואל.'),
('“Of course!” they say.','״בוודאי!״ הם אומרים.'),
('The rain is still a problem, but now we can think about it together.','הגשם עדיין בעיה, אבל עכשיו אנחנו יכולים לחשוב עליה יחד.'),
('Tomorrow, I will say hello at the bus stop.','מחר אגיד שלום בתחנת האוטובוס.')
]]
sentences=[{'en':e,'he':h,'part':chr(65+p),'n':sum(len(x) for x in parts[:p])+i+1} for p,items in enumerate(parts) for i,(e,h) in enumerate(items)]
paragraphs=[' '.join(e for e,h in p) for p in parts]
wordcount=len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b",' '.join(paragraphs)))
data={'title':'The Same Way','paragraphs':paragraphs,'sentences':sentences,'wordcount':wordcount}
(ROOT/'story.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('Story:',wordcount,'words;',len(sentences),'sentences')
