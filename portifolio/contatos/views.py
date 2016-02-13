from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from portifolio.contatos.forms import Contato


def contact(request):
    if request.method == 'POST':
        form = Contato(request.POST)

        if form.is_valid():
            body = render_to_string('contatos/contato.txt',
                                    form.cleaned_data)

            mail.send_mail('Contato feito pelo site',
                            body,
                            form.cleaned_data['email'],
                            ['contato@viniciusdamaceno.com.br'])

            messages.success(request, 'Mensagem enviada com sucesso!')

            return HttpResponseRedirect('/contato/')
        else:
            return render(request, 'contatos/contato.html',
                          {'form': form})

    else:
        context = {'form': Contato()}
        return render(request, 'contatos/contato.html', context)
