## info path
* info
  - action_info									
  - utter_anything_else

## greet path
* greet
  - utter_greet
  - utter_intro1
  - utter_intro2
  - utter_question_continue
* affirm
  - utter_continue  
  - utter_continue1

## greet path1
* greet
  - utter_greet
  - utter_intro1
  - utter_intro2  
  - utter_question_continue
* deny
  - utter_non_continue

## greet path2
* greet
  - utter_greet
  - utter_intro1
  - utter_intro2
  - utter_question_continue
* samples
  - utter_samples								
  - utter_question_continue2
* affirm
  - utter_continue  
  - utter_continue1

## greet path3
* greet	
  - utter_greet
  - utter_intro1
  - utter_intro2
  - utter_question_continue
* samples
  - utter_samples								
  - utter_question_continue2
* deny
  - utter_non_continue
  
## greet path4
* greet
  - utter_greet
  - utter_intro1
  - utter_intro2
  - utter_question_continue
* info
  - action_info									
  - utter_anything_else

## Place_Of_Submission-email path1_1
* Place_Of_Submission
  - action_db_Place_Of_Submission				
  - utter_location								
* affirm 
  - action_deactivate_form
  - action_reset_all_slots  
  - location_form								
  - form{"name": "location_form"}
  - form{"name": null}
  - utter_slots_location_values
  - action_db_Place_Of_Submission_location
* affirm	
  - email_form									
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_accept_email
  - action_send_email							
  - utter_anything_else

## Place_Of_Submission-mail-cancel path1_2
* Place_Of_Submission
  - action_db_Place_Of_Submission				
  - utter_location								
* affirm 
  - action_deactivate_form						
  - action_reset_all_slots    
  - location_form								
  - form{"name": "location_form"}
  - form{"name": null}
  - utter_slots_location_values
  - action_db_Place_Of_Submission_location		
* affirm										
  - email_form									
  - form{"name": "email_form"}
* cancel										
  - utter_cancel
  - action_deactivate_form  
  - form{"name": null}
  - utter_anything_else

## Place_Of_Submission-no mail path2
* Place_Of_Submission
  - action_db_Place_Of_Submission				
  - utter_location								
* affirm 
  - action_deactivate_form						
  - action_reset_all_slots  
  - location_form								
  - form{"name": "location_form"}
  - form{"name": null}
  - utter_slots_location_values
  - action_db_Place_Of_Submission_location		
* deny  										
  - action_deactivate_form
  - form{"name": null}
  - utter_anything_else
 
## Place_Of_Submission sad path
* Place_Of_Submission
  - action_db_Place_Of_Submission				
  - utter_location								
* deny
  - utter_anything_else

## Cost path
* Cost
  - action_db_cost	
  - utter_anything_else  

## CriterionRequirement happy path_1
* CriterionRequirement
  - action_db_CriterionRequirement				
* affirm 										
  - action_deactivate_form						
  - email_form									
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_accept_email
  - action_send_email							
  - utter_anything_else

## CriterionRequirement happy path_2
* CriterionRequirement
  - action_db_CriterionRequirement				
* affirm 										
  - action_deactivate_form						
  - email_form									
  - form{"name": "email_form"}
* cancel										
  - utter_cancel
  - action_deactivate_form  
  - form{"name": null}
  - utter_anything_else

## CriterionRequirement sad path
* CriterionRequirement
  - action_db_CriterionRequirement				
* deny											
  - utter_anything_else

## About path1
* About
  - action_db_about		
  - utter_about_details
* affirm
  - action_db_about_details
  - utter_anything_else  

## About path2
* About
  - action_db_about		
  - utter_about_details
* deny
  - utter_anything_else

  
## Cases_of_passport_issue path1_1
* Cases_of_passport_issue
  - action_db_cases_of_passport_issue			
  - utter_procedure_question					
* affirm
  - action_db_passport_issue_procedure			
* affirm										
  - action_deactivate_form						
  - email_form									
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_accept_email
  - action_send_email							
  - utter_anything_else

## Cases_of_passport_issue path1_2
* Cases_of_passport_issue
  - action_db_cases_of_passport_issue			
  - utter_procedure_question					
* affirm
  - action_db_passport_issue_procedure			
* affirm										
  - action_deactivate_form						
  - email_form									
  - form{"name": "email_form"}
* cancel										
  - utter_cancel
  - action_deactivate_form  
  - form{"name": null}
  - utter_anything_else

## Cases_of_passport_issue path2
* Cases_of_passport_issue
  - action_db_cases_of_passport_issue			
  - utter_procedure_question					
* affirm
  - action_db_passport_issue_procedure			
* deny											
  - utter_anything_else

## Cases_of_passport_issue path3
* Cases_of_passport_issue
  - action_db_cases_of_passport_issue			
  - utter_procedure_question					
* deny
  - utter_anything_else

## Passport_issue_procedure path1
* Passport_issue_procedure
  - action_db_passport_issue_procedure			
* affirm								 		
  - action_deactivate_form						
  - email_form									
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_accept_email
  - action_send_email							
  - utter_anything_else

## Passport_issue_procedure path2
* Passport_issue_procedure
  - action_db_passport_issue_procedure			
* deny											
  - utter_anything_else

## Duration_of_passport path
* Duration_of_passport
  - action_db_duration_of_passport				
  - utter_anything_else  

## Emergency_passport_issuance path
* Emergency_passport_issuance					
  - action_db_emergency_passport_issuance		
  - utter_anything_else  
  
## Loss_theft_of_passport path
* Loss_theft_of_passport						
  - action_db_loss_theft_of_passport			
  - utter_anything_else  
  
