from typing import Dict, Text, Any, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import (
    SlotSet,
    AllSlotsReset,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    ActionExecuted,
    UserUttered,
)
import mysql.connector
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email, EmailNotValidError
import csv
import json

INTENT_DESCRIPTION_MAPPING_PATH = "intent_description_mapping.csv"
config = {
    'host': 'localhost',
    'user': 'XXXXX',                    # Mysql user
    'password': 'XXXXX',                # Password for Mysql user
    'database':'cpsv_ap',
}
GOOGLE_MAP_ADDRESS = "https://www.google.com/maps/place/"
LOGIN_EMAIL = "passbot.chatbot@gmail.com"   # Passbot mail account
PASSWORD = "XXXXXX"                         # Password for Passbot mail account
SENDER_EMAIL = "passbot.chatbot@gmail.com"     
BUTTON_YES = "Ναι ✔" 
BUTTON_NO = "Όχι, δεν χρειάζεται ✖"
IDENTIFIER_PS_PASSPORT = "Ps0001"

class ActionDbCost(Action):	
#       Κόστος έκδοσης διαβατηρίου
#       Ανάκτηση δεδομένων από table "cost" για PS = Ps0001
    def name(self):
        return "action_db_cost"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)
       
       
        cursor = db.cursor()
        q = "select cost.value, cvcurrency.name, cost.sort_description from publicservice_cost as ps_cost, cost, cvcurrency where ps_cost.identifier_ps = '{}' and ps_cost.identifier_cost = cost.identifier and cost.currency = cvcurrency.code".format(IDENTIFIER_PS_PASSPORT)
        
        response = """Το κόστος έκδοσης διαβατηρίου εξαρτάται από την περίπτωση έκδοσης, την ηλικία του ενδιαφερομένου και ειδικές συνθήκες που ίσως υπάρχουν. Έτσι διαμορφώνεται ως εξής : """
        dispatcher.utter_message(response)
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            for row in results:
                costvalue = row[0]
                curname = row[1]
                costdescr = row[2]
                details = ('Κόστος: {0} {1}. - {2}'.format(costvalue, curname, costdescr))
                dispatcher.utter_message(format(details))
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα στοιχεία...")
            else:
                response = """Για την πληρωμή του κόστους εφαρμόζεται η διαδικασία είσπραξης του ηλεκτρονικού παραβόλου [e-paravolo](http://www.passport.gov.gr/diadikasia-ekdosis/documents/eparavolo.html)."""
                dispatcher.utter_message(response)
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()
        
        return []
        
        
class ActionDbPlaceOfSubmission(Action):	
#       Τόπος υποβολής των δικαιολογητικών
#       Ανάκτηση και εμφάνιση Sort_Description από table "rule" για PS = "Ps0001" και rule.name = 'PLACE OF SUBMISSION OF DOCUMENTS'.
    def name(self):
        return "action_db_Place_Of_Submission"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)

        cursor = db.cursor()
        q = "select rule.sort_description from publicservice_rule as ps_rule, rule where ps_rule.identifier_ps = '{}' and ps_rule.identifier_ru = rule.identifier and rule.name = 'PLACE OF SUBMISSION OF DOCUMENTS'".format(IDENTIFIER_PS_PASSPORT)

        response = """Τα δικαιολογητικά για την έκδοση διαβατηρίου, υποβάλλονται : """
        dispatcher.utter_message(response)
        
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            for row in results:
                descr = row[0]
                dispatcher.utter_message(format(descr))
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα στοιχεία...")
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()
        
        return []        
        
class ActionDbCriterionRequirement(Action):	
#       Προυποθέσεις έκδοσης διαβατηρίου
#       Ανάκτηση και εμφάνιση Sort_Description (Description για email) από table "CriterionRequirement" για PS = "Ps0001"
    def name(self):
        return "action_db_CriterionRequirement"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)
        
        cursor = db.cursor()
        q = "select cr.description, cr.sort_description from publicservice_criterionrequirement as ps_cr, criterionrequirement as cr where ps_cr.identifier_ps = '{}' and ps_cr.identifier_cr = cr.identifier".format(IDENTIFIER_PS_PASSPORT)
        
        email_subject = "PassBot - ΠΡΟΥΠΟΘΕΣΕΙΣ ΕΚΔΟΣΗΣ ΔΙΑΒΑΤΗΡΙΟΥ"
        email_results = ''
        
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            i = 0
            for row in results:
                i+=1
                descr = row[0]
                sort_descr = row[1]
                if i == 1:                                                       
                    response = """Οι προϋποθέσεις έκδοσης διαβατηρίου είναι οι εξής : """
                    dispatcher.utter_message(response)
                    response = """Οι λεπτομερείς προϋποθέσεις έκδοσης διαβατηρίου είναι οι εξής : """
                    email_results = response
                dispatcher.utter_message(format(sort_descr))
                email_results = email_results + "\n\n" + format(descr)
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα στοιχεία...")
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()
        
        # Ερώτηση για αποστολή mail, εφόσον εμφανίστηκαν στοιχεία 
        if not email_results:
            dispatcher.utter_message(template="utter_anything_else")            
        else:
            message = "Θα βοηθούσε να σου στείλω λεπτομερέστερη παρουσίαση των προϋποθέσεων με 📧 email;"
            buttons = [{'title': BUTTON_YES, 
                        'payload': '/affirm'}, 
                        {'title': BUTTON_NO, 
                        'payload': '/deny'}] 
            dispatcher.utter_message(message, buttons=buttons)

        return[SlotSet("email", None), SlotSet("info_for_email", email_results), SlotSet("subject_for_email", email_subject)]                

class ActionDbAbout(Action):	
#       Περί διαβατηρίου
#       Ανάκτηση και εμφάνιση Description από table "publicService" για PS = "Ps0001" .
    def name(self):
        return "action_db_about"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)
        
        cursor = db.cursor()
        q = "select description from publicservice where identifier = '{}'".format(IDENTIFIER_PS_PASSPORT)
        q1 = "select ch_type.description from publicservice as ps, channel as ch, publicservice_channel as ps_ch, cvchanneltype as ch_type where ps.identifier = '{}' and ps.identifier = ps_ch.identifier_ps and ps_ch.identifier_ch = ch.identifier and ch.type = ch_type.code".format(IDENTIFIER_PS_PASSPORT)
             
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            for row in results:
                descr = row[0]
                dispatcher.utter_message(format(descr))
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα στοιχεία...")
            else:
                response = """Η υπηρεσία της έκδοσης διαβατηρίου παρέχεται υπό προϋποθέσεις από τα εξής κανάλια : """
                dispatcher.utter_message(response)
                cursor.execute(q1)
                results = cursor.fetchall()
                str_data = ''
                for row in results:
                    descr = row[0]
                    str_data = str_data + "- {}.\n".format(descr)
                if not results:
                    dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα στοιχεία των καναλιών...")
                else:
                    dispatcher.utter_message(str_data)
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()

        return []
        
