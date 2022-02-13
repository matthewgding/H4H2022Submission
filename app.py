from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

# Global variables to track exception cases
inCountry = ""
noTrip = ""
knowEng = ""
knowHistGov = ""


# Implemented by Edmund Allen
@app.route("/")  # base routing, landing page with home screen
def index():
    return render_template("homeIndex.html")  # takes homeIndex.html and loads it on home page


# Implemented by Edmund Allen
@app.route("/about")  # /about url routes to aboutIndex.html
def about():
    return render_template("aboutIndex.html")


# Implemented by Edmund Allen
@app.route("/eligibility", methods=['GET', 'POST'])  # /eligibility with implemented button
def eligibility():
    if request.method == 'POST':
        if request.form.get('begin') == 'Begin Eligibility Test':
            return redirect(url_for('calcPage1'))
    return render_template("eligibilityIndex.html")  # eligibilityIndex.html gets loaded via the /eligibility route


# Implemented by Edmund Allen
@app.route("/resources")  # /resources routes to resourceIndex.html, has loaded navbar as well
def resources():
    return render_template("resourceIndex.html")


# Page with notification that the user is eligible for citizenship
# Implemented by Matthew Ding
@app.route('/eligible')
def eligible():
    return render_template('eligible.html')


# Page with notification that the user is not eligible for citizenship
# Implemented by Matthew Ding
@app.route('/ineligible')
def ineligible():
    return render_template('ineligible.html')


# First page of the eligibility test
# Implemented by Matthew Ding
@app.route('/calcPage1', methods=['GET', 'POST'])
def calcPage1():
    if request.method == 'POST':
        # Retrieve values from radio buttons on the page
        over18 = request.form.get('over18')
        permRes = request.form.get('permRes')
        resLength = request.form.get('resLength')
        if over18 == 'no' or permRes == 'no' or resLength == 'under3':
            # If a person does not meet all the above requirements, they are ineligible for citizenship
            return redirect(url_for('ineligible'))
        elif resLength == 'over3':
            # A person who has been a permanent resident between 3-5 years may continue under special conditions
            return redirect(url_for('calcPage2'))
        elif resLength == 'over5':
            # A person who has been a permanent resident for 5+ years may continue
            return redirect(url_for('calcPage3'))
    return render_template('calcPage1.html')


# Page with special conditions for people who have been permanent residents between 3-5 years
# Implemented by Matthew Ding
@app.route('/calcPage2', methods=['GET', 'POST'])
def calcPage2():
    if request.method == 'POST':
        # Retrieve values from radio buttons on the page
        spouseCit = request.form.get('spouseCit')
        marriageLen = request.form.get('marriageLen')
        spouseCitLen = request.form.get('spouseCitLen')
        inCountry = request.form.get('inCountry')
        if spouseCit == 'yes' and marriageLen == 'yes' and spouseCitLen == 'yes' and inCountry == 'yes':
            # A person who meets all these conditions may continue
            return redirect(url_for('calcPage3'))
        # A person who does not meet all the conditions is not eligible for citizenship
        return redirect(url_for('ineligible'))
    return render_template('calcPage2.html')


# Page for people who have met all the requirements on the first (and special conditions) page(s)
# Implemented by Edmund Allen and Matthew Ding
@app.route('/calcPage3', methods=['GET', 'POST'])
def calcPage3():
    global inCountry
    global noTrip
    global knowEng
    global knowHistGov
    if request.method == 'POST':
        # Retrieve the values from the radio buttons on the page
        inCountry = request.form.get('inCountry')
        noTrip = request.form.get('noTrip')
        livedState = request.form.get('livedState')
        knowEng = request.form.get('knowEng')
        knowHistGov = request.form.get('knowHistGov')
        if inCountry == 'no' and noTrip == 'no' and livedState == 'yes' and knowEng == 'yes' and knowHistGov == 'yes':
            # A person who appropriately meets all these requirements may continue
            return redirect(url_for('calcPage4'))
        elif inCountry == 'yes':
            return redirect(url_for('attachmentB'))
        elif noTrip == 'yes':
            return redirect(url_for('attachmentC'))
        elif knowEng == 'no':
            return redirect(url_for('attachmentD'))
        elif knowHistGov == 'no':
            return redirect(url_for('attachmentE'))
        # A person who does not meet all the requirements is not eligible
        return redirect(url_for('ineligible'))
    return render_template('calcPage3.html')


