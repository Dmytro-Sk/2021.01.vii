import csv


def create_file(spider_name):
    with open(f'../../iii_results/01-{spider_name}.csv') as old_f:
        reader = csv.reader(old_f)
        for line in reader:
            headers = line
            break
        with open(f'../../iii_results/{spider_name}.csv', 'w', newline='') as new_f:
            writer = csv.DictWriter(new_f, fieldnames=headers)
            writer.writeheader()


def empty_cells_check(line):
    if line[0] is not None and line[1] is not None and line[2] is not None:
        return line
    else:
        return None


def combine_csv(spider_name, files_amount):
    create_file(spider_name)
    for i in range(1, files_amount + 1):
        if i < 10:
            i = str(f'0{i}')
        with open(f'../../iii_results/{i}-{spider_name}.csv', encoding='utf-8') as old_f:
            reader = csv.reader(old_f)
            next(reader)
            with open(f'../../iii_results/{spider_name}.csv', 'a', newline='', encoding='utf-8') as new_f:
                writer = csv.writer(new_f)
                for line in reader:
                    # line = cheempty_cells_check(line)  # uncomment if need some check
                    writer.writerow(line)


combine_csv(spider_name='sephora_com', files_amount=46)