class ActionDbAboutDetails(Action):	
#       Περί διαβατηρίου λεπτομερέστερα
#       Ανάκτηση και εμφάνιση Sort_Description από table "rule" για PS = "Ps0001" και rule.name = 'ABOUT PASSPORT'.
    def name(self):
        return "action_db_about_details"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)
        
        cursor = db.cursor()
        q = "select rule.sort_description from publicservice_rule as ps_rule, rule where ps_rule.identifier_ps = '{}' and ps_rule.identifier_ru = rule.identifier and rule.name = 'ABOUT PASSPORT'".format(IDENTIFIER_PS_PASSPORT)
             
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            for row in results:
                descr = row[0]
                dispatcher.utter_message(format(descr))
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα στοιχεία...")
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()

        return []
        
        
class ActionDbCasesOfPassportIssue(Action):	
#       Περιπτώσεις έκδοσης διαβατηρίου
#       Ανάκτηση και εμφάνιση Sort_Description από table "rule" για PS = "Ps0001" και rule.name = 'CASES OF PASSPORT ISSUE'.
    def name(self):
        return "action_db_cases_of_passport_issue"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)    
        
        cursor = db.cursor()
        q = "select rule.sort_description from publicservice_rule as ps_rule, rule where ps_rule.identifier_ps = '{}' and ps_rule.identifier_ru = rule.identifier and rule.name = 'CASES OF PASSPORT ISSUE'".format(IDENTIFIER_PS_PASSPORT)

        response = """Οι περιπτώσεις έκδοσης διαβατηρίου είναι οι εξής : """
        dispatcher.utter_message(response)
        
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            for row in results:
                descr = row[0]
                dispatcher.utter_message(format(descr))
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα στοιχεία...")
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()
        
        return []        

class ActionDPassportIssueProcedure(Action):	
#       Διαδικασία έκδοσης διαβατηρίου
#       Ανάκτηση και εμφάνιση Sort_Description (Description για email) από table "rule" για PS = "Ps0001" και rule.name = 'PASSPORT ISSUE PROCEDURE'.
    def name(self):
        return "action_db_passport_issue_procedure"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)    
        
        cursor = db.cursor()
        q = "select rule.description, rule.sort_description from publicservice_rule as ps_rule, rule where ps_rule.identifier_ps = '{}' and ps_rule.identifier_ru = rule.identifier and rule.name = 'PASSPORT ISSUE PROCEDURE'".format(IDENTIFIER_PS_PASSPORT)

        email_subject = "PassBot - ΔΙΑΔΙΚΑΣΙΑ ΕΚΔΟΣΗΣ ΔΙΑΒΑΤΗΡΙΟΥ"
        email_results = ''
        
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            i = 0
            for row in results:
                i+=1
                descr = row[0]
                sort_descr = row[1]
                if i == 1:                                                       
                    response = """Η διαδικασία που ακολουθείται από την υποβολή των δικαιολογητικών μέχρι και την παραλαβή του νέου διαβατηρίου είναι η εξής : """
                    dispatcher.utter_message(response)                
                    email_results = response
                dispatcher.utter_message(format(sort_descr))
                email_results = email_results + "\n\n" + format(descr)
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα στοιχεία...")
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()

        # Ερώτηση για αποστολή mail, εφόσον εμφανίστηκαν στοιχεία 
        if not email_results:
            dispatcher.utter_message(template="utter_anything_else")            
        else:
            message = "Θα ήθελες να σου στείλω με 📧 email τις πληροφορίες εμπλουτισμένες;"
            buttons = [{'title': BUTTON_YES, 
                        'payload': '/affirm'}, 
                        {'title': BUTTON_NO, 
                        'payload': '/deny'}] 
            dispatcher.utter_message(message, buttons=buttons)     

        return[SlotSet("email", None), SlotSet("info_for_email", email_results), SlotSet("subject_for_email", email_subject)]
        
class ActionDbDurationOfPassport(Action):	
#       Διάρκεια ισχύος του διαβατηρίου
#       Ανάκτηση και εμφάνιση Sort_Description από table "rule" για PS = "Ps0001" και rule.name = 'DURATION OF PASSPORT'.
    def name(self):
        return "action_db_duration_of_passport"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)    
        
        cursor = db.cursor()
        q = "select rule.sort_description from publicservice_rule as ps_rule, rule where ps_rule.identifier_ps = '{}' and ps_rule.identifier_ru = rule.identifier and rule.name = 'DURATION OF PASSPORT'".format(IDENTIFIER_PS_PASSPORT)

        response = """Η διαρκεια ισχύος των διαβατηρίων είναι η εξής : """
        dispatcher.utter_message(response)
        
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            for row in results:
                descr = row[0]
                dispatcher.utter_message(format(descr))
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα στοιχεία...")                
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()
        
        return []
              
class ActionDbEmergencyPassportIssuance(Action):	
#       Επείγουσα έκδοση διαβατηρίου
#       Ανάκτηση και εμφάνιση Sort_Description από table "rule" για PS = "Ps0001" και rule.name = 'EMERGENCY PASSPORT ISSUANCE'.
    def name(self):
        return "action_db_emergency_passport_issuance"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)        
        
        cursor = db.cursor()
        q = "select rule.sort_description from publicservice_rule as ps_rule, rule where ps_rule.identifier_ps = '{}' and ps_rule.identifier_ru = rule.identifier and rule.name = 'EMERGENCY PASSPORT ISSUANCE'".format(IDENTIFIER_PS_PASSPORT)

        response = """Επείγουσα έκδοση διαβατηρίου ; """
        dispatcher.utter_message(response)
        
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            for row in results:
                descr = row[0]
                dispatcher.utter_message(format(descr))
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα στοιχεία...")                
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()
        
        return []        
        
class ActionDbLossTheftOofPpassport(Action):	
#       Απώλεια/κλοπή διαβατηρίου
#       Ανάκτηση και εμφάνιση Sort_Description από table "rule" για PS = "Ps0001" και rule.name = 'LOSS-THEFT OF PASSPORT'.
    def name(self):
        return "action_db_loss_theft_of_passport"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)            
        
        cursor = db.cursor()
        q = "select rule.sort_description from publicservice_rule as ps_rule, rule where ps_rule.identifier_ps = '{}' and ps_rule.identifier_ru = rule.identifier and rule.name = 'LOSS-THEFT OF PASSPORT'".format(IDENTIFIER_PS_PASSPORT)
       
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            for row in results:
                descr = row[0]
                dispatcher.utter_message(format(descr))
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα στοιχεία...")
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()
        
        return []                    

