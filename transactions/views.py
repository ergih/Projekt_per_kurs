from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
    PurchaseBill,
    Supplier,
    PurchaseItem,
    PurchaseBillDetails,
    SaleBill,
    SaleItem,
    SaleBillDetails,
    Costumer,
    Agent

)
from .forms import (
    SelectSupplierForm,
    PurchaseItemFormset,
    PurchaseDetailsForm,
    SupplierForm,
    SaleForm,
    SaleItemFormset,
    SaleDetailsForm,
    AgentForm,
    CostumerForm,
    # SelectAgentForm,
    # SelectCostumerForm,
    SelectCostumerForm
)
from inventory.models import Stock


class SupplierListView( ListView ):
    model = Supplier
    template_name = "suppliers/suppliers_list.html"
    queryset = Supplier.objects.filter( is_deleted=False )
    paginate_by = 10


# used to add a new supplier
class SupplierCreateView( SuccessMessageMixin, CreateView ):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transactions/suppliers'
    success_message = "Supplier has been created successfully"
    template_name = "suppliers/edit_supplier.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs )
        context["title"] = 'New Supplier'
        context["savebtn"] = 'Add Supplier'
        return context

    # used to update a supplier's info


class SupplierUpdateView( SuccessMessageMixin, UpdateView ):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transactions/suppliers'
    success_message = "Supplier details has been updated successfully"
    template_name = "suppliers/edit_supplier.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs )
        context["title"] = 'Edit Supplier'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Supplier'
        return context


# used to delete a supplier
class SupplierDeleteView( View ):
    template_name = "suppliers/delete_supplier.html"
    success_message = "Supplier has been deleted successfully"

    def get(self, request, pk):
        supplier = get_object_or_404( Supplier, pk=pk )
        return render( request, self.template_name, {'object': supplier} )

    def post(self, request, pk):
        supplier = get_object_or_404( Supplier, pk=pk )
        supplier.is_deleted = True
        supplier.save()
        messages.success( request, self.success_message )
        return redirect( 'suppliers-list' )


# used to view a supplier's profile
class SupplierView( View ):
    def get(self, request, name):
        supplierobj = get_object_or_404( Supplier, name=name )
        bill_list = PurchaseBill.objects.filter( supplier=supplierobj )
        page = request.GET.get( 'page', 1 )
        paginator = Paginator( bill_list, 10 )
        try:
            bills = paginator.page( page )
        except PageNotAnInteger:
            bills = paginator.page( 1 )
        except EmptyPage:
            bills = paginator.page( paginator.num_pages )
        context = {
            'supplier': supplierobj,
            'bills': bills
        }
        return render( request, 'suppliers/supplier.html', context )


class CostumerListView( ListView ):
    model = Costumer
    template_name = "costumer/costumer_list.html"
    queryset = Costumer.objects.filter( is_deleted=False, )
    paginate_by = 10


class CostumerCreateView( SuccessMessageMixin, CreateView ):
    model = Costumer
    form_class = CostumerForm
    success_url = '/transactions/costumer'
    success_message = "Costumer has been created successfully"
    template_name = "costumer/edit_costumer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs, )
        context["title"] = 'New Costumer'
        context["savebtn"] = 'Add Costumer'
        return context


# used to update a supplier's info
class CostumerUpdateView( SuccessMessageMixin, UpdateView ):
    model = Costumer
    form_class = CostumerForm
    success_url = '/transactions/costumer'
    success_message = "Costumer details has been updated successfully"
    template_name = "costumer/edit_costumer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs, )
        context["title"] = 'Edit Costumer'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Costumer'
        return context


# used to delete a supplier
class CostumerDeleteView( View ):
    template_name = "costumer/delete_costumer.html"
    success_message = "Costumer has been deleted successfully"

    def get(self, request, pk):
        costumer = get_object_or_404( Costumer, pk=pk )
        return render( request, self.template_name, {'object': costumer} )

    def post(self, request, pk):
        costumer = get_object_or_404( Costumer, pk=pk )
        costumer.is_deleted = True
        costumer.save()
        messages.success( request, self.success_message )
        return redirect( 'costumer-list' )


