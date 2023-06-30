from django.shortcuts import render
from django.http import JsonResponse


def index_page(request):

	data = {
		"status": 200,
		"message": "accepted"
	}

	return JsonResponse(data)