class ActionDbPassportContent(Action):	
#       Στοιχεία που περιλαμβάνει το διαβατήριο
#       Ανάκτηση και εμφάνιση Sort_Description από table "rule" για PS = "Ps0001" και rule.name = 'PASSPORT CONTENT'.
    def name(self):
        return "action_db_passport_content"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)        
        
        cursor = db.cursor()
        q = "select rule.sort_description from publicservice_rule as ps_rule, rule where ps_rule.identifier_ps = '{}' and ps_rule.identifier_ru = rule.identifier and rule.name = 'PASSPORT CONTENT'".format(IDENTIFIER_PS_PASSPORT)
       
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            for row in results:
                descr = row[0]
                dispatcher.utter_message(format(descr))
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα στοιχεία...")
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()
        
        return []

class ActionDbCancellationOfPassport(Action):	
#       Ακύρωση/Αφαίρεση διαβατηρίου
#       Ανάκτηση και εμφάνιση Sort_Description από table "rule" για PS = "Ps0001" και rule.name = 'CANCELLATION OF PASSPORT'.
    def name(self):
        return "action_db_cancellation_of_passport"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)            

        cursor = db.cursor()
        q = "select rule.sort_description from publicservice_rule as ps_rule, rule where ps_rule.identifier_ps = '{}' and ps_rule.identifier_ru = rule.identifier and rule.name = 'CANCELLATION OF PASSPORT'".format(IDENTIFIER_PS_PASSPORT)
       
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            for row in results:
                descr = row[0]
                dispatcher.utter_message(format(descr))
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα στοιχεία...")
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()
        
        return []

class ActionDbactionDbLegalResource(Action):	
#       Νομοθετικό πλαίσιο
#       Ανάκτηση και εμφάνιση lr.name, lrst.Description από table "Legalresource" για PS = "Ps0001".
    def name(self):
        return "action_db_legal_resource"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)        

        cursor = db.cursor()
        q = "select lr.name, lrst.description from legalresource as lr, publicservice_legalresource as ps_lr, cvlrstatus as lrst where ps_lr.identifier_ps = '{}' and ps_lr.identifier_lr = lr.identifier and lr.status = lrst.code".format(IDENTIFIER_PS_PASSPORT)

        response = """Το νομοθετικό πλαίσιο σχετικά με την έκδοση διαβατηρίων από την Ελληνική Αστυνομία, την ίδρυση της Διεύθυνσης Διαβατηρίων, τις προϋποθέσεις χορήγησης διαβατηρίων, χρονική ισχύς, δικαιολογητικά, διαδικασίες έκδοσης κ.α. είναι το εξής:"""
        dispatcher.utter_message(response)        
       
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            for row in results:
                descr = row[0]
                status = row[1]
                str_data = "- {} / Status: {}".format(descr,status)
                dispatcher.utter_message(str_data)                
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα στοιχεία...")
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()
        
        return []

class ActionDbListOfEvidence(Action):	
#       Λίστα των πιθανών δικαιολογητικών
#       Ανάκτηση και εμφάνιση ev.name από table "evidence" για PS = "Ps0001".
    def name(self):
        return "action_db_list_of_evidence"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)            

        response = """Τα πιθανά δικαιολογητικά 🧾 που μπορεί να ζητηθούν για τη έκδοση διαβατηρίου είναι τα εξής (αναλόγως την περίπτωση):"""
        dispatcher.utter_message(response)        

        cursor = db.cursor()
        q = "select distinct ev.name from evidence as ev, publicservice_evidence as ps_ev where ps_ev.identifier_ps = '{}' and ps_ev.identifier_ev = ev.identifier".format(IDENTIFIER_PS_PASSPORT)
       
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            str_data = ''
            for row in results:
                descr = row[0]
                str_data = str_data + "- {}.\n".format(descr)                
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν τα δικαιολογητικά...")
            else:
                dispatcher.utter_message(str_data)
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()
        
        return []
        
