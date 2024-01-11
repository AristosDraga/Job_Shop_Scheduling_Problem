import matplotlib.pyplot as plt

def spt_dispatching_rule(jobs):
    sorted_jobs = sorted(jobs, key=lambda x: x[2])
    return sorted_jobs

def read_instance(file_path):
    with open(file_path, 'r') as file:
        num_jobs = int(file.readline().strip())
        num_machines = int(file.readline().strip())

        # Skip the makespan for now
        _ = file.readline()

        operations = []

        for _ in range(num_jobs):
            operation_times = list(map(int, file.readline().split()))
            operations.append(operation_times)

        return num_jobs, num_machines, operations

def assign_jobs_to_machines(jobs_list, num_machines):
    schedule = {machine_id: [] for machine_id in range(1, num_machines + 1)}

    for job_id, machine_id, processing_time in jobs_list:
        schedule[machine_id].append((job_id, processing_time))

    return schedule

def plot_gantt_chart(schedule):
    fig, gnt = plt.subplots()

    # Setting Y-axis limits
    gnt.set_ylim(0, len(schedule) * 10 + 10)

    

    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Time (seconds)')
    gnt.set_ylabel('Processor')

    # Setting ticks on y-axis
    gnt.set_yticks([i * 10 + 5 for i in range(1, len(schedule) + 1)])
    # Labelling tickes of y-axis
    gnt.set_yticklabels([str(i) for i in range(1, len(schedule) + 1)])

    # Setting graph attribute
    gnt.grid(True)

    # Plotting the Gantt chart with different colors for each job
    colors = plt.cm.viridis.colors  # Use Viridis colormap
    total_processing_time = {machine_id: 0 for machine_id in schedule.keys()}

    for machine_id, machine_schedule in schedule.items():
        for i, (job_id, processing_time) in enumerate(machine_schedule):
            gnt.broken_barh([(total_processing_time[machine_id], processing_time)],
                            (machine_id * 10, 9), facecolors=colors[i % len(colors)])
            total_processing_time[machine_id] += processing_time

    plt.savefig("gantt_chart.png")
    plt.show()

# List of file paths.
file_paths = ['txt_files/la01.txt']

# Solve JSSP instances for each txt file.
for file_path in file_paths:
    num_jobs, num_machines, operations = read_instance(file_path)
    jobs_list = [(job_id, machine_id, processing_time) for job_id, processing_times in enumerate(operations, 1)
                 for machine_id, processing_time in enumerate(processing_times, 1)]
    result_order = spt_dispatching_rule(jobs_list)
    schedule = assign_jobs_to_machines(result_order, num_machines)
    plot_gantt_chart(schedule)
