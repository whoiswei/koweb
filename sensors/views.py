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
    keys = [
        'mod1_dirs', 'mod2_keys', 'mod3_freq', 'mod4_rgb', 'mod5_morse',
        'mod6_knob_clicks', 'mod7_pwd', 'mod8_wires', 'mod9_switches', 'error_count'
    ]
    
    response_data = {}
    for key in keys:
        record = SensorData.objects.filter(topic=key).first()
        response_data[key] = record.value if record else "等待資料..."
        
    return JsonResponse(response_data)

def api_history_data(request):
    # Fetch all records for table as requested
    records = SensorData.objects.all()
    records_data = [
        {
            'topic': r.topic,
            'value': r.value,
            'timestamp': localtime(r.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        }
        for r in records
    ]
    
    # Fetch historical data for Chart.js
    # We only chart mod3_freq, mod6_knob_clicks, and error_count
    chart_topics = ['mod3_freq', 'mod6_knob_clicks', 'error_count']
    chart_records = SensorData.objects.filter(topic__in=chart_topics).order_by('timestamp')[:100]
    
    labels = []
    freq_data = []
    knob_data = []
    error_data = []
    
    # Simple mapping for chart data
    for r in chart_records:
        time_str = localtime(r.timestamp).strftime('%H:%M:%S')
        if time_str not in labels:
            labels.append(time_str)
            
    for label in labels:
        # Group by time label
        def get_val(topic_name):
            try:
                # Find the record matching the time and topic
                val_str = next((r.value for r in chart_records if localtime(r.timestamp).strftime('%H:%M:%S') == label and r.topic == topic_name), None)
                return float(val_str) if val_str is not None else None
            except ValueError:
                return None
                
        freq_data.append(get_val('mod3_freq'))
        knob_data.append(get_val('mod6_knob_clicks'))
        error_data.append(get_val('error_count'))

    return JsonResponse({
        'records': records_data,
        'chart_data': {
            'labels': labels,
            'mod3_freq': freq_data,
            'mod6_knob_clicks': knob_data,
            'error_count': error_data,
        }
    })