class ActionDbEvidence(Action):	
#       Εξατομικευμένα δικαιολογητικά
#       Ανάκτηση περιγραφών απαντήσεων που έχουν δοθεί, από table "AnswerForDoc". Απαιτείται μόνο για το email.
#       Ανάκτηση δικαιολογητικών βάσει των απαντήσεων, από table "evidence". Εμφάνιση name. Email name, description.
#       Ανάκτηση κόστους βάσει των απαντήσεων, από table "cost". Εμφάνιση αξίας, νομίσματος, sort_description. Email αξία νόμισμα, description.
#       Ανάκτηση εξόδου βάσει των απαντήσεων, από table "output". Εμφάνιση name. Email name , description.
    def name(self):
        return "action_db_evidence"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)        

        a1 = tracker.get_slot("answer1")
        a2 = tracker.get_slot("answer2")
        a3 = tracker.get_slot("answer3")
        a4 = tracker.get_slot("answer4")
        a5 = tracker.get_slot("answer5")
        a6 = tracker.get_slot("answer6")
        a7 = tracker.get_slot("answer7")
        a8 = tracker.get_slot("answer8")
        a9 = tracker.get_slot("answer9")
        a10 = tracker.get_slot("answer10")
        a11 = tracker.get_slot("answer11")
        a12 = tracker.get_slot("answer12")
        
        str_data = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12)

        # Ετοιμασία ερωτήματος για ανάκτηση των απαντήσεων - όπου έχει εξαιρεθεί η ερώτηση δεν θα ανακτηθεί εγγραφή
        q_email = "select name from answerfordoc where identifier in ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12)
        
        # Ενημέρωση περιεχομένου με 'Όχι' στις απαντήσεις των ερωτήσεων που τυχόν εξαιρέθηκαν (5-10-12) για εξαγωγή των ορθών δικαιολογητικών
        if a5 == None:
           a5 = 'A0014'
        if a10 == None:
           a10 = 'A0026'
        if a12 == None:
           a12 = 'A0030'   
       
        str_data = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12)
       
        response = """😃 Ευχαριστώ για το χρόνο σου..."""
        dispatcher.utter_message(response)        
               
        # Ετοιμασία ερωτήματος για ανάκτηση των δικαιολογητικών που απαιτούνται
        q = "select name, description from evidence as ev where ev.identifier not in (select distinct identifier_ev from answerfordoc_ex_ev where identifier_a='{}' or identifier_a='{}' or identifier_a='{}' or identifier_a='{}' or identifier_a='{}' or identifier_a='{}' or identifier_a='{}' or identifier_a='{}' or identifier_a='{}' or identifier_a='{}' or identifier_a='{}' or identifier_a='{}')".format(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12)
        # Ετοιμασία ερωτήματος για ανάκτηση του κόστους
        q_cost = "select value, cvcurrency.name, description, sort_description from cost, cvcurrency where cost.currency = cvcurrency.code and weight = (select min(weight) from answerfordoc as afd, cost as co where afd.cost <> 'null' and afd.cost = co.identifier and afd.identifier in ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'))".format(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12)
        # Ετοιμασία ερωτήματος για ανάκτηση της εξόδου
        q_export = "select name, description from output where weight = (select min(weight) from answerfordoc as afd, output as ou where afd.output <> 'null' and afd.output = ou.identifier and afd.identifier in ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'))".format(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12)

        email_subject = "PassBot - ΕΞΑΤΟΜΙΚΕΥΜΕΝΑ ΔΙΚΑΙΟΛΟΓΗΤΙΚΑ ΠΟΥ ΑΠΑΙΤΟΥΝΤΑΙ ΓΙΑ ΕΚΔΟΣΗ ΔΙΑΒΑΤΗΡΙΟΥ"
        email_results = ''

        cursor = db.cursor()
        
        try:
            # Ανάκτηση περιγραφών των απαντήσεων - μόνο για το email
            cursor.execute(q_email)
            results = cursor.fetchall()
            i = 0
            len_data = len(results)
            for row in results:
                descr = row[0]
                i+=1                
                if i == 1:
                   str_data = "💡 Οι απαντήσεις οι οποίες έδωσες προκειμένου να εξαχθούν τα εξατομικευμένα δικαιολογητικά για την περίπτωση σου, είναι οι εξής : \n"
                   email_results = email_results + str_data
                str_data = format(descr)
                email_results = email_results + "\n" + "✔ "+ str_data
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν στοιχεία των απαντήσεων σου...")        

            # Ανάκτηση εξόδου διαβατηρίου
            cursor.execute(q_export)
            results = cursor.fetchall()
            for row in results:
                name = row[0]
                descr = row[1]                
                str_data = "🗨 To διαβατήριο που θα εκδοθεί για την περίπτωσή σου είναι {}.".format(name)
                str_data_email = "🗨 To διαβατήριο που θα εκδοθεί για την περίπτωσή σου είναι {}.\n{}".format(name, descr)
                email_results = email_results + "\n\n" + str_data_email
                dispatcher.utter_message(str_data)
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκε έξοδος διαβατηρίου...")                

            # Ανάκτηση κόστους διαβατηρίου
            cursor.execute(q_cost)
            results = cursor.fetchall()
            for row in results:
                val = row[0]
                cur_name = row[1]
                descr = row[2]                
                sort_descr = row[3]
                str_data = "🗨 Θα κοστίσει {} {}.\n{}".format(val, cur_name, sort_descr)
                str_data_email = "🗨 Θα κοστίσει {} {}.\n{}".format(val, cur_name, descr)
                email_results = email_results + "\n\n" + str_data_email
                dispatcher.utter_message(str_data)
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκε κόστος...")                

            # Ανάκτηση δικαιολογητικών
            cursor.execute(q)
            results = cursor.fetchall()
            str_data        = "🗨 Τα δικαιολογητικά 📄 που απαιτούνται είναι τα εξής: \n"
            str_data_mail   = str_data
            for row in results:
                descr = row[0]
                detail = row[1]
                str_data = str_data + "- {}.\n".format(descr)
                str_data_mail  = str_data_mail + "✔ {}.\n".format(descr)
                str_data_mail = str_data_mail + " {}\n\n".format(detail)
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν δικαιολογητικά...")
            else:
                email_results = email_results + "\n\n" + str_data_mail
                dispatcher.utter_message(str_data)                
                               
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()

        # Ερώτηση για αποστολή mail, εφόσον εμφανίστηκαν στοιχεία 
        if not email_results:
            dispatcher.utter_message(template="utter_anything_else")            
        else:
            message = "Θα ήθελες να σου στείλω με 📧 email τις πληροφορίες εμπλουτισμένες;"
            buttons = [{'title': BUTTON_YES, 
                        'payload': '/affirm'}, 
                        {'title': BUTTON_NO, 
                        'payload': '/deny'}] 
            dispatcher.utter_message(message, buttons=buttons)

        return[SlotSet("email", None), SlotSet("info_for_email", email_results), SlotSet("subject_for_email", email_subject)]

