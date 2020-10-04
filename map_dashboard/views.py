from django.shortcuts import render
from .models import (AreaEn, Indicator,Tab1, Tab2, Tab3, Tab4, NiStDtbPoly)
from django.views.generic import TemplateView
from django.core import serializers
from django.core.serializers import serialize
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse




# Create your views here.
@csrf_exempt
def create_post(request):
			indicatorSelected = request.POST.get('indicator')
			tabSelected = request.POST.get('tab')
			areaSelected = request.POST.get('area')
			if tabSelected =='tab1':
				allData= Tab1.objects.all()
			elif tabSelected =='tab2':
				allData= Tab2.objects.all()
			elif tabSelected =="tab3":
				allData= Tab3.objects.all()	
			else:
				allData= Tab4.objects.all()	
			subgroup_list=allData.filter(Q(indicator_id=indicatorSelected) & Q(area_id=areaSelected)).values('subgroup_id','subgroup_name').distinct().order_by('subgroup_order')
			timeperiod_list=allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_order=1) & Q(area_id=areaSelected)).values('timeperiod_id','timeperiod').distinct().order_by('-timeperiod_id')
			timeperiodSelect= timeperiod_list[0].get('timeperiod_id')
			
			areaDetails=AreaEn.objects.filter(area_id=areaSelected).values('area_level','area_name')
			select_area_level = areaDetails[0].get('area_level')
			select_area_name = areaDetails[0].get('area_name')
			area_geodata =[]
			select_area_data = [] 
			if select_area_level == 2:
				area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=select_area_name),
                                geometry_field = 'wkb_geometry',
                                fields = ('id','st_name','dt_name'))
				select_area_data = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_parent_id=areaSelected)).only('area_name','area_code', 'data_value')

			elif select_area_level == 3:
				area_parentid =AreaEn.objects.filter(area_id=areaSelected).value('area_parent_id')
				area_parent_name= AreaEn.objects.filter(area_parent_id=area_parentid).value('area_name')
				area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=area_parent_name),
                                geometry_field = 'wkb_geometry',
                                fields = ('id','st_name','dt_name'))
				select_area_data = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_parent_id=area_parentid)).only('area_name','area_code', 'data_value')

			
			
			datalevel3 = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_level=3)).only('area_name','area_code', 'data_value')
			datalevel2 = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_level=2)).only('area_name','area_code', 'data_value')
			
			jsonSelectAreaData = serializers.serialize('json',select_area_data)
			jsondatalevel3 = serializers.serialize('json',datalevel3)
			jsondatalevel2 = serializers.serialize('json',datalevel2)

			context = {
            'data_level2': jsondatalevel2,
            'data_level3': jsondatalevel3,
			'select_area_data' : jsonSelectAreaData,
			'select_area_geodata' : area_geodata
			}

			return JsonResponse({'context': context, 'subresults': list(subgroup_list), 'timeresults': list(timeperiod_list ), 'area_level': select_area_level})	

@csrf_exempt
def create_post_area(request):
			indicatorSelected = request.POST.get('indicator')
			subgroupSelected = request.POST.get('subgroup')
			areaSelected = request.POST.get('area')
			tabSelected = request.POST.get('tab')
			if tabSelected =='tab1':
				allData= Tab1.objects.all()
			elif tabSelected =='tab2':
				allData= Tab2.objects.all()
			elif tabSelected =="tab3":
				allData= Tab3.objects.all()	
			else:
				allData= Tab4.objects.all()	
			
			timeperiod_list=allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_id=subgroupSelected) & Q(area_id=areaSelected)).values('timeperiod_id','timeperiod').distinct().order_by('-timeperiod_id')
			timeperiodSelect= timeperiod_list[0].get('timeperiod_id')
			areaDetails=AreaEn.objects.filter(area_id=areaSelected).values('area_level','area_name')
			select_area_level = areaDetails[0].get('area_level')
			select_area_name = areaDetails[0].get('area_name')
			area_geodata =[]
			select_area_data = [] 
			if select_area_level == 2:
				area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=select_area_name),
                                geometry_field = 'wkb_geometry',
                                fields = ('id','st_name','dt_name'))
				select_area_data = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_id=subgroupSelected) & Q(timeperiod_id=timeperiodSelect) & Q(area_parent_id=areaSelected)).only('area_name','area_code', 'data_value')

			elif select_area_level == 3:
				area_parentid =AreaEn.objects.filter(area_id=areaSelected).value('area_parent_id')
				area_parent_name= AreaEn.objects.filter(area_parent_id=area_parentid).value('area_name')
				area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=area_parent_name),
                                geometry_field = 'wkb_geometry',
                                fields = ('id','st_name','dt_name'))
				select_area_data = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_id=subgroupSelected) & Q(timeperiod_id=timeperiodSelect) & Q(area_parent_id=area_parentid)).only('area_name','area_code', 'data_value')

			datalevel3 = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_id=subgroupSelected) & Q(timeperiod_id=timeperiodSelect) & Q(area_level=3)).only('area_name','area_code', 'data_value')
			datalevel2 = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_id=subgroupSelected) & Q(timeperiod_id=timeperiodSelect) & Q(area_level=2)).only('area_name','area_code', 'data_value')
			
			jsonSelectAreaData = serializers.serialize('json',select_area_data)
			jsondatalevel3 = serializers.serialize('json',datalevel3)
			jsondatalevel2 = serializers.serialize('json',datalevel2)

			context = {
            'data_level2': jsondatalevel2,
            'data_level3': jsondatalevel3,
			'select_area_data' : jsonSelectAreaData,
			'select_area_geodata' : area_geodata
			}

			return JsonResponse({'context': context,  'timeresults': list(timeperiod_list), 'area_level': select_area_level })	



