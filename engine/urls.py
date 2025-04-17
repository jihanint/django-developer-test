from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import custom_logout_view, module_list, install_module, uninstall_module, upgrade_module


urlpatterns = [
   # path('admin/', admin.site.urls),
    path('modules/', module_list, name='module_list'),
    path('modules/install/<int:module_id>/', install_module, name='install_module'),
    path('modules/uninstall/<int:module_id>/', uninstall_module, name='uninstall_module'),
    path('modules/upgrade/<int:module_id>/', upgrade_module, name='upgrade_module'),
    #path('modules/', include('engine.urls')),
    #path('product/', include('product_module.urls')),
    #path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    #path('logout/', custom_logout_view, name='logout'),
]
