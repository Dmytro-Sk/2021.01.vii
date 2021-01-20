from random import randint


def get_id(project_name):
    id = f"{project_name}_id - {''.join(str(randint(0, 9)) for _ in range(10))}"

    with open(f'../{project_name}_id.txt', 'a') as f:
        f.write(id)


get_id(project_name='sephora_com')
