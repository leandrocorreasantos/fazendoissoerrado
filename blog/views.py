from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Post
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .forms import ContatoForm
import smtplib
from django.contrib import messages
from django.core.mail import BadHeaderError
from fazendoissoerrado.settings import (
    CONTACT_EMAIL_BOX,
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    EMAIL_USE_SSL
)


# Create your views here.


def post_details(request, category, slug, pk):
    queryset = Post.objects.filter(
        published=True
    ).filter(
        published_date__lt=timezone.now()
    ).filter(pk=pk)
    post = get_object_or_404(queryset)
    keywords = post.taglist()
    ''' prevent counter view to repeat counter on update page '''
    last_post = request.session.get('LAST_POST', None)
    this_post = request.path
    if not last_post or this_post != last_post:
        ''' increment counter from post '''
        post.views += 1
        post.save()
        ''' remember the last post viewed '''
        request.session['LAST_POST'] = this_post

    return render(
        request,
        'blog/post_details.html',
        {'post': post, 'keywords': keywords}
    )


def post_list(request):
    page = request.GET.get('page', 1)
    post_search = Post.find()
    paginator = Paginator(post_search, 10)
    posts = paginator.get_page(page)

    return render(
        request,
        'blog/post_list.html',
        {'posts': posts}
    )


def post_by_category(request, category_slug):
    page = request.GET.get('page', 1)
    post_search = Post.objects.filter(
        published_date__lte=timezone.now()
    ).filter(
        published=True
    ).filter(
        category__slug=category_slug
    ).order_by('-published_date').all()

    paginator = Paginator(post_search, 10)
    posts = paginator.get_page(page)

    return render(
        request,
        'blog/post_list.html',
        {'posts': posts}
    )


def index(request):
    page = 1
    highlights = Post.find()[:3]
    post_search = Post.find()
    paginator = Paginator(post_search, 10)
    pagination = paginator.get_page(page)
    posts = pagination[3:]

    return render(
        request,
        'blog/index.html',
        {
            'posts': posts,
            'highlights': highlights,
            'pagination': pagination
        }
    )


def search(request):
    page = request.GET.get('page', 1)
    q = request.GET.get('q', None)
    if q:
        post_search = Post.objects.filter(
            published_date__lte=timezone.now()
        ).filter(published=True).filter(
            Q(title__icontains=q) |
            Q(subtitle__icontains=q) |
            Q(content__icontains=q)
        ).order_by('-published_date').all()

        paginator = Paginator(post_search, 10)
        posts = paginator.get_page(page)

        return render(
            request,
            'blog/search.html',
            {'posts': posts, 'q': q}
        )

    return redirect('/')


def tag(request, tag_name):
    page = request.GET.get('page', 1)
    post_search = Post.objects.filter(
        published_date__lte=timezone.now()
    ).filter(published=True).filter(
        tags__name__in=[tag_name]
    ).order_by('-published_date').all()

    if not post_search:
        return render(
            request,
            'blog/list_by_tag.html'
        )

    paginator = Paginator(post_search, 10)
    posts = paginator.get_page(page)

    return render(
        request,
        'blog/list_by_tag.html',
        {'posts': posts}
    )


def contato(request):
    assunto = 'Fazendo Isso Errado - Contato do Site'
    form = ContatoForm()
    if request.method == 'POST':
        if form.is_valid():
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            telefone = form.cleaned_data['telefone']
            msg = form.cleaned_data['mensagem']

            body_message = u"Nome: {}\nEmail: {}\nTelefone: {}\n\n{}".format(
                nome, email, telefone, msg
            )

            mensagem = u"\r\n".join((
                "From: %s" % EMAIL_HOST_USER,
                "To: %s" % CONTACT_EMAIL_BOX,
                "Subject: %s" % assunto,
                "Reply-To: %s" % email,
                "",
                body_message
            )).encode('utf-8')

            try:
                if EMAIL_USE_SSL is True:
                    smtp = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
                    smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
                else:
                    smtp = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
                    smtp.use_ehlo_or_helo_if_needed()

                smtp.sendmail(EMAIL_HOST_USER, [CONTACT_EMAIL_BOX], mensagem)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "E-mail enviado com sucesso!"
                )
                smtp.quit()
            except BadHeaderError:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Houve um erro ao enviar a mensagem (Bad Header)"
                )
            except Exception as e:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Houve um erro ao enviar a mensagem"
                )
                print(e)

    return render(request, 'blog/contato.html', {'form': form})
