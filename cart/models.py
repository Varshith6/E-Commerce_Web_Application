from django.conf import settings
from django.db import models
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('Sarees','Sarees'),
    ('Nighties','Nighties'),
    ('Dress materials','Dress materials'),
    ('Tops','Tops')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping')
)

SIZE_CHOICES = (
    ('Nighties-Regular','Nighties-Regular'),
    ('Nighties-XL','Nighties-XL'),
    ('Nighties-XXL','Nighties-XXL'),
    ('Top-S','Top-S'),
    ('Top-M','Top-M'),
    ('Top-L','Top-L'),
    ('Top-XL','Top-XL'),
    ('Top-XXL','Top-XXL'),
    ('Top-XXXL','Top-XXXL')
)


class Item(models.Model):
    title = models.CharField(max_length=100,unique=True)
    image_url = models.ImageField(upload_to='media/',blank=True,null=True)
    img2 = models.ImageField(upload_to='media/',blank=True,null=True)
    img3 = models.ImageField(upload_to='media/',blank=True,null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    size = models.CharField(choices=SIZE_CHOICES,max_length=30,blank=True,null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cart:product',kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('cart:add-to-cart',kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('cart:remove-from-cart',kwargs={
            'slug': self.slug
        })

    def get_CategoryView_url(self):
        return reverse('cart:category',kwargs={
            'cats':self.category
        })



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_final_price(self):
        if self.item.discount_price:
            return self.item.discount_price
        return self.item.price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('Address',related_name='billing_address', on_delete=models.SET_NULL,blank=True,null=True)
    shipping_address = models.ForeignKey('Address',related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    personal_details = models.ForeignKey('Personaldetails',related_name='personal_details',on_delete=models.SET_NULL, blank=True, null=True)
    txnid = models.CharField(max_length=100,default='',blank=True,null=True)
    cancelled = models.BooleanField(default=False)
    cancel_refunded = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    delivery_refunded = models.BooleanField(default=False)
    amount = models.CharField(max_length=100, default='', blank=True, null=True)
    days_since_order = models.FloatField(blank=True, null=True)




    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    apartment_address = models.CharField(max_length=255)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Pincode = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices= ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

class Personaldetails(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    altmobile = models.CharField(max_length=20,default='', blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Personal details'


class Payment(models.Model):
    txnid = models.CharField(max_length=100, default='', blank=True, null=True)
    amount = models.CharField(max_length=100, default='', blank=True, null=True)
    date_of_payment = models.CharField(max_length=100, default='', blank=True, null=True)
    name_on_card = models.CharField(max_length=100, default='', blank=True, null=True)
    cardnumber = models.CharField(max_length=100, default='', blank=True, null=True)
    bank_ref_num = models.CharField(max_length=100, default='', blank=True, null=True)
    bankcode = models.CharField(max_length=100, default='', blank=True, null=True)
    status = models.CharField(max_length=100, default='', blank=True, null=True)
    mode = models.CharField(max_length=100, default='', blank=True, null=True)
    pg_type = models.CharField(max_length=100, default='', blank=True, null=True)
    mihpayid = models.CharField(max_length=100, default='', blank=True, null=True)
    encryptedPaymentId = models.CharField(max_length=100, default='', blank=True, null=True)
    payuMoneyId = models.CharField(max_length=100, default='', blank=True, null=True)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Messages'