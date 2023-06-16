from datetime import datetime, timedelta
import math
import pandas as pd
    
    #tickvals_x = [0, 3, 6, 9, 12, 15, 18, 21, 24]

    #finding nearest value
    # nearest = 0
    # next = 0
    # for item in tickvals_x:
    #     currentHour = current_time_local_datetime.hour
    #     print(currentHour)
    #     if ( ((currentHour - item) >= 0) and ((currentHour - item - 3) < 0) ):
    #         nearest = item
    #         next = nearest + 3
    #         break
    # print(nearest)

    # tick = ((current_time_local_datetime.hour-nearest)*3600 + (current_time_local_datetime.minute*60))/3600
    # if tick > 2.0:
    #     pass

    # print(tick)
    # for i in range(0, len(tickvals_x)):
    #     tickvals_x[i] = tickvals_x[i] - (tick) + 2  
    
    # print(tickvals_x)

    # # timestamps_local = [(current_time_local_datetime+timedelta(hours=i)).hour for i in range(0, 24, 3)]
    # # timestamps_utc = [(current_time_utc_datetime+timedelta(hours=i)).hour for i in range(0, 24, 3)]
    # timestamps_local = []
    # timestamps_utc = []

    # to_24 = False
    # for i in range(0, 8):
    #     value = 0
    #     if to_24 == False:
    #         if len(timestamps_local) == 0 or timestamps_local[i-1] != 24:
    #             value = i*3
    #         else:
    #             to_24 = True
    #             continue
    #     else:
    #         val = 3
    #         while val != nearest:
    #             timestamps_local.append(val)
    #             val+= 3
    #         break

    #     timestamps_local.append(nearest+value)






    # fig.update_yaxes(
    #     tickformat=".1f", 
    #     title=None, 
    #     gridcolor="rgba(245,247,251,1.0)",
    #     gridwidth=2,
    #     tickvals=tickvals_y,
    #     ticktext=[f'{i} m  ' for i in tickvals_y],
    #     showgrid=True,
    #     tickmode='array',
    #     zeroline=False,
    #     fixedrange=True,
    # )

    # fig.update_xaxes(

    # )

    # fig.update_layout(
    #     xaxis=dict(
    #         tickvals=tickvals_x,
    #         ticktext=ticktext_x,
    #         range=[
    #             current_time_local_datetime-timedelta(hours=2), 
    #             current_time_local_datetime+timedelta(hours=24)
    #         ],
    #         tickmode='linear',
    #         dtick=timedelta(hours=3)
    #     )
    # )

            # mainBtn.style.color = "rgb(37, 150, 190)"
        # mainBtn.style.background = "white"
        # mainBtn.style.border = "solid rgb(37, 150, 190) 2px"
        # auxBtn.style.color = "black"
        # auxBtn.style.background = "rgba(245,247,251,1.0)"
        # auxBtn.style.border = "none"
        # auxBtn.disabled = false;
        # mainBtn.disabled = true;

                # pdfBtn.style.background = "white";
        # pdfBtn.style.color = "black";
        # auxBtn.style.background = "#091624";
        # mainBtn.style.background = "#091624";