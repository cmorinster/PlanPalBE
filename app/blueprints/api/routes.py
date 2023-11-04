from flask import jsonify, request
import requests
import os 
from app import db
from flask_cors import CORS, cross_origin
# import base64
# import requests
from app.blueprints.api import api
from app.blueprints.api.models import Event, Invitees, Questions, PollAnswers
from sqlalchemy import select, and_
from sqlalchemy import desc






# # Login - Get Token with Username/Password in header
# @api.route('/token', methods=['POST'])
# # @cross_origin
# @basic_auth.login_required
# def get_token():
#     user = basic_auth.current_user()
#     token = user.get_token()
#     return jsonify({'token': token})


# Create an event
@api.route('/event', methods=['POST'])
@cross_origin
def create_event():
    data = request.json
    # Validate the data
     # modeled data from front end:
        # data = { 'event':{creatorname:bleh,...},
        #         'questions':{'question1': {questiondate:blah, questiontime:bleh}, 'question2'...
        #   
        # }
    for field in ['creatorname', 'creatoremail', 'eventname', 'shareresults']:
        if field not in data['event']:
            return jsonify({'error': f"You are missing the {field} field"}), 400
    new_event = Event(**data['event'])
    new_event_dict = new_event.to_dict()
    print(new_event_dict['id'])
    # Grab the data from the request body
    count = 0 
   
    for question in data['questions']:
        print(data['questions'][question])
        for fieldq in ['questiondate', 'questiontime']:
            print('hi')
            if fieldq not in data['questions'][question]:
                return jsonify({'error': f"You are missing the {fieldq} field"}), 400
        count += 1
        data['questions'][question]['event_id'] = new_event_dict['id']
        new_question = Questions(**data['questions'][question])
        print(new_question.to_dict())

       


        # }
    print(count)

    # Check if the username or email already exists
    #user_exists = User.query.filter((User.username == username)|(User.email == email)).all()
    # if it is, return back to register
    #if user_exists:
        #return jsonify({'error': f"User with username {username} or email {email} already exists"}), 400

    # Create the new user
    # new_user = User(username=username, email=email, password=password)
    
    return jsonify(new_event_dict)

@api.route('/pollresults', methods=['POST'])
@cross_origin
def poll_results():
    data = request.json
    # data = {invitees:{inviteename:, inviteeemail:, eventid:}, pollanswers:{question1{questions_id:, answer:, invitees_id}, question2 {questionsid:,  answer:, invitees_id}
    for field in ['inviteename', 'inviteeemail', 'event_id']:
        if field not in data['invitees']:
            return jsonify({'error': f"You are missing the {field} field"}), 400
    new_invitee = Invitees(**data['invitees'])
    new_invitee_dict = new_invitee.to_dict()
    count = 0
    for answer in data['pollanswers']:
        for fielda in ['answer', 'questions_id']:
            if fielda not in data['pollanswers'][answer]:
                return jsonify({'error': f"You are missing the {fielda} field"}), 400
        count += 1
        data['pollanswers'][answer]['invitees_id'] = new_invitee_dict['id']
        new_answer = PollAnswers(**data['pollanswers'][answer])
    
    return "hello"





@api.route('/getresults/<int:event_id>/<string:share>')
@cross_origin
def get_results(event_id,share):

    #what do i need to return to react:
    #questiondates and question times, amount of answers for each(), who voted for what.
    # we having a page the admin and page the voters.  the page for the admin needs qds and qts, 
    #could be nice to have per person {questiondate, questionname, answers:{personA:answer}, {personB:answer}}
    #get all questions with eventID = blank. then get all answers to each question and get the corresponfing person 
    question_dict = {}
    allquestion_dict = {}
    event_dict = {}
    count = 0
    count_all = 0
    count_event = 0
    if share == "True":
        newshare= True
    else:
        newshare= False
    questions = db.session.execute(db.select(Questions.questiondate, Questions.questiontime, PollAnswers.answer, PollAnswers.invitees_id).where(and_((Questions.event_id == event_id), Questions.id == PollAnswers.questions_id))).all()
    for question in questions:
        row_dict = []
        inviteename = db.session.execute(db.select(Invitees.inviteename).where(Invitees.id == question[3])).first()
        row_dict = [question[0], question[1], question[2], inviteename[0]]
        question_dict[count] = row_dict
        count += 1

    allquestions = db.session.execute(db.select(Questions.questiondate, Questions.questiontime).where((Questions.event_id == event_id))).all()
    for all_question in allquestions:
        row_dict2 = [all_question[0], all_question[1]]
        allquestion_dict[count_all] = row_dict2
        count_all += 1

    eventinfo = db.session.execute(db.select(Event.creatorname, Event.creatoremail, Event.eventname, Event.shareresults, Event.polldescription).where((Event.id == event_id))).all()
    for event_item in eventinfo:
        row_dict3 = [event_item[0], event_item[1], event_item[2], event_item[3], event_item[4]]
        event_dict[count_event]= row_dict3
        count_event += 1

    q_a_merge = {}
    prevdate = ""
    if newshare == True:
        for q in allquestion_dict:

            answers = {}
            count_a_merge = 0
            q_date = allquestion_dict[q][0]
        
            if prevdate != q_date:
                q_a_merge[q_date]={}
            q_time = allquestion_dict[q][1]
            for a in question_dict:
                if (q_date == question_dict[a][0]) and (q_time ==  question_dict[a][1]):
                    answers[count_a_merge]= [question_dict[a][2], question_dict[a][3]]
                count_a_merge += 1    
            q_a_merge[q_date][q_time] = answers
            prevdate = q_date
            print('here')
    else:
        for q in allquestion_dict:
            print(q)
            q_date = allquestion_dict[q][0]
            q_time = allquestion_dict[q][1]
            print(q_time)
            print(prevdate)
            if prevdate !=q_date:
                time_list = []
            time_list.append(q_time)
            q_a_merge[q_date]= time_list
            print(q_a_merge)
            prevdate = q_date

    complete_dict = {
        "event": event_dict,
        "questions": q_a_merge
    }
    

    print((complete_dict))
    return((complete_dict))

#change to questions dict no matter what, newshare instead of share and the if share statement, allquestions section
#need to add event as well 
#we need the votes so that we can populate the bar and the circles and the number on the side. we need the event for the top section.  We need the questions and answers to populate the rest of the bottom section.  Only 
   
