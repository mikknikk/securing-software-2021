from django.shortcuts import render, redirect

from .models import questions

def find_topic(tid):
	for q in questions:
		if q['id'] == tid:
			return q
	return None


def quizView(request, tid):
	topic = find_topic(tid)

	request.session['level'] = 0
	request.session['old_level'] = -1
	request.session['tid'] = tid
	request.session['incorrect'] = 0
	request.session['finish'] = 0
	return render(request, 'pages/question.html', {'topic' : topic, 'question' : topic['questions'][0]})



def answerView(request, tid, aid):
	request.session['finish'] = 0

	if request.session['incorrect'] == 1:
		return redirect('/cheater/')

	if tid != request.session['tid']:
		return redirect('/cheater/')

	topic = find_topic(tid)

	level = request.session['level']
	old_level = request.session['old_level']
	
	if level != old_level + 1:
		return redirect('/cheater/')

	if topic['questions'][level]['correct'] == aid:
		old_level += 1
		request.session['old_level'] = old_level
		level += 1
		request.session['level'] = level
		if level == len(topic['questions']):
			request.session['finish'] = 1
			return redirect('/finish/')

		return render(request, 'pages/question.html', {'topic' : topic, 'question' : topic['questions'][level]})
	else:
		request.session['incorrect'] = 1
		return redirect('/incorrect/')


def incorrectView(request):
	return render(request, 'pages/incorrect.html')


def finishView(request):
	if 'finish' in request.session.keys() and request.session['finish'] == 1:
		return render(request, 'pages/finish.html')
	else:
		return redirect('/cheater/')


def cheaterView(request):
	return render(request, 'pages/cheater.html')


def thanksView(request):
	# Like we were going to pay anyone
	return render(request, 'pages/thanks.html')



def topicView(request, tid):
	topic = find_topic(tid)
	return render(request, 'pages/topic.html', {'topic' : topic})


def topicsView(request):
	return render(request, 'pages/topics.html', {'questions' : questions})
