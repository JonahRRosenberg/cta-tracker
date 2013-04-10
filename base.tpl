<html>
<head>
<!--<script type="text/javascript" src="jquery.js"></script>-->
<script>
</script>
<style>
</style>
</head>
<body>
<div>
<script type="text/javascript">
document.write('<form><input type=button value="Refresh" onClick="history.go()"></form>')
</script>
</div>

<p><span style="font-weight:bold;">Current Time:</span> {{current_time}}</p>
%for station in stations:
  %if station.stp_id in trains:
    <p><span style="font-weight:bold; color:red;">{{station.name}}</span>
      &nbsp;- Arrived: {{trains[station.stp_id].get_initialize_time()}}
      <span style="font-size:70%">
      &nbsp;&nbsp;
      %for stop_data in station.stop_data_list:
        %if not stop_data.is_dly:
          ({{stop_data.time_to_arrival()}} 
          Min{{('*' if stop_data.is_sch else '')}})
        %else:
          (Delayed)
        %end
        &nbsp;&nbsp;&nbsp;
      %end
      </span>
    </p>
  %else:
    %if len(station.stop_data_list) > 0:
      <p><span style="font-weight:bold;">{{station.name}}</span>
        &nbsp;- Predicted: {{station.stop_data_list[0].predicted_arrival_time()}}&nbsp;
        
        %if not station.stop_data_list[0].is_dly:
          ({{station.stop_data_list[0].time_to_arrival()}} 
          Min{{('*' if station.stop_data_list[0].is_sch else '')}})
        %else:
          (Delayed)
        %end
        <span style="font-size:70%">
        &nbsp;&nbsp;
        %for stop_data in station.stop_data_list[1:]:
          %if not stop_data.is_dly:
            ({{stop_data.time_to_arrival()}} 
            Min{{('*' if stop_data.is_sch else '')}})
          %else:
            (Delayed)
          %end
          &nbsp;&nbsp;&nbsp;
        %end
        </span>
      </p>
    %else:
      <p><span style="font-weight:bold;">{{station.name}}</span> - N/A</p>
    %end
  %end
%end
<br>
<div>
<script type="text/javascript">
document.write('<form><input type=button value="Refresh" onClick="history.go()"></form>')
</script>
</div>
</body>

</html>