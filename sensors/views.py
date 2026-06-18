from django.shortcuts import render
from django.http import JsonResponse
from .models import SensorData
from django.utils.timezone import localtime

def index_view(request):
    context = {
        'name': '柯祐緯',
        'student_id': 'B11113036',
    }
    return render(request, 'sensors/index.html', context)

def api_latest_data(request):
    latest_temp = SensorData.objects.filter(topic__endswith='temperature').first()
    latest_hum = SensorData.objects.filter(topic__endswith='humidity').first()
    latest_light = SensorData.objects.filter(topic__endswith='light').first()
    
    return JsonResponse({
        'temperature': latest_temp.value if latest_temp else None,
        'humidity': latest_hum.value if latest_hum else None,
        'light': latest_light.value if latest_light else None,
    })

def api_history_data(request):
    # Fetch latest 20 records for table
    records = SensorData.objects.all()[:20]
    records_data = [
        {
            'topic': r.topic,
            'value': r.value,
            'timestamp': localtime(r.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        }
        for r in records
    ]
    
    # Fetch historical data for Chart.js (ascending order for charting)
    chart_records = SensorData.objects.all().order_by('timestamp')[:100]
    labels = []
    temp_data = []
    hum_data = []
    light_data = []
    
    # Simple mapping for chart data
    for r in chart_records:
        time_str = localtime(r.timestamp).strftime('%H:%M:%S')
        if time_str not in labels:
            labels.append(time_str)
            
    for label in labels:
        # Group by time label (approximate)
        temp_val = next((r.value for r in chart_records if localtime(r.timestamp).strftime('%H:%M:%S') == label and 'temperature' in r.topic), None)
        hum_val = next((r.value for r in chart_records if localtime(r.timestamp).strftime('%H:%M:%S') == label and 'humidity' in r.topic), None)
        light_val = next((r.value for r in chart_records if localtime(r.timestamp).strftime('%H:%M:%S') == label and 'light' in r.topic), None)
        
        temp_data.append(temp_val)
        hum_data.append(hum_val)
        light_data.append(light_val)

    return JsonResponse({
        'records': records_data,
        'chart_data': {
            'labels': labels,
            'temperature': temp_data,
            'humidity': hum_data,
            'light': light_data,
        }
    })