@csrf_exempt
def create_post_sub(request):
			indicatorSelected = request.POST.get('indicator')
			subgroupSelected = request.POST.get('subgroup')
			areaSelected = request.POST.get('area')
			tabSelected = request.POST.get('tab')
			if tabSelected =='tab1':
				allData= Tab1.objects.all()
			elif tabSelected =='tab2':
				allData= Tab2.objects.all()
			elif tabSelected =="tab3":
				allData= Tab3.objects.all()	
			else:
				allData= Tab4.objects.all()	

			timeperiod_list=allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_id=subgroupSelected) & Q(area_id=areaSelected)).values('timeperiod_id','timeperiod').distinct().order_by('-timeperiod_id')
			timeperiodSelect= timeperiod_list[0].get('timeperiod_id')
			areaDetails=AreaEn.objects.filter(area_id=areaSelected).values('area_level','area_name')
			select_area_level = areaDetails[0].get('area_level')
			select_area_name = areaDetails[0].get('area_name')
			area_geodata =[]
			select_area_data = [] 
			if select_area_level == 2:
				area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=select_area_name),
                                geometry_field = 'wkb_geometry',
                                fields = ('id','st_name','dt_name'))
				select_area_data = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_id=subgroupSelected) & Q(timeperiod_id=timeperiodSelect) & Q(area_parent_id=areaSelected)).only('area_name','area_code', 'data_value')

			elif select_area_level == 3:
				area_parentid =AreaEn.objects.filter(area_id=areaSelected).value('area_parent_id')
				area_parent_name= AreaEn.objects.filter(area_parent_id=area_parentid).value('area_name')
				area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=area_parent_name),
                                geometry_field = 'wkb_geometry',
                                fields = ('id','st_name','dt_name'))
				select_area_data = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_id=subgroupSelected) & Q(timeperiod_id=timeperiodSelect) & Q(area_parent_id=area_parentid)).only('area_name','area_code', 'data_value')



			datalevel3 = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_id=subgroupSelected) & Q(timeperiod_id=timeperiodSelect) & Q(area_level=3)).only('area_name','area_code', 'data_value')
			datalevel2 = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_id=subgroupSelected) & Q(timeperiod_id=timeperiodSelect) & Q(area_level=2)).only('area_name','area_code', 'data_value')
			
			jsonSelectAreaData = serializers.serialize('json',select_area_data)
			jsondatalevel3 = serializers.serialize('json',datalevel3)
			jsondatalevel2 = serializers.serialize('json',datalevel2)

			context = {
            'data_level2': jsondatalevel2,
            'data_level3': jsondatalevel3,
			'select_area_data' : jsonSelectAreaData,
			'select_area_geodata' : area_geodata
			}
			return JsonResponse({'context': context, 'timeresults': list(timeperiod_list), 'area_level': select_area_level })	

