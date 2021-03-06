from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import ListView
from boxes.forms import SingleArchiveForm, BatchArchiveForm, ArchiveForm, ListForm, Batch2Form
from boxes.models import Box, BoxItem
from accounts.models import Account, Settings

@login_required()
def Single(request):

    donor_id_accounts = Settings.objects.filter(require_donor_id=True)

    if request.method == 'POST':
        form = SingleArchiveForm(request.POST)
        if form.is_valid():
            # Get form data
            account = form.cleaned_data['account']

            # Add the accession to an array for the next view (/archive/) to process
            accession = list()
            accession.append(form.cleaned_data['accession'])

            # Begin new session
            #request.session.flush()
            request.session['accessions'] = accession
            request.session['count'] = 0
            request.session['account'] = account
            request.session['type'] = 'single'

            # Redirect for archiving accessions
            return HttpResponseRedirect('/archive/')
        else:
            print form.errors
            return render_to_response('singlearchive.html', {'form': form}, context_instance=RequestContext(request))

    else:
        form = SingleArchiveForm()
        context = {'form': form,
                   'donor_id_accounts': donor_id_accounts}
        return render_to_response('singlearchive.html', context, context_instance=RequestContext(request))

@login_required
def Batch(request):
    if request.method == 'POST':
        form = BatchArchiveForm(request.POST)
        if form.is_valid():
            # Get form data
            account = form.cleaned_data['account']
            accessions_string = form.cleaned_data['accessions']

            # Split accessions by newline characters
            accessions_list = accessions_string.split('\r\n')

            # Remove empty accession items
            accessions_list = filter(None, accessions_list)
            accessions_list = list(accessions_list)

            # Begin new session
            #request.session.flush()
            request.session['accessions'] = accessions_list
            request.session['count'] = 0
            request.session['account'] = account
            request.session['type'] = 'batch'

            # Redirect for archiving accessions
            return HttpResponseRedirect('/archive/')
        else:
            return render_to_response('batcharchive.html', {'form': form}, context_instance=RequestContext(request))

    else:
        form = BatchArchiveForm()
        context = {'form': form,
                   'usertest': request.user.employee.employee_id }

        # Anytime this page is loaded, clear session variables
        #request.session.flush()

        return render_to_response('batcharchive.html', context, context_instance=RequestContext(request))

def Archive(request):
    # Get accession variable from session object
    account = request.session.get('account')
    accessions = request.session.get('accessions')

    # Check if account requires donor id
    settings = account.settings()
    require_donor_id = settings.require_donor_id

    if request.method == 'POST':
        form = ArchiveForm(request.POST)

        # Require donor ID if necessary
        if require_donor_id:
            form.fields['donor_id'].required = True

        if form.is_valid():

            # Add 1 to session count after each submission
            request.session['count'] += 1

            accession = accessions[request.session['count']-1]
            serum = int(form.cleaned_data['serum'])
            plasma = int(form.cleaned_data['plasma'])
            user = request.user.employee.employee_id

            # Add donor id if required
            if require_donor_id:
                donor_id = form.cleaned_data['donor_id']
            else:
                donor_id = None

            account.append(user, serum, plasma, accession, donor_id)
        else:
            context = {'accession': accessions[request.session['count']],
                       'count': request.session['count'],
                       'require_donor_id': require_donor_id,
                       'form': form}
            return render_to_response('archive.html', context, context_instance=RequestContext(request))

    # Redirect to batch_archive when finished
    if request.session['count'] == len(accessions):

        # Get latest box number for redirect
        box = Box.objects.filter(account=account).latest('number').number

        # Redirect to the single archive form if necessary
        if request.session.get('type') == 'single':
            return HttpResponseRedirect('/single/')

        return HttpResponseRedirect(view_url(account.slug, box))

    # Form variables
    form = ArchiveForm()
    context = {'accession': accessions[request.session['count']],
               'count': request.session['count'],
               'require_donor_id': require_donor_id,
               'form': form}

    return render_to_response('archive.html', context, context_instance=RequestContext(request))

@login_required()
def BoxList(request):
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            box_number = form.cleaned_data['number']

            return HttpResponseRedirect(view_url(account.slug, box_number))

    form = ListForm()
    context = { 'form' : form }

    return render_to_response('list_choice.html', context, context_instance=RequestContext(request))

class BoxListView(ListView):

    context_object_name = 'box_list'
    template_name = 'boxes/boxitem_list.html'

    def get_queryset(self):

        self.account = get_object_or_404(Account, slug=self.kwargs['slug'])
        self.settings = Settings.objects.get(account_id=self.account.id)
        self.box = get_object_or_404(Box, account=self.account, number=self.kwargs['box_number'])

        return BoxItem.objects.filter(box=self.box)

    def get_context_data(self, **kwargs):

        context = super(BoxListView, self).get_context_data(**kwargs)
        context['account'] = self.account
        context['box_number'] = self.box.number
        if self.settings.require_donor_id:
            context['donor_id'] = True

        return context

def view_url(account_slug, box_number):
    return '/view/' + str(account_slug) + '/' + str(box_number) + '/'

@login_required()
def Archive2(request):
    if request.method == 'POST':
        form = Batch2Form(request.POST)
        if form.is_valid():
            # Get form data
            account = form.cleaned_data['account']
            accessions_list = request.POST.getlist('accessions')

            # Split accessions by newline characters
            #accessions_list = accessions_string.split('\r\n')

            # Remove empty accession items
            accessions_list = filter(None, accessions_list)
            #accessions_list = list(accessions_list)

            # Begin new session
            #request.session.flush()
            request.session['accessions'] = accessions_list
            request.session['count'] = 0
            request.session['account'] = account
            request.session['type'] = 'batch'

            # Redirect for archiving accessions
            return HttpResponseRedirect('/archive/')
        else:
            print "errors: " + form.errors
            return render_to_response('archive2.html', context_instance=RequestContext(request))

    else:
        form = BatchArchiveForm()
        context = {'form': form,
                   'usertest': request.user.employee.employee_id }

        # Anytime this page is loaded, clear session variables
        #request.session.flush()

        return render_to_response('batcharchive.html', context, context_instance=RequestContext(request))

@login_required()
def Batch2(request):
    if request.method == 'POST':
        form = Batch2Form(request.POST)
        if not request.POST.getlist('accessions'):
            form = Batch2Form
            is_empty = True
            context = {'form' : form,
                       'is_empty' : is_empty}
            return render_to_response('archive2.html', context, context_instance=RequestContext(request))
        elif form.is_valid():
            # Get form data
            account = form.cleaned_data['account']
            accessions_list = request.POST.getlist('accessions')

            # Split accessions by newline characters
            #accessions_list = accessions_string.split('\r\n')

            # Remove empty accession items
            accessions_list = filter(None, accessions_list)
            #accessions_list = list(accessions_list)

            # Begin new session
            #request.session.flush()
            request.session['accessions'] = accessions_list
            request.session['count'] = 0
            request.session['account'] = account
            request.session['type'] = 'batch'

            # Redirect for archiving accessions
            return HttpResponseRedirect('/archive/')
        else:
            # Reload accession data
            accessions_list = request.POST.getlist('accessions')
            accessions_list = filter(None, accessions_list)
            context = { 'form': form,
                        'accessions': accessions_list}

            return render_to_response('archive2.html', context, context_instance=RequestContext(request))
    else:
        form = Batch2Form()
        return render_to_response('archive2.html', {'form': form}, context_instance=RequestContext(request))