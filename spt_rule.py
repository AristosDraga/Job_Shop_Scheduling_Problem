import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

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

def convert_to_job_structure(operations, num_machines):
    jobs = []
    for i, operation_times in enumerate(operations, 1):
        job = {'arrival': 0, 'operations': []}
        for j, processing_time in enumerate(operation_times):
            operation = {
                'name': f'job_{i}_op_{j+1}',
                'machine': f'machine_{j+1}',
                'duration': processing_time,
                'next': f'job_{i}_op_{j+2}' if j < len(operations[i-1])-1 else None
            }
            job['operations'].append(operation)
        jobs.append(job)
    return jobs

def create_init_state(machines, jobs):
    init_state = {
        "machine_idle_time": {},
        "operation_ready_time": {},
        "schedule": {},
        "completed": []  # no operation is completed initially
    }

    # Initially, the idle time of all the machines are 0.
    for m in machines:
        init_state["machine_idle_time"][m] = 0

    # Initially, only the first operation of each job is ready at the job arrival time
    for job in jobs:
        first_op = job['operations'][0]
        init_state["operation_ready_time"][first_op["name"]] = job['arrival']

    # Initially, the machine schedules are empty
    for m in machines:
        init_state["schedule"][m] = []

    return init_state

def dispatching_rule_search(machines, jobs, priority):
    # Create the operation dictionary for state space search
    operations = {}
    for job in jobs:
        for op in job['operations']:
            operations[op['name']] = op

    # Create the initial state
    state = create_init_state(machines, jobs)

    # Search until reaching a goal state
    while len(state["completed"]) < len(operations):
        # Find the best action by a dispatching rule (priority function).
        # First, find the earliest applicable action.
        # Then, if there are multiple exist, select the one with the highest priority.

        best_action = None
        earliest_time = float('inf')
        best_priority = -float('inf')
        for opname in state["operation_ready_time"].keys():
            op = operations[opname]
            machine = op['machine']
            time = state["operation_ready_time"][opname]
            if time < state["machine_idle_time"][machine]:
                time = state["machine_idle_time"][machine]

            if time < earliest_time:
                best_action = (op, time)
                earliest_time = time
                best_priority = priority(best_action, state)
            elif time == earliest_time:
                p = priority((op, time), state)
                if p > best_priority:
                    best_action = (op, time)
                    best_priority = p

        # Apply the best action to the state
        op = best_action[0]  # action operation
        machine = op['machine']  # action machine
        time = best_action[1]  # action start time
        finish_time = time + op['duration']  # action finish time

        # Apply the action to the current state, create the next state
        state["schedule"][machine].append(best_action)  # add action to corresponding machine schedule sequence
        state["completed"].append(op['name'])  # add operation name to completed
        state["operation_ready_time"].pop(op['name'])  # delete completed operation name from ready time
        state["machine_idle_time"][machine] = finish_time  # machine will become idle after completion

        # If the operation is not the last operation of the job, then its next operation becomes ready
        if op['next'] is not None:
            next_op = operations[op['next']]
            state["operation_ready_time"][next_op['name']] = finish_time

    return state["schedule"]

# Define the priority function of the SPT rule: priority = - duration
spt_rule = lambda action, state: -action[0]['duration']


# List of file paths.
file_paths = ['txt_files/la01.txt', 'txt_files/la02.txt', 'txt_files/la03.txt', 'txt_files/la04.txt',
              'txt_files/la05.txt','txt_files/mt06.txt', 'txt_files/mt10.txt', 'txt_files/mt20.txt']


# Printing the spt schedule in which the jobs are processed and on what machine.
for file_path in file_paths:
    num_jobs, num_machines, operations = read_instance(file_path)
    jobs = convert_to_job_structure(operations, num_machines)
    machines = [f'machine_{i+1}' for i in range(num_machines)]
    if os.path.basename(file_path) == 'la01.txt':
        print(f'File: {os.path.basename(file_path)}')
        print(f'Number of Jobs: {num_jobs}')
        print(f'Number of Machines: {num_machines}')
        print('\nSPT Schedule:')
        spt_schedule = dispatching_rule_search(machines, jobs, spt_rule)
        for machine, schedule in spt_schedule.items():
            print(f'  {machine}:')
            for action in schedule:
                op_name = action[0]['name']
                start_time = action[1]
                duration = action[0]['duration']
                print(f'    Operation: {op_name}, Start Time: {start_time}, Duration: {duration}')
        print('\n' + '=' * 40 + '\n')



# Convert schedule into DataFrame so we can plot
def schedule_data_frame(schedule):
    schedule_dict = []
    for machine_schedule in schedule.values():
        for action in machine_schedule:
            a_dict = {
                'Operation': action[0]['name'],
                'Machine': action[0]['machine'],
                'Start': action[1],
                'Duration': action[0]['duration'],
                'Finish': action[1] + action[0]['duration']
            }
            schedule_dict.append(a_dict)
    
    return pd.DataFrame(schedule_dict)

# Plot the data with number naming of each job and the order they are processed
def gantt_chart(schedule):
    schedule_df = schedule_data_frame(schedule)

    JOBS = sorted(list(schedule_df['Operation'].apply(lambda x: x.split('_')[1]).unique()))
    MACHINES = sorted(list(schedule_df['Machine'].unique()))
    makespan = schedule_df['Finish'].max()

    bar_style = {'alpha': 1.0, 'lw': 25, 'solid_capstyle': 'butt'}
    text_style = {'color': 'white', 'weight': 'bold', 'ha': 'center', 'va': 'center'}
    colors = mpl.cm.Dark2.colors

    schedule_df.sort_values(by=['Operation', 'Start'])
    schedule_df.set_index(['Operation', 'Machine'], inplace=True)

    fig, ax = plt.subplots(figsize=(12, 5 + (len(MACHINES)) / 4))

    for jdx, j in enumerate(JOBS, 1):
        for mdx, m in enumerate(MACHINES, 1):
            op_name = f'job_{j}_op_{mdx}'
            if (op_name, m) in schedule_df.index:
                xs = schedule_df.loc[(op_name, m), 'Start']
                xf = schedule_df.loc[(op_name, m), 'Finish']
                ax.plot([xs, xf], [mdx] * 2, c=colors[jdx % 7], **bar_style)
                ax.text((xs + xf) / 2, mdx, j, **text_style)

    ax.set_title('Gantt Chart for Job Schedule for la01.txt data')
    ax.set_ylabel('Machine')
    ax.set_xlabel('Time')
    ax.set_ylim(0.5, len(MACHINES) + 0.5)
    ax.set_yticks(range(1, 1 + len(MACHINES)))
    ax.set_yticklabels(MACHINES)
    ax.text(makespan, ax.get_ylim()[0] - 0.2, "{0:0.1f}".format(makespan), ha='center', va='top')
    ax.plot([makespan] * 2, ax.get_ylim(), 'r--')
    ax.grid(True)

    plt.show()

# spt_schedule is the schedule obtained from the dispatching_rule_search function
gantt_chart(spt_schedule)
