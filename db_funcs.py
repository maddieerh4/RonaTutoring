import sqlite3

def requestTutoring(form):  # sourcery skip: merge-nested-ifs
    """
    userType
    lastName
    firstName
    location
    age
    grade
    availability
    marketingSource (if from other, then make this otherWay)
    studentContact
    parentContact
    math
    science
    english
    history
    compsci
    wantOther
    otherSubj
    specificClass
    additional
    ['id', 'userType', 'lastName', 'firstName', 'location', 'age', 'grade', 'availability', 
    'marketingSource', 'studentContact', 'parentContact', 'math', 'science', 'english', 
    'history', 'compsci', 'wantOther', 'otherSubj', 'specificClass', 'additional']
    """

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
        (len(form['lastName']) >= 1000) or (len(form['firstName']) >= 1000) or (len(form['location']) >= 1000)
        or (len(form['availability']) >= 4000) or (len(marketingSource) >= 1000) or (len(form['parentContact']) >= 400)
        or (len(form['specificClass']) >= 4000) 
    ):
        return

    # Open database
    conn = sqlite3.connect("ronatutoring.sqlite")
    c = conn.cursor()

    # Insert form data into database
    c.execute('''INSERT INTO users 
    (userType, lastName, firstName, location, age, grade, availability, marketingSource, studentContact, 
    parentContact, math, science, english, history, compsci, otherSubj, specificClass, additional)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
    (form['userType'], form['lastName'], form['firstName'], form['location'], age, grade, form['availability'], 
    marketingSource, studentContact, form['parentContact'], math, science, english, history, compsci, otherSubj, 
    form['specificClass'], additional))

    # Commit and close
    conn.commit()
    conn.close()