from django.shortcuts import render, redirect
from models import User, Poke
import bcrypt

def index(request):
	if ('errors' in request.session) and len(request.session['errors']):
		context = {'errors':request.session['errors']}
		request.session['errors'] = []
		return render(request, 'pokes/index.html', context)
	return render(request, 'pokes/index.html')


def register(request):
	if request.method == 'POST':
		request.session['errors'] = []
		if not User.userManager.namev(request.POST['name']):
			request.session['errors'].append('Name is NOT Valid.')
		if not User.userManager.namev(request.POST['alias']):
			request.session['errors'].append('Alias is NOT Valid.')
		if not User.userManager.email(request.POST['email']):
			request.session['errors'].append('Email address is NOT Valid.')
		if not User.userManager.password(request.POST['password']):
			request.session['errors'].append(
									'Password must be at least eight characters.')
		if not User.userManager.confirm(
								request.POST['password'], request.POST['confirm']):
			request.session['errors'].append(
								'Password and Confirm Password must be the same.')

		if len(request.session['errors']) == 0:
			passw = request.POST['password'].encode('utf-8')
			bpassw = bcrypt.hashpw(passw, bcrypt.gensalt())
			u =	User.userManager.create(name=request.POST['name'],
								alias=request.POST['alias'], email=request.POST['email'],
								password=bpassw)
			request.session['user'] = u.id
			return redirect('/pokes')
	return redirect('/')

def login(request):
	if request.method == 'POST':
		request.session['errors'] = []
		if not User.userManager.email(request.POST['email']):
			request.session['errors'].append('Email address is NOT Valid.')
		else:
			u = User.userManager.filter(email=request.POST['email'])
			if len(u):
				passw = request.POST['password'].encode('utf-8')
				if bcrypt.checkpw(passw, u[0].password.encode('utf-8')):
					request.session['user'] = u[0].id
					return redirect('/pokes')
				else:
					request.session['errors'].append('Incorrect password entered.')
			else:
				request.session['errors'].append('Email address not found')
	return redirect('/')

def pokes(request):
	# Some route protection. Won't render pokes.html if not logged in.
	if not 'user' in request.session:
		return redirect('/')

	ps = Poke.objects.filter(pokee__id=int(request.session['user']))
	pcount = {}
	for p in ps:
		if p.poker.id in pcount:
			pcount[p.poker.id] += 1
		else:
			pcount[p.poker.id] = 1

	psort = []
	while len(pcount) > 0:
		maxp = 0
		key = -1
		for k in pcount:
			if pcount[k] >= maxp:
				maxp = pcount[k]
				key = k
		u = User.userManager.get(id=key)
		psort.append((u.alias, maxp))
		pcount.pop(key)

	us = User.userManager.exclude(id=int(request.session['user']))
	ps = Poke.objects.all()
	users = []
	for u in us:
		count = 0
		for p in ps:
			if p.pokee.id == u.id:
				count += 1
		users.append((u, count))

	u = User.userManager.get(id=int(request.session['user']))
	context = {'alias':u.alias, 'pokes':psort, 'users':users}
	return render(request, 'pokes/pokes.html', context)

def poke(request):
	if request.method == 'POST':
		poker = User.userManager.get(id=int(request.session['user']))
		pokee = User.userManager.get(id=int(request.POST['uid']))
		Poke.objects.create(poker=poker, pokee=pokee)
	return redirect('/pokes')

def logout(request):
	request.session.pop('user', None)
	return redirect('/')
