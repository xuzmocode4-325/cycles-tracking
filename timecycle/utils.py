import pandas as pd
import numpy as np
from math import pi
from datetime import datetime, timedelta
from .models import Activity, MetaCycle
from bokeh.io import show
from bokeh.embed import server_document, components
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.palettes import Category20c
from bokeh.models import Arrow, NormalHead


def get_today_tasks_dataframe(user):
    # Step 1: Get today's date and determine the current day
    today = datetime.now()
    current_day_name = today.strftime('%A').lower()  # e.g., 'monday'

    # Step 2: Get active time cycles.
    active_cycles = MetaCycle.objects.filter(frequency__name=current_day_name.title()).distinct()
  
    # Step 3: Retrieve all activities associated with those MetaCycles
    activities = Activity.objects.filter(
        meta_cycle__in=active_cycles,
    ).order_by('start_time')

    # Step 4: Determine gaps between tasks and create dummy tasks
    task_data = []
    previous_end_time = None

    
    for activity in activities:
        # Combine today's date with activity start and end times
        today_date = today.date()
        start_datetime = datetime.combine(today_date, activity.start_time)
        end_datetime = datetime.combine(today_date, activity.end_time)

        # Adjust for overnight activities
        if end_datetime < start_datetime:
            end_datetime += timedelta(days=1)  # Move end time to next day if it goes past midnight

        # Check for gaps between tasks
        if previous_end_time:
            gap_duration = (start_datetime - previous_end_time).total_seconds() / 60  # Gap in minutes
            if gap_duration > 0:
                # Create a dummy task for the gap
                dummy_task = {
                    'activity': 'No Task',
                    'duration': gap_duration,
                }
                task_data.append(dummy_task)

        # Append current activity data
        task_data.append({
            'activity': activity.name,
            'start_time': activity.start_time.strftime("%H:%M"),
            'end_time': activity.end_time.strftime("%H:%M"),
            'duration': (end_datetime - start_datetime).total_seconds() / 60,  # Calculate duration in minutes
        })

        # Update previous_end_time to the current activity's end time
        previous_end_time = end_datetime

    if task_data:
        df = pd.DataFrame(task_data)
        
        # Assign colors based on task data length or unique activities
        num_tasks = len(df)

        df['colors'] = Category20c[num_tasks]
        
        df['angle'] = (df['duration'] / df['duration'].sum()) * 2 * np.pi  # Calculate angle for pie chart representation
                
        p = figure(height=750, title=None, toolbar_location=None,
           tools="hover", tooltips="@activity: @start_time: @end_time", x_range=(-1.0, 1.0), 
           y_range=(-1.0, 1.0)
        )
        
        p.wedge(x=0, y=0, radius=0.75,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='colors', legend_field='activity', source=df)


        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

         # Calculate total duration of tasks in minutes
        total_duration = df['duration'].sum()

        # Get current time's position in minutes since midnight
        now_minutes = today.hour * 60 + today.minute + 15

        print(today.hour, today.minute)  

        # Calculate which segment of the pie this corresponds to based on total duration
        current_angle_position = (now_minutes / total_duration) * (2 * pi) if total_duration > 0 else 0
        
        # Calculate arrow start and end coordinates using trigonometry
        x_start = np.cos(current_angle_position) * 0.75   # Position at edge of pie chart (radius 1.0)
        y_start = np.sin(current_angle_position) * 0.75
        
        x_end = np.cos(current_angle_position) * 0.70     # Position at edge of pie chart (radius exactly 1)
        y_end = np.sin(current_angle_position) * 0.70
        
        nh = NormalHead(fill_color=df['colors'][0], fill_alpha=0.5, line_color=df['colors'][0])
        
        p.add_layout(Arrow(end=nh, line_color=df['colors'][0], line_dash=[15, 5],
                           x_start=x_start, y_start=y_start, x_end=x_end, y_end=y_end))

        # Return the script and div for embedding
        # Use components instead of server_document
        script, div = components(p)  # Get script and div for embedding              
        return script, div
        
    return None, None