class ActionDbPlaceOfSubmissionLocation(Action):	
#       Εντοπισμός γραφείου διαβατηρίων
#       Εξαγωγή λέξεων από το String - έως 3 λέξεις
#       Αφαίρεση τελευταίου χαρακτήρα από τις εισαχθέντες λέξεις
#       Διερεύνιση σε 4 πεδία - areaServed, location, Title, Address
#       Εμφάνιση των στοιχείων σε carousel
    def name(self):
        return "action_db_Place_Of_Submission_location"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        db = mysql.connector.connect(**config)        
        
        nameoflocation = tracker.get_slot("location")

        if not nameoflocation:
            nameoflocation1 =  'ωωωωωωωωω'    # Περίπτωση να ζητηθεί αναζήτηση με κενή φράση. Προκειμένου να μην εμφανιστούν 
            nameoflocation2 =  ''             # όλα τα contact points θέτω στην 1η λέξη 'ωωωωωωωωωωωω', οπότε δεν θα επιστρέψει
            nameoflocation3 =  ''             # γραφεία διαβατηρίων
        else:
            words = nameoflocation.split()
            len_words = len(words)

            if len_words == 1:
               nameoflocation1 =  words[0]
               nameoflocation2 =  ''
               nameoflocation3 =  ''
            elif len_words == 2:
               nameoflocation1 =  words[0]
               nameoflocation2 =  words[1]
               nameoflocation3 =  ''
            else:
               nameoflocation1 =  words[0]
               nameoflocation2 =  words[1]
               nameoflocation3 =  words[2]       

            temp = nameoflocation1
            lenx = len(temp)
            nameoflocation1 = (temp[0:lenx-1:1])

            temp = nameoflocation2
            lenx = len(temp)
            nameoflocation2 = (temp[0:lenx-1:1])

            temp = nameoflocation3
            lenx = len(temp)
            nameoflocation3 = (temp[0:lenx-1:1])
                                    
        q = "select * from contactpoint as cp, publicservice_contactpoint as ps_cp where ps_cp.identifier_ps = '{3}' and ps_cp.identifier_cp = cp.identifier and ((cp.areaserved like '%{0}%' and cp.areaserved like '%{1}%' and cp.areaserved like '%{2}%') or (cp.location like '%{0}%' and cp.location like '%{1}%' and cp.location like '%{2}%') or (cp.title like '%{0}%' and cp.title like '%{1}%' and cp.title like '%{2}%') or (cp.address like '%{0}%' and cp.address like '%{1}%' and cp.address like '%{2}%')) order by title".format(nameoflocation1,nameoflocation2,nameoflocation3,IDENTIFIER_PS_PASSPORT)

        email_subject = "PassBot - ΓΡΑΦΕΙΑ ΕΚΔΟΣΗΣ ΔΙΑΒΑΤΗΡΙΩΝ ΓΙΑ ΠΕΡΙΟΧΗ/ΔΗΜΟ ΚΑΤΟΙΚΙΑΣ: {}".format(nameoflocation)
        email_results = ''
        json_data_list = []
        img_url_point = "https://cdn.pixabay.com/photo/2013/07/12/13/53/police-officer-147501_960_720.png"
        
        cursor = db.cursor()
        
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            i = 0
            len_data = len(results)
            for row in results:
                i+=1
                # Εμφάνιση των στοιχείων (έως 5) και ετοιμασία για email (όλα)
                title = row[1]
                address = row[2]
                location = row[3]   
                area = row[4]
                hours = row[5]
                Email = row[6]
                Tel = row[7]
                addr = ''
                addr = GOOGLE_MAP_ADDRESS + address.replace(" ","+")
                str_data_aa     = "{}. Υπηρεσία:".format(i)
                str_data        = "{},\nΔιεύθυνση: {},\nΠεριοχή: {},\nΕδαφική αρμοδιότητα: {},\nΩράριο Εξυπηρέτησης: {},\nE-mail: {},\nΤηλέφωνο: {}".format(title,address,location,area,hours,Email,Tel)
                str_data_email  = "{}.Υπηρεσία: {}\nΔιεύθυνση: {}\nΠεριοχή: {}\nΕδαφική αρμοδιότητα: {}\nΩράριο Εξυπηρέτησης: {}\nE-mail: {}\nΤηλέφωνο: {}\nΓια εμφάνιση στο χάρτη πάτησε ({}).\n".format(i,title,address,location,area,hours,Email,Tel, addr)
                elem = {
                    "title": str_data_aa,
                    "subtitle": str_data,
                    "image_url": img_url_point,
                    "buttons": [{
                        "title": "Εμφάνιση στο χάρτη",
                        "url": addr,
                        "type": "web_url"
                    }]
                }                               
                if i == 1:
                   response = """Το/τα γραφεία έκδοσης διαβατηρίων που εντοπίστηκαν για την περιοχή {} είναι {} : \n""".format(nameoflocation, len_data)
                   dispatcher.utter_message(response)
                   email_results = response
                email_results = email_results + "\n" + str_data_email
                if i <= 5:
                   json_data_list.append(elem)                
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν γραφεία διαβατηρίων... Μπορείς να δεις και [εδώ](http://www.passport.gov.gr/grafeia-kai-orario/grafeia-diavatirion-ellada/)")
            elif len_data > 5:
                dispatcher.utter_message("Εμφανίστηκαν 5 από {} αποτελέσματα.\nΜπορείς να επαναδιατυπώσεις την περιοχή σου για περιορισμό των αποτελεσμάτων".format(len_data))
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()       

        if results:
            dsp_carousel = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": json_data_list                        
                }
            }
            dispatcher.utter_message(attachment=dsp_carousel)

        # Ερώτηση για αποστολή mail, εφόσον εμφανίστηκαν στοιχεία 
        if not email_results:
            dispatcher.utter_message(template="utter_anything_else")            
        else:
            message = "Θα ήθελες να σου στείλω με 📧 email όλες τις πληροφορίες;"
            buttons = [{'title': BUTTON_YES, 
                        'payload': '/affirm'}, 
                        {'title': BUTTON_NO, 
                        'payload': '/deny'}] 
            dispatcher.utter_message(message, buttons=buttons)

        return[SlotSet("location", None), SlotSet("email", None), SlotSet("info_for_email", email_results), SlotSet("subject_for_email", email_subject)]        

        
class ActionDbSundayΟffice(Action):	
#       Γραφεία ανοιχτά την Κυριακή / Εμφάνιση των στοιχείων σε carousel

    def name(self):
        return "action_db_Sunday_office"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        db = mysql.connector.connect(**config)        
            
        q = "select * from contactpoint as cp, publicservice_contactpoint as ps_cp where ps_cp.identifier_ps = '{}' and ps_cp.identifier_cp = cp.identifier and (hoursavailable like '%ΚΥ%' or hoursavailable like '%ΚΥΡΙΑΚΗ%' or hoursavailable like '%κυριακή%' or hoursavailable like '%Sunday%') order by title".format(IDENTIFIER_PS_PASSPORT)
        
        cursor = db.cursor()

        email_subject = "PassBot - ΓΡΑΦΕΙΑ ΕΚΔΟΣΗΣ ΔΙΑΒΑΤΗΡΙΩΝ ΑΝΟΙΚΤΑ ΤΗΝ ΚΥΡΙΑΚΗ "
        email_results = ''
        json_data_list = []
        img_url_point = "https://cdn.pixabay.com/photo/2013/07/12/13/53/police-officer-147501_960_720.png"        
        
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            i = 0
            len_data = len(results)
            for row in results:
                i+=1
                # Εμφάνιση των στοιχείων (έως 5) και ετοιμασία για email (όλα)
                title = row[1]
                address = row[2]
                location = row[3]   
                area = row[4]
                hours = row[5]
                Email = row[6]
                Tel = row[7]
                addr = ''
                addr = GOOGLE_MAP_ADDRESS + address.replace(" ","+")
                str_data_aa     = "{}. Υπηρεσία:".format(i)
                str_data        = "{},\nΔιεύθυνση: {},\nΠεριοχή: {},\nΕδαφική αρμοδιότητα: {},\nΩράριο Εξυπηρέτησης: {},\nE-mail: {},\nΤηλέφωνο: {}".format(title,address,location,area,hours,Email,Tel)
                str_data_email  = "{}.Υπηρεσία: {}\nΔιεύθυνση: {}\nΠεριοχή: {}\nΕδαφική αρμοδιότητα: {}\nΩράριο Εξυπηρέτησης: {}\nE-mail: {}\nΤηλέφωνο: {}\nΓια εμφάνιση στο χάρτη πάτησε ({}).\n".format(i,title,address,location,area,hours,Email,Tel, addr)
                elem = {
                    "title": str_data_aa,
                    "subtitle": str_data,
                    "image_url": img_url_point,
                    "buttons": [{
                        "title": "Εμφάνιση στο χάρτη",
                        "url": addr,
                        "type": "web_url"
                    }]
                }
                if i == 1:
                   response = """Το/τα γραφεία έκδοσης διαβατηρίων που εντοπίστηκαν, σε όλη την Ελλάδα, ανοιχτά την Κυριακή, είναι {} : \n""".format(len_data)        
                   dispatcher.utter_message(response)
                   email_results = response
                email_results = email_results + "\n" + str_data_email
                if i <= 5:
                   json_data_list.append(elem)
            if not results:
                dispatcher.utter_message("Λυπάμαι... Δεν βρέθηκαν γραφεία διαβατηρίων... Εναλλακτικά εναλλακτικά μπορείς να ψάξεις και [εδώ](http://www.passport.gov.gr/grafeia-kai-orario/grafeia-diavatirion-ellada/)")
            elif len_data > 5:
                dispatcher.utter_message("Εμφανίστηκαν 5 από {} αποτελέσματα.".format(len_data))
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία...")
            
        db.close()

        if results:
            dsp_carousel = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": json_data_list                        
                }
            }
            dispatcher.utter_message(attachment=dsp_carousel)

        # Ερώτηση για αποστολή mail, εφόσον εμφανίστηκαν στοιχεία 
        if not email_results:
            dispatcher.utter_message(template="utter_anything_else")            
        else:
            message = "Θα ήθελες να σου στείλω με 📧 email όλες τις πληροφορίες;"
            buttons = [{'title': BUTTON_YES, 
                        'payload': '/affirm'}, 
                        {'title': BUTTON_NO, 
                        'payload': '/deny'}] 
            dispatcher.utter_message(message, buttons=buttons)
        
        return[SlotSet("email", None), SlotSet("info_for_email", email_results), SlotSet("subject_for_email", email_subject)]


