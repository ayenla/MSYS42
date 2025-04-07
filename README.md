————————————————————————————————————————————————————————————
As of April 7, 2025 8:00 PM - Iya
[TLDR]
• FIXED PHYSICIAN'S EXAM [Completed]
• Started Family Medical Records

[IMPORTANT]
• Added other field for PE- only 1 "other" field is allowed (not sure if this is right or if i should let them add as many other fields as needed)
• Created View Family Medical Records (View Family Members)
• Created Add Family Member Pop up(Functional- UI needs work) 
• Created View Family Medical Record
• Created Edit Family Medical Record (not functional- will result in an error if u try to save)


[MISCELLANEOUS]
• Fixed home page for physician's exams
• Fixed buttons for physician's exam and family medical records in view_cp
• Fixed Year List in PE to remove years with existing exams
• Added Labels for PE

————————————————————————————————————————————————————————————
As of April 7, 2025 2:24 AM - Robin
‼️STUFF ADDED‼️
[TLDR]
• Annual Medical History CRUD [Completed]
• Medical History CRUD [Completed]
• Search Child Profile[Completed]
[IMPORTANT]
• Fixed layoutting issues for Medical History sections 
• Added Clear Buttons to Medical History Section
• Added EDIT/DELETE functionality for Annual Medical Check section 
• Added SEARCH BAR functionality to home page
[MISCELLANEOUS]
• Added animation to navbar "Home" button
• Added animation to navbar section buttons
• Added "Others" checkbox to Allergies/Conditions portion in Medical History

———————————————————————————————————————————————————————————

————————————————————————————————————————————————————————————
As of March 24, 2025 2:24 AM - Robin
‼️STUFF ADDED‼️
• Programmed ADD/VIEW of Annual Medical Checks (general look)
• added back to list button when viewing a specific annual med check record
• Updated Navbar hyperlinking

———————————————————————————————————————————————————————————


As of March 24, 2025 7:38 PM - Iya
• [TLDR] create and view physician's exam are working but needs more refining

‼️STUFF THAT STILL NEEDS TO BE FIXED/ADDED‼️
• [CREATE PHYSICIANS EXAM] Input Fields for 'OTHERS' are not yet properly implemented (no field yet, no add/plus button yet)
• [CREATE PHYSICIANS EXAM] Select Year field lists all years from 1900 to current year. Years with existing physicians exams are not yet excluded.
• [HOME PHYSICIANS EXAM] Listing of all physician's exams are not styled yet (they're not in card form as seen in the figma. they are currently in a weird table form)
• [HOME PHYSICIANS EXAM] Not sure how to do the blurred view background for the year
• [VIEW PHYSICIANS EXAM] Edit button doesn't work yet
• [VIEW PHYSICIANS EXAM] Year is not properly formatted
• [NAVBAR] Fix the format
————————————————————————————————————————————————————————————
✨THINGS THAT DO WORK ✨
• [NAVBAR] Handles buttons for medical history and physician's exam
• [HOME PHYSICIANS EXAM] Lists the physician's exam for the selected child
• [HOME PHYSICIANS EXAM] Working Create Physicians Exam button
• [HOME PHYSICIANS EXAM] Working View Physician's Exam button
• [CREATE PHYSICIANS EXAM] Working Dropdowns for the fields
• [CREATE PHYSICIANS EXAM] Working save button
• [VIEW PHYSICIANS EXAM] You can view the saved physician's exam
• [ADMIN] You can view the saved physician's exam


————————————————————————————————————————————————————————————
As of March 24, 2025 2:24 AM - Robin
‼️STUFF THAT STILL NEEDS TO BE FIXED/ADDED‼️
• Input Fields for Create Medical History are short
• Update/Test form validations
• Formatting of checkboxes (make 3 columned if possible)
• Clear Button Under Each Section

————————————————————————————————————————————————————————————
• All dedicated/main features such as viewing and editing/adding has been added
• FEATURE NOT ADDED: Clear Button under each section




As of Mar 14, 2025  12:21 PM
‼️STUFF THAT STILL NEEDS TO BE FIXED‼️
• Models for Education
• Edit Child Profile (currently, the fields only display the values but save button does not work. Some fields don't display values at all)
• View Child Profile html Does not include education yet
• Create child profile error handling is not uniform 
• style.css doesnt work (idk why not)

————————————————————————————————————————————————————————————
‼️CURRENT FEATURES‼️
1) Upon start up, screen should show table of child profiles, a search field (does not work), and Create Child Profile Button
- Table of Child Profiles should show child info and view button
- Search Field does not work
- Query Button does not work

2) Clicking Create Child Profile button should lead to Create Child profile page. This should follow the Use Case Description for UC 01.
- Clicking Create should lead to home page with newly created child profile
TO FIX: unify the error handling 

3) Clicking View on a specific child profile will lead to View Profile Page
- Updated Nav Bar with Health buttons
- Child Information
- Health Buttons (beside child information)
- Education card with empty info
- Working Edit CHild Profile button

TO FIX: 
- Have health buttons working
- Fix Education Table

4) Clicking Edit Child Profile shows Edit Child Profile page with some fields occupied with SPC info 
TO FIX:
- some fields don't show proper information (Ex. Birthday, Guardian Relationship, Contact Numebrs)
- Edit Child Profile view does not work yet
