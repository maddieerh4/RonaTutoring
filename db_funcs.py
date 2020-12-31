import sqlite3

# Constants
tellTutorToReact = '''
            
React to this message with an emoji of your choice if you're interested in taking this request. Our discord bot will reach out to those interested with more details.'''

def requestTutoring(form):
    # Preprocess form data
    marketingSource = form['marketingSource'] if (not form.get('otherWay')) else form.get('otherWay')
    age = int(form['age'])
    grade = int(form['grade'])
    studentContact = form.get('studentContact') or None
    math = 1 if form.get('math') else 0
    science = 1 if form.get('science') else 0
    english = 1 if form.get('english') else 0
    history = 1 if form.get('history') else 0
    compsci = 1 if form.get('compsci') else 0
    otherSubj = form.get('otherSubj') or None
    additional = form.get('additional') or None


    # Validate(ish) the form data and make sure that the database will accept the data without any problems
    # If not validated, then don't accept the form
    if studentContact:
        if len(studentContact) >= 400:
            return False
    if additional:
        if len(additional) >= 4000:
            return False
    if (
        (len(form['studentFullName']) >= 1000) or (len(form['parentFullName']) >= 1000) or (len(form['location']) >= 1000)
        or (len(form['availability']) >= 4000) or (len(marketingSource) >= 1000) or (len(form['parentContact']) >= 400)
        or (len(form['specificClass']) >= 4000) 
    ):
        return


    # Create message that will go into tutor-requests channel in discord server
    subjects = f"{'Math, ' if math else ''}{'Science, ' if science else ''}{'English, ' if english else ''}{'History, ' if history else ''}{'Computer Science, ' if compsci else ''}{otherSubj if otherSubj else ''}".strip()
    if subjects[-1] == ',': subjects = subjects[:-1]
    if additional:
        additionalPart = f'''
-----------------
Additional Information: {additional}'''
    else:
        additionalPart = ''
    
    discordMessage = f'''**Student from {form['location']} needs help with {subjects}**
-----------------
Grade: {grade}, Age: {age}
-----------------
Specific Class(es): {form['specificClass']}
-----------------
Availability: {form['availability']} {additionalPart}{tellTutorToReact}'''


    # Open database
    conn = sqlite3.connect("ronatutoring.sqlite")
    c = conn.cursor()

    # Insert form data into database
    c.execute('''INSERT INTO pending_requests 
    (studentFullName, parentFullName, location, age, grade, availability, marketingSource, studentContact, 
    parentContact, math, science, english, history, compsci, otherSubj, specificClass, additional, discordMessage)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
    (form['studentFullName'], form['parentFullName'], form['location'], age, grade, form['availability'], 
    marketingSource, studentContact, form['parentContact'], math, science, english, history, compsci, otherSubj, 
    form['specificClass'], additional, discordMessage))

    # Commit and close
    conn.commit()
    conn.close()