# used to view a supplier's profile
class CostumerView( View ):
    def get(self, request, name):
        costumerobj = get_object_or_404( Costumer, name=name )
        sale_bill = SaleBill.objects.filter( costumer=costumerobj )
        page = request.GET.get( 'page', 1 )
        paginator = Paginator( sale_bill, 10 )
        try:
            sales = paginator.page( page )
        except PageNotAnInteger:
            sales = paginator.page( 1 )
        except EmptyPage:
            sales = paginator.page( paginator.num_pages )
        context = {
            'costumer': costumerobj,
            'bills': sales
        }
        return render( request, 'costumer/costumer.html', context )


# shows the list of bills of all purchases
class PurchaseView( ListView ):
    model = PurchaseBill
    template_name = "purchases/purchases_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


class AgentListView( ListView ):
    model = Agent
    template_name = "agents/agents_list.html"
    queryset = Agent.objects.filter( is_deleted=False )
    paginate_by = 10


# used to add a new supplier
class AgentCreateView( SuccessMessageMixin, CreateView ):
    model = Agent
    form_class = AgentForm
    success_url = '/transactions/agents'
    success_message = "Agent has been created successfully"
    template_name = "agents/edit_agents.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs )
        context["title"] = 'New Agent'
        context["savebtn"] = 'Add Agent'
        return context

    # used to update a supplier's info


class AgentUpdateView( SuccessMessageMixin, UpdateView ):
    model = Agent
    form_class = AgentForm
    success_url = '/transactions/agents'
    success_message = "Agent details has been updated successfully"
    template_name = "agents/edit_agents.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs )
        context["title"] = 'Edit Agents'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Agent'
        return context


# used to delete a supplier
class AgentDeleteView( View ):
    template_name = "agents/delete_agents.html"
    success_message = "Agent has been deleted successfully"

    def get(self, request, pk):
        agent = get_object_or_404( Agent, pk=pk )
        return render( request, self.template_name, {'object': agent} )

    def post(self, request, pk):
        agent = get_object_or_404( Agent, pk=pk )
        agent.is_deleted = True
        agent.save()
        messages.success( request, self.success_message )
        return redirect( 'agent-list' )


# used to view a supplier's profile
class AgentView( View ):
    def get(self, request, name):
        agentobj = get_object_or_404( Agent, name=name )
        sale_bill = SaleBill.objects.filter( agent=agentobj )
        page = request.GET.get( 'page', 1 )
        paginator = Paginator( sale_bill, 10 )
        try:
            sales = paginator.page( page )
        except PageNotAnInteger:
            sales = paginator.page( 1 )
        except EmptyPage:
            sales = paginator.page( paginator.num_pages )
        context = {
            'agent': agentobj,
            'bills': sales
        }
        return render( request, 'agents/agents.html', context )


# shows the list of bills of all purchases
class PurchaseView( ListView ):
    model = PurchaseBill
    template_name = "purchases/purchases_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


# used to select the supplier
class SelectSupplierView( View ):
    form_class = SelectSupplierForm
    template_name = 'purchases/select_supplier.html'

    def get(self, request, *args, **kwargs):  # loads the form page
        form = self.form_class
        return render( request, self.template_name, {'form': form} )

    def post(self, request, *args, **kwargs):  # gets selected supplier and redirects to 'PurchaseCreateView' class
        form = self.form_class( request.POST )
        if form.is_valid():
            supplierid = request.POST.get( "supplier" )
            supplier = get_object_or_404( Supplier, id=supplierid )
            return redirect( 'new-purchase', supplier.pk )
        return render( request, self.template_name, {'form': form} )