@csrf_exempt
def create_post_timeperiod(request):
			indicatorSelected = request.POST.get('indicator')
			subgroupSelected = request.POST.get('subgroup')
			timeperiodSelected = request.POST.get('timeperiod')
			areaSelected = request.POST.get('area')
			tabSelected = request.POST.get('tab')
			if tabSelected =='tab1':
				allData= Tab1.objects.all()
			elif tabSelected =='tab2':
				allData= Tab2.objects.all()
			elif tabSelected =="tab3":
				allData= Tab3.objects.all()	
			else:
				allData= Tab4.objects.all()	

			areaDetails=AreaEn.objects.filter(area_id=areaSelected).values('area_level','area_name')
			select_area_level = areaDetails[0].get('area_level')
			select_area_name = areaDetails[0].get('area_name')
			area_geodata =[]
			select_area_data = []

			datalevel3 = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_id=subgroupSelected) & Q(timeperiod_id=timeperiodSelected) & Q(area_level=3)).only('area_name','area_code', 'data_value')
			datalevel2 = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_id=subgroupSelected) & Q(timeperiod_id=timeperiodSelected) & Q(area_level=2)).only('area_name','area_code', 'data_value')
			if select_area_level == 2:
				area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=select_area_name),
                                geometry_field = 'wkb_geometry',
                                fields = ('id','st_name','dt_name'))
				select_area_data = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_id=subgroupSelected) & Q(timeperiod_id=timeperiodSelected) & Q(area_parent_id=areaSelected)).only('area_name','area_code', 'data_value')

			elif select_area_level == 3:
				area_parentid =AreaEn.objects.filter(area_id=areaSelected).value('area_parent_id')
				area_parent_name= AreaEn.objects.filter(area_parent_id=area_parentid).value('area_name')
				area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=area_parent_name),
                                geometry_field = 'wkb_geometry',
                                fields = ('id','st_name','dt_name'))
				select_area_data = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_id=subgroupSelected) & Q(timeperiod_id=timeperiodSelected) & Q(area_parent_id=area_parentid)).only('area_name','area_code', 'data_value')
			# print("in time period change")
			# print(datalevel2)
			jsondatalevel3 = serializers.serialize('json',datalevel3)
			jsondatalevel2 = serializers.serialize('json',datalevel2)
			jsonSelectAreaData = serializers.serialize('json', select_area_data)

			context = {
            'data_level2': jsondatalevel2,
            'data_level3': jsondatalevel3,
			'select_area_data' : jsonSelectAreaData,
			'select_area_geodata' : area_geodata
       		 }
			return JsonResponse({'context': context, 'area_level': select_area_level})	
		

class DashboardView(TemplateView):

	def get(self,request):
		allData= Tab1.objects.all()
		areaSelect = request.GET.get('area')
		indicator_list=Indicator.objects.all().filter(Q(classification=8)).order_by('indicator_order')
		area_list=AreaEn.objects.values('area_id', 'area_name')
		# print(area_list)
		area_geodata =[]
		select_area_data = []
		select_area_level = 1
		if(areaSelect != None):
			subgroup_list=allData.filter(Q(indicator_order=1) & Q(area_id=areaSelect)).values('subgroup_id','subgroup_name').distinct().order_by('subgroup_order')
			timeperiod_list=allData.filter(Q(indicator_order=1) & Q(subgroup_order=1) & Q(area_id=areaSelect)).values('timeperiod_id','timeperiod').distinct().order_by('-timeperiod_id')
			timeperiodSelect= timeperiod_list[0].get('timeperiod_id')
			areaDetails=AreaEn.objects.filter(area_id=areaSelect).values('area_level','area_name')
			select_area_level = areaDetails[0].get('area_level')
			select_area_name = areaDetails[0].get('area_name')
			if select_area_level == 2:
				area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=select_area_name),
									geometry_field = 'wkb_geometry',
									fields = ('id','st_name','dt_name'))
				select_area_data = allData.filter(Q(indicator_order=1) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_parent_id=areaSelect)).only('area_name','area_code', 'data_value')

			elif select_area_level == 3:
				area_parentid =AreaEn.objects.filter(area_id=areaSelect).value('area_parent_id')
				area_parent_name= AreaEn.objects.filter(area_parent_id=area_parentid).value('area_name')
				area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=area_parent_name),
									geometry_field = 'wkb_geometry',
									fields = ('id','st_name','dt_name'))
				select_area_data = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_parent_id=area_parentid)).only('area_name','area_code', 'data_value')
		else:
			subgroup_list=allData.filter(Q(indicator_order=1)).values('subgroup_id','subgroup_name').distinct().order_by('subgroup_order')
			timeperiod_list=allData.filter(Q(indicator_order=1) & Q(subgroup_order=1)).values('timeperiod_id','timeperiod').distinct().order_by('-timeperiod_id')
			timeperiodSelect= timeperiod_list[0].get('timeperiod_id')
		
		datalevel3 = allData.filter(Q(indicator_order=1) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_level=3)).only('area_name','area_code', 'data_value')
		datalevel2 = allData.filter(Q(indicator_order=1) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_level=2)).only('area_name','area_code', 'data_value')
		
		jsondatalevel3 = serializers.serialize('json',datalevel3)
		jsondatalevel2 = serializers.serialize('json',datalevel2)
		jsonSelectAreaData = serializers.serialize('json', select_area_data)

		context = {
            'data_level2': jsondatalevel2,
            'data_level3': jsondatalevel3,
			'select_area_data' : jsonSelectAreaData,
			'select_area_geodata' : area_geodata
        }
		return render(request,'map_dashboard/map.html', {'context':context, 'areaList': area_list ,'indicatorList': indicator_list,'subgroupList': subgroup_list, 'timeperiodList': timeperiod_list, 'area_level': select_area_level  })
	
