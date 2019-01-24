import time
import threading
import datetime
from django.shortcuts import render
from django_eventstream import get_current_event_id, send_event
from django.http import JsonResponse
import requests
import sseclient
import json
import collections

def _inmemory_live_test_scores_worker():
	url = "http://live-test-scores.herokuapp.com/scores"
	response = requests.get(url, stream = True)
	client = sseclient.SSEClient(response)

	for event in client.events():
		data = json.loads(event.data)
		global_live_test_scores[data["studentId"]].append([data["exam"], data["score"]])
		global_exams[data["exam"]].append([data["studentId"], data["score"]])
		send_event('test', 'score', data)

def students(request):
	studentList = {}
	studentList["studentList"] = [student for student, value in global_live_test_scores.items() if len(value) >= 1]
	return JsonResponse(studentList)

def studentTestScores(request, id):
	test_scores = {}
	test_scores["test_results"] = global_live_test_scores[id]
	test_scores["average_score"] = sum(test[1] for test in global_live_test_scores[id]) / len(global_live_test_scores[id])
	return JsonResponse(test_scores)

def exams(request):
	exams = {}
	exams["exams"] = list(global_exams.keys())
	return JsonResponse(exams)

def examScores(request, number):
	exam_scores = {}
	number = int(number)
	exam_scores["exam_results"] = global_exams[number]
	exam_scores["average_score"] = sum(exam[1] for exam in global_exams[number]) / len(global_exams[number])
	return JsonResponse(exam_scores)

global_live_test_scores = collections.defaultdict(list)
global_exams = collections.defaultdict(list)

inmemory_live_test_scores_thread = threading.Thread(target = _inmemory_live_test_scores_worker)
inmemory_live_test_scores_thread.daemon = True
inmemory_live_test_scores_thread.start()