# used to generate a bill object and save items
class PurchaseCreateView( View ):
    template_name = 'purchases/new_purchase.html'

    def get(self, request, pk):
        formset = PurchaseItemFormset( request.GET or None )  # renders an empty formset
        supplierobj = get_object_or_404( Supplier, pk=pk )  # gets the supplier object
        context = {
            'formset': formset,
            'supplier': supplierobj,
        }  # sends the supplier and formset as context
        return render( request, self.template_name, context )

    def post(self, request, pk):
        formset = PurchaseItemFormset( request.POST )  # recieves a post method for the formset
        supplierobj = get_object_or_404( Supplier, pk=pk )  # gets the supplier object
        if formset.is_valid():
            # saves bill
            billobj = PurchaseBill(
                supplier=supplierobj )  # a new object of class 'PurchaseBill' is created with supplier field set to 'supplierobj'
            billobj.save()  # saves object into the db
            # create bill details object
            billdetailsobj = PurchaseBillDetails( billno=billobj, supplier=supplierobj )
            billdetailsobj.save()
            for form in formset:  # for loop to save each individual form as its own object
                # false saves the item and links bill to the item
                billitem = form.save( commit=False )
                billitem.billno = billobj  # links the bill object to the items
                # gets the stock item
                stock = get_object_or_404( Stock, name=billitem.stock.name )  # gets the item
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                stock.quantity += billitem.quantity  # updates quantity
                # saves bill item and stock
                stock.save()
                billitem.save()
            messages.success( request, "Purchased items have been registered successfully" )
            return redirect( 'purchase-bill', billno=billobj.billno )
        formset = PurchaseItemFormset( request.GET or None )
        context = {
            'formset': formset,
            'supplier': supplierobj
        }
        return render( request, self.template_name, context )


# used to delete a bill object
class PurchaseDeleteView( SuccessMessageMixin, DeleteView ):
    model = PurchaseBill
    template_name = "purchases/delete_purchase.html"
    success_url = '/transactions/purchases'

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = PurchaseItem.objects.filter( billno=self.object.billno )
        for item in items:
            stock = get_object_or_404( Stock, name=item.stock.name )

            if stock.is_deleted == False:
                stock.quantity -= item.quantity
                stock.save()
        messages.success( self.request, "Purchase bill has been deleted successfully" )
        return super( PurchaseDeleteView, self ).delete( *args, **kwargs )


# shows the list of bills of all sales

# shows the list of bills of all purchases
class SaleView( ListView ):
    model = SaleBill
    template_name = "sales/sales_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


# used to select the supplier
class SelectCostumerView( View ):
    form_class = SelectCostumerForm
    template_name = 'sales/select_customer.html'

    def get(self, request, *args, **kwargs):  # loads the form page
        form = self.form_class
        return render( request, self.template_name, {'form': form} )

    def post(self, request, *args, **kwargs):  # gets selected supplier and redirects to 'PurchaseCreateView' class
        form = self.form_class( request.POST )
        if form.is_valid():
            costumerid = request.POST.get( "costumer" )
            costumer = get_object_or_404( Costumer, id=costumerid )
            return redirect( 'new-sale', costumer.pk )
        return render( request, self.template_name, {'form': form} )


# used to generate a bill object and save items
class SaleCreateView( View ):
    template_name = 'sales/new_sale.html'

    def get(self, request, pk):
        formset = SaleItemFormset( request.GET or None )
        costumerobj = get_object_or_404( Costumer, pk=pk )
        agent = costumerobj.agent
        context = {
            'formset': formset,
            'costumer': costumerobj,
            'agent': agent
        }
        return render( request, self.template_name, context )

    def post(self, request, pk):
        formset = SaleItemFormset( request.POST )
        costumerobj = get_object_or_404( Costumer, pk=pk )
        agent = costumerobj.agent
        if formset.is_valid():
            billobj = SaleBill( costumer=costumerobj, agent=agent )
            billobj.save()
            billdetailsobj = SaleBillDetails( billno=billobj, costumer=costumerobj, agent=agent )
            billdetailsobj.save()
            for form in formset:
                billitem = form.save( commit=False )
                billitem.billno = billobj
                stock = get_object_or_404( Stock, id=billitem.stock.id )
                billitem.totalprice = billitem.perprice * billitem.quantity
                stock.quantity -= billitem.quantity
                stock.save()
                billitem.save()
            messages.success( request, "Sold items have been registered successfully" )
            return redirect( 'sale-bill', billno=billobj.billno )
        form = SaleForm( request.GET or None )
        formset = SaleItemFormset( request.GET or None )
        context = {
            'form': form,
            'formset': formset,
        }
        return render( request, self.template_name, context )


