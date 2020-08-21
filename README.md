<h1 align="center">PassBot Chatbot 💬</h1>
<h5 align="center">
 A Ahatbot for greek Passport Issuance <a href="http://195.251.209.218:8000/index.htm">PassBot</a>.
</h5>
<br />
<br />

<div align="center">
<img align="center" src="https://cdn.pixabay.com/photo/2013/07/12/13/53/police-officer-147501_960_720.png" alt="demonstration">
</div>


# PassBot_project
RASA CHATBOT FOR GREEK PASSPORT ISSUANCE

## Ιntroduction
Το παρόν chatbot (PassBot) έχει δημιουργηθεί στο πλαίσιο Διπλωματικής Εργασίας με θέμα 'Ανάπτυξη Chatbot για την έκδοση Διαβατηρίου' 
του μεταπτυχιακού φοιτητή Αντωνιάδη Παντελή, του τμήματος 'Μεταπτυχιακή Εξειδίκευση στα Πληροφοριακά Συστήματα (ΠΛΣ)' του Ελληνικού 
Ανοιχτού Πανεπιστημίου, κατά το ακαδηματικό έτος 2019-2020.
Επιβλέπων καθηγητής : Ευθύμιος Ταμπούρης - Καθηγητής τμήματος εφαρμοσμένης πληροφορικής του Πανεπιστημίου Μακεδονίας.

Η ανάπτυξη του Chatbot έχει πραγματοποιηθεί με το open source framework 'Rasa'.
Η σχετική πληροφορία για το διαβατήριο είναι καταχωρημένη σύμφωνα με το ευρωπαϊκό μοντέλο CPSV-AP σε MysQL database, 
από την οποία πραγματοποιείται on-line ανάκτηση για κάθε ανταπόκριση του ChatBot.
Η ιστοσελίδα και το Chatbot φιλοξενούται σε server (Ip: 195.251.209.218) του τμήματος Εφαρμοσμένης Πληροφορικής του Πανεπιστημίου Μακεδονίας, 
που παραχωρήθηκε ευγενικά από τον επ.καθηγητή κ.Ε.Μαμάτα. 

Το chatbot καλύπτει την παρακάτω πληροφόρηση σχετικά με το διαβατήριο:
   Τι είναι διαβατήριο.
   Προϋποθέσεις έκδοσης διαβατηρίου (συνοπτικά/αναλυτικά).
   Περιπτώσεις έκδοσης διαβατηρίου.
   Kόστος έκδοσης διαβατηρίου.
   Διαδικασία έκδοσης.
   Δικαιολογητικά που απαιτούνται (λίστα).
   Εξατομικευμένη πληροφόρηση δικαιολογητικών - Κόστους - Εξόδου διαβατηρίου.
   Τόπος υποβοβολής των δικαιολογητικών.
   Εύρεση γραφείου διαβατηρίων περιοχής.
   Εύρεση γραφείων που λειτουργούν Κυριακή.
   Διάρκεια ισχύος των διαβατηρίων.
   Επείγουσα έκδοση διαβατηρίου.
   Απώλεια/κλοπή διαβατηρίου.
   Στοιχεία που περιλαμβάνει το διαβατήριο.
   Ακύρωση / Αφαίρεση διαβατηρίου.
   Νομοθετικό πλαίσιο.

Παραπέμπτει στο site των διαβατηρίων της Ελληνικής Αστυνομιας για τις περιπτώσεις:
   Πορεία αίτησης έκδοσης διαβατηρίου.
   Πληροφορίες για το e-paravolo.
   Τεχνικές προδιαγραφές φωτογραφίας.

Αποστέλλει και με email, τις σημαντικές πληροφορίες :
   Εξατομικευμένα δικαιολογητικά - Κόστος - Έξοδος διαβατηρίου.
   Διαδικασία έκδοσης.
   Προυποθέσεις έκδοσης.
   Γραφείο διαβατηρίων περιοχής χρήστη.
   Ανοικτά Γραφεία Διαβατηρίων την Κυριακή.
  
Επιπλέον καλύπτει :
   Small talk.
   Χαιρετισμούς.
   Ευχαριστίες.
   Χειρισμό 'out of scope' ερωτήσεων.
   Feedback. Δίνεται κατά την αποχώρηση του χρήστη, εφόσον υπάρχει χαιρετισμός (πχ αντίο) ή μετά από ευχαριστίες του.

Από οποιοδήποτε σημείο του διαλόγου γράφοντας 'Επιλογές' εμφανίζονται με buttons προτεινόμενες επιλογές πληροφόρησης.



## Installation

Project folders '../passbot_project' :
1. other_files	: Sql scripts for 'cpsv_ap' MySql database and other useful files
2. passbot		: The chatbot's folder
3. webchat		: Chat Widget to deploy virtual assistants made with Rasa

## To create a mysql database:
	In Mysql prompt, run Sql scripts file from 'other_files' folder.

## To run PassBot:

1. Activate virtual environment. 

2. cd passbot
	Use `rasa train` to train a model.

3. Then, to run, first set up your action server in one terminal window:
	'rasa run actions' 
		
	There are some custom actions that require connections to external services.
	For these to run you would need to have your own Gmail account for passbot.
	First, in 'actions.py' file fill the credentials for mysql database and gmail account and save it.

4. In another window, run the bot:
	'rasa shell'
	Then talk to the bot in greek.

5. If you would like to run Passbot on your website, you can use the 'webchat' folder or follow the 
	instructions [here](https://github.com/botfront/rasa-webchat) to place the chat widget on your website.
	
	5a. Replace the command 4 with : 
		'python -m rasa run --m ./models --endpoints endpoints.yml --port 5005 -vv --enable-api --cors "*"'
	5b. Then from the 'webchat' folder run :
		'python -m http.server 8000'
	5c. Run Chatbot from browser: 
		http://Your_web_site:8000/index.html


## Overview of the files

`data/core/` - contains stories 

`data/nlu` - contains NLU training data

`actions` - contains custom action code

`domain.yml` - the domain file, including bot response templates

`config.yml` - training configurations for the NLU pipeline and policy ensemble