class ActionInfo(Action):	
#       Εμφάνιση πληροφοριών ανάπτυξης του Chatbot
    def name(self):
        return "action_info"

    def run(self, dispatcher, tracker, domain):
           
        str_data = "- Το παρόν chatbot 👮 έχει δημιουργηθεί στο πλαίσιο Διπλωματικής Εργασίας με θέμα 'Ανάπτυξη Chatbot για την έκδοση Διαβατηρίου' του μεταπτυχιακού φοιτητή Αντωνιάδη Παντελή, του τμήματος 'Μεταπτυχιακή Εξειδίκευση στα Πληροφοριακά Συστήματα (ΠΛΣ)' του Ελληνικού Ανοιχτού Πανεπιστημίου, κατά το ακαδημαϊκό έτος 2019-2020.\n"
        str_data = str_data + "- Η ανάπτυξη του έχει πραγματοποιηθεί με το open source framework 'Rasa'.\n"
        str_data = str_data + "- Η σχετική πληροφορία για το διαβατήριο είναι καταχωρημένη σύμφωνα με το ευρωπαϊκό μοντέλο CPSV-AP σε MysQL database, από την οποία πραγματοποιείται on-line ανάκτηση για κάθε ανταπόκριση του ChatBot.\n"
        dispatcher.utter_message(str_data)
        
        str_data = "Καλύπτει την παρακάτω πληροφόρηση σχετικά με το διαβατήριο:\n"
        str_data = str_data + "- Τι είναι διαβατήριο.\n"
        str_data = str_data + "- Προϋποθέσεις έκδοσης διαβατηρίου (συνοπτικά/αναλυτικά).\n"
        str_data = str_data + "- Περιπτώσεις έκδοσης διαβατηρίου.\n"
        str_data = str_data + "- Kόστος έκδοσης διαβατηρίου.\n"
        str_data = str_data + "- Διαδικασία έκδοσης.\n"
        str_data = str_data + "- Δικαιολογητικά που απαιτούνται (λίστα).\n"
        str_data = str_data + "- Εξατομικευμένη πληροφόρηση δικαιολογητικών - Κόστους - Εξόδου διαβατηρίου.\n"
        str_data = str_data + "- Τόπος υποβοβολής των δικαιολογητικών.\n"
        str_data = str_data + "- Εύρεση γραφείου διαβατηρίων περιοχής.\n"
        str_data = str_data + "- Εύρεση γραφείων που λειτουργούν Κυριακή.\n"
        str_data = str_data + "- Διάρκεια ισχύος των διαβατηρίων.\n"
        str_data = str_data + "- Επείγουσα έκδοση διαβατηρίου.\n"      
        str_data = str_data + "- Απώλεια/κλοπή διαβατηρίου.\n"      
        str_data = str_data + "- Στοιχεία που περιλαμβάνει το διαβατήριο.\n"
        str_data = str_data + "- Ακύρωση / Αφαίρεση διαβατηρίου.\n"        
        str_data = str_data + "- Νομοθετικό πλαίσιο.\n"   
        dispatcher.utter_message(str_data)
        
        str_data = "Παραπέμπτει στο site των διαβατηρίων της Ελληνικής Αστυνομιας για τις περιπτώσεις:\n"
        str_data = str_data + "- Πορεία αίτησης έκδοσης διαβατηρίου.\n"
        str_data = str_data + "- Πληροφορίες για το e-paravolo.\n"     
        str_data = str_data + "- Τεχνικές προδιαγραφές φωτογραφίας.\n"     
        dispatcher.utter_message(str_data)
        
        str_data = "Αποστέλλει και με email, τις σημαντικές πληροφορίες :\n"
        str_data = str_data + "- Εξατομικευμένα δικαιολογητικά - Κόστος - Έξοδος διαβατηρίου.\n"
        str_data = str_data + "- Διαδικασία έκδοσης.\n"
        str_data = str_data + "- Προυποθέσεις έκδοσης.\n"
        str_data = str_data + "- Γραφείο διαβατηρίων περιοχής χρήστη.\n"
        str_data = str_data + "- Ανοικτά Γραφεία Διαβατηρίων την Κυριακή.\n"                
        dispatcher.utter_message(str_data)
        
        str_data = "Επιπλέον καλύπτει :\n"
        str_data = str_data + "- Small talk.\n"
        str_data = str_data + "- Χαιρετισμούς.\n"
        str_data = str_data + "- Ευχαριστίες.\n"
        str_data = str_data + "- Χειρισμό 'out of scope' ερωτήσεων.\n"        
        str_data = str_data + "- Feedback. \nΔίνεται κατά την αποχώρηση του χρήστη, εφόσον υπάρχει χαιρετισμός (πχ αντίο) ή μετά από ευχαριστίες του."
        dispatcher.utter_message(str_data)

        str_data = "Από οποιοδήποτε σημείο του διαλόγου γράφοντας 'Επιλογές' εμφανίζονται με buttons προτεινόμενες επιλογές πληροφόρησης."
        dispatcher.utter_message(str_data)
        
        db = mysql.connector.connect(**config)        
        cursor = db.cursor()

        # Ανάκτηση θετικών εντυπώσεων για το chatbot από talbe "feedback"
        q = "select count(*) from feedback where vote_useful = 'affirm'"
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            i = 0
            for row in results:
                i+=1
                if i==1:
                   useful_affirm = row[0]
            if not results:
                useful_affirm = 0