class DashboardViewTab2(TemplateView):

	def get(self, request):
		areaSelect = request.GET.get('area')
		allData= Tab2.objects.all()
		indicator_list=Indicator.objects.all().filter(Q(classification=1)).order_by('indicator_order')
		subgroup_list=allData.filter(Q(indicator_order=1) & Q(area_id=areaSelect)).values('subgroup_id','subgroup_name').distinct().order_by('subgroup_order')
		timeperiod_list=allData.filter(Q(indicator_order=1) & Q(subgroup_order=1) & Q(area_id=areaSelect)).values('timeperiod_id','timeperiod').distinct().order_by('-timeperiod_id')
		timeperiodSelect= timeperiod_list[0].get('timeperiod_id')
		area_list=AreaEn.objects.values('area_id', 'area_name')
		areaDetails=AreaEn.objects.filter(area_id=areaSelect).values('area_level','area_name')
		select_area_level = areaDetails[0].get('area_level')
		select_area_name = areaDetails[0].get('area_name')
		area_geodata =[]
		select_area_data = [] 
		if select_area_level == 2:
			area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=select_area_name),
                                geometry_field = 'wkb_geometry',
                                fields = ('id','st_name','dt_name'))
			select_area_data = allData.filter(Q(indicator_order=1) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_parent_id=areaSelect)).only('area_name','area_code', 'data_value')

		elif select_area_level == 3:
			area_parentid =AreaEn.objects.filter(area_id=areaSelect).value('area_parent_id')
			area_parent_name= AreaEn.objects.filter(area_parent_id=area_parentid).value('area_name')
			area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=area_parent_name),
                                geometry_field = 'wkb_geometry',
                                fields = ('id','st_name','dt_name'))
			select_area_data = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_parent_id=area_parentid)).only('area_name','area_code', 'data_value')

		datalevel3 = allData.filter(Q(indicator_order=1) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_level=3)).only('area_name','area_code', 'data_value')
		datalevel2 = allData.filter(Q(indicator_order=1) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_level=2)).only('area_name','area_code', 'data_value')
		
		jsondatalevel3 = serializers.serialize('json',datalevel3)
		jsondatalevel2 = serializers.serialize('json',datalevel2)
		jsonSelectAreaData = serializers.serialize('json', select_area_data)

		context = {
            'data_level2': jsondatalevel2,
            'data_level3': jsondatalevel3,
			'select_area_data' : jsonSelectAreaData,
			'select_area_geodata' : area_geodata
        }
		return render(request,'map_dashboard/map-tab2.html', {'context':context, 'areaList': area_list, 'indicatorList': indicator_list,'subgroupList': subgroup_list, 'timeperiodList': timeperiod_list, 'area_level': select_area_level})