# used to delete a bill object
class SaleDeleteView( SuccessMessageMixin, DeleteView ):
    model = SaleBill
    template_name = "sales/delete_sale.html"
    success_url = '/transactions/sales'

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = SaleItem.objects.filter( billno=self.object.billno )
        for item in items:
            stock = get_object_or_404( Stock, name=item.stock.name )
            if stock.is_deleted == False:
                stock.quantity += item.quantity
                stock.save()
        messages.success( self.request, "Sale bill has been deleted successfully" )
        return super( SaleDeleteView, self ).delete( *args, **kwargs )


# used to display the purchase bill object
class PurchaseBillView( View ):
    model = PurchaseBill
    template_name = "bill/purchase_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill': PurchaseBill.objects.get( billno=billno ),
            'items': PurchaseItem.objects.filter( billno=billno ),
            'billdetails': PurchaseBillDetails.objects.get( billno=billno ),
            'bill_base': self.bill_base,
        }
        return render( request, self.template_name, context )

    def post(self, request, billno):
        form = PurchaseDetailsForm( request.POST )
        if form.is_valid():
            billdetailsobj = PurchaseBillDetails.objects.get( billno=billno )

            billdetailsobj.eway = request.POST.get( "eway" )
            billdetailsobj.veh = request.POST.get( "veh" )
            billdetailsobj.destination = request.POST.get( "destination" )
            billdetailsobj.po = request.POST.get( "po" )
            billdetailsobj.cgst = request.POST.get( "cgst" )
            billdetailsobj.sgst = request.POST.get( "sgst" )
            billdetailsobj.igst = request.POST.get( "igst" )
            billdetailsobj.cess = request.POST.get( "cess" )
            billdetailsobj.tcs = request.POST.get( "tcs" )
            billdetailsobj.total = request.POST.get( "total" )

            billdetailsobj.save()
            messages.success( request, "Bill details have been modified successfully" )
        context = {
            'bill': PurchaseBill.objects.get( billno=billno ),
            'items': PurchaseItem.objects.filter( billno=billno ),
            'billdetails': PurchaseBillDetails.objects.get( billno=billno ),
            'bill_base': self.bill_base,
        }
        return render( request, self.template_name, context )


# used to display the sale bill object
class SaleBillView( View ):
    model = SaleBill
    template_name = "bill/sale_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill': SaleBill.objects.get( billno=billno ),
            'items': SaleItem.objects.filter( billno=billno ),
            'billdetails': SaleBillDetails.objects.get( billno=billno ),

            'bill_base': self.bill_base,

        }
        return render( request, self.template_name, context )

    def post(self, request, billno):
        form = SaleDetailsForm( request.POST )
        if form.is_valid():
            billdetailsobj = SaleBillDetails.objects.get( billno=billno )

            billdetailsobj.eway = request.POST.get( "eway" )
            billdetailsobj.veh = request.POST.get( "veh" )
            billdetailsobj.destination = request.POST.get( "destination" )
            billdetailsobj.po = request.POST.get( "po" )
            billdetailsobj.cgst = request.POST.get( "cgst" )
            billdetailsobj.sgst = request.POST.get( "sgst" )
            billdetailsobj.igst = request.POST.get( "igst" )
            billdetailsobj.cess = request.POST.get( "cess" )
            billdetailsobj.tcs = request.POST.get( "tcs" )
            billdetailsobj.total = request.POST.get( "total" )

            billdetailsobj.save()
            messages.success( request, "Bill details have been modified successfully" )
        context = {
            'bill': SaleBill.objects.get( billno=billno ),
            'items': SaleItem.objects.filter( billno=billno ),
            'billdetails': SaleBillDetails.objects.get( billno=billno ),
            'bill_base': self.bill_base,
        }
        return render( request, self.template_name, context )