#                dispatcher.utter_message("Τέλος, δεν βρέθηκαν στοιχεία 'affirm' feedback...")
        except:
            useful_affirm = 0
#            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία 'affirm' feedback...")
        
        # Ανάκτηση αρνητικών εντυπώσεων για το chatbot από talbe "feedback"
        q = "select count(*) from feedback where vote_useful = 'deny'"
        try:
            cursor.execute(q)
            results = cursor.fetchall()
            i = 0
            for row in results:
                i+=1
                if i==1:
                   useful_deny = row[0]
            if not results:
                useful_deny = 0
#                dispatcher.utter_message("Τέλος, δεν βρέθηκαν στοιχεία 'deny' feedback...")
        except:
            useful_deny = 0
#            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ανακτήσω στοιχεία 'deny' feedback...")                               
        
        useful_affirm_per = 0
        useful_deny_per = 0
        if useful_affirm > 0:
            useful_affirm_per = (useful_affirm / (useful_affirm + useful_deny)) * 100
        if useful_deny > 0:
            useful_deny_per = (useful_deny / (useful_affirm + useful_deny)) * 100
        response = ('Τέλος, από την έως τώρα χρήση του Chatbot καταγράφηκαν {} ({:2.1f}%) θετικές εντυπώσεις και {} ({:2.1f}%) αρνητικές.'.format(useful_affirm, useful_affirm_per, useful_deny, useful_deny_per))
        dispatcher.utter_message(response)                           
            
        db.close()        

        return[]

class ActionDefaultAskAffirmation(Action):
#       Ερώτηση επιβεβαίωσης για πρόθεση χρήστη εφόσον το confidence rate είναι κάτω από το δηλωμένο κατώφλι
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self) -> Text:
        return "action_default_ask_affirmation"

    def __init__(self) -> None:
        import pandas as pd

        self.intent_mappings = pd.read_csv(INTENT_DESCRIPTION_MAPPING_PATH,encoding ='utf-8')
        self.intent_mappings.fillna("", inplace=True)
        self.intent_mappings.entities = self.intent_mappings.entities.map(
            lambda entities: {e.strip() for e in entities.split(",")}
        )

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        
        # Λήψη της λίστας των ταξινομημένων intents
        intent_ranking = tracker.latest_message.get("intent_ranking", [])
                      
        first_intent_names=[]
        i=0        
        # Εξαγωγή των 2 πρώτων intents, εκτός αυτών που δεν πρέπει να προταθούν
        for row in intent_ranking:
            if row.get("name", "") not in ["q1","q2","q3","q4","q5","q6","q7","q8","q9","q10","q11","q12","enter_email","out_of_scope"]:
               first_intent_names.append(row.get("name", ""))
               i+=1
               if i >= 2:
                  break
                
        message_title = (
            "Δυστυχώς δεν είμαι σίγουρος ότι κατάλαβα σωστά 🤔 Εννοείς..."
        )

        entities = tracker.latest_message.get("entities", [])
        entities = {e["entity"]: e["value"] for e in entities}

        entities_json = json.dumps(entities)

        buttons = []
        for intent in first_intent_names:
            button_title = self.get_button_title(intent, entities)
            if "/" in intent:
                # here we use the button title as the payload as well, because you
                # can't force a response selector sub intent, so we need NLU to parse
                # that correctly
                buttons.append({"title": button_title, "payload": button_title})
            else:
                buttons.append(
                    {"title": button_title, "payload": f"/{intent}{entities_json}"}
                )

        buttons.append({"title": "Κάτι άλλο", "payload": "/trigger_rephrase"})

        dispatcher.utter_message(text=message_title, buttons=buttons)

        return []    

    def get_button_title(self, intent: Text, entities: Dict[Text, Text]) -> Text:
        default_utterance_query = self.intent_mappings.intent == intent
        utterance_query = (self.intent_mappings.entities == entities.keys()) & (
            default_utterance_query
        )

        utterances = self.intent_mappings[utterance_query].button.tolist()

        if len(utterances) > 0:
            button_title = utterances[0]
        else:
            utterances = self.intent_mappings[default_utterance_query].button.tolist()
            button_title = utterances[0] if len(utterances) > 0 else intent

        return button_title.format(**entities)
        

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        # Fallback caused by TwoStageFallbackPolicy
        if (
            len(tracker.events) >= 4
            and tracker.events[-4].get("name") == "action_default_ask_affirmation"
        ):

            dispatcher.utter_message(template="utter_restart_with_button")

            return []
            
        # Fallback caused by Core
        else:
            dispatcher.utter_message(template="utter_default")
            return [UserUtteranceReverted()]        
            
            
class ActionfeedBack(Action):	
#       Εγγραφή feedback από τον χρήστη
    def name(self):
        return "action_db_feedback"

    def run(self, dispatcher, tracker, domain):
        db = mysql.connector.connect(**config)
              
        last_message = tracker.latest_message['intent'].get('name')
        
        cursor = db.cursor()
        q = "insert into feedback (vote_useful) values ('%s')" % (last_message.replace('/', ''))
  
        try:
            cursor.execute(q)
            db.commit()
        except:
            dispatcher.utter_message("Ούπς... ⚙ Δεν μπόρεσα να ενημερώσω την DataBase...")
            
        db.close()
                
        return []            

        