class DashboardViewTab3(TemplateView):

	def get(self,request):
		areaSelect = request.GET.get('area')
		allData= Tab3.objects.all()
		indicator_list=Indicator.objects.all().filter(Q(classification=3)).order_by('indicator_order')
		subgroup_list=allData.filter(Q(indicator_order=1)).values('subgroup_id','subgroup_name').distinct().order_by('subgroup_order')
		timeperiod_list=allData.filter(Q(indicator_order=1) & Q(subgroup_order=1)).values('timeperiod_id','timeperiod').distinct().order_by('-timeperiod_id')
		timeperiodSelect= timeperiod_list[0].get('timeperiod_id')
		area_list=AreaEn.objects.values('area_id', 'area_name')
		areaDetails=AreaEn.objects.filter(area_id=areaSelect).values('area_level','area_name')
		select_area_level = areaDetails[0].get('area_level')
		select_area_name = areaDetails[0].get('area_name')
		area_geodata =[]
		select_area_data = [] 
		if select_area_level == 2:
			area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=select_area_name),
                                geometry_field = 'wkb_geometry',
                                fields = ('id','st_name','dt_name'))
			select_area_data = allData.filter(Q(indicator_order=1) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_parent_id=areaSelect)).only('area_name','area_code', 'data_value')

		elif select_area_level == 3:
			area_parentid =AreaEn.objects.filter(area_id=areaSelect).value('area_parent_id')
			area_parent_name= AreaEn.objects.filter(area_parent_id=area_parentid).value('area_name')
			area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=area_parent_name),
                                geometry_field = 'wkb_geometry',
                                fields = ('id','st_name','dt_name'))
			select_area_data = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_parent_id=area_parentid)).only('area_name','area_code', 'data_value')
		
		datalevel3 = allData.filter(Q(indicator_order=1) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_level=3)).only('area_name','area_code', 'data_value')
		datalevel2 = allData.filter(Q(indicator_order=1) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_level=2)).only('area_name','area_code', 'data_value')
		
		jsondatalevel3 = serializers.serialize('json',datalevel3)
		jsondatalevel2 = serializers.serialize('json',datalevel2)
		jsonSelectAreaData = serializers.serialize('json', select_area_data)

		context = {
            'data_level2': jsondatalevel2,
            'data_level3': jsondatalevel3,
			'select_area_data' : jsonSelectAreaData,
			'select_area_geodata' : area_geodata
        }
		return render(request,'map_dashboard/map-tab3.html', {'context':context, 'areaList': area_list, 'indicatorList': indicator_list,'subgroupList': subgroup_list, 'timeperiodList': timeperiod_list, 'area_level': select_area_level })

class DashboardViewTab4(TemplateView):

	def get(self,request):
		areaSelect = request.GET.get('area')
		allData= Tab4.objects.all()
		indicator_list=Indicator.objects.all().filter(Q(classification=6)).order_by('indicator_order')
		subgroup_list=allData.filter(Q(indicator_order=1)).values('subgroup_id','subgroup_name').distinct().order_by('subgroup_order')
		timeperiod_list=allData.filter(Q(indicator_order=1) & Q(subgroup_order=1)).values('timeperiod_id','timeperiod').distinct().order_by('-timeperiod_id')
		timeperiodSelect= timeperiod_list[0].get('timeperiod_id')
		area_list=AreaEn.objects.values('area_id', 'area_name')
		areaDetails=AreaEn.objects.filter(area_id=areaSelect).values('area_level','area_name')
		select_area_level = areaDetails[0].get('area_level')
		select_area_name = areaDetails[0].get('area_name')
		area_geodata =[]
		select_area_data = [] 
		if select_area_level == 2:
			area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=select_area_name),
                                geometry_field = 'wkb_geometry',
                                fields = ('id','st_name','dt_name'))
			select_area_data = allData.filter(Q(indicator_order=1) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_parent_id=areaSelect)).only('area_name','area_code', 'data_value')

		elif select_area_level == 3:
			area_parentid =AreaEn.objects.filter(area_id=areaSelect).value('area_parent_id')
			area_parent_name= AreaEn.objects.filter(area_parent_id=area_parentid).value('area_name')
			area_geodata = serialize('geojson', NiStDtbPoly.objects.all().filter(st_name=area_parent_name),
                                geometry_field = 'wkb_geometry',
                                fields = ('id','st_name','dt_name'))
			select_area_data = allData.filter(Q(indicator_id=indicatorSelected) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_parent_id=area_parentid)).only('area_name','area_code', 'data_value')


		datalevel3 = allData.filter(Q(indicator_order=1) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_level=3)).only('area_name','area_code', 'data_value')
		datalevel2 = allData.filter(Q(indicator_order=1) & Q(subgroup_order=1) & Q(timeperiod_id=timeperiodSelect) & Q(area_level=2)).only('area_name','area_code', 'data_value')
		
		jsondatalevel3 = serializers.serialize('json',datalevel3)
		jsondatalevel2 = serializers.serialize('json',datalevel2)
		jsonSelectAreaData = serializers.serialize('json', select_area_data)

		context = {
            'data_level2': jsondatalevel2,
            'data_level3': jsondatalevel3,
			'select_area_data' : jsonSelectAreaData,
			'select_area_geodata' : area_geodata
        }
		return render(request,'map_dashboard/map-tab4.html', {'context':context, 'areaList': area_list, 'indicatorList': indicator_list,'subgroupList': subgroup_list, 'timeperiodList': timeperiod_list, 'area_level': select_area_level })