# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import Customer, Cart

# # def cart_view(request):
# #     # Assume that the customer is linked to the logged-in user or a session ID
# #     customer = None
# #     if request.user.is_authenticated:
# #         try:
# #             customer = Customer.objects.get(user=request.user)
# #         except Customer.DoesNotExist:
# #             messages.error(request, "Customer not found.")
# #             return redirect('login')  # Redirect to login page if customer is not found
# #     else:
# #         messages.error(request, "You need to be logged in to view the cart.")
# #         return redirect('login')  # Redirect to login page if the user is not authenticated

# #     # Fetch the cart items for the customer (assuming there is a Cart model)
# #     carts = Cart.objects.filter(customer=customer)
# #     total = sum(cart.amount for cart in carts)
# #     discount = total * 0.10  # Assuming 10% discount
# #     grand_total = total - discount

# #     # Render the cart template with the necessary context
# #     return render(request, 'cart.html', {
# #         'carts': carts,
# #         'total': total,
# #         'discount': discount,
# #         'grand_total': grand_total,
# #     })

# def products_view(request):
#     # Get all categories and brands
#     categories = Category.objects.all()
#     brands = Brand.objects.all()

#     # Get the selected brand ID from the query parameters
#     brand_id = request.GET.get('brand')

#     # Filter products by the selected brand
#     if brand_id:
#         products = Product.objects.filter(brand_id=brand_id)
#     else:
#         products = Product.objects.all()

#     # Pass context to the template
#     context = {
#         'categories': categories,
#         'brands': brands,
#         'products': products,
#     }

#     return render(request, 'your_template.html', context)
