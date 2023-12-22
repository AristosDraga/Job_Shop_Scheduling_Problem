from mip import Model, xsum, BINARY
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def spt_dispatching_rule(jobs):
    sorted_jobs = sorted(jobs, key=lambda x: x[1])
    return [job[0] for job in sorted_jobs]


def plot_gantt(result_order, num_machines):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    fig, ax = plt.subplots(figsize=(10, 6))
    patches = []

    model = Model()

    start_times = [0] * num_machines

    for job_id, processing_time in result_order:
        machine_id = job_id  # Assign each job to a separate machine
        processing_time = 3  # Update processing time based on your data

        machine_index = machine_id - 1

        if machine_index < len(start_times):
            start_time = start_times[machine_index]
            end_time = start_time + processing_time

            color = colors[machine_index % len(colors)]

            rect = mpatches.Rectangle((start_time, machine_id - 0.4),
                                      end_time - start_time, 0.8, color=color, label=f'Machine {machine_id}')
            patches.append(rect)
            ax.text((start_time + end_time) / 2, machine_id, f'Job {job_id}', ha='center', va='center', color='white')

            # Update start times for the next iteration
            start_times[machine_index] = end_time
        else:
            print(f"Machine {machine_id} not initialized properly in start_times. "
                  f"Num Machines: {num_machines}, Length of Start Times: {len(start_times)}")


    ax.set_xlabel('Time')
    ax.set_yticks(range(1, num_machines + 1))
    ax.set_yticklabels([f'Machine {i}' for i in range(1, num_machines + 1)])
    ax.set_title('Optimal Schedule (Gantt Chart)')
    plt.show()


# Processing times for la01
processing_times = [
    [3, 2, 9, 5, 1],
    [2, 8, 9, 2, 3],
    [1, 5, 5, 8, 3],
    [6, 10, 9, 9, 2],
    [1, 6, 1, 4, 8],
    [6, 5, 4, 7, 2],
    [10, 4, 4, 7, 10],
    [4, 6, 10, 5, 8],
    [7, 7, 6, 7, 1],
    [10, 3, 9, 0, 0]
]

# Flatten the operations list to (job_id, processing_time) tuples.
jobs_list = [(job_id, processing_time) for job_id, processing_times in enumerate(processing_times, 1)
             for processing_time in processing_times if processing_time > 0]

# Solve JSSP instance using SPT dispatching rule
result_order = spt_dispatching_rule(jobs_list)

# Plot Gantt chart for the SPT solution
plot_gantt([(job_id, processing_time) for job_id, processing_time in jobs_list], num_machines=5)
