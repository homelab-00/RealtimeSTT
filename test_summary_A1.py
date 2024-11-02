from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("kriton/greek-text-summarization")
model = AutoModelForSeq2SeqLM.from_pretrained("kriton/greek-text-summarization")


from transformers import pipeline

summarizer = pipeline("summarization", model="kriton/greek-text-summarization", device="cuda")

article = """ 
Στα σχόλια του πρώην πρωθυπουργού, Αλέξη Τσίπρα, ο οποίος τόνισε, μεταξύ άλλων, πως η εκτελεστική αλλά και η δικαστική της εξουσία επιβάλλεται να σταθεί στο ύψος των περιστάσεων, απάντησε ο κυβερνητικός εκπρόσωπος, Παύλος Μαρινάκης, κάνοντας λόγο για «θράσος». 

«Λίγες μόλις μέρες μετά την απόφαση-σταθμό της Ανεξάρτητης Ελληνικής Δικαιοσύνης να βγάλει τις “κουκούλες” από τους ψευδομάρτυρες της σκευωρίας της Novartis, ο πρώην πρόεδρος του ΣΥΡΙΖΑ, αντί να απολογηθεί για τη συντεταγμένη εκστρατεία κηλίδωσης των πολιτικών του αντιπάλων, στη σημερινή του ομιλία σε ημερίδα στη Βουλή κάνει έμμεσες υποδείξεις στη Δικαιοσύνη για εν εξελίξει, υπό διερεύνηση υποθέσεις», τονίζει στην ανακοίνωσή του.

«Ταυτόχρονα, ο πρώην πρωθυπουργός, που είχε δύο υπουργούς οι οποίοι εκ των υστέρων καταδικάστηκαν αμετάκλητα από τη Δικαιοσύνη, εργαλειοποιώντας με ανεπίτρεπτο τρόπο το δραματικό ναυάγιο ανοιχτά της Πύλου, συκοφαντεί τη χώρα του και “εκδίδει πορίσματα” ως αυτόκλητος “δικαστής” κάνοντας λόγο για “ολιγωρία των Αρχών”. 

Κύριε Τσίπρα, νυν και πρώην σύντροφοί του, κανείς δεν μπορεί να υπαγορεύσει στη Δικαιοσύνη τον τρόπο με τον οποίο θα επιτελεί τα καθήκοντά της, και αυτό γιατί πλέον στην Ελλάδα δεν λειτουργούν παρα-υπουργεία Δικαιοσύνης, όπως κυνικά είχε παραδεχτεί ότι συνέβαινε επί των ημερών σας ο πρώην υπουργός της κυβέρνησής σας κ. Κοντονής», καταλήγει ο ίδιος. 

Υπενθυμίζεται πως προηγουμένως, κατά την ομιλία του στο συνέδριο για την Ενδυνάμωση της Δημοκρατίας, που διοργάνωσαν η Προεδρία της Δημοκρατίας και η Βουλή των Ελλήνων, ο πρώην πρωθυπουργός είχε υπογραμμίσει πως «αν θέλουμε στο μέλλον να γιορτάζουμε με μεγαλύτερη περηφάνεια επετείους σαν τη σημερινή, των 50 χρόνων από την επανακύρωση της Ευρωπαϊκής Σύμβασης Δικαιωμάτων του Ανθρώπου από τη χώρα μας, επιβάλλεται η εκτελεστική αλλά και η δικαστική της εξουσία να σταθεί στο ύψος των περιστάσεων. Για να μπορούμε να μιλάμε πραγματικά για εμβάθυνση του Κράτους Δικαίου, για μια ισχυρή και όχι για μια πάσχουσα δημοκρατία».

Μάλιστα, αντιλαμβανόμενος την εισαγγελέα του Αρείου Πάγου, Γεωργία Αδειλίνη, να αποχωρεί όταν αναφερόταν στην υπόθεση των υποκλοπών, την τραγωδία στα Τέμπη, στο ναυάγιο στην Πύλο, μιλώντας για μεγάλες ευθύνες της Δικαιοσύνης, ο κ. Τσίπρας σε ένα εκτός κειμένου σχόλιο κάλεσε τη δικαστική εξουσία «τουλάχιστον να κάθεται και να ακούει».

"""

def genarate_summary(article):
    inputs = tokenizer(
        'summarize: ' + article, 
        return_tensors="pt", 
        max_length=1024, 
        truncation=True,
        padding="max_length",
    )

    outputs = model.generate(
        inputs["input_ids"], 
        max_length=512, 
        min_length=130, 
        length_penalty=3.0, 
        num_beams=8, 
        early_stopping=True,
        repetition_penalty=3.0,
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

print(genarate_summary(article))