## passport_content path
* passport_content
  - action_db_passport_content					
  - utter_anything_else  
  
## cancellation_of_passport path
* cancellation_of_passport
  - action_db_cancellation_of_passport			
  - utter_anything_else  
  
## poreia_aithshs path
* poreia_aithshs
  - utter_poreia_aithshs						
  - utter_anything_else  
  
## legal_resource path
* legal_resource
  - action_db_legal_resource					
  - utter_anything_else  
  
## say goodbye happy path
* goodbye
  - utter_goodbye
  - utter_last_think  
  - utter_feedback								
* affirm										
  - action_db_feedback
  - utter_thanks

## say goodbye sad path
* goodbye
  - utter_goodbye		
  - utter_last_think    
  - utter_feedback
* deny											
  - action_db_feedback
  - utter_never_mind

## bot challenge
* bot_challenge
  - utter_iamabot								
  - utter_anything_else  

## HowAreYou path
* HowAreYou
  - utter_fine									
  - utter_anything_else  
  
## thanks happy path1
* thanks
  - utter_noworries
  - utter_your_opinion
* affirm			
  - utter_feedback
* affirm										
  - action_db_feedback
  - utter_thanks  
  - utter_anything_else

## thanks happy path2
* thanks
  - utter_noworries
  - utter_your_opinion
* affirm			
  - utter_feedback
* deny							
  - action_db_feedback
  - utter_never_mind
  - utter_anything_else
  
## thanks sad path
* thanks
  - utter_noworries
  - utter_your_opinion
* deny 
  - utter_anything_else  
  
## menu path
* menu											
  - utter_continue1
  
## e-paravolo path
* eparavolo
  - utter_eparavolo								
  - utter_anything_else

## passport_photo path
* passport_photo
  - utter_passport_photo						
  - utter_anything_else

## sunday path1_1
* Sunday_office
  - action_db_Sunday_office						
* affirm 										
  - action_deactivate_form						
  - email_form									
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_accept_email
  - action_send_email							
  - utter_anything_else

## sunday path1_2
* Sunday_office
  - action_db_Sunday_office						
* affirm 										
  - action_deactivate_form						
  - email_form									
  - form{"name": "email_form"}
* cancel										
  - utter_cancel
  - action_deactivate_form  
  - form{"name": null}
  - utter_anything_else

## sunday path1
* Sunday_office
  - action_db_Sunday_office						
* deny	 										
  - utter_anything_else


## evidence happy path1_1
* evidence
  - utter_evidence								
* affirm
  - utter_inform_evidence						
  - action_deactivate_form						
  - action_reset_all_slots
  - evidence_form
  - form{"name": "evidence_form"}
  - form{"name": null}
  - action_db_evidence
* affirm										
  - action_deactivate_form						
  - email_form									
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_accept_email
  - action_send_email							
  - utter_anything_else  

## evidence happy path1_2
* evidence
  - utter_evidence								
* affirm
  - utter_inform_evidence						
  - action_deactivate_form						
  - action_reset_all_slots
  - evidence_form
  - form{"name": "evidence_form"}
  - form{"name": null}
  - action_db_evidence
* affirm										
  - action_deactivate_form						
  - email_form									
  - form{"name": "email_form"}
* cancel										
  - utter_cancel
  - action_deactivate_form  
  - form{"name": null}
  - utter_anything_else  

## evidence happy path2
* evidence
  - utter_evidence								
* affirm
  - utter_inform_evidence
  - action_deactivate_form						
  - action_reset_all_slots  
  - evidence_form
  - form{"name": "evidence_form"}
  - form{"name": null}
  - action_db_evidence
  * deny											
  - utter_anything_else

## evidence sad path
* evidence
  - utter_evidence								
* deny
  - utter_anything_else
  
## evidence list path1_1
* evidence
  - utter_evidence								
* list_of_evidence
  - action_db_list_of_evidence					
  - utter_evidence1								
* affirm  
  - utter_inform_evidence
  - action_deactivate_form						
  - action_reset_all_slots
  - evidence_form
  - form{"name": "evidence_form"}
  - form{"name": null}
  - action_db_evidence
* affirm										
  - action_deactivate_form						
  - email_form									
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_accept_email
  - action_send_email							
  - utter_anything_else  

## evidence list path1_2
* evidence
  - utter_evidence								
* list_of_evidence
  - action_db_list_of_evidence					
  - utter_evidence1								
* affirm  
  - utter_inform_evidence
  - action_deactivate_form						
  - action_reset_all_slots
  - evidence_form
  - form{"name": "evidence_form"}
  - form{"name": null}
  - action_db_evidence
* affirm										
  - action_deactivate_form						
  - email_form									
  - form{"name": "email_form"}
* cancel										
  - utter_cancel
  - action_deactivate_form  
  - form{"name": null}
  - utter_anything_else

## evidence list path2
* evidence
  - utter_evidence								
* list_of_evidence
  - action_db_list_of_evidence					
  - utter_evidence1								
* affirm  
  - utter_inform_evidence
  - action_deactivate_form						
  - action_reset_all_slots  
  - evidence_form
  - form{"name": "evidence_form"}
  - form{"name": null}
  - action_db_evidence							
* deny											
  - utter_anything_else

## evidence list path3
* evidence
  - utter_evidence								
* list_of_evidence
  - action_db_list_of_evidence					
  - utter_evidence1								
* deny
  - utter_anything_else

## affirm or deny or cancel only path
* affirm OR deny OR cancel							
  - utter_affirm_deny_only

  