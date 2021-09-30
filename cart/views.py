from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.template.loader import get_template
from .forms import CheckoutForm, ContactForm
from .models import Item, OrderItem, Order, Address, Personaldetails,Payment,Contact, CATEGORY_CHOICES
from django.views.decorators.csrf import csrf_exempt
from hashlib import sha512,sha256
from random import randint
from django.http import HttpResponse
from datetime import datetime, timedelta
import pytz
from django.core.paginator import Paginator
from django.utils import functional

#Homepage View
class ItemsView(ListView):
    model = Item
    template_name = 'home1.html'
    queryset = Item.objects.all()[:12]


    def get_context_data(self,*args,**kwargs):
        context = super(ItemsView,self).get_context_data(*args,**kwargs)
        categories = CATEGORY_CHOICES
        context['category_list'] = CATEGORY_CHOICES
        context['categories'] = categories
        return context

def baseview(request):
    categories = CATEGORY_CHOICES
    context = {
        'category_list':CATEGORY_CHOICES,
        'categories':categories
    }
    return render(request,'base.html',context)



class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'

    def get_context_data(self,**kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        similar_products = Item.objects.filter(category=self.object.category).exclude(slug = self.object.slug)[:4]
        context['similar_products'] = similar_products
        item = Item.objects.filter(slug = self.object.slug)
        for x in item:
            if x.quantity == 1:
                a=1
            else:
                a=None
        context['a'] = a
        return context

    def similarity(self):
        similar_products = Item.objects.filter(category=self.object.category).exclude(slug=self.object.slug)
        return similar_products

@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Now below we will check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            # order_item.quantity += 1
            # order_item.save()
            # messages.info(request, 'This item quantity was updated.')
            # return redirect('cart:product', slug=slug)
            messages.info(request,'This item was already present in your cart')
            return redirect('cart:other-items')
        else:
            order.items.add(order_item)
            messages.info(request, 'This item was added to your cart.')
            return redirect('cart:product', slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'This item was added to your cart.')
        return redirect('cart:product', slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user,
                                    ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Now below we will check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item =  OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, 'This item has been successfully removed from your cart.')
            return redirect('cart:order-summary')

        else:
            # add a message saying the order does not contain the order_item
            messages.info(request, 'This item was not in your cart.')
            return redirect('cart:product', slug=slug)

    else:
        # add a message saying the user does not have an order
        messages.info(request, 'Your cart is empty.')
        return redirect('cart:product', slug=slug)




#View to show order summary when clicked on cart

class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            for x in order.items.all():
                if x.item.quantity == 0:
                    order.items.remove(x)

            context = {
                'object':order,
            }
            return render(self.request, 'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Your Shopping cart is empty ')
            return render(self.request, 'order_summary.html')


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            for x in order.items.all():
                if x.item.quantity == 0:
                    order.items.remove(x)
            form = CheckoutForm()
            totality = order.get_total()


            context = {
                'form':form,
                'order':order,
                'totality':totality
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )

            if shipping_address_qs.exists():
                context.update({'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update({'default_billing_address': billing_address_qs[0]})

            return render(self.request,'checkout.html',context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have an active order')
            return redirect('cart:order-summary')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)


        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():
                firstname = form.cleaned_data.get('firstname')
                lastname = form.cleaned_data.get('lastname')
                mobile = form.cleaned_data.get('mobile')
                altmobile = form.cleaned_data.get('altmobile')
                email = form.cleaned_data.get('email')

                if is_valid_form([firstname,lastname,mobile]):
                    personal_details =Personaldetails(
                        user=self.request.user,
                        firstname = firstname,
                        lastname = lastname,
                        mobile = mobile,
                        altmobile = altmobile,
                        email = email
                    )
                    personal_details.save()
                    order.personal_details = personal_details
                    order.save()


                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        print(address_qs[0])
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(self.request, 'You do not have a saved shipping address')
                        return redirect('cart:checkout')
                else:
                    print('User is entering a new shipping address')
                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    City = form.cleaned_data.get('City')
                    State = form.cleaned_data.get('State')
                    shipping_Pincode = form.cleaned_data.get('shipping_Pincode')

                    if is_valid_form([shipping_address1,shipping_Pincode]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            City=City,
                            State=State,
                            Pincode=shipping_Pincode,
                            address_type='S'
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(self.request,'Please fill in the required address fields')

                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address = form.cleaned_data.get('same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print('Using the saved billing address')
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(self.request, 'You do not have a saved billing address')
                        return redirect('cart:checkout')
                else:
                    print('User is entering a new billing address')
                    billing_address1 = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    City = form.cleaned_data.get('City')
                    State = form.cleaned_data.get('State')
                    billing_Pincode = form.cleaned_data.get('billing_Pincode')

                    if is_valid_form([billing_address1, billing_Pincode]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            City=City,
                            State=State,
                            Pincode=billing_Pincode,
                            address_type='B'
                        )
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()
                    else:
                        messages.info(self.request, 'Billing address(Optional) is set empty')
                payment_option = form.cleaned_data.get('payment_option')
                # TODO: add redirect to the selected payment option
                return redirect('cart:payment')
            messages.warning(self.request, 'Checkout Failed')
            return redirect('cart:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, 'Your Shopping cart is empty ')
            return redirect('cart:order-summary')




# Page afer addresses in Checkout
class PaymentView(View):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            for x in order.items.all():
                if x.item.quantity == 0:
                    order.items.remove(x)
            user = self.request.user.id
            form = CheckoutForm()
            print('hihihi')
            key = settings.PAYU_MERCHANT_KEY
            service_provider = settings.SERVICE_PROVIDER
            email = self.request.user.email
            hash_object = sha256(str(randint(0, 9999)).encode("utf-8"))
            txnid = hash_object.hexdigest().lower()[0:20]
            salt = 'aqp5DZjgqS'
            productinfo = 'asasas'
            firstname = 'ddasdad'
            phone = '9898989898'
            amount = "%.2f" % order.get_total()
            x = float(amount)
            totality = x
            hash_string = key + "|" + txnid + "|" + str(totality) + "|" + productinfo + "|"
            hash_string += firstname + "|" + email + "|"
            hash_string += "||||||||||" + salt
            hash = sha512(hash_string.encode('utf-8')).hexdigest().lower()


            print(key)
            print(txnid)
            print("%.2f" % order.get_total())
            print(self.request.user.email)
            print(hash)

            context = {
                'form': form,
                'order': order,
                'user':user,
                'amount': amount,
                'key':key,
                'email': email,
                'txnid': txnid,
                'productinfo': productinfo,
                'surl': 'http://127.0.0.1:8000/payment_success',
                'hash': hash,
                'firstname': firstname,
                'phone': phone,
                'furl': 'http://127.0.0.1:8000/payment_failure',
                'service_provider': service_provider,
                'totality': totality,
            }
            if order.shipping_address:
                return render(self.request, 'payment.html', context)
            else:
                return redirect('cart:checkout')
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have an active order')
            return redirect('cart:order-summary')




# View to be redirected to if payment is successful
@csrf_exempt
def payment_success(request):
    print(dict(request.POST))
    salt = 'aqp5DZjgqS'
    status = request.POST.get('status')
    id = int(request.POST.get('address1'))
    email = request.POST.get('email')
    firstname = request.POST.get('firstname')
    productinfo = request.POST.get('productinfo')
    amount = request.POST.get('amount')
    txnid = request.POST.get('txnid')
    key = request.POST.get('key')
    ret_hash_string = salt + "|" + status + "|" + "||||||||||" + email + "|" + firstname + "|"
    ret_hash_string += productinfo + "|" + amount + "|"
    ret_hash_string += txnid + "|" + key
    ret_hash = sha512(ret_hash_string.encode('utf-8')).hexdigest().lower()
    order = Order.objects.get(user = id,ordered = False)

    for x in order.items.all():
        x.item.quantity = 0
        x.item.save()

    apartment = order.shipping_address.apartment_address
    street = order.shipping_address.street_address
    pincode = order.shipping_address.Pincode
    order_items = order.items.all()
    order_items.update(ordered = True)
    for item in order_items:
        item.save()
    order.txnid = txnid
    order.amount = amount
    a = float(amount)
    b = a-49
    totalamount = str(b)

    payment, created = Payment.objects.get_or_create(
        txnid='',
        paid=False
    )
    payment.txnid = txnid
    payment.amount = amount
    payment.date_of_payment = request.POST.get('addedon')
    payment.name_on_card = request.POST.get('name_on_card')
    payment.cardnumber = request.POST.get('cardnum')
    payment.bank_ref_num = request.POST.get('bank_ref_num')
    payment.bankcode = request.POST.get('bankcode')
    payment.status = request.POST.get('status')
    payment.mode = request.POST.get('mode')
    payment.pg_type = request.POST.get('PG_TYPE')
    payment.mihpayid = request.POST.get('mihpayid')
    payment.encryptedPaymentId = request.POST.get('encryptedPaymentId')
    payment.payuMoneyId = request.POST.get('payuMoneyId')




    payment.paid = True
    payment.save()


    order.ordered_date = datetime.now()
    order.ordered = True
    order.save()


    context = {
        'order':order,
        'txnid':txnid,
        'amount':amount,
        'totalamount':totalamount,
        'street': street,
        'apartment': apartment,
        'pincode': pincode
    }
    order_qs = Order.objects.filter(user=id,
                                    ordered=True)

    subject = 'Your SareeHouse order'
    from_email = 'Saree House <admin@sareehouseonline.com>'
    to_email = [email]
    with open(settings.BASE_DIR + '/templates/orderplaced.txt') as f:
        signup_message = f.read()
    message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email)
    html_template = get_template('orderplaced.html').render(context)
    message.attach_alternative(html_template, 'text/html')
    message.send()


    if ret_hash == request.POST['hash']:
        return render(request,'payment_success.html',context)
    else:
        return HttpResponse("Sorry, some error occurred. Transaction has failed. Please try again.If money has been deducted,"
                            "we will process full refund within a few days. Contact us for more information.")

# view to be redirected to if payment fails
@csrf_exempt
def payment_failure(request):
    return render(request,'payment_failure.html')





# View to be redirected to if user tries to increase quantity of item already present in cart
class other_items(ListView):
    template_name = 'other-items.html'
    context_object_name = 'items'
    model = Item


    # def get_context_data(self, **kwargs):
    #     context = super(other_items, self).get_context_data(**kwargs)
    #     context.update({
    #         'order_items':OrderItem.objects.all()
    #     })
    #     return context







#View for Allproducts page
class Allproducts(ListView):
    model = Item
    paginate_by = 12
    template_name = 'Allproducts.html'

    def get_context_data(self, **kwargs):
        context = super(Allproducts, self).get_context_data(**kwargs)
        context.update({
            'all_categories':CATEGORY_CHOICES
        })
        return context




def faqs(request):
    return render(request,'FAQs.html')



#Test views(Rough)

def Hometest(request):
    context = {
        'items':Item.objects.all()
    }
    return render(request, 'hometest.html', context)




# View products according to category on search

def search(request):
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        cats = q.capitalize()
        category_products = Item.objects.filter(category = q.capitalize())
        if cats == 'Nighties':
            size_filter_nighties = 'yes'
            size_filter_tops = None
        elif cats == 'Tops':
            size_filter_nighties = None
            size_filter_tops = 'yes'
        else:
            size_filter_nighties = None
            size_filter_tops = None

        context = {
            'cats':cats,
            'category_products':category_products,
            'all_categories': CATEGORY_CHOICES,
            'size_filter_nighties': size_filter_nighties,
            'size_filter_tops': size_filter_tops
        }

        if request.method == 'POST':
            Nsize = request.POST.get('nighties_size')
            Tsize = request.POST.get('tops_size')

            if Nsize:
                Nsize = 'Nighties-' + Nsize
                category_products = Item.objects.filter(category=cats, size=Nsize)
            else:
                Tsize = 'Top' + Tsize
                category_products = Item.objects.filter(category=cats, size=Tsize)

            params = {
                'cats': cats,
                'category_products': category_products,
                'all_categories': CATEGORY_CHOICES,
                'size_filter_nighties': size_filter_nighties,
                'size_filter_tops': size_filter_tops
            }
            return render(request, 'post_category.html', params)


    else:
        return redirect('cart:item-list')
    return render(request,'search_results.html',context)






# View products according to category on href


def CategoryView(request,cats):
    category_products = Item.objects.filter(category = cats)
    if cats == 'Nighties':
        size_filter_nighties = 'yes'
        size_filter_tops = None
    elif cats == 'Tops':
        size_filter_nighties = None
        size_filter_tops = 'yes'
    else:
        size_filter_nighties = None
        size_filter_tops = None

    context = {
        'cats':cats,
        'category_products':category_products,
        'all_categories':CATEGORY_CHOICES,
        'size_filter_nighties':size_filter_nighties,
        'size_filter_tops':size_filter_tops
    }

    if request.method == 'POST':
        Nsize = request.POST.get('nighties_size')
        Tsize = request.POST.get('tops_size')

        if Nsize:
            Nsize = 'Nighties-' + Nsize
            category_products = Item.objects.filter(category=cats, size=Nsize)
        else:
            Tsize = 'Top' + Tsize
            category_products = Item.objects.filter(category=cats, size=Tsize)


        params = {
            'cats':cats,
            'category_products':category_products,
            'all_categories':CATEGORY_CHOICES,
            'size_filter_nighties':size_filter_nighties,
            'size_filter_tops':size_filter_tops
        }
        return render(request,'post_category.html',params)


    return render(request,'post_category.html',context)



@login_required
def Order_tracking(request):
        try:
            orders = Order.objects.filter(user=request.user, ordered=True, delivered=False, cancelled = False)
            now = datetime.now()
            x = now.replace(tzinfo=pytz.UTC)

            for order in orders:
                a = x - order.ordered_date - timedelta(hours=5,minutes=30)
                days_passed = (a).days
                if days_passed >= 1:
                    order.days_since_order = None
                    order.save()
                else:
                    order.days_since_order = 0.5
                    order.save()

            context = {
                'orders': orders,
            }

            if request.method == 'POST':
                transactionid = request.POST.get('txnid')
                req_order = Order.objects.filter(user=request.user, ordered=True, delivered=False, txnid = transactionid)
                for order in req_order:
                    order.cancelled = True
                    order.save()
                return redirect('cart:order_tracking')


            return render(request, 'order_tracking.html',context)
        except ObjectDoesNotExist:
            messages.error(request, 'You do not have an active order')
            return redirect('cart:order_tracking')






# Contact page

class ContactView(View):
    def get(self, *args, **kwargs):
        form = ContactForm()
        context = {
            'form':form,
        }
        return render(self.request,'contact.html',context)

    def post(self, *args, **kwargs):
        form = ContactForm(self.request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')

            if is_valid_form([name, email, phone]):
                contact = Contact(
                    name=name,
                    email=email,
                    phone=phone,
                    subject=subject,
                    message=message
                )
                contact.save()

            return redirect('cart:contact_success')

        messages.warning(self.request, 'Please fill in the contact form correctly and try again')
        return redirect('cart:contact')



def contact_success(request):

    return render(request,'contact_success.html')

def tailoring(request):
    return render(request,'tailoring.html')


def about_us(request):
    return render(request,'about_us.html')