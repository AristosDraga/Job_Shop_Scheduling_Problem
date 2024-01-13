def spt_dispatching_rule(jobs):
    """
    Shortest Processing Time (SPT) dispatching rule implementation.

    Parameters:
    - jobs: List of tuples representing jobs. Each tuple is (job_id, processing_time).

    Returns:
    - List of job_ids in the order they should be processed (shortest processing time first).
    """
    sorted_jobs = sorted(jobs, key=lambda x: x[1])
    return sorted_jobs # returning the jobs with the shortest processing time for each job.

def read_instance(file_path): # reading the txt files.
    with open(file_path, 'r') as file:
        num_jobs = int(file.readline().strip())
        num_machines = int(file.readline().strip())

        # Skip the makespan for now
        try: # check if there is a makespan.
            makespan = int(file.readline().strip())
        except ValueError:
            makespan = None # if not, None is assigned to it.

        operations = []

        for _ in range(num_jobs):
            operation_times = list(map(int, file.readline().split()))
            operations.append(operation_times)


        return num_jobs, num_machines, operations, makespan


def solve_jssp_instance(file_path):
    num_jobs, num_machines, operations, makespan= read_instance(file_path)

    # Flatten the operations list to (job_id, processing_time) tuples.
    jobs_list = [(job_id, processing_time) for job_id, processing_times in enumerate(operations, 1)
                 for processing_time in processing_times]

    result_order = spt_dispatching_rule(jobs_list)

    print(f'\nSolving JSSP instance in file {file_path}:')
    print(f'Number of jobs: {num_jobs}')
    print(f'Number of machines: {num_machines}')
    print(f'Makespan: {makespan}')
    print(f'Job processing order (SPT rule): {result_order}')


# List of file paths.
file_paths = ['txt_files/la01.txt', 'txt_files/la02.txt', 'txt_files/la03.txt', 'txt_files/la04.txt',
              'txt_files/la05.txt', 'txt_files/mt06.txt', 'txt_files/mt10.txt', 'txt_files/mt20.txt']

# Solve JSSP instances for each txt file.
for file_path in file_paths:
    solve_jssp_instance(file_path)