# Page for people who pass all base requirements (and special conditions)
# Implemented by Matthew Ding
@app.route('/calcPage4', methods=['GET', 'POST'])
def calcPage4():
    if request.method == 'POST':
        # Retrieve the values from the radio buttons on the page
        moral = request.form.get('moral')
        description = request.form.get('description')
        deserted = request.form.get('deserted')
        discharged = request.form.get('discharged')
        service = request.form.get('service')
        constitution = request.form.get('constitution')
        allegiance = request.form.get('allegiance')
        if (moral == 'yes' and description == 'yes' and deserted == 'no' and discharged == 'no' and service == 'yes'
                and constitution == 'yes' and allegiance == 'yes'):
            # A person who appropriately meets all these requirements may continue
            return redirect(url_for('eligible'))
        # A person who does not appropriately meet all the requirements is not eligible
        return redirect(url_for('ineligible'))
    return render_template('calcPage4.html')


# Page for people who were out of the country for 30+ months in a five-year span
# Implemented by Edmund Allen
@app.route('/attachmentB', methods=['GET', 'POST'])
def attachmentB():
    # Declaring our use of the following global variables
    global noTrip
    global knowEng
    global knowHistGov
    if request.method == 'POST':
        marinerStatus = request.form.get('marinerStatus')
        govWorker = request.form.get('govWorker')
        priestHood = request.form.get('priestHood')
        if marinerStatus == 'yes' or govWorker == 'yes' or priestHood == 'yes':
            # A person who appropriately meets all these requirements may continue
            if noTrip == 'yes':
                return redirect(url_for('attachmentC'))
            elif knowEng == 'no':
                return redirect(url_for('attachmentD'))
            elif knowHistGov == 'no':
                return redirect(url_for('attachmentE'))
            elif marinerStatus == 'yes' or govWorker == 'yes' or priestHood == 'yes':
                return redirect(url_for('calcPage4'))
        # A person who does not appropriately meet all the requirements is not eligible
        return redirect(url_for('ineligible'))
    return render_template('attachmentB.html')


# Page for people who went on a trip for longer than a year in a five-year span
# Implemented by Edmund Allen
@app.route('/attachmentC', methods=['GET', 'POST'])
def attachmentC():
    # Declaring our use of the following global variables
    global knowEng
    global knowHistGov
    if request.method == 'POST':
        filedAppNat = request.form.get('filedAppNat')
        if filedAppNat == 'yes':
            # A person who appropriately meets this requirement may continue
            if knowEng == 'no':
                return redirect(url_for('attachmentD'))
            elif knowHistGov == 'no':
                return redirect(url_for('attachmentE'))
            elif filedAppNat == 'yes':
                return redirect(url_for('calcPage4'))
        # A person who does not appropriately meet all the requirements is not eligible
        return redirect(url_for('ineligible'))
    return render_template('attachmentC.html')


# Page for people who cannot read, write, or speak basic English
# Implemented by Edmund Allen
@app.route('/attachmentD', methods=['GET', 'POST'])
def attachmentD():
    # Declaring our use of the following global variable
    global knowHistGov
    if request.method == 'POST':
        age50residency20 = request.form.get('age50residency20')
        age55residency15 = request.form.get('age55residency15')
        englishDisability = request.form.get('englishDisability')
        if age50residency20 == 'yes' or age55residency15 == 'yes' or englishDisability == 'yes':
            # A person who appropriately meets all these requirements may continue
            if knowHistGov == 'no':
                return redirect(url_for('attachmentE'))
            elif age50residency20 == 'yes' or age55residency15 == 'yes' or englishDisability == 'yes':
                return redirect(url_for('calcPage4'))
        # A person who does not appropriately meet all the requirements is not eligible
        return redirect(url_for('ineligible'))
    return render_template('attachmentD.html')


# Page for people who have a disability that prevent them from fulfilling the civics requirement
# Implemented by Edmund Allen
@app.route('/attachmentE', methods=['GET', 'POST'])
def attachmentE():
    if request.method == 'POST':
        civicDisability = request.form.get('civicDisability')
        if civicDisability == 'yes':
            # A person who appropriately meets this requirement may continue to the final page
            return redirect(url_for('calcPage4'))
        return redirect(url_for('ineligible'))
    return render_template('attachmentE.html')


@app.route('/acquisition')
def acquisition():
    return render_template("acquisition.html")


@app.route('/derivation')
def derivation():
    return render_template("derivation.html")

@app.route('/naturalization')
def naturalization():
    return render_template("naturalization.html")

if __name__ == "__main__":  # runs app through main
    app.run()
