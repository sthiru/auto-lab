# Import micromotion controller
import pandas
from micromotion_controller import *
from osciloscope import *
from pandas import DataFrame
import matplotlib.pyplot as plt

# Initialize the controller
port = 'COM8'
controller = micromotion_controller(port)

# Initialize the osciloscope
scope = osciloscope()

# Move the controller to Home position
controller.speed(4000)
controller.move(150000, Direction.negative.value)

# Move the controller to the 11.0cm position
controller.move(110000, Direction.positive.value)
controller.speed(500)

# Move the motor by 50 microns and get scope data - store it in pandas df
step_size = 100
datax = []
datay = []
total_distance_cm = 2.0
total_distance_micro = total_distance_cm * 10000
total_steps = int(total_distance_micro / step_size)
channel_no = 3



try:
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # define line colors and legend
    ax.set_prop_cycle(color=['tab:blue', 'tab:orange', 'tab:green'])
    ax.legend(loc='upper right')
    ax.set_xlabel("Position")
    ax.set_ylabel("Volts")
    ax.set_title("AutoCorrelation Position vs Volts")

    for position in range(total_steps):
        controller.move(step_size, Direction.positive.value)
        y_max, y_min, avg = scope.get_min_max(channel_no)
        print(step_size * position, y_max, y_min, avg)
        datax.append([step_size*position])
        datay.append([y_max, y_min, avg])

        #Plot the data for each data point
        l1,l2,l3,=ax.plot(datax,datay[:])        
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()

# on prog break close scope and controller
except KeyboardInterrupt:
    print("Program interrupted. Saving data...")
    controller.close()
    dfx = DataFrame({'position': datax})
    dfy = DataFrame(datay, columns = ['y_max', 'y_min', 'avg'])
    pandas.concat([dfx, dfy], axis=1).to_csv(f'{time.time():.0f}.csv', index=False)
    plt.savefig(str(time.time()) + '.png')
    sys.exit()

finally:
    # Close the controller
    controller.close()
    print("Program finished. Saving data...")
    dfx = DataFrame({'position': datax})
    dfy = DataFrame(datay, columns = ['y_max', 'y_min', 'avg'])
    pandas.concat([dfx, dfy], axis=1).to_csv(f'{time.time():.0f}.csv', index=False)
    plt.savefig(str(time.time()) + '.png')