class EvidenceForm(FormAction):
#   Φόρμα για τις 12 ερωτήσεις εξαγωγής των εξατομικευμένων δικαιολογητικών

    def name(self) -> Text:

        return "evidence_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        
        a1 = tracker.get_slot("answer1")
        a2 = tracker.get_slot("answer2")

        # Περίπτωση Αρχικής έκδοσης/Ανανέωσης/Αντικατάστασης - Ενήλικος == αποκλεισμός ερώτησης 12-κατ'εξαίρεση έκδοσης μετά από απώλεια-κλοπή
        if (a1 == 'A0001' or a1 == 'A0002' or a1 == 'A0003') and (a2 == 'A0005'):
           return ["answer1", "answer2", "answer3", "answer4", "answer5", "answer6", "answer7", "answer8", "answer9", "answer10", "answer11"]
        # Περίπτωση Αρχικής έκδοσης/Ανανέωσης/Αντικατάστασης - <12 και 12 ετών == αποκλεισμός ερωτήσεων 5-δακτυλικά αποτυπώματα, 10-ανυπότακτος εξωτερικού, 12-κατ'εξαίρεση έκδοσης μετά από απώλεια-κλοπή
        elif (a1 == 'A0001' or a1 == 'A0002' or a1 == 'A0003') and (a2 == 'A0006' or a2 == 'A0007') :
           return ["answer1", "answer2", "answer3", "answer4", "answer6", "answer7", "answer8", "answer9", "answer11"]
        # Περίπτωση Αρχικής έκδοσης/Ανανέωσης/Αντικατάστασης - 13-14 και >14 ετών == αποκλεισμός ερωτήσεων 10-ανυπότακτος εξωτερικού, 12-κατ'εξαίρεση έκδοσης μετά από απώλεια-κλοπή
        elif (a1 == 'A0001' or a1 == 'A0002' or a1 == 'A0003') and (a2 == 'A0008' or a2 == 'A0009') :          
           return ["answer1", "answer2", "answer3", "answer4", "answer5", "answer6", "answer7", "answer8", "answer9", "answer11"]
        # Περίπτωση Απώλειας/κλοπής - <12 και 12 ετών == αποκλεισμός ερωτήσεων 5-δακτυλικά αποτυπώματα, 10-ανυπότακτος εξωτερικού
        elif (a1 == 'A0004') and (a2 == 'A0006' or a2 == 'A0007') :          
           return ["answer1", "answer2", "answer3", "answer4", "answer6", "answer7", "answer8", "answer9", "answer11", "answer12"]
        # Περίπτωση Απώλειας/κλοπής - 13-14 και >14 ετών == αποκλεισμός ερώτησης 10-ανυπότακτος εξωτερικού
        elif (a1 == 'A0004') and (a2 == 'A0008' or a2 == 'A0009') :
           return ["answer1", "answer2", "answer3", "answer4", "answer5", "answer6", "answer7", "answer8", "answer9", "answer11", "answer12"]
        # Περίπτωση Απώλειας/κλοπής - Ενήλικος == ισχύουν όλες οι ερωτήσεις
        else:   
           return ["answer1", "answer2", "answer3", "answer4", "answer5", "answer6", "answer7", "answer8", "answer9", "answer10", "answer11", "answer12"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "answer1": self.from_entity(entity="answer1",   intent="q1"),
            "answer2": self.from_entity(entity="answer2",   intent="q2"),          
            "answer3": self.from_entity(entity="answer3",   intent="q3"),
            "answer4": self.from_entity(entity="answer4",   intent="q4"),            
            "answer5": self.from_entity(entity="answer5",   intent="q5"),            
            "answer6": self.from_entity(entity="answer6",   intent="q6"),
            "answer7": self.from_entity(entity="answer7",   intent="q7"),
            "answer8": self.from_entity(entity="answer8",   intent="q8"),
            "answer9": self.from_entity(entity="answer9",   intent="q9"),
            "answer10": self.from_entity(entity="answer10", intent="q10"),
            "answer11": self.from_entity(entity="answer11", intent="q11"),
            "answer12": self.from_entity(entity="answer12", intent="q12"),
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        return []

class LocationForm(FormAction):
#       Εισαγωγή της τοποθεσίας για την αναζήτηση γραφείου διαβατηρίων, 
#       με εισαγωγή οποιασδήποτε φράσης χωρίς έλεγχο intent (μέσω του self.from_text)
#       και της δήλωσης του type του location unfeaturized

    def name(self) -> Text:

        return "location_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["location"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "location": [self.from_entity(entity="location"), self.from_text()],
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        return []

class EmailForm(FormAction):
#       Εισαγωγή email του χρήστη

    def name(self) -> Text:
        return "email_form"

    @staticmethod
    def     required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["email"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
        
            "email": [self.from_entity(entity="email"), 
                      self.from_text(intent="enter_email")],
        }

    def validate_email(self, value, dispatcher, tracker, domain):
        """Check to see if an email entity was actually picked up by duckling."""

        if any(tracker.get_latest_entity_values("email")):
            try:                
                valid = validate_email(value)               # Validate.                
                email = valid.email                         # Update with the normalized form.
                return {"email": value}
            except EmailNotValidError as e:
                # email is not valid, exception message is human-readable
                dispatcher.utter_message(template="utter_no_email")
                return {"email": None}

        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_message(template="utter_no_email")
            return {"email": None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        
        return []

class SendAnEmail(Action):
#       Αποστολή email 

    def name(self) -> Text:
        return "action_send_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        email_text      = format(tracker.get_slot("info_for_email"))
        subject         = format(tracker.get_slot("subject_for_email"))

        if not email_text:
            dispatcher.utter_message("Φαίνεται ότι δεν υπάρχουν στοιχεία για αποστολή! 😢 Λυπάμαι αλλά η αποστολή ακυρώνεται... ")
            return[]
            
        port =  465
        smtp_server = "smtp.gmail.com"
        login = LOGIN_EMAIL    # paste your login generated by Gmail
        password = PASSWORD    # paste your password generated by Gmail
        sender_email = SENDER_EMAIL
        receiver_email = tracker.get_slot("email")

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email
        # Write the plain text part

        text = "Γειά σου!\nΠαρακάτω μπορείς να βρεις τις πληροφορίες που ζήτησες.\n\n"
        text = text + email_text + "\n\nPassBot.\nThe Greek Virtual Passport Agent.\n\n\n\nΑυτόματο email - ΠΑΡΑΚΑΛΩ ΜΗΝ ΑΠΑΝΤΗΣΕΙΣ"
        
        part1 = MIMEText(text, "plain")
        message.attach(part1)

        context = ssl.create_default_context()

        # send the email
        dispatcher.utter_message ("Αποστολή email σε {}".format(receiver_email))
        
        try:
          with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(login, password)
            server.sendmail( sender_email, receiver_email, message.as_string() )
        except smtplib.SMTPAuthenticationError:
          dispatcher.utter_message('Αδυναμία σύνδεσης με mail Server. Username and Password not accepted...')
        except (gaierror, ConnectionRefusedError):
          dispatcher.utter_message('Αδυναμία σύνδεσης με mail Server. Bad connection settings...')
        except smtplib.SMTPServerDisconnected:
          dispatcher.utter_message('Αδυναμία σύνδεσης με mail Server. Disconnected...')          
        except smtplib.SMTPException as e:
          dispatcher.utter_message('Αδυναμία σύνδεσης με mail Server. ' + str(e))
        else:
          dispatcher.utter_message('Η αποστολή του email ολοκληρώθηκε.')
        
        return[AllSlotsReset()]
        
class ResetAllSlots(Action):
#       Reset All Slots 

    def name(self) -> Text:
        return "action_reset_all_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                   
        return[AllSlotsReset()]
