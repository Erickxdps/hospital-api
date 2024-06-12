def render_paciente_list(pacientes):
    return [
        {
            "id": paciente.id,
            "name": paciente.name,
            "lastname": paciente.lastname,
            "ci": paciente.ci,
            "birth_date": paciente.birth_date,
        }
        for paciente in pacientes
    ]


def render_paciente_detail(paciente):

    return {
        "id": paciente.id,
        "name": paciente.name,
        "lastname": paciente.lastname,
        "ci": paciente.ci,
        "birth_date": paciente.birth_date,
    }
